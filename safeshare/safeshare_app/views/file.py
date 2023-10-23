import threading
import uuid

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
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

        # Define a function to save a single file in a thread
        def save_file_to_redis(file):
            key = uuid.uuid4().hex

            # Get the filename
            filename = file.name

            # Convert file to bytes
            file_content = file.read()

            # Set with the provided TTL
            cache.set(key, file_content, timeout=ttl)

            response = {
                'key': key,
                'msg': f"{key} successfully set to {filename} with TTL {ttl} seconds"
            }

            # Append the response to the shared responses list
            responses.append(response)

        # Create a list to store the responses for each file
        responses = []

        # Create a thread for each file
        file_threads = []
        for file in files:
            file_thread = threading.Thread(target=save_file_to_redis, args=(file,))
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
        if kwargs['key']:
            value = cache.get(kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'file': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'file': None,
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

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = cache.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['key']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'file': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

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
