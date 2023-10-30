import os
import threading

import environ
import redis
from django.conf import settings


class TrashCollector:
    def __init__(self):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.media_root = settings.MEDIA_ROOT

        # Connect to Redis
        self.redis = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def run(self):
        while not self.stop_event.is_set():
            # Get all keys from the Redis database
            all_keys = self.redis.keys("*")

            # Search through redis keys for expired keys
            # Delete the files of expired keys or keys that have been deleted (dont exist)
            if not all_keys:
                # Delete all files
                for file in os.listdir(self.media_root):
                    file_path = os.path.join(self.media_root, file)
                    try:
                        if os.path.isfile(file_path):
                            print(f"Deleting file {file_path}")
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)

            else:
                # Delete files(value) of expired keys
                for key in all_keys:
                    if not self.redis.exists(key):
                        file_path = os.path.join(self.media_root, key.decode("utf-8"))
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                        except Exception as e:
                            print(e)

                    else:
                        if self.redis.ttl(key) == -1:
                            file_path = os.path.join(self.media_root, key.decode("utf-8"))
                            try:
                                if os.path.isfile(file_path):
                                    print(f"Deleting file {file_path}")
                                    os.unlink(file_path)
                            except Exception as e:
                                print(e)

            # Sleep for a specific interval in seconds
            self.stop_event.wait(timeout=settings.TRASH_TIMEOUT)


if __name__ == '__main__':
    trash_collector = TrashCollector()
    try:
        print("Starting trash collector")
        trash_collector.start()
        print("Trash collector started")
    except KeyboardInterrupt:
        trash_collector.stop()
        print("Trash collector stopped")
