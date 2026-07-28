from typing import Dict, Any

class ConfidencePipeline:
    def calculate(self, capture_score: float, ocr_score: float, ui_score: float) -> Dict[str, Any]:
        """Calcula la matriz de confianza por etapas."""
        overall = round((capture_score * 0.4) + (ocr_score * 0.3) + (ui_score * 0.3), 2)
        allow_proposal = overall >= 0.70

        return {
            "capture_confidence": capture_score,
            "ocr_confidence": ocr_score,
            "ui_confidence": ui_score,
            "overall_confidence": overall,
            "proposal_allowed": allow_proposal
        }

confidence_pipeline = ConfidencePipeline()
