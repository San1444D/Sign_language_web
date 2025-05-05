from flask import request, Response, stream_with_context, jsonify
from firebase_admin import firestore
import numpy as np
import ffmpeg
import threading
import re

from .config import df, logger

# === Precompute label-to-path mapping and max n-gram size ===
label_to_path = dict(zip(df['label'].str.lower(), df['path']))
max_ngram = max(len(label.split()) for label in label_to_path)


# Log stderr output in a separate thread
def log_stderr(process):
    for line in iter(process.stderr.readline, b''):
        # print(f"FFmpeg stderr: {line.decode('utf-8').strip()}")
        pass



def get_user_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    return ip

def extract_keypoints(results):
    pose = np.array([[res['x'], res['y'], res['z'], res['visibility']] for res in results['pose_landmarks']]).flatten() if results['pose_landmarks'] else np.zeros(33*4)
    face = np.array([[res['x'], res['y'], res['z']] for res in results['face_landmarks']]).flatten() if results['face_landmarks'] else np.zeros(468*3)
    lh = np.array([[res['x'], res['y'], res['z']] for res in results['left_hand_landmarks']]).flatten() if results['left_hand_landmarks'] else np.zeros(21*3)
    rh = np.array([[res['x'], res['y'], res['z']] for res in results['right_hand_landmarks']]).flatten() if results['right_hand_landmarks'] else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


def create_user_document(uid: str, email: str, display_name: str = None) -> dict:
    """
    Creates a default user document with all required fields
    """
    return {
        # Required fields
        "uid": uid,
        "email": email,
        "name": display_name or email.split('@')[0],
        "created_at": firestore.SERVER_TIMESTAMP,
        
        # Optional profile fields
        "picture": None,
        "phone_number": None,
        "bio": None,
        "disablity": None,
        
        # Application specific fields
        "is_active": True,
        "is_deleted": False,
        "is_verified": False,

        "last_login": firestore.SERVER_TIMESTAMP,
        "role": "user",  # Default role
        
        # Learning progress
        "completed_lessons": [],
        "practice_sessions": 0,
        "accuracy_rate": 0.0,
        
        # Settings and preferences
        # "notification_settings": {
        #     "email_notifications": True,
        #     "push_notifications": True
        # },
        "language_preference": "en",  # Default to English
        # "accessibility_settings": {
        #     "high_contrast": False,
        #     "large_text": False
        # },
        
        # Metadata
        "updated_at": firestore.SERVER_TIMESTAMP,
        "device_info": {}
    }





def merge_videos_in_memory(video_paths):
    """
    Merges multiple video files into a single video stream using FFmpeg.
    This function streams the merged video in memory without saving it to disk.
    """
    try:
        streams = []
        for path in video_paths:
            input_stream = ffmpeg.input(path)
            streams.append(input_stream.video)  # Only take the video stream

        # Concat only videos (no audio)
        concat_stream = ffmpeg.concat(*streams, v=1, a=0).output('pipe:', format='matroska')

        # Run ffmpeg
        process = concat_stream.run_async(pipe_stdout=True, pipe_stderr=True)
        threading.Thread(target=log_stderr, args=(process,), daemon=True).start()

        while True:
            chunk = process.stdout.read(1024 * 1024)
            if not chunk:
                break
            yield chunk

        process.wait()

    except Exception as e:
        logger.error(f"Error merging videos: {e}")
        raise


def get_video_paths(text: str):
    """
    Tokenize input text, match largest n-gram labels first,
    and return list of video paths in order.
    """
    clean = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    tokens = clean.split()
    L = len(tokens)
    paths = []
    i = 0
    while i < L:
        matched = False
        # try largest ngram down to 1
        for n in range(min(max_ngram, L - i), 0, -1):
            phrase = " ".join(tokens[i:i+n])
            if phrase in label_to_path:
                paths.append(label_to_path[phrase])
                i += n
                matched = True
                break
        if not matched:
            logger.warning(f"No video found for token: {tokens[i]}")
            i += 1
    return paths



def play_video(text: str):
    """
    Stream a merged ISL video for the given English text or paragraph.
    Supports multi-word phrases and variable-length input.
    """
    try:
        text = text or ''
        if not text.strip():
            return jsonify({"error": "Missing or empty 'text' in request"}), 400

        # Get video paths via optimized n-gram matching
        video_paths = get_video_paths(text)
        if not video_paths:
            return jsonify({"error": "No matching videos found"}), 404

        # Stream concatenated videos as Matroska
        return Response(
            stream_with_context(merge_videos_in_memory(video_paths)),
            mimetype='video/x-matroska',
            headers={
                'Content-Disposition': 'inline',
                'Cache-Control': 'no-cache',
            }
        )

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise
