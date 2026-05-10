"""
Module 2: CLIP Matcher

Performs semantic matching between images and captions using CLIP model.
Calculates image-text similarity scores to detect misalignment.
"""

import torch
import logging
from typing import Dict, Tuple, Any
from pathlib import Path

try:
 import open_clip
except ImportError:
 raise ImportError("open_clip not found. Install with: pip install open-clip-torch")

try:
 from PIL import Image
except ImportError:
 raise ImportError("Pillow not found. Install with: pip install Pillow")

logger = logging.getLogger(__name__)


class CLIPMatcher:
 """
 Semantic matching using CLIP model to detect caption-image misalignment.
 """
 
 def __init__(
 self,
 model_name: str = "ViT-B/32",
 pretrained: str = "openai",
 device: str = "cuda"
 ):
 """
 Initialize CLIP model.
 
 Args:
 model_name (str): CLIP model architecture (e.g., 'ViT-B/32')
 pretrained (str): Pretrained weights source
 device (str): Computation device ('cuda' or 'cpu')
 """
 self.device = device if torch.cuda.is_available() else "cpu"
 self.model_name = model_name
 
 try:
 # Load CLIP model and preprocessing
 self.model, _, self.preprocess = open_clip.create_model_and_transforms(
 model_name,
 pretrained=pretrained,
 device=self.device
 )
 self.tokenizer = open_clip.get_tokenizer(model_name)
 
 # Set to evaluation mode
 self.model.eval()
 
 logger.info(f"CLIP Model loaded: {model_name} on {self.device}")
 
 except Exception as e:
 logger.error(f"Failed to load CLIP model: {str(e)}")
 raise
 
 def _load_and_process_image(self, image_path: str) -> torch.Tensor:
 """
 Load and preprocess image for CLIP.
 
 Args:
 image_path (str): Path to image file
 
 Returns:
 torch.Tensor: Processed image tensor
 """
 if not Path(image_path).exists():
 raise FileNotFoundError(f"Image not found: {image_path}")
 
 image = Image.open(image_path).convert("RGB")
 image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
 
 return image_tensor
 
 def calculate_similarity(self, image_path: str, caption: str) -> Dict[str, Any]:
 """
 Calculate semantic similarity between image and caption.
 
 Args:
 image_path (str): Path to image file
 caption (str): Text caption to compare
 
 Returns:
 dict: Similarity metrics:
 - similarity_score: Float 0-1 indicating match strength
 - match_status: 'High', 'Medium', or 'Low' alignment
 - confidence: Confidence level of assessment
 - description: Explanation of the match
 """
 
 try:
 # Load image
 image_tensor = self._load_and_process_image(image_path)
 
 # Tokenize caption
 caption_lower = caption.strip().lower()
 text_tokens = self.tokenizer([caption_lower]).to(self.device)
 
 # Get embeddings
 with torch.no_grad():
 image_features = self.model.encode_image(image_tensor)
 text_features = self.model.encode_text(text_tokens)
 
 # Normalize features
 image_features /= image_features.norm(dim=-1, keepdim=True)
 text_features /= text_features.norm(dim=-1, keepdim=True)
 
 # Calculate cosine similarity
 similarity = (image_features @ text_features.T).item()
 
 # Scale to 0-1 range (CLIP gives -1 to 1)
 similarity_score = (similarity + 1) / 2
 
 # Determine match status
 if similarity_score >= 0.65:
 match_status = "High Alignment"
 description = "Caption accurately describes the image content"
 confidence = min(100, int(similarity_score * 100))
 elif similarity_score >= 0.45:
 match_status = "Medium Alignment"
 description = "Caption partially matches image content with some mismatch"
 confidence = min(100, int(similarity_score * 100))
 else:
 match_status = "Low Alignment"
 description = "Caption appears misaligned with image content"
 confidence = min(100, int((1 - similarity_score) * 100))
 
 logger.info(f"CLIP similarity calculated: {similarity_score:.3f}")
 
 return {
 "similarity_score": round(similarity_score, 3),
 "match_status": match_status,
 "confidence": confidence,
 "description": description,
 "raw_similarity": round(float(similarity), 3),
 }
 
 except Exception as e:
 logger.error(f"Error during similarity calculation: {str(e)}")
 return {
 "similarity_score": 0.5,
 "match_status": "Unknown",
 "confidence": 0,
 "description": f"Analysis failed: {str(e)}",
 "error": str(e),
 }
 
 def batch_analyze_captions(
 self,
 image_path: str,
 captions: list
 ) -> Dict[str, Any]:
 """
 Compare single image with multiple caption candidates.
 Useful for finding best matching caption or detecting duplicates.
 
 Args:
 image_path (str): Path to image file
 captions (list): List of caption strings to compare
 
 Returns:
 dict: Comparison results with rankings
 """
 
 try:
 # Load image once
 image_tensor = self._load_and_process_image(image_path)
 
 # Tokenize all captions
 captions_lower = [c.strip().lower() for c in captions]
 text_tokens = self.tokenizer(captions_lower).to(self.device)
 
 # Get embeddings
 with torch.no_grad():
 image_features = self.model.encode_image(image_tensor)
 text_features = self.model.encode_text(text_tokens)
 
 # Normalize
 image_features /= image_features.norm(dim=-1, keepdim=True)
 text_features /= text_features.norm(dim=-1, keepdim=True)
 
 # Calculate similarities
 similarities = (image_features @ text_features.T).squeeze()
 
 # Scale to 0-1
 similarities = (similarities + 1) / 2
 
 # Rank captions
 rankings = []
 for caption, score in zip(captions, similarities.tolist()):
 rankings.append({
 "caption": caption,
 "score": round(float(score), 3),
 })
 
 # Sort by score descending
 rankings.sort(key=lambda x: x["score"], reverse=True)
 
 return {
 "best_match": rankings[0] if rankings else None,
 "all_matches": rankings,
 "top_3": rankings[:3],
 }
 
 except Exception as e:
 logger.error(f"Error during batch caption analysis: {str(e)}")
 return {
 "error": str(e),
 "all_matches": [],
 }
 
 def analyze_caption_variations(
 self,
 image_path: str,
 original_caption: str
 ) -> Dict[str, Any]:
 """
 Analyze variations of a caption to test robustness of matching.
 
 Args:
 image_path (str): Path to image file
 original_caption (str): Original caption text
 
 Returns:
 dict: Analysis of caption robustness
 """
 
 # Generate variations
 variations = [
 original_caption,
 original_caption.upper(),
 original_caption.lower(),
 original_caption[:int(len(original_caption)*0.7)] + "...",
 f"Image shows: {original_caption}",
 f"This is {original_caption}",
 ]
 
 # Analyze
 analysis = self.batch_analyze_captions(image_path, variations)
 
 return {
 "original_caption": original_caption,
 "variation_analysis": analysis,
 "robustness_score": round(
 (max(s["score"] for s in analysis["all_matches"]) if analysis["all_matches"] else 0) * 100
 ),
 }


# Example usage
if __name__ == "__main__":
 # Setup logging
 logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
 )
 
 # Initialize matcher
 matcher = CLIPMatcher(device="cuda" if torch.cuda.is_available() else "cpu")
 
 # Example usage (uncomment with actual image and caption)
 # result = matcher.calculate_similarity(
 # "path/to/image.jpg",
 # "A cat sitting on a bench"
 # )
 # print(f"\nSimilarity Score: {result['similarity_score']}")
 # print(f"Match Status: {result['match_status']}")
 # print(f"Description: {result['description']}")
