import os
import shutil
from typing import Optional
from fastapi.datastructures import UploadFile

from ..utils.logger import logger

class FileHandler:

    @staticmethod
    def validate_file_extension(media: UploadFile, extensions: Optional[tuple[str, ...]] = ()) -> bool:
        """Validate if the file extension is valid"""
        if not extensions:
            return True
        return media.filename.lower().endswith(extensions) #type: ignore

    @staticmethod
    def upload_image(media: UploadFile, path: str, folder: str = 'images') -> str | None:
        """Upload a file to a specific path"""
        _path = f'media/{folder}/{path}'
        if len(folder.split('/')) > 1 and not os.path.exists(f'media/{folder}'):
            os.makedirs(f'media/{folder}', exist_ok=True)
        try:
            with open(_path, 'wb') as buffer:
                shutil.copyfileobj(media.file, buffer)
        except Exception as err:
            logger.error(f'Error uploading file: {err}')
            return None
        return _path
    
    @staticmethod
    def get_file(path: str) -> UploadFile | None:
        """Get a file from a specific path"""
        try:
            return UploadFile(file=open(path, 'rb'))
        except Exception as err:
            logger.error(f'Error getting file: {err}')
            return None
    
    @staticmethod
    def delete_image(path: str) -> bool:
        """Delete a file from a specific path"""
        try:
            os.remove(path)
            return True
        except Exception as err:
            logger.error(f'Error deleting file: {err}')
            return False