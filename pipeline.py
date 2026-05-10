"""
TruthLens AI - Main Pipeline

Orchestrates all analysis modules (Vision, CLIP, Metadata, Verdict)
to provide comprehensive fake news detection.
"""

import logging
import os
from typing import Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TruthLensPipeline:
 """
 Main pipeline that orchestrates all analysis modules.
 
 Process Flow:
 1. Vision Analyzer (Module 1): Blind image analysis
 2. CLIP Matcher (Module 2): Caption consistency
 3. Metadata Checker (Module 3): EXIF verification
 4. Verdict Engine (Module 4): Final classification
 """
 
 def __init__(self, config: Dict[str, Any] = None):
 """
 Initialize TruthLens Pipeline.
 
 Args:
 config (dict): Configuration dictionary
 """
 self.config = config or self._load_default_config()
 
 # Import modules
 from vision_analyzer import VisionAnalyzer
 from clip_matcher import CLIPMatcher
 from metadata_checker import MetadataChecker
 from verdict_engine import VerdictEngine
 
 # Initialize modules
 logger.info("Initializing TruthLens AI Pipeline...")
 
 try:
 self.vision_analyzer = VisionAnalyzer(
 api_key=self.config.get("groq_api_key"),
 model_name=self.config.get("vision_model", "llava-1.5-7b-4096-preview")
 )
 logger.info("[OK] Vision Analyzer initialized")
 except Exception as e:
 logger.error(f"[FAIL] Failed to initialize Vision Analyzer: {e}")
 self.vision_analyzer = None
 
 try:
 self.clip_matcher = CLIPMatcher(
 model_name=self.config.get("clip_model", "ViT-B/32"),
 device=self.config.get("device", "cuda")
 )
 logger.info("[OK] CLIP Matcher initialized")
 except Exception as e:
 logger.error(f"[FAIL] Failed to initialize CLIP Matcher: {e}")
 self.clip_matcher = None
 
 try:
 self.metadata_checker = MetadataChecker()
 logger.info("[OK] Metadata Checker initialized")
 except Exception as e:
 logger.error(f"[FAIL] Failed to initialize Metadata Checker: {e}")
 self.metadata_checker = None
 
 try:
 self.verdict_engine = VerdictEngine(config)
 logger.info("[OK] Verdict Engine initialized")
 except Exception as e:
 logger.error(f"[FAIL] Failed to initialize Verdict Engine: {e}")
 self.verdict_engine = None
 
 logger.info("Pipeline initialization complete!\n")
 
 def _load_default_config(self) -> Dict[str, Any]:
 """Load default configuration."""
 from dotenv import load_dotenv
 
 load_dotenv()
 
 return {
 "groq_api_key": os.getenv("GROQ_API_KEY", ""),
 "device": os.getenv("DEVICE", "cuda"),
 "vision_model": "llava-1.5-7b-4096-preview",
 "clip_model": "ViT-B/32",
 "clip_authentic_threshold": 0.65,
 "clip_suspicious_threshold": 0.45,
 "ai_likelihood_high": 8,
 "ai_likelihood_medium": 6,
 "ai_likelihood_low": 3,
 "fake_signals_threshold": 4,
 }
 
 def analyze(
 self,
 image_path: str,
 caption: str,
 verbose: bool = False
 ) -> Dict[str, Any]:
 """
 Analyze image-caption pair through all modules.
 
 Args:
 image_path (str): Path to image file
 caption (str): Image caption text
 verbose (bool): Print detailed progress
 
 Returns:
 dict: Complete analysis result with:
 - verdict: Final classification
 - confidence: Confidence score
 - all_results: Raw results from each module
 """
 
 if not Path(image_path).exists():
 raise FileNotFoundError(f"Image not found: {image_path}")
 
 if not caption or not caption.strip():
 raise ValueError("Caption cannot be empty")
 
 logger.info(f"\n{'='*60}")
 logger.info(f"Analyzing: {Path(image_path).name}")
 logger.info(f"Caption: {caption[:50]}...")
 logger.info(f"{'='*60}\n")
 
 results = {}
 
 # ── Module 1: Vision Analysis ──────────────────────────
 if self.vision_analyzer:
 logger.info(" Module 1: Running blind image analysis...")
 try:
 results["vision"] = self.vision_analyzer.analyze(image_path)
 logger.info(f" [OK] AI Likelihood: {results['vision']['ai_likelihood']}/10")
 if verbose:
 logger.debug(f" Visual Flags: {results['vision']['visual_flags']}")
 except Exception as e:
 logger.error(f" [FAIL] Vision analysis failed: {e}")
 results["vision"] = {"ai_likelihood": 5, "visual_flags": [], "real_indicators": []}
 
 # ── Module 2: CLIP Semantic Matching ───────────────────
 if self.clip_matcher:
 logger.info(" Module 2: Analyzing image-caption consistency...")
 try:
 results["clip"] = self.clip_matcher.calculate_similarity(
 image_path,
 caption
 )
 logger.info(f" [OK] Similarity Score: {results['clip']['similarity_score']:.3f}")
 logger.info(f" Status: {results['clip']['match_status']}")
 if verbose:
 logger.debug(f" Description: {results['clip']['description']}")
 except Exception as e:
 logger.error(f" [FAIL] CLIP analysis failed: {e}")
 results["clip"] = {"similarity_score": 0.5, "match_status": "Unknown"}
 
 # ── Module 3: Metadata Analysis ────────────────────────
 if self.metadata_checker:
 logger.info(" Module 3: Extracting and analyzing metadata...")
 try:
 results["metadata"] = self.metadata_checker.analyze_authenticity(
 image_path
 )
 logger.info(f" [OK] Authenticity Score: {results['metadata']['authenticity_score']}")
 logger.info(f" Verdict: {results['metadata']['verdict']}")
 if verbose and results["metadata"].get("red_flags"):
 for flag in results["metadata"]["red_flags"][:3]:
 logger.debug(f" [WARN] {flag}")
 except Exception as e:
 logger.error(f" [FAIL] Metadata analysis failed: {e}")
 results["metadata"] = {
 "authenticity_score": 0.5,
 "metadata_summary": {
 "has_exif": False,
 "camera_model": None,
 "has_gps": False,
 "timestamp": None,
 }
 }
 
 # ── Module 4: Verdict Engine ───────────────────────────
 if self.verdict_engine:
 logger.info(" Module 4: Generating final verdict...")
 try:
 final_verdict = self.verdict_engine.generate_verdict(
 results.get("vision", {}),
 results.get("clip", {}),
 results.get("metadata", {})
 )
 results["verdict"] = final_verdict
 logger.info(f" [OK] Verdict: {final_verdict['verdict_emoji']} {final_verdict['verdict']}")
 logger.info(f" Confidence: {final_verdict['confidence']}%")
 if verbose:
 logger.debug(f" Reasoning: {final_verdict['reasoning']}")
 except Exception as e:
 logger.error(f" [FAIL] Verdict generation failed: {e}")
 results["verdict"] = {
 "verdict": "UNKNOWN",
 "confidence": 0,
 "reasoning": f"Analysis failed: {e}"
 }
 
 logger.info(f"\n{'='*60}")
 logger.info("Analysis Complete!")
 logger.info(f"{'='*60}\n")
 
 return self._format_output(results, image_path, caption)
 
 def _format_output(
 self,
 results: Dict[str, Any],
 image_path: str,
 caption: str
 ) -> Dict[str, Any]:
 """Format analysis results into clean output."""
 
 output = {
 "image": str(image_path),
 "caption": caption,
 "verdict": results.get("verdict", {}).get("verdict", "UNKNOWN"),
 "confidence": results.get("verdict", {}).get("confidence", 0),
 "modules": {
 "vision": results.get("vision", {}),
 "clip": results.get("clip", {}),
 "metadata": results.get("metadata", {}),
 },
 "raw_verdict": results.get("verdict", {}),
 }
 
 return output
 
 def print_report(self, analysis_result: Dict[str, Any]) -> None:
 """Print formatted analysis report."""
 
 verdict = analysis_result["raw_verdict"]
 
 print("\n" + "="*70)
 print(f" {'TruthLens AI Detection Report':^66}")
 print("="*70)
 
 print(f"\nImage: {analysis_result['image']}")
 print(f"Caption: {analysis_result['caption'][:60]}...")
 
 print(f"\n{' VERDICT ':^70}")
 print("-"*70)
 print(f" {verdict['verdict_emoji']} {verdict['verdict']:<15} | Confidence: {verdict['confidence']}%")
 print("-"*70)
 
 print(f"\n{' EVIDENCE AGAINST ':^70}")
 if verdict["evidence_against"]:
 for i, evidence in enumerate(verdict["evidence_against"], 1):
 print(f" {i}. {evidence}")
 else:
 print(" None detected")
 
 print(f"\n{' EVIDENCE FOR ':^70}")
 if verdict["evidence_for"]:
 for i, evidence in enumerate(verdict["evidence_for"], 1):
 print(f" {i}. {evidence}")
 else:
 print(" None detected")
 
 print(f"\n{' ANALYSIS SCORES ':^70}")
 print(f" • AI Likelihood: {verdict['scores']['ai_likelihood']}/10")
 print(f" • Image-Caption Match: {verdict['scores']['clip_similarity']:.3f}/1.0")
 print(f" • Metadata Authenticity: {verdict['scores']['metadata_authenticity']:.2f}/1.0")
 
 print(f"\n{' REASONING ':^70}")
 print(f" {verdict['reasoning']}")
 
 print("\n" + "="*70 + "\n")


# Example usage
if __name__ == "__main__":
 # Initialize pipeline
 pipeline = TruthLensPipeline()
 
 # Example (uncomment with actual image and caption)
 # result = pipeline.analyze(
 # image_path="path/to/image.jpg",
 # caption="A description of the image",
 # verbose=True
 # )
 # 
 # pipeline.print_report(result)
