# Scientific Assumptions & Architecture Decision Records (ADR)

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Last Updated**: 2026-11-01  

---

## ADR-001: Clinical Ground Truth Independence
- **Date**: 2026-11-01
- **Status**: **Approved**
- **Decision**: Primary diabetes classification ground-truth labels must originate strictly from independent biochemical laboratory reference standards (HbA1c, FPG, OGTT) or validated medical history records, never from Diabetic Retinopathy (DR) grading.
- **Alternatives Considered**: Using DR grade > 0 as a surrogate for diabetes.
- **Rationale for Rejection**: Diabetic eye disease is a downstream complication, not diabetes itself. Millions of diabetic individuals possess healthy-appearing retinas (DR = 0); conversely, retinal microaneurysms can rarely arise from severe hypertension or vein branch occlusion. Conflating the two invalidates the clinical hypothesis.
- **Scientific Impact**: Enables answering the core question: *Can AI detect systemic diabetes before clinical retinopathy appears?*

---

## ADR-002: Mandatory Patient-Level Grouped Splitting
- **Date**: 2026-11-01
- **Status**: **Approved**
- **Decision**: All images belonging to a single participant (left eye, right eye, and any repeat visits) must be grouped together into the same split partition.
- **Alternatives Considered**: Random stratified splitting at the individual image level.
- **Rationale for Rejection**: Bilateral eye correlation introduces severe data leakage, causing artificial model memorization of patient features rather than pathology.
- **Scientific Impact**: Ensures true out-of-sample patient generalization and eliminates optimism bias.

---

## ADR-003: Hierarchical Model Evaluation Strategy
- **Date**: 2026-11-01
- **Status**: **Approved**
- **Decision**: Establish a strict experimental progression:
  1. Standard Baseline: ResNet50 (pre-trained on ImageNet).
  2. Modern CNN: EfficientNetV2 and ConvNeXt.
  3. Retinal Foundation Model: RETFound (self-supervised on retinal fundus imagery).
- **Alternatives Considered**: Immediately training a foundation Vision Transformer without a baseline.
- **Rationale for Rejection**: Scientific integrity requires establishing an empirical lower bound with a standard baseline before justifying the complexity and compute overhead of advanced foundation models.

---

## ADR-004: Post-Hoc Probability Calibration as a Primary Requirement
- **Date**: 2026-11-01
- **Status**: **Approved**
- **Decision**: Neural network sigmoid outputs must not be presented directly as clinical probabilities. All scores must undergo validation-partition calibration (Platt scaling or isotonic regression) with Brier scores and calibration curves reported.
- **Alternatives Considered**: Raw softmax/sigmoid probabilities.
- **Rationale for Rejection**: Deep neural networks trained with cross-entropy loss are notorious for miscalibration (overconfidence), which is hazardous in healthcare triage.

