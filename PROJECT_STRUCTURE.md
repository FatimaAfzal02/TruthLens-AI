# TruthLens AI — Project Structure

---

## Directory Layout

```
truthlens-ai/
│
├── README.md                       # Project overview and documentation
├── QUICKSTART.md                   # Setup guide
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
│
├── requirements.txt                # Runtime dependencies
├── setup.py                        # Package setup (optional)
├── .gitignore                      # Git exclusion rules
├── .env.example                    # Environment variable template
│
├── src/                            # Source code
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── pipeline.py                 # Pipeline orchestrator
│   │
│   ├── modules/                    # Analysis modules
│   │   ├── __init__.py
│   │   ├── vision_analyzer.py      # Module 1: LLaVA visual analysis
│   │   ├── clip_matcher.py         # Module 2: CLIP semantic matching
│   │   ├── metadata_checker.py     # Module 3: EXIF analysis
│   │   └── verdict_engine.py       # Module 4: Decision logic
│   │
│   └── utils/                      # Shared utilities
│       ├── __init__.py
│       ├── image_loader.py         # Image I/O and validation
│       ├── metadata_extractor.py   # EXIF extraction helpers
│       └── logger.py               # Logging configuration
│
├── notebooks/
│   └── TruthLens_AI.ipynb          # Google Colab notebook
│
├── docs/
│   ├── ARCHITECTURE.md             # Technical architecture
│   ├── API.md                      # API reference
│   ├── FAQ.md                      # Frequently asked questions
│   └── EXAMPLES.md                 # Extended usage examples
│
├── tests/
│   ├── __init__.py
│   ├── test_vision_analyzer.py
│   ├── test_clip_matcher.py
│   ├── test_metadata_checker.py
│   └── test_pipeline.py
│
├── examples/
│   ├── sample_images/              # Sample images for testing
│   ├── example_analysis.py         # Single-image example
│   └── batch_analysis.py           # Batch processing example
│
├── outputs/                        # Analysis results (git-ignored)
│
├── app.py                          # Streamlit web interface
├── main.py                         # CLI entry point
│
└── .github/
    └── workflows/
        └── tests.yml               # CI/CD pipeline
```

---

## File Descriptions

### Root Files

| File              | Purpose                                              |
|-------------------|------------------------------------------------------|
| `README.md`       | Project overview, installation, and usage reference  |
| `QUICKSTART.md`   | Concise setup guide                                  |
| `CONTRIBUTING.md` | Contribution standards and workflow                  |
| `LICENSE`         | MIT License                                          |
| `requirements.txt`| Python package dependencies                          |
| `.gitignore`      | Files and directories excluded from version control  |
| `.env.example`    | Template for required environment variables          |

### Source Code (`src/`)

#### Core Files

**`config.py`** — Centralized configuration
- API settings and model parameters
- Detection thresholds and constants
- Environment variable loading and validation

**`pipeline.py`** — Main orchestrator
- Coordinates all four analysis modules
- Handles module-level error recovery
- Formats and returns structured output
- Generates console reports

#### Modules (`src/modules/`)

**`vision_analyzer.py`** — Module 1: Visual Understanding
- LLaVA model integration via Groq API
- Blind image analysis (caption-independent)
- AI generation likelihood scoring
- Visual anomaly detection

**`clip_matcher.py`** — Module 2: Semantic Matching
- CLIP model for image-text similarity
- Caption consistency verification
- Batch caption comparison
- Semantic alignment classification

**`metadata_checker.py`** — Module 3: Metadata Analysis
- EXIF data extraction and parsing
- GPS coordinate validation
- Camera information verification
- AI software signature detection

**`verdict_engine.py`** — Module 4: Decision Logic
- Weighted multi-signal scoring
- Evidence aggregation and ranking
- Final verdict generation
- Human-readable report formatting

#### Utilities (`src/utils/`)

- **`image_loader.py`** — Image loading, format validation, and resizing
- **`metadata_extractor.py`** — Low-level EXIF extraction utilities
- **`logger.py`** — Structured logging configuration

### Interface Files

**`app.py`** — Streamlit web interface
- Image upload and caption input
- Real-time analysis with progress indicators
- Structured report display

