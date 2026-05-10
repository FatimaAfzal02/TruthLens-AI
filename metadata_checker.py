"""
Module 3: Metadata Checker

Extracts and analyzes EXIF metadata from images to verify authenticity.
Checks for camera information, GPS data, timestamps, and software signatures.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

try:
 from PIL import Image
 from PIL.ExifTags import TAGS
except ImportError:
 raise ImportError("Pillow not found. Install with: pip install Pillow")

logger = logging.getLogger(__name__)


class MetadataChecker:
 """
 Analyzes EXIF and image metadata to assess image authenticity.
 """
 
 # EXIF tags to focus on
 IMPORTANT_TAGS = {
 271: "Manufacturer",
 272: "Camera Model",
 306: "DateTime",
 274: "Orientation",
 305: "Software",
 33432: "Copyright",
 34864: "Camera Serial Number",
 }
 
 # GPS-related EXIF tags
 GPS_TAGS = {
 0: "GPS Version",
 1: "GPS Latitude Ref",
 2: "GPS Latitude",
 3: "GPS Longitude Ref",
 4: "GPS Longitude",
 5: "GPS Altitude Ref",
 6: "GPS Altitude",
 }
 
 # Known AI image generation software signatures
 AI_SOFTWARE_SIGNATURES = [
 "stable diffusion",
 "midjourney",
 "dall-e",
 "diffusers",
 "comfyui",
 "automatic1111",
 "invokeai",
 "generative",
 "ai generated",
 ]
 
 def __init__(self):
 """Initialize Metadata Checker."""
 logger.info("MetadataChecker initialized")
 
 def extract_all_metadata(self, image_path: str) -> Dict[str, Any]:
 """
 Extract all available metadata from image.
 
 Args:
 image_path (str): Path to image file
 
 Returns:
 dict: Comprehensive metadata dictionary
 """
 
 if not Path(image_path).exists():
 raise FileNotFoundError(f"Image not found: {image_path}")
 
 try:
 image = Image.open(image_path)
 metadata = {
 "file_info": self._extract_file_info(image_path),
 "image_properties": self._extract_image_properties(image),
 "exif_data": self._extract_exif_data(image),
 "gps_data": self._extract_gps_data(image),
 }
 
 logger.info(f"Metadata extracted from: {image_path}")
 return metadata
 
 except Exception as e:
 logger.error(f"Error extracting metadata: {str(e)}")
 return {
 "error": str(e),
 "file_info": {},
 "image_properties": {},
 "exif_data": {},
 "gps_data": {},
 }
 
 def _extract_file_info(self, image_path: str) -> Dict[str, Any]:
 """Extract basic file information."""
 path = Path(image_path)
 
 return {
 "filename": path.name,
 "file_size": path.stat().st_size,
 "file_size_mb": round(path.stat().st_size / (1024*1024), 2),
 "file_format": path.suffix.upper(),
 "created_time": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
 "modified_time": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
 }
 
 def _extract_image_properties(self, image: Image.Image) -> Dict[str, Any]:
 """Extract image properties."""
 return {
 "width": image.width,
 "height": image.height,
 "format": image.format,
 "mode": image.mode,
 "is_animated": hasattr(image, 'is_animated') and image.is_animated,
 "dpi": image.info.get('dpi', None),
 }
 
 def _extract_exif_data(self, image: Image.Image) -> Dict[str, Any]:
 """Extract EXIF metadata."""
 exif_data = {}
 
 try:
 exif = image._getexif()
 
 if exif is None:
 return {"has_exif": False}
 
 exif_data["has_exif"] = True
 
 for tag_id, tag_name in TAGS.items():
 if tag_id in exif:
 value = exif[tag_id]
 
 # Format specific tags
 if tag_name == "DateTime":
 exif_data["timestamp"] = str(value)
 elif tag_name == "Make":
 exif_data["camera_manufacturer"] = str(value)
 elif tag_name == "Model":
 exif_data["camera_model"] = str(value)
 elif tag_name == "Software":
 exif_data["software"] = str(value)
 elif tag_name == "Orientation":
 exif_data["orientation"] = str(value)
 elif tag_name == "Copyright":
 exif_data["copyright"] = str(value)
 else:
 exif_data[tag_name] = str(value) if not isinstance(value, bytes) else value
 
 except AttributeError:
 exif_data["has_exif"] = False
 except Exception as e:
 logger.warning(f"Error extracting EXIF: {str(e)}")
 exif_data["extraction_error"] = str(e)
 
 return exif_data
 
 def _extract_gps_data(self, image: Image.Image) -> Dict[str, Any]:
 """Extract GPS information from EXIF."""
 gps_data = {"has_gps": False}
 
 try:
 exif = image._getexif()
 
 if exif is None:
 return gps_data
 
 # IFD 34853 contains GPS data
 if 34853 in exif:
 gps_ifd = exif[34853]
 gps_data["has_gps"] = True
 
 for tag_id, tag_name in self.GPS_TAGS.items():
 if tag_id in gps_ifd:
 gps_data[tag_name] = str(gps_ifd[tag_id])
 
 # Parse latitude and longitude if available
 if 2 in gps_ifd and 4 in gps_ifd:
 lat = self._convert_to_degrees(gps_ifd[2])
 lon = self._convert_to_degrees(gps_ifd[4])
 
 if gps_ifd.get(1) == 'S':
 lat = -lat
 if gps_ifd.get(3) == 'W':
 lon = -lon
 
 gps_data["latitude"] = round(lat, 6)
 gps_data["longitude"] = round(lon, 6)
 gps_data["coordinates"] = f"{lat:.6f}, {lon:.6f}"
 
 except Exception as e:
 logger.warning(f"Error extracting GPS: {str(e)}")
 
 return gps_data
 
 @staticmethod
 def _convert_to_degrees(value) -> float:
 """Convert GPS coordinates to decimal degrees."""
 try:
 d, m, s = value
 return float(d) + float(m)/60 + float(s)/3600
 except:
 return 0.0
 
 def analyze_authenticity(self, image_path: str) -> Dict[str, Any]:
 """
 Analyze metadata to assess image authenticity.
 
 Args:
 image_path (str): Path to image file
 
 Returns:
 dict: Authenticity assessment with signals and evidence
 """
 
 metadata = self.extract_all_metadata(image_path)
 
 if "error" in metadata:
 return {
 "authenticity_score": 0.5,
 "verdict": "UNKNOWN",
 "evidence": ["Could not extract metadata"],
 "red_flags": ["Metadata extraction failed"],
 }
 
 evidence = []
 red_flags = []
 authenticity_signals = 0
 
 # Check EXIF presence
 exif_data = metadata["exif_data"]
 if exif_data.get("has_exif"):
 evidence.append("EXIF metadata present")
 authenticity_signals += 2
 else:
 red_flags.append("No EXIF metadata found")
 
 # Check camera information
 if exif_data.get("camera_model"):
 evidence.append(f"Camera: {exif_data['camera_model']}")
 authenticity_signals += 2
 elif exif_data.get("has_exif"):
 red_flags.append("EXIF present but no camera model")
 
 # Check for AI software signatures
 software = exif_data.get("software", "").lower()
 if software:
 for sig in self.AI_SOFTWARE_SIGNATURES:
 if sig in software:
 red_flags.append(f"AI software detected: {software}")
 break
 else:
 evidence.append(f"Software: {exif_data['software']}")
 authenticity_signals += 1
 
 # Check timestamp
 if exif_data.get("timestamp"):
 evidence.append(f"Timestamp: {exif_data['timestamp']}")
 authenticity_signals += 1
 else:
 red_flags.append("No timestamp found")
 
 # Check GPS data
 gps_data = metadata["gps_data"]
 if gps_data.get("has_gps"):
 coords = gps_data.get("coordinates", "Unknown")
 evidence.append(f"GPS: {coords}")
 authenticity_signals += 2
 else:
 red_flags.append("No GPS data (common for edited/digital images)")
 
 # Check file info
 file_info = metadata["file_info"]
 if file_info.get("file_size_mb") < 0.01:
 red_flags.append("Suspiciously small file size")
 elif file_info.get("file_size_mb") > 50:
 red_flags.append("Unusually large file size")
 
 # Calculate authenticity score
 max_signals = 10
 authenticity_score = min(1.0, authenticity_signals / max_signals)
 
 return {
 "authenticity_score": round(authenticity_score, 2),
 "authenticity_signals": authenticity_signals,
 "verdict": "LIKELY AUTHENTIC" if authenticity_score > 0.6 else "QUESTIONABLE",
 "evidence": evidence,
 "red_flags": red_flags,
 "metadata_summary": {
 "has_exif": exif_data.get("has_exif", False),
 "camera_model": exif_data.get("camera_model"),
 "has_gps": gps_data.get("has_gps", False),
 "timestamp": exif_data.get("timestamp"),
 },
 }


# Example usage
if __name__ == "__main__":
 # Setup logging
 logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
 )
 
 # Initialize checker
 checker = MetadataChecker()
 
 # Example analysis (uncomment with actual image)
 # result = checker.analyze_authenticity("path/to/image.jpg")
 # print("\nAuthenticity Analysis:")
 # print(f" Score: {result['authenticity_score']}")
 # print(f" Verdict: {result['verdict']}")
 # print(f" Evidence: {result['evidence']}")
 # print(f" Red Flags: {result['red_flags']}")
