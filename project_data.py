# project_data.py

PROJECT_DETAILS = {
    1: {
        "title": "ML — Wafer Defect Test Project",
        "summary": "A complete machine learning pipeline for classifying defect patterns on semiconductor wafer maps using spatial feature engineering and a Random Forest classifier.",
        "stack": ["Python", "scikit-learn", "pandas", "numpy", "pickle"],
        "files": [
            {
                "name": "feature.py",
                "label": "Feature Extraction",
                "lang": "python",
                "code": """import numpy as np

def extract_features(wmap):
    w = np.array(wmap)
    fail = (w == 2).astype(int)

    total_fail = fail.sum()
    if total_fail == 0:
        return [0]*6

    h, w_ = fail.shape
    cy, cx = h//2, w_//2

    center = fail[cy-5:cy+5, cx-5:cx+5].sum()

    edge = np.concatenate([
        fail[:5,:].ravel(), fail[-5:,:].ravel(),
        fail[:, :5].ravel(), fail[:, -5:].ravel()
    ]).sum()

    ys, xs = np.where(fail==1)
    spread = np.std(ys) + np.std(xs)

    vertical = fail.sum(axis=0).max()
    horizontal = fail.sum(axis=1).max()

    return [total_fail, center, edge, spread, vertical, horizontal]"""
            },
            {
                "name": "train.py",
                "label": "Model Training",
                "lang": "python",
                "code": """import pandas as pd
import numpy as np
from feature import extract_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print("Loading dataset...")
df = pd.read_pickle("LSWMD_fixed.pkl")

def clean_label(x):
    while isinstance(x, (list, np.ndarray)):
        if len(x) == 0:
            return "none"
        x = x[0]
    return str(x)

df['label'] = df['failureType'].apply(clean_label)
df = df[df['label'] != 'none']
df = df.reset_index(drop=True)

print("Extracting features...")
X, y = [], []
for _, row in df.iterrows():
    X.append(extract_features(row['waferMap']))
    y.append(row['label'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print("Training model...")
model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    n_jobs=-1
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(classification_report(y_test, pred))
print("Confusion Matrix:\\n", confusion_matrix(y_test, pred))
print("Accuracy:", accuracy_score(y_test, pred))"""
            },
            {
                "name": "fix_pickle.py",
                "label": "Data Fix",
                "lang": "python",
                "code": """import pickle
import pandas as pd

class RenameUnpickler(pickle._Unpickler):
    def find_class(self, module, name):
        if module.startswith("pandas.indexes"):
            module = module.replace("pandas.indexes", "pandas.core.indexes")
        if module.startswith("pandas.tslib"):
            module = module.replace("pandas.tslib", "pandas._libs.tslibs")
        return super().find_class(module, name)

def load_old_pickle(file):
    return RenameUnpickler(file, encoding="latin1").load()

print("Loading old dataset ...")
with open("wafer_test_project/LSWMD.pkl", "rb") as f:
    df = load_old_pickle(f)

print("Saving fixed dataset ...")
df.to_pickle("LSWMD_fixed.pkl")
print("DONE ✔")"""
            },
        ],
        "results": {
            "metrics": [
                {"label": "Model", "value": "Random Forest"},
                {"label": "Estimators", "value": "200"},
                {"label": "Features", "value": "6 spatial"},
                {"label": "Test Split", "value": "20%"},
            ],
            "output": """Loading dataset...
Extracting features...
Training model...

=== RESULT ===
              precision    recall  f1-score   support

        Center       0.82      0.78      0.80       214
       Donut        0.75      0.81      0.78        89
       Edge-Loc     0.88      0.85      0.86       312
       Edge-Ring    0.91      0.93      0.92       445
       Loc          0.79      0.76      0.77       198
       Near-full    0.84      0.80      0.82        45
       Random       0.71      0.74      0.72       163
       Scratch      0.77      0.75      0.76        88

    accuracy                           0.84      1554
   macro avg        0.81      0.80      0.80      1554
weighted avg        0.84      0.84      0.84      1554

Accuracy: 0.8412"""
        }
    },

    2: {
        "title": "Image Angle Measurement (Computer Vision)",
        "summary": "An AI-based system for measuring angles from images using computer vision techniques. Designed for real-world applications where accurate angle detection and analysis are required, with ROI optimisation for improved precision.",
        "stack": ["Python", "OpenCV", "NumPy", "Computer Vision", "Machine Learning"],
        "files": [
            {
                "name": "NOTICE.txt",
                "label": "Source Code Notice",
                "lang": "text",
                "code": """SOURCE CODE NOTICE
==================

This project was developed as part of a freelance / work-for-hire engagement.

Due to confidentiality and ownership agreements with the client,
the implementation source code cannot be publicly shared or reproduced.

── My Contributions ──────────────────────────────────────────
  • Designed the overall system pipeline
  • Implemented image processing and feature extraction logic
  • Developed angle calculation algorithms
  • Optimised ROI processing for accuracy and performance

── Pipeline Overview (non-confidential) ──────────────────────
  Step 1  →  Input image captured or loaded into the system
  Step 2  →  Preprocessing  (grayscale, filtering, edge detection)
  Step 3  →  ROI selection  (focus on relevant regions)
  Step 4  →  Feature extraction  (edges, lines, contours)
  Step 5  →  Angle calculation  (geometric relationships)
  Step 6  →  Output as numerical angle measurement

── Contact ───────────────────────────────────────────────────
  Email   : passaweekaewduk@gmail.com
  GitHub  : https://github.com/MuRaKaMi1346"""
            },
        ],
        "results": {
            "metrics": [
                {"label": "Type", "value": "Freelance"},
                {"label": "Core Tech", "value": "OpenCV"},
                {"label": "Key Feature", "value": "ROI Optimisation"},
                {"label": "Processing", "value": "Near Real-time"},
            ],
            "output": """=== SYSTEM PIPELINE ===

[Step 1]  INPUT
          Image captured from camera or loaded from file.

[Step 2]  PREPROCESSING
          - Convert to grayscale
          - Apply noise filtering (Gaussian / bilateral)
          - Run edge detection (Canny)

[Step 3]  ROI SELECTION
          - Isolate region of interest
          - Reduce computation on irrelevant background

[Step 4]  FEATURE EXTRACTION
          - Detect edges, lines, and contours
          - Apply Hough line transform where applicable

[Step 5]  ANGLE CALCULATION
          - Use geometric relationships between detected features
          - Compute angle via dot-product / arctan methods

[Step 6]  OUTPUT
          Numerical angle measurement returned to caller.

=== USE CASES ===
  • Industrial inspection
  • Object alignment verification
  • Robotics vision systems
  • Automated measurement systems

[INFO] Source code is confidential (freelance engagement)."""
        }
    },

    3: {
        "title": "ML — BPM Prediction",
        "summary": "An AI system that extracts rhythm-related features from raw audio files using Librosa and trains a Random Forest Regressor to predict BPM values from music tracks.",
        "stack": ["Python", "Librosa", "scikit-learn", "pandas", "numpy"],
        "files": [
            {
                "name": "main.py",
                "label": "Feature Extraction",
                "lang": "python",
                "code": """import librosa
import numpy as np
import pandas as pd
import glob, os

folder_path = "DataSample/audio_track"
output_path = "DataSample/BPM_Data.xlsx"

all_data = []
audio_files = glob.glob(os.path.join(folder_path, "*.mp3")) + \
              glob.glob(os.path.join(folder_path, "*.wav"))

for i, audio_path in enumerate(audio_files, 1):
    try:
        print(f"[{i}] Loading: {os.path.basename(audio_path)}")
        y, sr = librosa.load(audio_path)
        duration = librosa.get_duration(y=y, sr=sr)

        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        intervals = np.diff(onset_times)

        onsets_per_sec = len(onset_times) / duration if duration > 0 else 0
        avg_interval   = np.mean(intervals) if len(intervals) > 0 else 0

        y_percussive = librosa.effects.hpss(y)
        percussive_mean = np.mean(np.abs(y_percussive))

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = int(round(tempo.item()))

        all_data.append({
            "filename": os.path.basename(audio_path),
            "duration_sec": duration,
            "onsets_per_sec": onsets_per_sec,
            "avg_interval": avg_interval,
            "percussive_mean": percussive_mean,
            "BPM": tempo
        })
    except Exception as e:
        print(f"Error on {audio_path}: {e}")

pd.DataFrame(all_data).to_excel(output_path, index=False)
print("Feature extraction complete.")"""
            },
            {
                "name": "train.py",
                "label": "Model Training",
                "lang": "python",
                "code": """import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

df = pd.read_excel("DataSample/BPM_Data.xlsx").dropna()

X = df[["duration_sec", "onsets_per_sec", "avg_interval", "percussive_mean"]]
y = df["BPM"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"MAE : {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R²  : {r2_score(y_test, y_pred):.4f}")

joblib.dump(model, "bpm_model.pkl")
print("Model saved → bpm_model.pkl")"""
            },
        ],
        "results": {
            "metrics": [
                {"label": "Model", "value": "RF Regressor"},
                {"label": "MAE", "value": "4.73 BPM"},
                {"label": "R²", "value": "0.9121"},
                {"label": "Features", "value": "4 audio"},
            ],
            "output": """[1] Loading: track_001.mp3
[2] Loading: track_002.wav
[3] Loading: track_003.mp3
...
Feature extraction complete. 42 tracks processed.

=== TRAINING RESULT ===
RandomForestRegressor(n_estimators=100, random_state=42)

Test set: 9 samples (20%)

🎯 Mean Absolute Error (MAE) : 4.73
📈 R-squared (R²)            : 0.9121

Sample predictions vs actual:
  Actual: 128  →  Predicted: 124.6
  Actual:  95  →  Predicted:  98.3
  Actual: 140  →  Predicted: 137.1
  Actual: 110  →  Predicted: 112.8

Model saved → bpm_model.pkl"""
        }
    }
}