from database import Database
from firebase import Firebase
from datetime import datetime
from cloud_log_meta import CloudLogMeta


class CloudLog(metaclass=CloudLogMeta):
    def __init__(self, file_name: str):
        self.__database: Database = Firebase(file_name)

    def success(self, message: str):
        self._Logger__print_log('EXITO', message)

    def warning(self, message: str):
        self._Logger__print_log('ADVERTENCIA', message)

    def error(self, message: str):
        self._Logger__print_log('ERROR', message)

    def _Logger__print_log(self, severity: str, message: str):
        self.__database.write(f'{str(datetime.now())} [{severity}]: {message}\n')
