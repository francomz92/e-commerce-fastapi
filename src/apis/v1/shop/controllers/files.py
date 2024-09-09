from .....helpers.files import FileHandler
from .....handlers.errors import NotFoundError
from .....utils.constants import ERROR__NOT_FOUND

class FilesControler:
    
    @staticmethod
    def get_file_content(file_path: str):
        media = FileHandler.get_file(file_path)
        if not media:
            raise NotFoundError(msg=ERROR__NOT_FOUND % file_path.split('/')[-1])
        return media