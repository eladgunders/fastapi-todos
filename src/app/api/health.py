from fastapi import APIRouter, status

router = APIRouter(
    prefix='/health',
    tags=['Health']
)


@router.get('', status_code=status.HTTP_204_NO_CONTENT)
async def health():
    return
