import os
from logging import getLogger

from core.config import settings
from core.storage import storage
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

router = APIRouter()


@router.get(path="/stream/{video}")
def stream_video(video: str) -> FileResponse:
    """Stream Video"""
    logger = getLogger(__name__ + ".stream_video")
    try:
        path = f"./{settings.VIDEO_DIRECTORY}/{video}"
        logger.info(f"Serving {path}")
        # path = r"./videos/67a1fe27ef93a0385ff36090/master.m3u8"
        if not os.path.isfile(path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
            )
        return FileResponse(path=path, media_type="application/x-mpegURL")
    except HTTPException as ex:
        logger.error(ex)
        raise ex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error loading video",
        )
