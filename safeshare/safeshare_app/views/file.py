import uuid

import redis
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    if request.method == 'GET':
        # Not supposed to enumerate all items, so return 405
        return Response({
            'msg': 'Method not allowed'
        }, status=405)

    if request.method == 'POST':
        key = uuid.uuid4().hex
        file = request.FILES['file']
        filename = 'file.txt'

        # Convert file to bytes
        file = file.read()
        redis_instance.set(key, file)

        response = {
            'key': key,
            'msg': f"{key} successfully set to {filename}: {file}"
        }
        return Response(response, 201)


@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_instance.get(kwargs['key'])
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
            result = redis_instance.delete(kwargs['key'])
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
