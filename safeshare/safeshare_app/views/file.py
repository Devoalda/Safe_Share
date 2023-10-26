import threading
import uuid
import os
import hashlib

from safeshare.safeshare_vdb.client import Client
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings
from urllib.parse import quote


@api_view(['POST'])
def manage_items(request):
    if request.method == 'POST':
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
            print(f"Hash signature: {hash_signature}")

            # Call RPC For virus scan
            client = Client()
            result = client.CheckFile(hash_signature)

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


@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if 'key' in kwargs:
            value = cache.get(kwargs['key'])
            if value:
                # Check if the 'path' key is in the stored value
                if 'path' in value:
                    file_path = value['path']
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            response = HttpResponse(f.read(), content_type='application/octet-stream')
                            response['Content-Disposition'] = f'attachment; filename="{quote(value["filename"])}"'
                            return response
                else:
                    response = {
                        'msg': 'File not found'
                    }
                    return Response(response, status=404)
            else:
                response = {
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if 'key' in kwargs:
            value = cache.get(kwargs['key'])
            if value:
                if 'path' in value:
                    file_path = value['path']

                    # Check if the file exists
                    if os.path.exists(file_path):
                        # Delete the file
                        os.remove(file_path)

                    # Delete the cache entry
                    cache.delete(kwargs['key'])

                    response = {
                        'msg': f"{kwargs['key']} successfully deleted"
                    }
                    return Response(response, status=200)
                else:
                    response = {
                        'msg': 'File not found'
                    }
                    return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'msg': 'Not found'
                }
                return Response(response, status=404)

# elif request.method == 'PUT':
#     if kwargs['key']:
#         request_data = json.loads(request.body)
#         new_value = request_data['value']
#         value = redis_instance.get(kwargs['key'])
#         if value:
#             redis_instance.set(kwargs['key'], new_value)
#             response = {
#                 'key': kwargs['key'],
#                 'file': value,
#                 'msg': f"Successfully updated {kwargs['key']}"
#             }
#             return Response(response, status=200)
#         else:
#             response = {
#                 'key': kwargs['key'],
#                 'value': None,
#                 'msg': 'Not found'
#             }
#             return Response(response, status=404)
# class FileView(viewsets.ModelViewSet):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = ()
#
#     def get_queryset(self):
#         # Only allow GET with a key
#         key = self.request.query_params.get('key', None)
#         if key is not None:
#             # Remove / from end of key
#             if key[-1] == '/':
#                 key = key[:-1]
#
#             print(key)
#             data = self.queryset.filter(key=key)
#             return data
#
#         else:
#             # Return nothing if no key is provided
#             return File.objects.none()
