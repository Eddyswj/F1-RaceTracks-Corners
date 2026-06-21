from roboflow import Roboflow
import cv2
import json

rf = Roboflow(api_key="ixTIykvVW00km8WDyB96")
project = rf.workspace().project("f1_corner_detect")
model = project.version("5").model

job_id, signed_url, expire_time = model.predict_video(
    "video.mp4",
    fps=5,
    prediction_type="batch-video",
)

results = model.poll_until_video_results(job_id)

print(json.dumps(results, indent=2))

# Create annotated video from predictions
print(f"\nDebug - Results type: {type(results)}")
print(f"Debug - Results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")

# The results are under the 'f1_corner_detect' key
results_list = results.get("f1_corner_detect", [])
print(f"Debug - Found {len(results_list)} frames in f1_corner_detect")

if results_list:
    try:
        print("Trying...")
        input_path = "video.mp4"
        output_path = "video_annotated.mp4"
        
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Calculate the frame step (how many video frames per prediction)
        # If predictions were sampled at fps=3 but video is 30fps, step = 10
        total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_step = max(1, total_video_frames // len(results_list)) if results_list else 1
        
        print(f"Video has {total_video_frames} frames, {len(results_list)} predictions")
        print(f"Frame step: {frame_step}")
        
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate which prediction index this frame corresponds to
            pred_idx = frame_idx // frame_step
            
            frame_predictions = {}
            if pred_idx < len(results_list):
                frame_predictions = results_list[pred_idx].get("predictions", {})
            
            if frame_predictions:
                y_offset = 30
                for pred_name, pred_data in frame_predictions.items():
                    confidence = pred_data.get("confidence", 0)
                    if confidence > 0.5:
                        confidence_pct = int(confidence * 100)
                        text = f"{pred_name} {confidence_pct}%"
                        
                        # Get text size for background
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 0.7
                        thickness = 2
                        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                        
                        # Draw black background rectangle
                        cv2.rectangle(frame, (8, y_offset - text_size[1] - 5), 
                                     (15 + text_size[0], y_offset + 5), 
                                     (0, 0, 0), -1)
                        
                        # Draw text
                        cv2.putText(frame, text, (10, y_offset), 
                                   font, font_scale, (0, 255, 0), thickness)
                        y_offset += 30
            
            out.write(frame)
            frame_idx += 1
        
        cap.release()
        out.release()
        
        print(f"\n✓ Extracted frames: {len(results_list)}")
        print(f"✓ Video created successfully: {output_path}")
        
    except Exception as e:
        print(f"✗ Error creating video: {e}")
else:
    print("No frames found in results")

