"""
Configuration Module for TruthLens AI

Manages environment variables, API settings, and system parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
 """Central configuration class for TruthLens AI."""
 
 # ── Project Information ──────────────────────────────────────
 PROJECT_NAME = "TruthLens AI"
 PROJECT_VERSION = "1.0.0"
 PROJECT_DESCRIPTION = "Vision Language Model-powered fake news detection system"
 
 # ── API Configuration ────────────────────────────────────────
 GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
 
 # Vision Model Settings
 VISION_MODEL = "llava-1.5-7b-4096-preview" # LLaVA model via Groq
 
 # CLIP Model Settings
 CLIP_MODEL_NAME = "ViT-B/32"
 CLIP_MODEL_PRETRAINED = "openai"
 
 # ── Device Configuration ─────────────────────────────────────
 DEVICE = os.getenv("DEVICE", "cuda") # 'cuda' or 'cpu'
 
 # ── Image Processing ────────────────────────────────────────
 MAX_IMAGE_SIZE = (1024, 1024) # Maximum image resolution
 MIN_IMAGE_SIZE = (100, 100) # Minimum image resolution
 SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
 
 # ── Analysis Parameters ─────────────────────────────────────
 CLIP_THRESHOLD_AUTHENTIC = 0.65 # Similarity threshold for authentic content
 CLIP_THRESHOLD_SUSPICIOUS = 0.45 # Threshold for suspicious classification
 
 AI_LIKELIHOOD_HIGH = 8 # High AI generation score threshold
 AI_LIKELIHOOD_MEDIUM = 6 # Medium AI generation score threshold
 AI_LIKELIHOOD_LOW = 3 # Low AI generation score threshold
 
 # Verdict thresholds (fake signals)
 FAKE_SIGNALS_THRESHOLD_FAKE = 4 # Signals count for FAKE verdict
 FAKE_SIGNALS_THRESHOLD_SUSPICIOUS = 2 # Signals count for SUSPICIOUS verdict
 
 # ── Output Configuration ────────────────────────────────────
 OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
 RESULTS_FORMAT = "json" # 'json' or 'csv'
 SAVE_REPORTS = True
 
 # ── Logging Configuration ───────────────────────────────────
 LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
 LOG_DIR = "logs"
 LOG_FILE = "truthlens.log"
 
 # ── API Timeout Settings ────────────────────────────────────
 API_REQUEST_TIMEOUT = 30 # Seconds
 API_MAX_RETRIES = 3
 API_RETRY_DELAY = 2 # Seconds between retries
 
 # ── Feature Flags ───────────────────────────────────────────
 ENABLE_METADATA_ANALYSIS = True
 ENABLE_VISUAL_ANALYSIS = True
 ENABLE_SEMANTIC_MATCHING = True
 ENABLE_VERDICT_ENGINE = True
 
 # ── EXIF Analysis Settings ──────────────────────────────────
 EXIF_TAGS_TO_CHECK = {
 "Make": "Camera manufacturer",
 "Model": "Camera model",
 "DateTime": "Original timestamp",
 "GPSInfo": "GPS coordinates",
 "Software": "Image processing software",
 "ExifImageWidth": "Image width",
 "ExifImageHeight": "Image height",
 }
 
 # ── Prompts for Vision Model ────────────────────────────────
 VISION_ANALYSIS_PROMPT = """Analyze this image carefully and provide:
1. A detailed description of what you see in the image
2. Any visual anomalies or unusual features
3. Assessment of whether this looks like a real photograph or AI-generated
4. Confidence level (0-10) that this could be AI-generated
5. List any red flags or authenticity indicators

Be thorough and specific in your analysis."""

 CAPTION_ANALYSIS_PROMPT = """Given the image analysis above, now evaluate the caption:
"{caption}"

Determine:
1. Does the caption accurately describe the image?
2. Are there any mismatches between the image content and caption?
3. What is the confidence level (0-100) that the caption matches the image?

Provide a detailed comparison."""
 
 # ── Verdict Engine Settings ─────────────────────────────────
 VERDICT_SCALE = {
 "AUTHENTIC": "The image and caption pair appear authentic",
 "SUSPICIOUS": "There are indicators suggesting potential misinformation",
 "FAKE": "Strong evidence indicates fake or AI-generated content",
 }
 
 @classmethod
 def validate(cls):
 """Validate critical configuration settings."""
 errors = []
 
 if not cls.GROQ_API_KEY:
 errors.append("GROQ_API_KEY is not set. Please configure it in .env file")
 
 if cls.DEVICE not in ["cuda", "cpu"]:
 errors.append(f"Invalid DEVICE '{cls.DEVICE}'. Must be 'cuda' or 'cpu'")
 
 if cls.CLIP_THRESHOLD_AUTHENTIC < cls.CLIP_THRESHOLD_SUSPICIOUS:
 errors.append("CLIP_THRESHOLD_AUTHENTIC should be >= CLIP_THRESHOLD_SUSPICIOUS")
 
 if errors:
 raise ValueError("\n".join(f"[ERROR] {error}" for error in errors))
 
 return True
 
 @classmethod
 def display(cls):
 """Display all configuration settings (excluding sensitive data)."""
 print("\n" + "="*60)
 print(f" {cls.PROJECT_NAME} v{cls.PROJECT_VERSION}")
 print("="*60)
 
 config_display = {
 "Project": cls.PROJECT_NAME,
 "Version": cls.PROJECT_VERSION,
 "Device": cls.DEVICE,
 "Vision Model": cls.VISION_MODEL,
 "CLIP Model": cls.CLIP_MODEL_NAME,
 "Output Directory": cls.OUTPUT_DIR,
 "Log Level": cls.LOG_LEVEL,
 "Max Image Size": f"{cls.MAX_IMAGE_SIZE[0]}x{cls.MAX_IMAGE_SIZE[1]}",
 "CLIP Authentic Threshold": cls.CLIP_THRESHOLD_AUTHENTIC,
 "Fake Signals Threshold": cls.FAKE_SIGNALS_THRESHOLD_FAKE,
 }
 
 for key, value in config_display.items():
 print(f" {key:<25} : {value}")
 
 print("="*60 + "\n")
