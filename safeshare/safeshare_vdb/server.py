from concurrent.futures import ThreadPoolExecutor

import re
import grpc
import dynamo_pb2 as pb2
import dynamo_pb2_grpc as pb2_grpc
import environ
import os
import requests

import boto3 as boto  # 1.28.68

# TotalVirus API key
environ.Env.read_env('./.env')
api = environ.Env().str('API_TOKEN')

# dynamo db instance
session = boto.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('REGION')
)

dynamodb = session.resource('dynamodb')
sha256_table = dynamodb.Table('safeshare_sha256')
sha1_table = dynamodb.Table('safeshare_sha1')
md5_table = dynamodb.Table('safeshare_md5')

headers = {
    "accept": "application/json",
    "x-apikey": api
}

# hash
hex_pattern = re.compile("^[a-fA-F0-9]+$")


def upload(hash_val):
    if not hex_pattern.match(hash_val):
        return False
    else:
        length = len(hash_val)
        if length == 64:
            sha256_table.put_item(Item={'sha256': hash_val})
        elif length == 40:
            sha1_table.put_item(Item={'sha1': hash_val})
        elif length == 32:
            md5_table.put_item(Item={'md5': hash_val})
        else:
            return False

        return True


def scan(hash_val):
    url = "https://www.virustotal.com/api/v3/files/" + hash_val
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        return data["attributes"]["last_analysis_stats"]["malicious"] > 0
    else:
        return False


def check_sha256(sha256):
    response = sha256_table.get_item(Key={'sha256': sha256})
    if "Item" not in response:
        return upload(sha256) if scan(sha256) else False
    else:
        return True


def check_sha1(sha1):
    response = sha1_table.get_item(Key={'sha1': sha1})
    if "Item" not in response:
        return upload(sha1) if scan(sha1) else False
    else:
        return True


def check_md5(md5):
    response = md5_table.get_item(Key={'md5': md5})
    if "Item" not in response:
        return upload(md5) if scan(md5) else False
    else:
        return True


class Dynamo(pb2_grpc.Dynamo_DBServicer):
    def CheckHash(self, request, context):
        if not hex_pattern.match(request.file_hash):
            return pb2.Response(is_exist=False)
        else:
            print(f"Checking file {request.file_hash} with hash signature {request.file_hash}")
            length = len(request.file_hash)
            if length == 64:
                print("check sha256")
                return pb2.Response(is_exist=check_sha256(request.file_hash))
            elif length == 40:
                return pb2.Response(is_exist=check_sha1(request.file_hash))
            elif length == 32:
                return pb2.Response(is_exist=check_md5(request.file_hash))
            else:
                return pb2.Response(is_exist=False)

    def UpdateHash(self, request, context):
        return pb2.Response(is_exist=upload(request.file_hash))


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_Dynamo_DBServicer_to_server(Dynamo(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
