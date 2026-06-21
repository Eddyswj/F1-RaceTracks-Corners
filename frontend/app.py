from pathlib import Path
import json
import sys
import uuid

from flask import Flask, jsonify, render_template, request, send_file

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SPA_MAP_FILE = PROJECT_ROOT / "Tracks" / "Spa" / "Spa trackmap with name.png"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from werkzeug.utils import secure_filename

from run_model import analyze_video

TRACKS_FILE = BASE_DIR / "data" / "tracks.json"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
OUTPUT_DIR = BASE_DIR / "static" / "outputs"

ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "m4v", "webm", "avi"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)
app.config["MAX_CONTENT_LENGTH"] = 600 * 1024 * 1024


def _is_allowed_video(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_VIDEO_EXTENSIONS


def _load_tracks_data():
    with TRACKS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def index():
    tracks_data = _load_tracks_data()
    return render_template("index.html", tracks_data=tracks_data)


@app.get("/api/tracks")
def get_tracks():
    return jsonify(_load_tracks_data())


@app.get("/assets/spa-map")
def spa_map():
    return send_file(SPA_MAP_FILE)


@app.post("/api/analyze")
def analyze_uploaded_video():
    track_id = request.form.get("track", "").strip().lower()
    file = request.files.get("video")

    if not file or not file.filename:
        return jsonify({"error": "Please upload a video file."}), 400

    if not _is_allowed_video(file.filename):
        return jsonify({"error": "Unsupported video format. Use mp4, mov, m4v, webm, or avi."}), 400

    safe_name = secure_filename(file.filename)
    stem = Path(safe_name).stem
    extension = Path(safe_name).suffix.lower() or ".mp4"
    unique_id = uuid.uuid4().hex[:12]

    upload_name = f"{stem}_{unique_id}{extension}"
    output_name = f"{stem}_{unique_id}_annotated.mp4"

    upload_path = UPLOAD_DIR / upload_name
    output_path = OUTPUT_DIR / output_name

    file.save(upload_path)

    try:
        payload = analyze_video(
            input_path=str(upload_path),
            output_path=str(output_path),
            prediction_fps=5,
            confidence_threshold=0.5,
        )
    except Exception as ex:
        return jsonify({"error": f"Model inference failed: {ex}"}), 500

    tracks_data = _load_tracks_data()
    selected_track = tracks_data.get("tracks", {}).get(track_id) if track_id else None

    return jsonify(
        {
            "track": track_id,
            "track_meta": selected_track,
            "video_url": f"/static/uploads/{upload_name}",
            "annotated_video_url": f"/static/outputs/{output_name}",
            "events": payload.get("events", []),
            "prediction_frames": len(payload.get("results_list", [])),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
