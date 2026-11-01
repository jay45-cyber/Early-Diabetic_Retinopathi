# Application & Inference Specification (Screening-Support Prototype)

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Component**: Streamlit Screening-Support Prototype (`app/streamlit_app.py`)  

---

## 1. Prototype Workflow & Safety Gateways

```
   [User Upload: JPEG/PNG Fundus Image]
                    |
   [Gateway 1: File Integrity & Dimension Check] ----(Invalid)----> [Reject: "Unsupported Image Format"]
                    |
   [Gateway 2: Automated Image Quality Screening] --(Ungradable)---> [Abstain: "Image Ungradable. Retake Photo."]
                    |
   [Gateway 3: Preprocessing & Standardization]
                    |
   [Gateway 4: Calibrated Model Inference]
                    |
   [Gateway 5: Grad-CAM++ Saliency Generation]
                    |
   [Output Dashboard Display]:
    - Calibrated Risk Score (%)
    - Confidence Category (Low / Moderate / High Risk)
    - Side-by-Side Saliency Overlay
    - Mandatory Clinical Screening Disclaimer
```

---

## 2. Abstention Mechanism for Low-Quality Images
A critical safety requirement in clinical AI is **abstention**. If an image is severely out of focus, underexposed, or contaminated with cataract clouding:
- The system **must not** generate a confident low-risk score (which might falsely reassure a diabetic patient).
- The system must explicitly output:
  > **STATUS: UNGRADABLE IMAGE**  
  > *The retinal fundus photograph does not meet diagnostic quality criteria (sharpness or illumination insufficient). Please recapture the image under appropriate pupillary dilation or adjust camera focus.*

---

## 3. Mandatory User-Facing Clinical Disclaimer
The application must prominently render the following regulatory and clinical safety notice:

> **RESEARCH SCREENING-SUPPORT PROTOTYPE ONLY**  
> *This artificial intelligence software is an academic research prototype designed to investigate early retinal screening markers. It is **not** an FDA/CDSCO-cleared medical diagnostic device. It does **not** diagnose diabetes mellitus and does not replace standardized venous blood testing (HbA1c or Fasting Plasma Glucose) or consultation with a qualified physician.*

