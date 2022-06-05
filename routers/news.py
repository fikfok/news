from fastapi import APIRouter, Depends, HTTPException, status


# router = APIRouter(prefix="/api/v1/news", tags=["Импорт новостей"])
router = APIRouter(tags=["Импорт новостей"])


@router.get("/")
def list_speedsters():
    return {'status': 'ok'}
