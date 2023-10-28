import threading
import uuid
import os
import hashlib

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from urllib.parse import quote


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

        # Define a function to save a single file
        def save_file_locally(file):
            key = uuid.uuid4().hex

            # Get the filename
            filename = file.name

            # Define the path to save the file locally
            save_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Hash the file
            hasher = hashlib.sha256()

            # Save the file locally
            with open(save_path, 'wb') as destination:
                for chunk in file.chunks():
                    hasher.update(chunk)
                    destination.write(chunk)

            # Get the hash signature
            hash_signature = hasher.hexdigest()
            # print(f"Hash signature: {hash_signature}")

            # If RPC client import fails, skip virus scan
            # Call RPC For virus scan
            try:
                client = Client()
                result = client.CheckFile(hash_signature)
            except Exception as e:
                result = False

            # If infected, delete the file and return an error
            if result:
                response = {
                    'msg': f"File {filename} is infected with a virus"
                }
                os.remove(save_path)
                responses.append(response)
                return Response(responses, status=400)

            # Store the file path in the cache with the provided TTL
            cache.set(key,
                      {
                          'filename': filename,
                          'path': save_path,
                      },
                      timeout=ttl)

            response = {
                'key': key,
                'filename': filename,
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

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{quote(value["filename"])}"'
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
