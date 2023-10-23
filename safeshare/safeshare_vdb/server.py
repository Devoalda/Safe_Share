from concurrent.futures import ThreadPoolExecutor

import re
import grpc
import dynamo_pb2 as pb2
import dynamo_pb2_grpc as pb2_grpc

import boto3 as boto  # 1.28.68

# dynamo db instance
dynamodb = boto.resource('dynamodb')
sha256_table = dynamodb.Table('safeshare_sha256')
sha1_table = dynamodb.Table('safeshare_sha1')
md5_table = dynamodb.Table('safeshare_md5')

# hash
hex_pattern = re.compile("^[a-fA-F0-9]+$")


def check_sha256(sha256):
    response = sha256_table.get_item(Key={'sha256': sha256})
    return True if 'Item' in response else False


def check_sha1(sha1):
    response = sha1_table.get_item(Key={'sha1': sha1})
    return True if 'Item' in response else False


def check_md5(md5):
    response = md5_table.get_item(Key={'md5': md5})
    return True if 'Item' in response else False


class Dynamo(pb2_grpc.Dynamo_DBServicer):
    def CheckFile(self, request, context):
        if not hex_pattern.match(request.file_hash):
            return pb2.Response(is_exist=False)
        else:
            length = len(request.file_hash)
            if length == 64:
                return pb2.Response(is_exist=check_sha256(request.file_hash))
            elif length == 40:
                return pb2.Response(is_exist=check_sha1(request.file_hash))
            elif length == 32:
                return pb2.Response(is_exist=check_md5(request.file_hash))
            else:
                return pb2.Response(is_exist=False)

    def UpdateFile(self, request, context):
        if not hex_pattern.match(request.file_hash):
            return pb2.Response(is_exist=False)
        else:
            length = len(request.file_hash)
            if length == 64:
                sha256_table.put_item(Item={'sha256': request.file_hash})
                return pb2.Response(is_exist=True)
            elif length == 40:
                sha1_table.put_item(Item={'sha1': request.file_hash})
                return pb2.Response(is_exist=True)
            elif length == 32:
                md5_table.put_item(Item={'md5': request.file_hash})
                return pb2.Response(is_exist=True)
            else:
                return pb2.Response(is_exist=False)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_Dynamo_DBServicer_to_server(Dynamo(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
