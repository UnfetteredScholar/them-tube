import os
import shutil
from datetime import UTC, datetime
from typing import Dict, List, Optional

import gridfs
from bson.objectid import ObjectId
from core.authentication.hashing import hash_bcrypt
from core.config import settings
from fastapi import status
from fastapi.exceptions import HTTPException
from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient
from schemas import user as s_user
from schemas import video as s_video


class MongoStorage:
    """Storage class for interfacing with mongo db"""

    def __init__(
        self,
        connection_url: str = settings.MONGO_URI,
        db_name: str = settings.DATABSE_NAME,
    ):
        """Initializes a MongoStorage object"""

        self.client = MongoClient(connection_url)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

        # Create indexes
        self.db["users"].create_index(keys=[("email", ASCENDING)], unique=True)

    # users
    def user_create_record(
        self,
        user_data: s_user.UserIn,
        role: s_user.Role = "user",
        sign_in_type: s_user.SignInType = "NORMAL",
        verified: bool = False,
    ) -> str:
        """Creates a user record"""

        users_table = self.db["users"]

        if users_table.find_one({"email": user_data.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken",
            )

        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password length."
                + " Password length must be at least 8 characters",
            )

        date = datetime.now(UTC)
        user = user_data.model_dump()
        user["password"] = hash_bcrypt(user_data.password)
        user["role"] = role
        user["sign_in_type"] = sign_in_type
        user["verified"] = verified
        user["status"] = s_user.UserStatus.ENABLED
        user["date_created"] = date
        user["date_modified"] = date

        id = str(users_table.insert_one(user).inserted_id)

        return id

    def user_get_record(self, filter: Dict) -> Optional[s_user.User]:
        """Gets a user record from the db using the supplied filter"""
        users = self.db["users"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        user = users.find_one(filter)

        if user:
            user = s_user.User(**user)

        return user

    def user_get_all_records(self, filter: Dict) -> List[s_user.User]:
        """Gets all user records from the db using the supplied filter"""
        users = self.db["users"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        users_list = users.find(filter)

        users_list = [s_user.User(**user) for user in users_list]

        return users_list

    def user_verify_record(self, filter: Dict) -> s_user.User:
        """
        Gets a user record using the filter
        and raises an error if a matching record is not found
        """

        user = self.user_get_record(filter)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    def user_update_record(self, filter: Dict, update: Dict):
        """Updates a user record"""
        self.user_verify_record(filter)

        for key in ["_id", "email"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")
        update["date_modified"] = datetime.now(UTC)

        return self.db["users"].update_one(filter, {"$set": update})

    def user_delete_record(self, filter: Dict):
        """Deletes a user record"""
        self.user_verify_record(filter)

        self.db["users"].delete_one(filter)

    # videos
    def video_create_record(
        self,
        title: str,
        user_id: str,
        duration_in_sec: float,
        description: Optional[str] = None,
        tags: List[str] = [],
        available: bool = False,
    ) -> str:
        """Creates a video record"""

        videos_table = self.db["videos"]

        date = datetime.now(UTC)
        video = {
            "title": title,
            "user_id": user_id,
            "description": description,
            "tags": tags,
            "available": available,
            "duration_in_sec": duration_in_sec,
        }

        video["date_created"] = date
        video["date_modified"] = date

        id = str(videos_table.insert_one(video).inserted_id)

        return id

    def video_get_record(self, filter: Dict) -> Optional[s_video.Video]:
        """Gets a video record from the db using the supplied filter"""
        videos = self.db["videos"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        video = videos.find_one(filter)

        if video:
            video = s_video.Video(**video)

        return video

    def video_get_all_records(
        self, filter: Dict, limit: int = 0
    ) -> List[s_video.Video]:
        """Gets all video records from the db using the supplied filter"""
        videos = self.db["videos"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        videos_list = videos.find(filter).limit(limit)

        videos_list = [s_video.Video(**video) for video in videos_list]

        return videos_list

    def video_verify_record(self, filter: Dict) -> s_video.Video:
        """
        Gets a video record using the filter
        and raises an error if a matching record is not found
        """

        video = self.video_get_record(filter)

        if video is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
            )

        return video

    def video_update_record(self, filter: Dict, update: Dict):
        """Updates a video record"""
        self.video_verify_record(filter)

        for key in ["_id", "user_id"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")
        update["date_modified"] = datetime.now(UTC)

        return self.db["videos"].update_one(filter, {"$set": update})

    def video_delete_record(self, filter: Dict):
        """Deletes a video record"""
        video = self.video_verify_record(filter)

        self.db["videos"].delete_one(filter)
        path = f"./{settings.VIDEO_DIRECTORY}/{video.id}"
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
