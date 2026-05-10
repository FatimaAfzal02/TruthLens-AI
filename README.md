# TruthLens AI

A Vision Language Model-powered misinformation detection system that analyzes image-caption pairs to identify fake news and manipulated media.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

# Overview

TruthLens AI performs multi-layered analysis on image-caption pairs using Vision Language Models and semantic similarity techniques to detect misinformation, manipulated media, and suspicious content.

The system combines:

- Visual understanding
- Image-caption consistency verification
- Metadata analysis
- Rule-based verdict generation

---

# Key Features

- Multi-stage misinformation detection pipeline
- Vision-language reasoning using LLaVA via Groq API
- CLIP-based image-caption semantic matching
- EXIF metadata inspection and validation
- Weighted verdict scoring system
- Modular Python architecture

---

# Detection Pipeline

```text
Input (Image + Caption)
        |
        v
+---------------------------------------+
|  Module 1: Blind Image Analysis       |
|  - Visual scene understanding         |
|  - AI generation likelihood           |
|  - Anomaly detection                  |
+---------------------------------------+
        |
        v
+---------------------------------------+
|  Module 2: Caption Consistency        |
|  - Image-text similarity scoring      |
|  - Semantic alignment verification    |
+---------------------------------------+
        |
        v
+---------------------------------------+
|  Module 3: Metadata Verification      |
|  - EXIF inspection                    |
|  - GPS and timestamp validation       |
|  - Editing software detection         |
+---------------------------------------+
        |
        v
+---------------------------------------+
|  Module 4: Verdict Engine             |
|  - Weighted evidence aggregation      |
|  - Final authenticity classification  |
+---------------------------------------+
        |
        v
Output: AUTHENTIC / SUSPICIOUS / FAKE
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Vision Analysis | LLaVA via Groq API |
| Semantic Matching | CLIP |
| Core Language | Python 3.8+ |
| Image Processing | Pillow, OpenCV |
| Deep Learning | PyTorch |

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/FatimaAfzal02/TruthLens-AI.git
cd TruthLens-AI
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

Get a free API key from:

https://console.groq.com

---

# Usage

## Example Usage

```python
from pipeline import TruthLensPipeline

pipeline = TruthLensPipeline()

result = pipeline.analyze(
    image_path="sample.jpg",
    caption="Breaking news image"
)

print(result)
```

---

# Project Structure

```text
TruthLens-AI/
├── clip_matcher.py
├── config.py
├── metadata_checker.py
├── pipeline.py
├── verdict_engine.py
├── vision_analyzer.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── CONTRIBUTING.md
├── PROJECT_STRUCTURE.md
├── LICENSE
└── .gitignore
```

---

# Module Details

## Vision Analyzer

Performs image understanding and visual reasoning using LLaVA.

Capabilities:

- Scene description
- AI-generated content estimation
- Visual anomaly detection
- Context understanding

---

## CLIP Matcher

Measures semantic consistency between image content and captions.

Capabilities:

- Similarity scoring
- Caption alignment verification
- Mismatch detection

---

## Metadata Checker

Extracts and validates EXIF metadata.

Capabilities:

- Camera information extraction
- GPS validation
- Timestamp verification
- Editing software detection

---

## Verdict Engine

Combines evidence from all modules to produce the final classification.

Possible outputs:

- AUTHENTIC
- SUSPICIOUS
- FAKE

---

# Example Output

```text
============================================================
                TruthLens AI Detection Report
============================================================

Verdict:     SUSPICIOUS
Confidence:  78%

Evidence Against Authenticity:
- High AI generation likelihood
- Caption mismatch detected
- Missing GPS metadata

Evidence Supporting Authenticity:
- Valid EXIF metadata present
- Camera information detected

============================================================
```

---

# Requirements

- Python 3.8+
- Internet connection for Groq API access
- 4 GB RAM minimum
- CUDA-compatible GPU (optional)

---

# Troubleshooting

## API Key Error

Ensure your `.env` file contains:

```env
GROQ_API_KEY=your_api_key
```

## Dependency Issues

Upgrade pip before installation:

```bash
python -m pip install --upgrade pip
```

## Slow Processing

- Use smaller image sizes
- Enable GPU acceleration if available
- Ensure stable internet connection

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a pull request

Please review `CONTRIBUTING.md` for contribution guidelines.

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Disclaimer

TruthLens AI is intended as a decision-support tool and should not be treated as a definitive authority on content authenticity.

Always verify critical information through trusted and independent sources.

