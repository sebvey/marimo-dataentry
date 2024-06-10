from abc import ABC, abstractmethod
import logging

from pathlib import Path

class Uploader(ABC):

    @abstractmethod
    def upload(self, local_path: Path) -> None: pass


class AWSUploaderMock(Uploader):

    def __init__(self, bucket: str, target_prefix: str, is_lame = False) -> None:
        self._bucket = bucket
        self._target_prefix = target_prefix
        self.is_lame = is_lame

    def upload(self, local_file_path: Path) -> None:

        logging.warning("MOCKED AWS UPLOADER USED")
        if self.is_lame:
            raise Exception("TEST Exception")


__all__ = [
    Uploader,
    AWSUploaderMock
]
