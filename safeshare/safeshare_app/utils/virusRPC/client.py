import grpc

import scan_pb2_grpc
import scan_pb2


class Client:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = scan_pb2_grpc.VirusScanServiceStub(self.channel)

    def ScanFile(self, sha_256_id: str):
        response = self.stub.ScanFile(scan_pb2.ScanFileRequest(file_SHA256=sha_256_id))
        print(response)


if __name__ == "__main__":
    client = Client()
    id = "15e4313dddb45875ed67d1ab25f1f5b76f0b3a23e4fa9308c521e3fb30068028"
    client.ScanFile(id)
