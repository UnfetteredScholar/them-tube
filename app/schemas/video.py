from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from schemas.base import PyObjectId


class Video(BaseModel):
    id: PyObjectId = Field(validation_alias="_id")
    user_id: str
    title: str
    description: Optional[str] = None
    tags: List[str]
    available: bool = False
    duration_in_sec: float
    date_created: datetime
    date_modified: datetime


class VideoUpdate(BaseModel):
    title: str = ""
    description: Optional[str] = None
    tags: List[str] = []


{
    "streams": [
        {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High 10",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "closed_captions": 0,
            "has_b_frames": 2,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
            "pix_fmt": "yuv420p10le",
            "level": 40,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "refs": 1,
            "is_avc": "true",
            "nal_length_size": "4",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "time_base": "1/15360",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 224256,
            "duration": "14.600000",
            "bit_rate": "23424164",
            "bits_per_raw_sample": "10",
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
            },
            "tags": {
                "language": "und",
                "handler_name": "VideoHandler",
                "vendor_id": "[0][0][0][0]",
                "encoder": "Lavc59.37.100 libx264",
            },
        }
    ],
    "format": {
        "filename": "test.mp4",
        "nb_streams": 1,
        "nb_programs": 0,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime / MOV",
        "start_time": "0.000000",
        "duration": "14.600000",
        "size": "42753669",
        "bit_rate": "23426667",
        "probe_score": 100,
        "tags": {
            "major_brand": "iso5",
            "minor_version": "512",
            "compatible_brands": "iso5iso6mp41",
            "encoder": "Lavf59.27.100",
        },
    },
}
