import grpc
import dynamo_pb2 as pb2
import dynamo_pb2_grpc as pb2_grpc


class Client:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.Dynamo_DBStub(self.channel)

    def CheckFile(self, sha_256_id: str):
        print(f"Checking file {sha_256_id} with hash signature {sha_256_id}")
        response = self.stub.CheckHash(pb2.Request(file_hash=sha_256_id))
        return response.is_exist

    def UpdateFile(self, sha_256_id: str):
        print(f"Updating file {sha_256_id} with hash signature {sha_256_id}")
        response = self.stub.UpdateHash(pb2.Request(file_hash=sha_256_id))
        return response.is_exist


# if __name__ == "__main__":
#     client = Client()
#     id = "15e4313dddb45875ed67d1ab25f1f5b76f0b3a23e4fa9308c521e3fb30068028"
#     print(client.CheckFile(id))
#     # client.UpdateFile(id)
