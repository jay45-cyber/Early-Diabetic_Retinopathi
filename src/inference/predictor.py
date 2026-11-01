"""End-to-end inference predictor with image validation and abstention."""
from typing import Dict, Any, Optional
from PIL import Image
import torch
import numpy as np
from src.inference.image_validation import validate_inference_input
from src.inference.risk_output import format_screening_output, CLINICAL_DISCLAIMER
from src.data.preprocessing import preprocess_fundus_image, normalize_to_tensor


class RetinaDiabetesPredictor:
    """Predictor handling end-to-end validation, preprocessing, model execution, and risk triage."""

    def __init__(
        self,
        model: torch.nn.Module,
        device: torch.device | None = None,
        calibrator: Optional[Any] = None
    ):
        self.device = device or torch.device("cpu")
        self.model = model.to(self.device)
        self.model.eval()
        self.calibrator = calibrator

    def predict(self, image_input: str | Image.Image) -> Dict[str, Any]:
        """Execute screening prediction on an input fundus photograph.
        
        Returns structured triage output or safe abstention if image is ungradable.
        """
        # Step 1: Input & Quality Validation Gateway
        val_res = validate_inference_input(image_input)
        if not val_res["valid"]:
            return {
                "status": "Abstained",
                "gradable": False,
                "reason": val_res["reason"],
                "disclaimer": CLINICAL_DISCLAIMER
            }

        # Step 2: Preprocessing
        clean_img = preprocess_fundus_image(val_res["image"], target_size=(384, 384))
        tensor_arr = normalize_to_tensor(clean_img)
        input_tensor = torch.from_numpy(tensor_arr).unsqueeze(0).to(self.device)

        # Step 3: Forward Pass
        with torch.no_grad():
            raw_logit = self.model(input_tensor).item()

        # Step 4: Probability Calibration
        if self.calibrator is not None:
            prob = float(self.calibrator.predict_proba(np.array([raw_logit]))[0])
        else:
            prob = float(torch.sigmoid(torch.tensor(raw_logit)).item())

        # Step 5: Clinical Triage Formatting
        output = format_screening_output(prob)
        output["status"] = "Success"
        output["gradable"] = True
        output["raw_logit"] = round(raw_logit, 4)
        output["preprocessed_image"] = clean_img

        return output

