from fastapi import APIRouter
from fastapi.responses import FileResponse

from ..controllers.files import FilesControler


router = APIRouter(prefix='/files')

@router.get('', response_class=FileResponse)
def get_file(path: str):
    media = FilesControler.get_file_content(path)
    return FileResponse(path=path, filename=media.filename, media_type=media.content_type)