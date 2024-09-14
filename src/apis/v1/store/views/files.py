from fastapi import APIRouter
from fastapi.responses import FileResponse

from ..controllers.files import FilesControler


router = APIRouter(prefix='/files', tags=['Archivos'])

@router.get(
    '',
    response_class=FileResponse,
    description='Almacena un nuevo producto en la base de datos',
    summary='Crear un nuevo producto',
)
def get_file(path: str):
    media = FilesControler.get_file_content(path)
    return FileResponse(path=path, filename=media.filename, media_type=media.content_type)