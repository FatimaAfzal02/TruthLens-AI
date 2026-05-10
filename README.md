# TruthLens AI

A Vision Language Model-powered misinformation detection system that analyzes image-caption pairs to identify fake news and manipulated media.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

TruthLens AI performs multi-layered analysis on image-caption pairs by leveraging state-of-the-art Vision Language Models to understand image content, verify textual consistency, and identify suspicious claims.

### Key Features

- **Four-Stage Detection Pipeline** — Specialized modules work together for robust verification
- **Visual Understanding** — LLaVA model for advanced visual reasoning via Groq API
- **Semantic Matching** — CLIP for precise image-text consistency scoring
- **Metadata Analysis** — Location, timestamp, and EXIF data verification
- **Fast Inference** — Groq API integration for low-latency results
- **Web Interface** — Streamlit-based application for interactive use

---

## Pipeline Architecture

```
Input (Image + Caption)
        |
        v
+---------------------------------------+
|  Module 1: Blind Image Analysis       |
|  (LLaVA - Visual Understanding)       |
|  - Describes visual content           |
|  - Flags visual anomalies             |
|  - Estimates AI generation likelihood |
+---------------------------------------+
        |
        v
+---------------------------------------+
|  Module 2: Caption Consistency        |
|  (CLIP - Semantic Similarity)         |
|  - Matches image with caption         |
|  - Detects semantic misalignment      |
|  - Calculates similarity score        |
+---------------------------------------+
        |
        v
+---------------------------------------+
|  Module 3: Metadata Verification      |
|  (EXIF & Location Analysis)           |
|  - Validates camera metadata          |
|  - Verifies GPS coordinates           |
|  - Checks timestamp integrity         |
+---------------------------------------+
        |
        v
+---------------------------------------+
|  Module 4: Verdict Engine             |
|  (Decision Logic)                     |
|  - Aggregates all module evidence     |
|  - Applies weighted scoring           |
|  - Produces final classification      |
+---------------------------------------+
        |
        v
Output: AUTHENTIC / SUSPICIOUS / FAKE
```

---

## Tech Stack

| Component         | Technology              | Purpose                          |
|-------------------|-------------------------|----------------------------------|
| Vision Model      | LLaVA (via Groq API)    | Image understanding and analysis |
| Semantic Matching | CLIP                    | Image-text consistency checking  |
| Web Interface     | Streamlit               | Interactive web application      |
| Core Engine       | Python 3.8+             | Implementation and orchestration |
| Image Processing  | Pillow, OpenCV          | Image handling and metadata      |
| Deep Learning     | PyTorch                 | Neural network operations        |

---

## Requirements

