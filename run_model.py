from roboflow import Roboflow
import cv2
import json
import re

rf = Roboflow(api_key="ixTIykvVW00km8WDyB96")
project = rf.workspace().project("f1_corner_detect")
model = project.version("5").model


def _normalize_predictions(predictions):
    if isinstance(predictions, dict):
        normalized = []
        for label, payload in predictions.items():
            confidence = 0.0
            if isinstance(payload, dict):
                confidence = float(payload.get("confidence", 0.0))
            elif isinstance(payload, (float, int)):
                confidence = float(payload)
            normalized.append({"label": label, "confidence": confidence})
        return normalized

    if isinstance(predictions, list):
        normalized = []
        for payload in predictions:
            if not isinstance(payload, dict):
                continue
            label = payload.get("class") or payload.get("label") or payload.get("name")
            if not label:
                continue
            normalized.append({"label": str(label), "confidence": float(payload.get("confidence", 0.0))})
        return normalized

    return []


def _best_prediction(predictions, confidence_threshold=0.5):
    normalized = _normalize_predictions(predictions)
    if not normalized:
        return None

    best = max(normalized, key=lambda p: p.get("confidence", 0.0))
    if best.get("confidence", 0.0) < confidence_threshold:
        return None
    return best


def label_to_section_id(label):
    label_lower = label.lower().strip()

    turn_match = re.search(r"(?:turn|corner)\s*[-_]?\s*(\d+)", label_lower)
    if turn_match:
        return f"turn-{turn_match.group(1)}"

    sector_match = re.search(r"sector\s*[-_]?\s*(\d+)", label_lower)
    if sector_match:
        return f"sector-{sector_match.group(1)}"

    if "drs" in label_lower:
        drs_match = re.search(r"drs\s*[-_]?\s*(\d+)", label_lower)
        if drs_match:
            return f"drs-{drs_match.group(1)}"
        return "drs-1"

    return "unknown"


def build_timeline_events(results_list, prediction_fps=5, confidence_threshold=0.5):
    events = []
    if prediction_fps <= 0:
        prediction_fps = 5

    for idx, entry in enumerate(results_list):
        predictions = entry.get("predictions", {}) if isinstance(entry, dict) else {}
        best = _best_prediction(predictions, confidence_threshold=confidence_threshold)
        if not best:
            continue

        label = best["label"]
        confidence = float(best.get("confidence", 0.0))
        events.append(
            {
                "time": round(idx / float(prediction_fps), 2),
                "frame_index": idx,
                "label": label,
                "confidence": round(confidence, 3),
                "section_id": label_to_section_id(label),
            }
        )
    return events


def annotate_video(input_path, output_path, results_list, confidence_threshold=0.5):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = max(1, total_video_frames // max(1, len(results_list)))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        pred_idx = frame_idx // frame_step
        predictions = {}
        if pred_idx < len(results_list):
            item = results_list[pred_idx]
            if isinstance(item, dict):
                predictions = item.get("predictions", {})

        normalized = [
            p for p in _normalize_predictions(predictions) if p.get("confidence", 0.0) >= confidence_threshold
        ]

        if normalized:
            normalized.sort(key=lambda p: p.get("confidence", 0.0), reverse=True)
            y_offset = 30
            for pred in normalized[:3]:
                text = f"{pred['label']} {int(pred['confidence'] * 100)}%"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                thickness = 2
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

                cv2.rectangle(
                    frame,
                    (8, y_offset - text_size[1] - 5),
                    (15 + text_size[0], y_offset + 5),
                    (0, 0, 0),
                    -1,
                )
                cv2.putText(frame, text, (10, y_offset), font, font_scale, (40, 230, 120), thickness)
                y_offset += 30

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()


def analyze_video(input_path, output_path="video_annotated.mp4", prediction_fps=5, confidence_threshold=0.5):
    job_id, _, _ = model.predict_video(
        input_path,
        fps=prediction_fps,
        prediction_type="batch-video",
    )

    results = model.poll_until_video_results(job_id)
    results_list = results.get("f1_corner_detect", []) if isinstance(results, dict) else []

    if results_list:
        annotate_video(
            input_path=input_path,
            output_path=output_path,
            results_list=results_list,
            confidence_threshold=confidence_threshold,
        )

    events = build_timeline_events(
        results_list=results_list,
        prediction_fps=prediction_fps,
        confidence_threshold=confidence_threshold,
    )

    return {
        "results": results,
        "results_list": results_list,
        "events": events,
        "annotated_video_path": output_path,
    }


def main():
    input_path = "video.mp4"
    output_path = "video_annotated.mp4"
    payload = analyze_video(input_path=input_path, output_path=output_path, prediction_fps=5, confidence_threshold=0.5)

    print(json.dumps(payload.get("results", {}), indent=2))
    print(f"\nFound {len(payload.get('results_list', []))} prediction frames")
    print(f"Built {len(payload.get('events', []))} timeline events")
    print(f"Annotated video: {payload.get('annotated_video_path')}")


if __name__ == "__main__":
    main()

