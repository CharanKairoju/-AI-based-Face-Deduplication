# AI-Based Face Deduplication

A simple tool to detect duplicate faces across images and confirm user liveness with a webcam.

---

##  Features

- Scans a folder of images and computes face embeddings
- Finds and logs pairs of duplicate faces based on similarity threshold
- Offers a webcam-based blink detection liveness check to ensure genuine faces

---

##  Project Structure

├── face_deduplication.py # Deduplication + liveness logic
├── dataset/ # Place your input images here
├── duplicates_report.csv # Generated report of duplicates
└── venv/ # (Excluded via .gitignore)

yaml
Copy
Edit

---

##  Getting Started

### Prerequisites

- Python 3.10 (recommended for compatibility)
- Dependencies: fastai, OpenCV, scikit-learn, NumPy, pandas

### Setup

```bash
# from project root
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
Usage
Drop images (.jpg/.png) into the dataset/ folder.

Run the script:

bash
Copy
Edit
python face_deduplication.py
Options will appear:

1: Detect duplicate faces → writes duplicates_report.csv

2: Launch webcam for a blink-based liveness test, then press q to exit

Check duplicates_report.csv for pairs and their similarity scores.

How It Works
Face Deduplication:
Uses face embeddings and cosine similarity to identify similar faces.
You can adjust SIMILARITY_THRESHOLD in the script to make matching more or less strict.

Liveness Check:
Captures webcam feed, uses a simple rolling eye-detection threshold to detect blinks. Two blinks = pass.

Customization Tips
Use a lower SIMILARITY_THRESHOLD to filter more aggressively.

Integrate mediapipe or modern face detectors for better performance and accuracy.

Expand liveness logic with challenges (e.g., “move head left”) or hardware checks.

License & Warranty
MIT License — use freely. No warranty; test thoroughly for production.

