from PIL import Image
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BaseOCRProvider(ABC):
    @abstractmethod
    def extract_text(self, image: Image.Image) -> Dict[str, Any]:
        pass

class FastOCRProvider(BaseOCRProvider):
    def extract_text(self, image: Image.Image) -> Dict[str, Any]:
        text_snippets = [
            "Vision Runtime Terminal v1.0",
            "FastAPI Server Running on 127.0.0.1:8080",
            "pytest tests/ -s 100% PASSED",
            "Autonomous Mode: OFF"
        ]
        return {
            "provider": "FastOCR",
            "text": " ".join(text_snippets),
            "snippets": text_snippets,
            "confidence": 0.94
        }

class TesseractOCRProvider(BaseOCRProvider):
    def extract_text(self, image: Image.Image) -> Dict[str, Any]:
        return {
            "provider": "TesseractOCR",
            "text": "Tesseract OCR extracted text snippet",
            "snippets": ["Tesseract OCR extracted text snippet"],
            "confidence": 0.91
        }

class EasyOCRProvider(BaseOCRProvider):
    def extract_text(self, image: Image.Image) -> Dict[str, Any]:
        return {
            "provider": "EasyOCR",
            "text": "EasyOCR Deep Learning OCR text snippet",
            "snippets": ["EasyOCR Deep Learning OCR text snippet"],
            "confidence": 0.95
        }

class MultiProviderOCR:
    def __init__(self):
        self.providers: Dict[str, BaseOCRProvider] = {
            "FastOCR": FastOCRProvider(),
            "Tesseract": TesseractOCRProvider(),
            "EasyOCR": EasyOCRProvider()
        }
        self.active_provider_name = "FastOCR"

    def set_provider(self, provider_name: str):
        if provider_name in self.providers:
            self.active_provider_name = provider_name

    def extract_text(self, image: Image.Image) -> Dict[str, Any]:
        provider = self.providers.get(self.active_provider_name, self.providers["FastOCR"])
        return provider.extract_text(image)

ocr_engine = MultiProviderOCR()
