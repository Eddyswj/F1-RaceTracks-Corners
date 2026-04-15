# F1 tracks and corner recognizer

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

## Roadmap / To-Do

**Phase 1: Data Collection**
- Scrape open-source images
- Download YouTube videos
- Extract frames using ffmpeg

**Phase 2: Data Labeling**
- Define label schema (track + corner)
- Label initial dataset manually
- Implement weak labeling via timestamps

**Phase 3: Model Development**
- Train baseline track classifier
- Evaluate accuracy
- Extend to corner classification

**Phase 4: Optimization**
- Apply data augmentation
- Improve model architecture
- Use semi-supervised learning

**Phase 5: Evaluation**
- Test on unseen race footage
- Measure:
  - Accuracy (track)
  - Accuracy (corner)

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