**`main.py`** — Command-line interface
- Argument parsing
- Single and batch image processing
- Script-friendly output formatting

### Documentation (`docs/`)

| File                | Content                                          |
|---------------------|--------------------------------------------------|
| `ARCHITECTURE.md`   | System design, data flow, and technical decisions |
| `API.md`            | Function signatures, parameters, and return types |
| `FAQ.md`            | Troubleshooting and common usage questions        |
| `EXAMPLES.md`       | Advanced usage examples and integration patterns  |

### Tests (`tests/`)

```
tests/
├── test_vision_analyzer.py
│   ├── test_initialization
│   ├── test_analyze
│   └── test_batch_analyze
│
├── test_clip_matcher.py
│   ├── test_initialization
│   ├── test_similarity_calculation
│   └── test_batch_analysis
│
├── test_metadata_checker.py
│   ├── test_exif_extraction
│   ├── test_authenticity_analysis
│   └── test_gps_parsing
│
└── test_pipeline.py
    ├── test_full_pipeline
    ├── test_error_handling
    └── test_output_format
```

Run the full test suite:

```bash
pytest tests/ -v
```

---

## Data Flow

```
Input (Image + Caption)
        |
        v
Vision Analyzer (Module 1)
  - vision_analyzer.py
  - Groq API call
        |
        v
CLIP Matcher (Module 2)
  - clip_matcher.py
  - Semantic similarity computation
        |
        v
Metadata Checker (Module 3)
  - metadata_checker.py
  - EXIF extraction and validation
        |
        v
Verdict Engine (Module 4)
  - verdict_engine.py
  - Weighted scoring and classification
        |
        v
Final Report: AUTHENTIC / SUSPICIOUS / FAKE
```

---

## Security Considerations

### Files That Must Not Be Committed

```
.env                  # API keys and secrets
credentials.json      # Service account credentials
*.pem / *.key         # Private keys
outputs/              # User analysis results
logs/                 # Log files that may contain sensitive data
```

These exclusions are enforced via `.gitignore`.

### Best Practices

- Store all API keys in `.env`; never hardcode them in source files
- Do not analyze images containing personally identifiable information without appropriate authorization
- Avoid logging API keys, user data, or image content in log files
- Use environment-specific configuration rather than committed config files

---

## Installation

### For Users

```bash
git clone https://github.com/yourusername/truthlens-ai.git
cd truthlens-ai
pip install -r requirements.txt
```

### For Contributors

```bash
git clone https://github.com/yourusername/truthlens-ai.git
cd truthlens-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Development Workflow

### Feature Development

1. Create a branch: `git checkout -b feature/your-feature`
2. Implement changes with tests
3. Format: `black src/ *.py`
4. Lint: `flake8 src/ *.py`
5. Test: `pytest tests/ -v`
6. Push and open a Pull Request

### Adding a New Module

1. Create the module file in `src/modules/`
2. Implement the class with full docstrings and type hints
3. Add a corresponding test file in `tests/`
4. Integrate the module into `pipeline.py`
5. Update `docs/ARCHITECTURE.md` and `docs/API.md`

---

## Codebase Statistics

| Component     | Files | Approx. Lines |
|---------------|-------|---------------|
| Modules       | 4     | ~1,200        |
| Utilities     | 3     | ~300          |
| Configuration | 1     | ~200          |
| Pipeline      | 1     | ~350          |
| Interfaces    | 2     | ~500          |
| Tests         | 5     | ~800          |
| Documentation | 6     | ~2,000        |
| **Total**     | **22**| **~5,350**    |

---

## Roadmap

### Phase 1 (Complete)

- [x] Visual analysis module
- [x] CLIP semantic matching
- [x] Metadata extraction
- [x] Verdict engine
- [x] Web interface

### Phase 2 (Planned)

- [ ] Video analysis support
- [ ] Batch processing optimization
- [ ] Database integration for result persistence
- [ ] REST API deployment

### Phase 3 (Future)

- [ ] Browser extension
- [ ] Custom model fine-tuning
- [ ] Real-time monitoring dashboard
- [ ] Mobile application

---

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: README.md, QUICKSTART.md, docs/

---

## License

MIT License — see LICENSE file.