- Python 3.8+
- Groq API Key (free from [console.groq.com](https://console.groq.com))
- CUDA-capable GPU (optional, for faster inference)
- 4 GB RAM minimum (8 GB recommended)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/truthlens-ai.git
cd truthlens-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
DEVICE=cuda  # or 'cpu' if no GPU available
```

Obtain a free Groq API key at: https://console.groq.com

---

## Usage

### Web Interface

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`, upload an image, provide a caption, and submit for analysis.

### Command Line

```bash
python main.py --image path/to/image.jpg --caption "Caption text here"
```

### Programmatic API

```python
from src.pipeline import TruthLensPipeline
from src.config import Config

config = Config()
pipeline = TruthLensPipeline(config)

result = pipeline.analyze(
    image_path="path/to/image.jpg",
    caption="Image caption here"
)

print(result["verdict"])      # AUTHENTIC, SUSPICIOUS, or FAKE
print(result["confidence"])   # Confidence score (0-100)
print(result["evidence"])     # Supporting evidence list
```

### Google Colab

Open `notebooks/TruthLens_AI.ipynb` in Google Colab and run cells sequentially. No local setup required.

---

## Project Structure

```
truthlens-ai/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration and constants
│   ├── pipeline.py               # Main detection pipeline
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── vision_analyzer.py    # Module 1: LLaVA visual analysis
│   │   ├── clip_matcher.py       # Module 2: CLIP semantic matching
│   │   ├── metadata_checker.py   # Module 3: EXIF verification
│   │   └── verdict_engine.py     # Module 4: Decision logic
│   └── utils/
│       ├── __init__.py
│       ├── image_loader.py       # Image loading and validation
│       ├── metadata_extractor.py # EXIF data extraction
│       └── logger.py             # Logging utilities
│
├── notebooks/
│   └── TruthLens_AI.ipynb        # Google Colab notebook
│
├── app.py                        # Streamlit web interface
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore
├── LICENSE
└── README.md
```

---

## Module Details

### Module 1: Blind Image Analysis (LLaVA)

Analyzes the raw image independently of the caption to eliminate confirmation bias.

- Produces a detailed image description
- Detects visual anomalies and synthetic artifacts
- Scores AI generation likelihood (0-10)
- Identifies real-photograph indicators

### Module 2: Caption Consistency (CLIP)

Measures semantic alignment between the image and its associated caption.

- Computes a similarity score (0-1)
- Classifies alignment as matching, partial, or misaligned
- Reports specific mismatch indicators

### Module 3: Metadata Verification

Extracts and validates EXIF data embedded in the image file.

- Reads camera model and manufacturer
- Parses GPS coordinates
- Validates timestamp fields
- Detects AI software signatures (e.g., Stable Diffusion, Midjourney)

### Module 4: Verdict Engine

Aggregates evidence from all modules using a weighted scoring system.

- Fake signals: +1 to +4 points per indicator
- Authentic signals: +1 to +3 points per indicator
- Produces a final verdict with confidence score and supporting evidence

---

## Example Output

```
======================================================================
                    TruthLens AI Detection Report
======================================================================

Verdict:     SUSPICIOUS
Confidence:  78%

Evidence Against Authenticity:
  - Very high AI likelihood (8/10)
  - Caption mismatch detected (similarity: 0.42)
  - No GPS data found

Evidence For Authenticity:
  - EXIF metadata present
  - Camera: Canon EOS 5D Mark IV
  - Timestamp: 2024-01-15 14:32:00

Analysis Scores:
  AI Likelihood          : 8/10
  Image-Caption Match    : 0.420
  Metadata Authenticity  : 0.55

Reasoning:
  This content contains indicators that warrant further investigation.
  There is a moderate to high AI generation likelihood (8/10). The
  caption partially aligns with the image (similarity: 0.42).
  Additional verification from reliable sources is recommended.

======================================================================
```

---

## API Keys and Credentials

### Obtaining a Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Create a free account
3. Navigate to **API Keys**
4. Generate a new key
5. Add it to your `.env` file

**Never commit API keys to version control.** Use `.env` with `.gitignore` to keep credentials out of your repository.

---

## Troubleshooting

**API Key Not Found**
Ensure a `.env` file exists in the project root containing `GROQ_API_KEY=your_key`.

**CUDA Out of Memory**
Set `DEVICE=cpu` in `.env`, or reduce input image resolution before analysis.

**Slow Processing**
Enable GPU acceleration if available. Limit input images to 1024x1024 pixels maximum. Verify network connectivity for Groq API calls.

**Low Accuracy**
Use high-resolution, uncompressed images. Ensure captions are contextually relevant to the image. Confirm the selected model is available through your Groq account.

---

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) — System design and module interactions
- [API Reference](docs/API.md) — Function signatures and return values
- [Contributing Guide](CONTRIBUTING.md) — Development workflow and standards
- [FAQ](docs/FAQ.md) — Common questions and troubleshooting

---

## Contributing

Contributions are welcome. Please review [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: description'`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/truthlens-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/truthlens-ai/discussions)

---

## Acknowledgments

- **LLaVA** — Visual language model for image understanding
- **CLIP** — Semantic image-text matching by OpenAI
- **Groq** — High-speed inference API
- **Streamlit** — Web interface framework
- **PyTorch** — Deep learning foundation

---

## Disclaimer

TruthLens AI is a decision-support tool and should not be treated as a definitive authority on content authenticity. Always corroborate findings with additional research and credible sources.
