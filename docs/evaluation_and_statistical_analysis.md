# Evaluation Metrics & Statistical Analysis Protocol

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Senior Biostatistician & AI Evaluation Lead  

---

## 1. Core Evaluation Principles
1. **Accuracy is Insufficient**: In clinical screening populations where disease prevalence is typically $10\% - 20\%$, a naive model predicting all patients as negative achieves $80\% - 90\%$ accuracy while missing every single sick individual.
2. **Patient-Level Bootstrap Confidence Intervals**: Confidence intervals (95% CI) must be computed by resampling patients (not individual images) with replacement (1,000 bootstrap iterations).
3. **Partition Separation**: Performance is independently computed and reported across three partitions:
   - Development Cross-Validation
   - Locked Internal Test Set
   - Independent External Cohort (when available)

---

## 2. Quantitative Metric Suite

| Metric Name | Mathematical Definition | Clinical Significance in Screening |
| :--- | :--- | :--- |
| **AUROC** | Area Under Receiver Operating Characteristic Curve | Discrimination capacity across all potential classification thresholds. |
| **AUPRC** | Area Under Precision-Recall Curve | Essential metric under class imbalance; reflects positive class precision across recall tiers. |
| **Sensitivity (Recall)** | $\text{TP} / (\text{TP} + \text{FN})$ | **Primary clinical priority**: Percentage of true diabetic patients correctly identified for follow-up. |
| **Specificity** | $\text{TN} / (\text{TN} + \text{FP})$ | Percentage of non-diabetic controls spared unnecessary lab referral costs. |
| **Negative Predictive Value (NPV)** | $\text{TN} / (\text{TN} + \text{FN})$ | Confidence that a screen-negative individual is genuinely disease-free. |
| **Positive Predictive Value (Precision)** | $\text{TP} / (\text{TP} + \text{FP})$ | Likelihood that a screen-positive individual has true diabetes upon lab follow-up. |
| **F1-Score** | $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ | Harmonic mean balancing recall and precision. |
| **Brier Score** | $\frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$ | Overall measure of probability calibration and accuracy (lower is superior). |

---

## 3. Probability Calibration & Reliability Curves
Modern neural networks often output overconfident predicted probabilities ($p_i$). To provide trustworthy risk estimates:
- **Platt Scaling (Logistic Calibration)**: Fits a scalar logistic model on validation logits:
  $$P(Y=1 \mid z) = \frac{1}{1 + \exp(A \cdot z + B)}$$
- **Calibration Slope & Intercept**: Perfect calibration yields $\text{slope} = 1.0$ and $\text{intercept} = 0.0$.
- **Expected Calibration Error (ECE)**: Weighted average difference between predicted confidence and observed empirical accuracy across 10 probability bins.

---

## 4. Subgroup Analysis Protocol

A model may perform well on aggregate metrics while completely failing within specific vulnerability strata. Stratified evaluation will be conducted for:
1. **No Visible Retinopathy (DR = 0)**: The core research question.
2. **Sex Strata**: Female vs. Male participants.
3. **Age Brackets**: $< 45$, $45 - 60$, and $> 60$ years.
4. **Fundus Camera Model**: Evaluating domain stability across camera optics.

