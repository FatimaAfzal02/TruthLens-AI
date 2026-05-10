"""
Module 4: Verdict Engine

Combines results from all analysis modules (Vision, CLIP, Metadata)
using weighted scoring system to produce final verdict on image authenticity.
"""

import logging
from typing import Dict, List, Any, Tuple

logger = logging.getLogger(__name__)


class VerdictEngine:
 """
 Decision engine that synthesizes all analysis results
 into a final verdict with confidence score.
 """
 
 def __init__(self, config: Dict[str, Any] = None):
 """
 Initialize Verdict Engine with configuration.
 
 Args:
 config (dict): Configuration dictionary with thresholds
 """
 self.config = config or {}
 
 # Default thresholds
 self.clip_authentic_threshold = self.config.get("clip_authentic_threshold", 0.65)
 self.clip_suspicious_threshold = self.config.get("clip_suspicious_threshold", 0.45)
 self.ai_likelihood_high = self.config.get("ai_likelihood_high", 8)
 self.ai_likelihood_medium = self.config.get("ai_likelihood_medium", 6)
 self.ai_likelihood_low = self.config.get("ai_likelihood_low", 3)
 self.fake_signals_threshold = self.config.get("fake_signals_threshold", 4)
 
 logger.info("VerdictEngine initialized")
 
 def generate_verdict(
 self,
 vision_result: Dict[str, Any],
 clip_result: Dict[str, Any],
 metadata_result: Dict[str, Any]
 ) -> Dict[str, Any]:
 """
 Generate final verdict by combining all analysis results.
 
 Args:
 vision_result (dict): Output from Module 1 (Vision Analyzer)
 clip_result (dict): Output from Module 2 (CLIP Matcher)
 metadata_result (dict): Output from Module 3 (Metadata Checker)
 
 Returns:
 dict: Final verdict with:
 - verdict: 'AUTHENTIC', 'SUSPICIOUS', or 'FAKE'
 - confidence: Confidence score 0-100
 - evidence: Supporting evidence list
 - reasoning: Explanation of verdict
 """
 
 # Initialize scoring
 fake_signals = 0
 real_signals = 0
 evidence_against = []
 evidence_for = []
 
 # ── Module 1: Vision Analysis ──────────────────────────
 logger.debug("Processing vision analysis results...")
 
 ai_score = vision_result.get("ai_likelihood", 5)
 
 if ai_score >= self.ai_likelihood_high:
 fake_signals += 4
 evidence_against.append(f"Very high AI likelihood ({ai_score}/10)")
 elif ai_score >= self.ai_likelihood_medium:
 fake_signals += 2
 evidence_against.append(f"High AI likelihood ({ai_score}/10)")
 elif ai_score <= self.ai_likelihood_low:
 real_signals += 3
 evidence_for.append(f"Looks like real photo ({ai_score}/10)")
 else:
 real_signals += 1
 evidence_for.append(f"Moderate AI score ({ai_score}/10)")
 
 # Add visual flags (max 3)
 for flag in vision_result.get("visual_flags", [])[:3]:
 if flag and len(flag) > 5:
 fake_signals += 1
 evidence_against.append(flag)
 
 # Add real indicators (max 2)
 for indicator in vision_result.get("real_indicators", [])[:2]:
 if indicator and len(indicator) > 5:
 real_signals += 1
 evidence_for.append(indicator)
 
 # ── Module 2: CLIP Semantic Matching ───────────────────
 logger.debug("Processing CLIP similarity results...")
 
 clip_score = clip_result.get("similarity_score", 0.5)
 
 if clip_score >= self.clip_authentic_threshold:
 real_signals += 2
 evidence_for.append(f"High image-caption match ({clip_score:.2f})")
 elif clip_score >= self.clip_suspicious_threshold:
 fake_signals += 1
 evidence_against.append(f"Moderate caption mismatch ({clip_score:.2f})")
 else:
 fake_signals += 3
 evidence_against.append(f"Caption strongly misaligned ({clip_score:.2f})")
 
 # ── Module 3: Metadata Analysis ────────────────────────
 logger.debug("Processing metadata results...")
 
 metadata = metadata_result.get("metadata_summary", {})
 
 if not metadata.get("has_exif"):
 fake_signals += 2
 evidence_against.append("No EXIF metadata found")
 else:
 real_signals += 1
 evidence_for.append("EXIF metadata present")
 
 # Check camera model
 if not metadata.get("camera_model") and metadata.get("has_exif"):
 fake_signals += 2
 evidence_against.append("No camera model in metadata")
 elif metadata.get("camera_model"):
 real_signals += 2
 evidence_for.append(f"Camera: {metadata['camera_model']}")
 
 # Check GPS
 if not metadata.get("has_gps") and metadata.get("has_exif"):
 fake_signals += 1
 evidence_against.append("No GPS data found")
 elif metadata.get("has_gps"):
 real_signals += 1
 evidence_for.append("GPS data present")
 
 # Check timestamp
 if not metadata.get("timestamp") and metadata.get("has_exif"):
 fake_signals += 1
 evidence_against.append("No timestamp found")
 elif metadata.get("timestamp"):
 real_signals += 1
 evidence_for.append(f"Timestamp: {metadata['timestamp']}")
 
 # ── Final Decision ─────────────────────────────────────
 logger.debug(f"Final scoring - Fake signals: {fake_signals}, Real signals: {real_signals}")
 
 if fake_signals >= self.fake_signals_threshold:
 verdict = "FAKE"
 verdict_emoji = "[FAIL]"
 confidence = min(100, int((fake_signals / self.fake_signals_threshold) * 100))
 elif fake_signals > real_signals:
 verdict = "SUSPICIOUS"
 verdict_emoji = "[WARN]"
 confidence = min(100, int((fake_signals / self.fake_signals_threshold) * 50))
 else:
 verdict = "AUTHENTIC"
 verdict_emoji = "[OK]"
 confidence = min(100, int((real_signals / 5) * 100))
 
 # Build reasoning
 reasoning = self._build_reasoning(
 verdict,
 fake_signals,
 real_signals,
 ai_score,
 clip_score
 )
 
 return {
 "verdict": verdict,
 "verdict_label": verdict_label,
 "confidence": confidence,
 "fake_signals": fake_signals,
 "real_signals": real_signals,
 "evidence_against": evidence_against,
 "evidence_for": evidence_for,
 "reasoning": reasoning,
 "scores": {
 "ai_likelihood": ai_score,
 "clip_similarity": round(clip_score, 3),
 "metadata_authenticity": metadata_result.get("authenticity_score", 0.5),
 }
 }
 
 def _build_reasoning(
 self,
 verdict: str,
 fake_signals: int,
 real_signals: int,
 ai_score: int,
 clip_score: float
 ) -> str:
 """
 Build human-readable reasoning for the verdict.
 
 Args:
 verdict (str): Final verdict
 fake_signals (int): Count of fake indicators
 real_signals (int): Count of authentic indicators
 ai_score (int): AI likelihood score
 clip_score (float): CLIP similarity score
 
 Returns:
 str: Reasoning explanation
 """
 
 reasoning_parts = []
 
 if verdict == "FAKE":
 reasoning_parts.append("This content shows strong indicators of being AI-generated or heavily manipulated.")
 
 if ai_score >= self.ai_likelihood_high:
 reasoning_parts.append(f"The image has a high AI generation likelihood score of {ai_score}/10.")
 
 if clip_score < self.clip_suspicious_threshold:
 reasoning_parts.append(f"The caption significantly mismatches the image content (similarity: {clip_score:.2f}).")
 
 if fake_signals >= self.fake_signals_threshold:
 reasoning_parts.append("Multiple authenticity checks failed, confirming suspicious nature.")
 
 elif verdict == "SUSPICIOUS":
 reasoning_parts.append("This content contains indicators that warrant further investigation.")
 
 if ai_score >= self.ai_likelihood_medium:
 reasoning_parts.append(f"There is a moderate to high AI generation likelihood ({ai_score}/10).")
 
 if self.clip_suspicious_threshold <= clip_score < self.clip_authentic_threshold:
 reasoning_parts.append(f"The caption partially aligns with the image (similarity: {clip_score:.2f}).")
 
 reasoning_parts.append("We recommend additional verification from reliable sources.")
 
 else: # AUTHENTIC
 reasoning_parts.append("This content appears to be authentic with supporting evidence.")
 
 if ai_score <= self.ai_likelihood_low:
 reasoning_parts.append(f"The image shows characteristics of a real photograph (AI score: {ai_score}/10).")
 
 if clip_score >= self.clip_authentic_threshold:
 reasoning_parts.append(f"The caption closely matches the image content (similarity: {clip_score:.2f}).")
 
 if real_signals > fake_signals:
 reasoning_parts.append("Metadata and other authenticity checks support this assessment.")
 
 return " ".join(reasoning_parts)
 
 def generate_report(
 self,
 verdict_result: Dict[str, Any],
 image_path: str = None,
 caption: str = None
 ) -> str:
 """
 Generate formatted text report of the verdict.
 
 Args:
 verdict_result (dict): Output from generate_verdict()
 image_path (str, optional): Path to analyzed image
 caption (str, optional): Analyzed caption
 
 Returns:
 str: Formatted report text
 """
 
 report = []
 report.append("=" * 60)
 report.append("TruthLens AI - Misinformation Detection Report")
 report.append("=" * 60)
 report.append("")
 
 if image_path:
 report.append(f"Image: {image_path}")
 if caption:
 report.append(f"Caption: {caption}")
 
 report.append("")
 report.append(f"Verdict: {verdict_result['verdict_emoji']} {verdict_result['verdict']}")
 report.append(f"Confidence: {verdict_result['confidence']}%")
 report.append("")
 
 report.append("Evidence Against Authenticity:")
 if verdict_result["evidence_against"]:
 for evidence in verdict_result["evidence_against"]:
 report.append(f" [FAIL] {evidence}")
 else:
 report.append(" None")
 
 report.append("")
 report.append("Evidence For Authenticity:")
 if verdict_result["evidence_for"]:
 for evidence in verdict_result["evidence_for"]:
 report.append(f" [OK] {evidence}")
 else:
 report.append(" None")
 
 report.append("")
 report.append("Analysis Scores:")
 report.append(f" • AI Likelihood: {verdict_result['scores']['ai_likelihood']}/10")
 report.append(f" • Image-Caption Match: {verdict_result['scores']['clip_similarity']:.3f}/1.0")
 report.append(f" • Metadata Authenticity: {verdict_result['scores']['metadata_authenticity']:.2f}/1.0")
 
 report.append("")
 report.append("Reasoning:")
 report.append(f" {verdict_result['reasoning']}")
 
 report.append("")
 report.append("=" * 60)
 
 return "\n".join(report)


# Example usage
if __name__ == "__main__":
 logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
 )
 
 # Initialize engine
 engine = VerdictEngine()
 
 # Example results (mock data)
 vision_result = {
 "ai_likelihood": 8,
 "visual_flags": ["Unnatural blur in background", "Synthetic lighting"],
 "real_indicators": [],
 }
 
 clip_result = {
 "similarity_score": 0.3,
 }
 
 metadata_result = {
 "authenticity_score": 0.4,
 "metadata_summary": {
 "has_exif": False,
 "camera_model": None,
 "has_gps": False,
 "timestamp": None,
 },
 }
 
 # Generate verdict
 verdict = engine.generate_verdict(vision_result, clip_result, metadata_result)
 
 # Print report
 report = engine.generate_report(verdict, "test_image.jpg", "A realistic photo")
 print(report)
