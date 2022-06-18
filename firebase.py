from typing import Optional
from google.cloud.storage import Bucket, Blob
from database import Database
from firebase_admin import credentials, initialize_app, storage
import os


class Firebase(Database):
    def __init__(self, file_name: str):
        cred = credentials.Certificate('./serviceAccountKey.json')
        initialize_app(cred, {'storageBucket': 'cloudlog-ayd2.appspot.com'})

        self.__bucket = storage.bucket()
        self.__file_name: str = file_name + '.txt'

    def create_initial_log(self):
        file = open('initial.txt', 'w')
        file.close()
        blob: Blob = self.__bucket.blob(self.__file_name)
        blob.upload_from_filename('initial.txt')
        blob.make_public()
        os.remove('initial.txt')
        print('Guardando registros en: ', blob.public_url)

    def get_cloud_log(self) -> Blob:
        cloud_log: Optional[Blob] = self.__bucket.get_blob(self.__file_name)
        if cloud_log is None:
            self.create_initial_log()
            cloud_log = self.__bucket.get_blob(self.__file_name)
        return cloud_log

    def write(self, message: str):
        cloud_log: Blob = self.get_cloud_log()
        current_log: str = cloud_log.download_as_text(encoding='utf-8')
        file = open('uploading.txt', 'w', encoding='utf-8')
        file.write(current_log + message)
        file.close()
        cloud_log.upload_from_filename('uploading.txt')
        cloud_log.make_public()
        cloud_log.update()
        os.remove('uploading.txt')
