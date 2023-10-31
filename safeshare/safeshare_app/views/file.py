import hashlib
import os
import sys
import threading
import uuid
import logging
from urllib.parse import quote

import magic
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../utils/safeshare_vdb_client")

import client

logger = logging.getLogger(__name__)


class ManageItemsView(APIView):
    TIMEOUT = 20  # seconds

    def post(self, request):
        files = request.FILES.getlist('file')
        ttl = request.data.get('ttl') or 259200  # Default TTL is 3 days

        try:
            ttl = int(ttl)
            if ttl <= 0:
                return Response({'msg': 'TTL must be a positive integer'}, status=400)
        except ValueError:
            return Response({'msg': 'Invalid TTL format'}, status=400)

        responses = []
        threads = []

        client_ip = get_client_ip(request)
        logger.info(f"{request.method} request received from IP: {client_ip}")

        for file in files:
            thread = threading.Thread(target=self._save_file, args=(file, ttl, responses))
            threads.append(thread)

        for thread in threads:
            thread.start()

        timeout_event = threading.Event()
        timeout_timer = threading.Timer(self.TIMEOUT, lambda: timeout_event.set())

        try:
            timeout_timer.start()
            for thread in threads:
                thread.join()

            if not timeout_event.is_set():
                return Response(responses, status=201)
            else:
                logger.error('File saving timed out')
                return Response({'msg': 'File saving timed out'}, status=500)
        finally:
            timeout_timer.cancel()

    def _save_file(self, file, ttl, responses):
        key = uuid.uuid4().hex
        filename = file.name
        save_path = os.path.join(settings.MEDIA_ROOT, filename)
        hasher = hashlib.sha256()

        with open(save_path, 'wb') as destination:
            for chunk in file.chunks():
                hasher.update(chunk)
                destination.write(chunk)

        hash_signature = hasher.hexdigest()
        logger.info(f'File {filename} saved to {save_path} with hash signature {hash_signature}')

        try:
            grpc_client = client.Client()
            result = grpc_client.CheckFile(hash_signature, timeout=10)
        except Exception as e:
            result = False

        if result:
            response = {
                'msg': f"File {filename} is infected with a virus"
            }
            os.remove(save_path)
            responses.append(response)
            logger.warning(f'File {filename} is infected with a virus')
            return

            # Determine the MIME type of the file using python-magic
        try:
            file_type = magic.Magic()
            mime_type = file_type.from_file(save_path)
        except Exception as e:
            logger.warning(f'Error detecting MIME type: {str(e)}')
            mime_type = 'application/octet-stream'

        # Store the file path, filename, MIME type, and other information in the cache
        cache.set(key, {
            'filename': filename,
            'path': save_path,
            'mime_type': mime_type,  # Store the MIME type
        }, timeout=ttl)

        response = {
            'key': key,
            'filename': filename,
            'mime_type': mime_type,  # Include the MIME type in the response
            'msg': f"{key} successfully set to {filename} with TTL {ttl} seconds",
        }
        responses.append(response)
        logger.info(f'File {filename} successfully saved to cache with key {key} and TTL {ttl} seconds')


class ManageItemView(APIView):
    def get(self, request, key):
        value = cache.get(key)

        if not value:
            logger.warning(f'Key {key} not found')
            raise NotFound("Key not found")

        if 'path' not in value:
            logger.warning(f'File not found')
            raise NotFound("File not found")

        file_path = value['path']

        if not os.path.exists(file_path):
            logger.warning(f'File not found')
            raise NotFound("File not found")

        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Retrieve the MIME type from the cache
        mime_type = value.get('mime_type', 'application/octet-stream')

        response = HttpResponse(file_data, content_type=mime_type)

        # Set the Content-Disposition with the original filename
        response['Content-Disposition'] = f'attachment; filename="{quote(os.path.basename(file_path))}"'

        logger.info(f'File {file_path} successfully retrieved from cache with key {key}')
        return response

    def delete(self, request, key):
        value = cache.get(key)

        if not value:
            logger.warning(f'Key {key} not found')
            return Response({'msg': 'Not found'}, status=404)

        if 'path' in value and os.path.exists(value['path']):
            os.remove(value['path'])
            cache.delete(key)
            logger.info(f'File {value["path"]} successfully deleted from cache with key {key}')
            return Response({'msg': f"{key} successfully deleted"}, status=200)

        logger.warning(f'File not found')
        return Response({'msg': 'File not found'}, status=404)


PRIVATE_IPS_PREFIX = ('10.', '172.', '192.')


def get_client_ip(request):
    """get the client ip from the request
    """
    # remote_address = request.META.get('REMOTE_ADDR')
    remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX):
            proxies.pop(0)
            # take the first ip which is not a private one (of a proxy)
            if len(proxies) > 0:
                ip = proxies[0]
            print(ip)
    return ip
