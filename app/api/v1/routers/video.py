import json
import os
import subprocess
from logging import getLogger
from typing import Dict, List, Optional

from bson.objectid import ObjectId
from core.authentication.auth_middleware import get_current_active_user
from core.config import settings
from core.storage import storage
from core.video_processing import generate_hls
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.background import BackgroundTasks
from fastapi.responses import HTMLResponse
from schemas.user import User
from schemas.video import Video, VideoUpdate

router = APIRouter()


@router.get(path="/videos/{video_id}", response_model=Video)
def get_video(video_id: str) -> Video:
    """Gets a video by its id"""
    logger = getLogger(__name__ + ".get_video")
    try:
        video = storage.video_verify_record({"_id": video_id})
        return video
    except HTTPException as hex:
        logger.error(hex)
        raise hex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get video",
        )


@router.get(path="/videos/{video_id}/watch", response_class=HTMLResponse)
def watch_video_page(video_id: str) -> Video:
    """Gets a video viewing page by its id"""
    logger = getLogger(__name__ + ".watch_video_page")
    try:
        video = storage.video_verify_record({"_id": video_id})
        url = f"http://localhost:8000/stream/{video.id}/master.m3u8"
        html = ""
        with open("./templates/index.html", mode="r") as f:
            html = f.read()

        html = html.replace("VIDEO_URL", url)

        return HTMLResponse(content=html)
    except HTTPException as hex:
        logger.error(hex)
        raise hex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get video",
        )


@router.get(path="/videos", response_model=List[Video])
def get_videos(
    cursor: Optional[str] = None, limit: int = 0, only_available: bool = True
) -> Video:
    """Gets all available videos"""
    logger = getLogger(__name__ + ".get_videos")
    try:
        filter = {}
        if only_available:
            filter["available"] = True
        if cursor:
            filter["_id"] = {"$gt": ObjectId(cursor)}

        videos = storage.video_get_all_records(filter=filter, limit=limit)
        return videos
    except HTTPException as hex:
        logger.error(hex)
        raise hex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get video",
        )


@router.post(path="/videos", response_model=Video)
async def upload_video(
    video_file: UploadFile,
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: Optional[str] = Form(default=None),
    tags: List[str] = Form(default=[]),
    current_user: User = Depends(get_current_active_user),
) -> Video:
    """Uploads a video to the server"""
    logger = getLogger(__name__ + ".upload_video")
    try:
        os.makedirs(settings.VIDEO_DIRECTORY, exist_ok=True)

        id = storage.video_create_record(
            title=title,
            user_id=current_user.id,
            duration_in_sec=0,
            description=description,
            tags=tags,
        )
        output_path = f"{settings.VIDEO_DIRECTORY}/{id}"
        os.makedirs(output_path, exist_ok=True)
        video_path = f"{output_path}/{id}.mp4"

        with open(video_path, mode="wb") as f:
            f.write(await video_file.read())

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-print_format",
            "json",
            video_path,
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        metadata: dict = json.loads(result.stdout)

        update = {"duration_in_sec": float(metadata.get("format").get("duration"))}
        storage.video_update_record(
            filter={"_id": id, "user_id": current_user.id}, update=update
        )

        background_tasks.add_task(
            generate_hls, input_file=video_path, prefix=output_path, video_id=id
        )

        return storage.video_verify_record(
            filter={"_id": id, "user_id": current_user.id}
        )

    except HTTPException as hex:
        logger.error(hex)
        raise hex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to upload video",
        )


@router.patch(path="/videos/{video_id}", response_model=Video)
def update_video(
    video_id: str,
    video_data: VideoUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Video:
    """Updates a video by its id"""
    logger = getLogger(__name__ + ".update_video")
    try:
        update = video_data.model_dump(exclude_unset=True)
        storage.video_update_record(
            filter={"_id": video_id, "user_id": current_user.id}, update=update
        )

        video = storage.video_verify_record(filter={"_id": video_id})
        return video
    except HTTPException as hex:
        logger.error(hex)
        raise hex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get video",
        )


@router.delete(path="/videos/{video_id}", response_model=Dict[str, str])
def delete_video(
    video_id: str, current_user: User = Depends(get_current_active_user)
) -> Video:
    """Deletes a video by its id"""
    logger = getLogger(__name__ + ".delete_video")
    try:
        storage.video_delete_record({"_id": video_id, "user_id": current_user.id})
        return {"message": "Video deleted successfully"}
    except HTTPException as hex:
        logger.error(hex)
        raise hex
    except Exception as ex:
        logger.error(ex, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get video",
        )
