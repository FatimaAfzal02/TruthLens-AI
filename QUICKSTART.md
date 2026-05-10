# TruthLens AI — Quick Start Guide

Get TruthLens AI running in under five minutes.

---

## Prerequisites

- Python 3.8+ (`python --version` to verify)
- pip (Python package manager)
- Groq API Key (free from [console.groq.com](https://console.groq.com))
- 4 GB RAM minimum (8 GB recommended)

---

## Step 1: Obtain a Groq API Key

1. Visit https://console.groq.com
2. Create a free account
3. Navigate to **API Keys**
4. Generate a new API key
5. Copy the key — you will need it in Step 3

---

## Step 2: Install TruthLens AI

### Option A: Clone from GitHub (Recommended)

```bash
git clone https://github.com/yourusername/truthlens-ai.git
cd truthlens-ai
```

### Option B: Download as ZIP

1. Click **Code** > **Download ZIP**
2. Extract the archive
3. Open a terminal in the extracted folder

---

## Step 3: Setup and Configuration

### Create a Virtual Environment

```bash
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

```bash
cp .env.example .env
```

Open `.env` and set your API key:

```env
GROQ_API_KEY=your_actual_key_here
DEVICE=cuda  # or 'cpu' if no GPU
```

---

## Step 4: Run TruthLens AI

### Web Interface

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser, upload an image, enter a caption, and click **Analyze**.

### Command Line

```bash
python main.py --image path/to/image.jpg --caption "Caption text here"
```

### Google Colab (No Local Installation)

Open `notebooks/TruthLens_AI.ipynb` in Google Colab and run each cell in sequence.

---

## Verify Installation

```python
from pipeline import TruthLensPipeline

pipeline = TruthLensPipeline()

result = pipeline.analyze(
    image_path="test_image.jpg",
    caption="A test image"
)

print(result["verdict"])
```

---

## Usage Examples

### Single Image Analysis

```bash
streamlit run app.py
# Upload image and caption via the web interface
```

### Batch Analysis

```python
from pipeline import TruthLensPipeline

pipeline = TruthLensPipeline()

images = [
    ("image1.jpg", "Caption 1"),
    ("image2.jpg", "Caption 2"),
    ("image3.jpg", "Caption 3"),
]

for image_path, caption in images:
    result = pipeline.analyze(image_path, caption)
    print(f"{image_path}: {result['verdict']}")
```

### Module-Level Usage

```python
from vision_analyzer import VisionAnalyzer
from clip_matcher import CLIPMatcher
from metadata_checker import MetadataChecker

# Visual analysis only
analyzer = VisionAnalyzer(api_key="your_key")
vision_result = analyzer.analyze("image.jpg")
print(f"AI Likelihood: {vision_result['ai_likelihood']}/10")

# Semantic matching only
matcher = CLIPMatcher()
clip_result = matcher.calculate_similarity("image.jpg", "caption")
print(f"Similarity: {clip_result['similarity_score']:.3f}")

# Metadata analysis only
checker = MetadataChecker()
metadata = checker.analyze_authenticity("image.jpg")
print(f"EXIF Present: {metadata['has_exif']}")
```

---

## Understanding the Output

### Verdict Classification

| Verdict    | Interpretation                         | Recommended Action               |
|------------|----------------------------------------|----------------------------------|
| AUTHENTIC  | Likely a genuine image with a matching caption | Content is probably credible  |
| SUSPICIOUS | Some authenticity concerns detected    | Verify with additional sources   |
| FAKE       | Strong indicators of manipulation or AI generation | Treat as likely misinformation |

### Confidence Score

| Range     | Meaning                                |
|-----------|----------------------------------------|
| 90-100%   | High confidence in verdict             |
| 70-89%    | Moderate-to-high confidence            |
| 50-69%    | Moderate confidence                    |
| Below 50% | Low confidence; insufficient data      |

### Key Metrics

**AI Likelihood (0-10)**

| Score | Interpretation           |
|-------|--------------------------|
| 8-10  | Likely AI-generated      |
| 5-7   | Inconclusive             |
| 0-4   | Likely a real photograph |

**Image-Caption Similarity (0-1)**

| Score     | Interpretation     |
|-----------|--------------------|
| 0.7-1.0   | Strong match       |
| 0.4-0.7   | Partial match      |
| 0.0-0.4   | Significant mismatch |

---

## Troubleshooting

**"GROQ_API_KEY not found"**
Create a `.env` file in the project root and add: `GROQ_API_KEY=your_key`

**"CUDA out of memory"**
Set `DEVICE=cpu` in `.env`.

**"Streamlit not found"**
```bash
pip install streamlit
```

**"Image not found" error**
Use an absolute path (e.g., `/home/user/images/photo.jpg`) or verify the relative path is correct from the project root.

**Slow processing**
Use a GPU if available. Reduce input image size to 1024x1024 or smaller. Check your internet connection for Groq API latency.

---

## Next Steps

- Read the full documentation in `README.md`
- Explore individual modules in `src/modules/`
- Review contribution guidelines in `CONTRIBUTING.md`
- Report issues via GitHub Issues

---

## Notes

- TruthLens AI is a decision-support tool, not a definitive authority
- Always verify findings with credible independent sources
- The free Groq API tier has rate limits; plan batch workloads accordingly
- Do not analyze images containing personally identifiable information without appropriate authorization
