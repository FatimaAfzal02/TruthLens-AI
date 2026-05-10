"""
Module 1: Vision Analyzer

Performs blind image analysis using LLaVA vision model via Groq API.
Analyzes visual content without caption bias to detect anomalies
and assess likelihood of AI generation.
"""

import os
import base64
from typing import Dict, List, Any
from pathlib import Path
import logging

try:
 from groq import Groq
except ImportError:
 raise ImportError("Groq library not found. Install with: pip install groq")

logger = logging.getLogger(__name__)


class VisionAnalyzer:
 """
 Analyzes images using LLaVA model to detect visual anomalies
 and assess AI generation likelihood.
 """
 
 def __init__(self, api_key: str, model_name: str = "llava-1.5-7b-4096-preview"):
 """
 Initialize Vision Analyzer with Groq API.
 
 Args:
 api_key (str): Groq API key
 model_name (str): Vision model name to use
 """
 if not api_key:
 raise ValueError("Groq API key is required")
 
 self.client = Groq(api_key=api_key)
 self.model_name = model_name
 self.timeout = 30
 
 logger.info(f"VisionAnalyzer initialized with model: {model_name}")
 
 def _encode_image_to_base64(self, image_path: str) -> str:
 """
 Convert image file to base64 string for API transmission.
 
 Args:
 image_path (str): Path to image file
 
 Returns:
 str: Base64 encoded image string
 """
 with open(image_path, "rb") as image_file:
 return base64.standard_b64encode(image_file.read()).decode("utf-8")
 
 def _get_image_media_type(self, image_path: str) -> str:
 """
 Determine media type from file extension.
 
 Args:
 image_path (str): Path to image file
 
 Returns:
 str: Media type (e.g., 'image/jpeg')
 """
 ext = Path(image_path).suffix.lower()
 media_types = {
 ".jpg": "image/jpeg",
 ".jpeg": "image/jpeg",
 ".png": "image/png",
 ".webp": "image/webp",
 ".gif": "image/gif",
 ".bmp": "image/bmp",
 }
 return media_types.get(ext, "image/jpeg")
 
 def analyze(self, image_path: str, custom_prompt: str = None) -> Dict[str, Any]:
 """
 Perform blind image analysis (without caption context).
 
 Args:
 image_path (str): Path to image file
 custom_prompt (str, optional): Custom analysis prompt
 
 Returns:
 dict: Analysis results containing:
 - assessment: Detailed visual assessment
 - description: Image description
 - ai_likelihood: Score 0-10 for AI generation
 - visual_flags: List of concerning visual features
 - real_indicators: List of authenticity indicators
 """
 
 if not Path(image_path).exists():
 raise FileNotFoundError(f"Image not found: {image_path}")
 
 try:
 # Encode image to base64
 image_base64 = self._encode_image_to_base64(image_path)
 media_type = self._get_image_media_type(image_path)
 
 # Default analysis prompt
 if custom_prompt is None:
 custom_prompt = """Analyze this image carefully:

1. **Visual Description**: What do you see in detail?
2. **AI Generation Assessment**: Does this look AI-generated or real? Why?
3. **Confidence Score** (0-10): How confident are you it's AI-generated?
4. **Red Flags**: List any suspicious visual elements
5. **Authenticity Indicators**: List features that suggest it's real

Be specific and technical in your analysis."""
 
 # Call Groq API with vision model
 message = self.client.messages.create(
 model=self.model_name,
 max_tokens=1024,
 messages=[
 {
 "role": "user",
 "content": [
 {
 "type": "image",
 "source": {
 "type": "base64",
 "media_type": media_type,
 "data": image_base64,
 },
 },
 {
 "type": "text",
 "text": custom_prompt
 }
 ],
 }
 ],
 )
 
 response_text = message.content[0].text
 
 # Parse response to extract structured information
 analysis_result = self._parse_vision_response(response_text)
 analysis_result["raw_response"] = response_text
 
 logger.info(f"Vision analysis completed for: {image_path}")
 return analysis_result
 
 except Exception as e:
 logger.error(f"Error during vision analysis: {str(e)}")
 return {
 "assessment": f"Analysis failed: {str(e)}",
 "description": "",
 "ai_likelihood": 5,
 "visual_flags": [],
 "real_indicators": [],
 "error": str(e)
 }
 
 def _parse_vision_response(self, response: str) -> Dict[str, Any]:
 """
 Parse vision model response into structured data.
 
 Args:
 response (str): Raw response from vision model
 
 Returns:
 dict: Structured analysis results
 """
 
 result = {
 "assessment": response,
 "description": "",
 "ai_likelihood": 5, # Default neutral score
 "visual_flags": [],
 "real_indicators": [],
 }
 
 # Extract AI likelihood score from response
 response_lower = response.lower()
 
 # Look for confidence/likelihood mentions
 keywords_high_ai = [
 "likely ai-generated",
 "probably ai",
 "appears synthetic",
 "generated image",
 "artificial",
 "8/10", "9/10", "10/10",
 ]
 
 keywords_low_ai = [
 "real photograph",
 "authentic photo",
 "genuine",
 "not ai-generated",
 "0/10", "1/10", "2/10", "3/10",
 ]
 
 # Score based on keywords
 ai_score = 5
 
 high_ai_matches = sum(1 for kw in keywords_high_ai if kw in response_lower)
 low_ai_matches = sum(1 for kw in keywords_low_ai if kw in response_lower)
 
 if high_ai_matches > low_ai_matches:
 ai_score = min(10, 5 + high_ai_matches * 2)
 elif low_ai_matches > high_ai_matches:
 ai_score = max(0, 5 - low_ai_matches * 2)
 
 result["ai_likelihood"] = ai_score
 
 # Extract visual flags and indicators from response
 lines = response.split("\n")
 in_flags = False
 in_indicators = False
 
 for line in lines:
 line_lower = line.lower()
 
 # Identify sections
 if "flag" in line_lower or "suspicious" in line_lower or "red flag" in line_lower:
 in_flags = True
 in_indicators = False
 continue
 elif "indicator" in line_lower or "authentic" in line_lower:
 in_indicators = True
 in_flags = False
 continue
 
 # Extract items from sections
 if line.strip() and (in_flags or in_indicators):
 if line.strip().startswith(("-", "•", "*", "–")):
 item = line.strip().lstrip("-•*–").strip()
 if item:
 if in_flags:
 result["visual_flags"].append(item)
 else:
 result["real_indicators"].append(item)
 
 # Extract description if mentioned
 if "description" in response_lower:
 desc_start = response_lower.find("description")
 desc_end = response_lower.find(".", desc_start + 100)
 if desc_end > desc_start:
 result["description"] = response[desc_start+11:desc_end+1].strip()
 
 return result
 
 def batch_analyze(self, image_paths: List[str]) -> List[Dict[str, Any]]:
 """
 Analyze multiple images.
 
 Args:
 image_paths (List[str]): List of image file paths
 
 Returns:
 List[Dict]: List of analysis results
 """
 results = []
 for idx, image_path in enumerate(image_paths, 1):
 logger.info(f"Processing image {idx}/{len(image_paths)}: {image_path}")
 result = self.analyze(image_path)
 result["file"] = image_path
 results.append(result)
 
 return results


# Example usage
if __name__ == "__main__":
 # Setup logging
 logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
 )
 
 # Initialize analyzer
 api_key = os.getenv("GROQ_API_KEY")
 analyzer = VisionAnalyzer(api_key)
 
 # Example analysis (uncomment with actual image path)
 # result = analyzer.analyze("path/to/test/image.jpg")
 # print("\nAnalysis Result:")
 # print(f" AI Likelihood: {result['ai_likelihood']}/10")
 # print(f" Visual Flags: {result['visual_flags']}")
 # print(f" Real Indicators: {result['real_indicators']}")
