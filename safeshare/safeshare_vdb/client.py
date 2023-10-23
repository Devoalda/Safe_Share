from concurrent.futures import ThreadPoolExecutor

import re
import grpc
import dynamo_pb2 as pb2
import dynamo_pb2_grpc as pb2_grpc

class Client:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.Dynamo_DBStub(self.channel)

    def CheckFile(self, sha_256_id: str):
        response = self.stub.CheckFile(pb2.Request(file_hash=sha_256_id))
        print(response)

    def UpdateFile(self, sha_256_id: str):
        response = self.stub.UpdateFile(pb2.Request(file_hash=sha_256_id))
        print(response)


if __name__ == "__main__":
    client = Client()
    id = "15e4313dddb45875ed67d1ab25f1f5b76f0b3a23e4fa9308c521e3fb30068028"
    client.CheckFile(id)
    client.UpdateFile(id)
