import hashlib
import os
import sys
import threading
import uuid
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


class ManageItemsView(APIView):
    TIMEOUT = 5

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

        try:
            grpc_client = client.Client()
            result = grpc_client.CheckFile(hash_signature)
        except Exception as e:
            result = False

        if result:
            response = {
                'msg': f"File {filename} is infected with a virus"
            }
            os.remove(save_path)
            responses.append(response)
            return

        # Determine the MIME type of the file using python-magic
        file_type = magic.Magic()
        mime_type = file_type.from_file(save_path)

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


class ManageItemView(APIView):
    def get(self, request, key):
        value = cache.get(key)

        if not value:
            raise NotFound("Key not found")

        if 'path' not in value:
            raise NotFound("File not found")

        file_path = value['path']

        if not os.path.exists(file_path):
            raise NotFound("File not found")

        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Retrieve the MIME type from the cache
        mime_type = value.get('mime_type', 'application/octet-stream')

        response = HttpResponse(file_data, content_type=mime_type)

        # Set the Content-Disposition with the original filename
        response['Content-Disposition'] = f'attachment; filename="{quote(os.path.basename(file_path))}"'

        return response

    def delete(self, request, key):
        value = cache.get(key)

        if not value:
            return Response({'msg': 'Not found'}, status=404)

        if 'path' in value and os.path.exists(value['path']):
            os.remove(value['path'])
            cache.delete(key)
            return Response({'msg': f"{key} successfully deleted"}, status=200)

        return Response({'msg': 'File not found'}, status=404)
