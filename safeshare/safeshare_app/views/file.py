import uuid
import threading

import redis
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

# redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
#                                    port=settings.REDIS_PORT, db=0)


@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    if request.method == 'GET':
        # Not supposed to enumerate all items, so return 405
        return Response({'msg': 'Method not allowed'}, status=405)

    if request.method == 'POST':
        # Define a timeout value (in seconds)
        timeout = 5

        ttl = request.data['ttl']

        if not ttl:
            return Response({'msg': 'TTL not provided'}, status=400)

        try:
            # Convert the TTL to an integer
            ttl = int(ttl)

            if ttl <= 0:
                return Response({'msg': 'TTL must be a positive integer'}, status=400)
        except ValueError:
            return Response({'msg': 'Invalid TTL format'}, status=400)

        # Define a function to save the file in a thread
        def save_file_to_redis():
            key = uuid.uuid4().hex

            file = request.FILES['file']
            if not file:
                return Response({'msg': 'No file provided'}, status=400)

            filename = file.name

            # Convert file to bytes
            file = file.read()

            # Set with ttl if ttl is provided
            cache.set(key, file, timeout=ttl)

            response = {
                'key': key,
                'msg': f"{key} successfully set to {filename}: {file}, with a ttl of {ttl} seconds"
            }

            # Store the response in a shared variable
            nonlocal saved_response
            saved_response = response

        # Create a shared variable to store the response
        saved_response = None

        # Create a new thread for the file-saving process
        file_saving_thread = threading.Thread(target=save_file_to_redis)

        # Start the file-saving thread
        file_saving_thread.start()

        # Use a Timer to add a timeout
        timeout_event = threading.Event()
        timeout_timer = threading.Timer(timeout, lambda: timeout_event.set())

        try:
            # Start the timer
            timeout_timer.start()

            # Wait for the file-saving thread to complete
            file_saving_thread.join()

            # Check if the thread completed without a timeout
            if not timeout_event.is_set():
                if saved_response:
                    return Response(saved_response, status=201)
                else:
                    return Response({'msg': 'File saving failed'}, status=500)
            else:
                return Response({'msg': 'File saving timed out'}, status=500)
        finally:
            # Always cancel the timer to prevent it from firing after the thread completes
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
