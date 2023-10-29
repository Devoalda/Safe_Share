import hashlib
import os
import threading
import uuid
from urllib.parse import quote

from cryptography.fernet import Fernet
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../utils/safeshare_vdb_client")

import client


class ManageItemsView(APIView):
    def post(self, request):
        # Define a timeout value (in seconds)
        timeout = 5

        # Get the list of files and the TTL value from the request data
        files = request.FILES.getlist('file')
        ttl = request.data.get('ttl')

        if not ttl:
            # Set ttl to 3 days
            ttl = 259200  # 3 * 24 * 60 * 60

        try:
            # Convert the TTL to an integer
            ttl = int(ttl)

            if ttl <= 0:
                return Response({'msg': 'TTL must be a positive integer'}, status=400)
        except ValueError:
            return Response({'msg': 'Invalid TTL format'}, status=400)

        def save_file_locally(file):
            key = uuid.uuid4().hex
            filename = file.name
            save_path = os.path.join(settings.MEDIA_ROOT, filename)
            hasher = hashlib.sha256()

            # Save the file locally
            with open(save_path, 'wb') as destination:
                for chunk in file.chunks():
                    hasher.update(chunk)
                    destination.write(chunk)

            # Get the hash signature
            hash_signature = hasher.hexdigest()

            # If RPC client import fails, skip virus scan
            # Call RPC For virus scan
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
                return Response(responses, status=400)

            # Generate a random UUID to use as the encryption key
            encryption_key = Fernet.generate_key()
            cipher_suite = Fernet(encryption_key)

            # Encrypted Data Buffer
            encrypted_data = b""

            # Encrypt the filename
            encrypted_filename = cipher_suite.encrypt(filename.encode())

            # Reopen the file to encrypt it with the encryption key and Fernet algorithm
            with open(save_path, 'rb') as source_file:
                for chunk in source_file:
                    encrypted_chunk = cipher_suite.encrypt(chunk)
                    encrypted_data += encrypted_chunk

            # New save path
            save_path = os.path.join(settings.MEDIA_ROOT, str(encrypted_filename))

            # Overwrite the file with the encrypted data
            with open(save_path, 'wb') as destination:
                destination.write(encrypted_data)


            # Store the file path and encryption key in the cache with the provided TTL
            cache.set(key,
                      {
                          'filename': encrypted_filename,
                          'path': save_path,
                          'encryption_key': encryption_key,
                      },
                      timeout=ttl)

            response = {
                'key': key,
                'filename': encrypted_filename,
                'msg': f"{key} successfully set to {filename} with TTL {ttl} seconds",
            }

            # Append the response to the shared responses list
            responses.append(response)

        # Create a list to store the responses for each file
        responses = []

        # Create a thread for each file
        file_threads = []
        for file in files:
            file_thread = threading.Thread(target=save_file_locally, args=(file,))
            file_threads.append(file_thread)

        # Start all file-saving threads
        for file_thread in file_threads:
            file_thread.start()

        # Use a Timer to add a timeout
        timeout_event = threading.Event()
        timeout_timer = threading.Timer(timeout, lambda: timeout_event.set())

        try:
            # Start the timer
            timeout_timer.start()

            # Wait for all file-saving threads to complete
            for file_thread in file_threads:
                file_thread.join()

            # Check if the threads completed without a timeout
            if not timeout_event.is_set():
                return Response(responses, status=201)
            else:
                return Response({'msg': 'File saving timed out'}, status=500)
        finally:
            # Always cancel the timer to prevent it from firing after the threads complete
            timeout_timer.cancel()


class ManageItemView(APIView):
    def get(self, request, key):
        value = cache.get(key)

        if not value:
            return Response({'msg': 'Not found'}, status=404)

        if 'path' not in value:
            return Response({'msg': 'File not found'}, status=404)

        file_path = value['path']

        if not os.path.exists(file_path):
            return Response({'msg': 'File not found'}, status=404)

        # Retrieve the encryption key from the cache
        encryption_key = value.get('encryption_key')

        if not encryption_key:
            return Response({'msg': 'Encryption key not found'}, status=404)

        # Decrypt the filename
        cipher_suite = Fernet(encryption_key)
        decrypted_filename = cipher_suite.decrypt(value['filename']).decode()

        # Decrypt the file content
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)

        response = HttpResponse(decrypted_data, content_type='application/octet-stream')

        # Set the Content-Disposition with the decrypted filename
        response['Content-Disposition'] = f'attachment; filename="{quote(decrypted_filename)}"'
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
