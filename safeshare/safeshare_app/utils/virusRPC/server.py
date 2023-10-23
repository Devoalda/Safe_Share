import grpc
import scan_pb2
import scan_pb2_grpc
from concurrent import futures
import requests

apiKey = "" # API key from VirusTotal

headers = {
    "accept": "application/json",
    "x-apikey": apiKey
}


class VirusScanServicer(scan_pb2_grpc.VirusScanServiceServicer):
    url = "https://www.virustotal.com/api/v3/files/"

    def ScanFile(self, request, context):
        result = self.ScanSHA(request.file_SHA256)
        return result

    def ScanSHA(self, sha256_hash: str) -> scan_pb2.ScanFileResponse:
        self.url += sha256_hash

        response = requests.get(self.url, headers=headers)
        data = response.json()["data"]
        result = scan_pb2.ScanFileResponse()

        result.is_infected = data["attributes"]["last_analysis_stats"]["malicious"] > 0

        result.file_name = data["attributes"]["names"][0]
        result.file_SHA1 = data["attributes"]["sha1"]
        result.file_SHA256 = data["attributes"]["sha256"]

        return result


class VirusScanServer:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scan_pb2_grpc.add_VirusScanServiceServicer_to_server(VirusScanServicer(), server)
    server.add_insecure_port("[::]:50051")

    def serve(self):
        try:
            self.server.start()
            print("Server started, listening on 50051")
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            print("Server stopped")
            self.server.stop(0)

    def __del__(self):
        self.server.stop(0)

    def __enter__(self):
        return self


if __name__ == "__main__":
    cal = VirusScanServer()
    cal.serve()
