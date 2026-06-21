# F1 tracks and corner recognizer
<img src="https://dl.dropboxusercontent.com/scl/fi/mte5g6ffsf1yi50w4s27f/Screenshot-2026-06-21-at-9.44.36-PM.png?rlkey=3wx9l85pu7gfpyuat3h8xxfo4&st=jzcopb8y" width="600">

**Youtube Link**: https://youtu.be/6OtKCJvBxgk

## Purpose
The purpose of this project is to develop a computer vision system that can analyze visual input from Formula 1
races and automatically identify both the race circuit and the specific corner or section of the track.
By leveraging image processing and machine learning techniques, the system aims to bridge the gap between raw visual data and meaningful race context.

## Goal
The primary goal is to build a model that:
- Accurately classifies which Formula 1 track is shown in an image (from the current 24 circuits)
- Identifies the specific corner or segment of that track (e.g., Turn 1, hairpin, chicane)
- Provides clear and interpretable output in real time or near real time

An additional goal is to create a user-friendly system that can be used as an educational or assistive tool for viewers.

## Motivation
Formula 1 is a complex sport with many circuits,
each containing multiple unique corners that are often referenced during commentary.
For new fans and enthusiasts, it can be difficult to recognize which track is being shown or understand the significance of specific corners.

**This project aims to:**
- Help new fans better understand and engage with Formula 1 races
- Provide contextual information about tracks and corners automatically
- Enhance the viewing and learning experience through intelligent visual analysis

---

# File Structure:
The repository should be organised as follows:

Track/<br>
 └── Sector_1/<br>
      ├── Corners/<br>
      │     ├── corner1_{name or na}.jpg<br>
      │     ├── corner2_{name or na}.jpg<br>
      │     └── ...<br>
      └── Straights/<br>
            ├── sector1_{name or na}.jpg<br>
└── Sector_2/<br>
      ├── Corners/<br>
      │     ├── corner1_{name or na}.jpg<br>
      │     ├── corner2_{name or na}.jpg<br>
      │     └── ...<br>
      └── Straights/<br>
            ├── sector1_{name or na}.jpg<br>
└── Sector_3/<br>
      ├── Corners/<br>
      │     ├── corner1_{name or na}.jpg<br>
      │     ├── corner2_{name or na}.jpg<br>
      │     └── ...<br>
      └── Straights/<br>
            ├── sector1_{name or na}.jpg<br>

## Naming Conventions:
For the name that will be placed in the file name it will only be just the popular ones, not corner types.
Use **na** if the segment does not have a known name.

**Corners:**
- Format: corner{number}_{name or na}.jpg
- Example: corner_1_2_3_busstop_chicane.jpg, corner2_na.jpg

**Straights:**
- Format: sector{number}_{name or na}.jpg
- Example: sector1_mainstraight.jpg, sector2_na.jpg

---

## Dataset

The dataset for this project contains approximately **10,000 manually collected and labelled images** from Formula 1 race footage.

There was no publicly available dataset that matched the requirements of recognising both Formula 1 circuits and specific track corners. Therefore, the images were gathered manually from Formula 1 race videos and labelled individually.

Each image is labelled based on:

- **Track name** — the Formula 1 circuit where the image was taken
- **Sector number** — Sector 1, Sector 2, or Sector 3
- **Segment type** — corner or straight
- **Corner number** — for example, Turn 1, Turn 2, or Turn 3
- **Popular corner name**, if applicable — for example, `busstop_chicane`
- **Straight name**, if applicable — for example, `mainstraight`

If a corner or straight does not have a commonly known name, the label `na` is used.

The dataset includes images from different camera angles, weather conditions, lighting conditions, cars, and race sessions. This variation helps the model learn track features more reliably instead of depending only on one camera angle or race condition.

The dataset will be split into training, validation, and testing sets to evaluate the model's ability to classify unseen images correctly.

---

## Interactive Frontend (Track Classroom)

This repository now includes an interactive web app that:

- Lets you upload a race video
- Runs the existing Roboflow model from `run_model.py`
- Generates an annotated video
- Displays a hoverable map with track-specific facts
- Highlights sections in sync with detections while the video plays

### Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the web app:

```bash
python frontend/app.py
```

3. Open the app in your browser:

```text
http://127.0.0.1:5000
```

### Notes

- The Roboflow model configuration is reused exactly from `run_model.py`.
- Uploaded videos are saved to `frontend/static/uploads`.
- Annotated outputs are saved to `frontend/static/outputs`.



