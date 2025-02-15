import subprocess

from core.storage import storage


def generate_hls(input_file: str, prefix: str, video_id: str):
    # Command to check if there is an audio stream
    check_audio_cmd = ["ffmpeg", "-i", input_file]

    try:
        # Run the command to check for audio
        result = subprocess.run(
            check_audio_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        has_audio = "Audio" in result.stderr
        print(has_audio)

        if not has_audio:
            command = [
                "ffmpeg",
                "-i",
                input_file,
                "-filter_complex",
                "[0:v]split=3[v1][v2][v3]; "
                "[v1]scale=w=1920:h=1080[v1out]; "
                "[v2]scale=w=1280:h=720[v2out]; "
                "[v3]scale=w=854:h=480[v3out]",
                "-map",
                "[v1out]",
                "-c:v:0",
                "libx264",
                "-b:v:0",
                "5000k",
                "-maxrate:v:0",
                "5350k",
                "-bufsize:v:0",
                "7500k",
                "-map",
                "[v2out]",
                "-c:v:1",
                "libx264",
                "-b:v:1",
                "2800k",
                "-maxrate:v:1",
                "2996k",
                "-bufsize:v:1",
                "4200k",
                "-map",
                "[v3out]",
                "-c:v:2",
                "libx264",
                "-b:v:2",
                "1400k",
                "-maxrate:v:2",
                "1498k",
                "-bufsize:v:2",
                "2100k",
                "-f",
                "hls",
                "-hls_time",
                "10",
                "-hls_playlist_type",
                "vod",
                "-hls_flags",
                "independent_segments",
                "-hls_segment_type",
                "mpegts",
                "-hls_segment_filename",
                f"{prefix}/stream_%v/data%03d.ts",
                "-master_pl_name",
                f"master.m3u8",
                "-var_stream_map",
                "v:0 v:1 v:2",
                f"{prefix}/stream_%v/playlist.m3u8",
            ]
        else:
            command = [
                "ffmpeg",
                "-i",
                input_file,
                "-filter_complex",
                "[0:v]split=3[v1][v2][v3]; "
                "[v1]scale=w=1920:h=1080[v1out]; "
                "[v2]scale=w=1280:h=720[v2out]; "
                "[v3]scale=w=854:h=480[v3out]",
                "-map",
                "[v1out]",
                "-c:v:0",
                "libx264",
                "-b:v:0",
                "5000k",
                "-maxrate:v:0",
                "5350k",
                "-bufsize:v:0",
                "7500k",
                "-map",
                "[v2out]",
                "-c:v:1",
                "libx264",
                "-b:v:1",
                "2800k",
                "-maxrate:v:1",
                "2996k",
                "-bufsize:v:1",
                "4200k",
                "-map",
                "[v3out]",
                "-c:v:2",
                "libx264",
                "-b:v:2",
                "1400k",
                "-maxrate:v:2",
                "1498k",
                "-bufsize:v:2",
                "2100k",
                "-map",
                "a:0",
                "-c:a",
                "aac",
                "-b:a:0",
                "192k",
                "-ac",
                "2",
                "-map",
                "a:0",
                "-c:a",
                "aac",
                "-b:a:1",
                "128k",
                "-ac",
                "2",
                "-map",
                "a:0",
                "-c:a",
                "aac",
                "-b:a:2",
                "96k",
                "-ac",
                "2",
                "-f",
                "hls",
                "-hls_time",
                "10",
                "-hls_playlist_type",
                "vod",
                "-hls_flags",
                "independent_segments",
                "-hls_segment_type",
                "mpegts",
                "-hls_segment_filename",
                f"{prefix}/stream_%v/data%03d.ts",
                "-master_pl_name",
                "master.m3u8",
                "-var_stream_map",
                "v:0,a:0 v:1,a:1 v:2,a:2",
                f"{prefix}/stream_%v/playlist.m3u8",
            ]

        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during HLS conversion: {e}")
        print(e.stderr)
        storage.video_delete_record({"_id": video_id})
    else:
        storage.video_update_record({"_id": video_id}, update={"available": True})
