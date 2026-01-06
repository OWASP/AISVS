# C7 Model Behavior, Output Control & Safety Assurance

## Control Objective

This control category ensures that model outputs are technically constrained, validated, and monitored so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems.

---

## C7.1 Output Format Enforcement

Ensure the model outputs data in a way that helps prevents injection.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.1.1** | **Verify that** the application validates all model outputs against a strict schema (like JSON Schema) and rejects any output that does not match. | 1 | D/V |
| **7.1.2** | **Verify that** the system uses "stop sequences" or token limits to strictly cut off generation before it can overflow buffers or executes unintended commands. | 1 | D/V |
| **7.1.3** | **Verify that** components processing model output treat it as untrusted input (e.g., using parameterized queries or safe de-serializers). | 2 | D/V |
| **7.1.4** | **Verify that** the system logs the specific error type when an output is rejected for bad formatting. | 3 | V |

---

## C7.2 Hallucination Detection & Mitigation

Detect when the model is unsure or lying, and stop that information from reaching the user.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.2.1** | **Verify that** the system calculates a numerical confidence score (e.g., using log-probabilities) for generated answers. | 1 | D/V |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 1 | D/V |
| **7.2.3** | **Verify that** hallucination events (low-confidence responses) are logged with input/output metadata for analysis. | 2 | D/V |

---

## C7.3 Output Safety & Privacy Filtering

Technical controls to detect and scrub bad content before it is shown to the user.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.3.1** | **Verify that** automated classifiers scan every response and block content that matches hate, harassment, or sexual violence categories. | 1 | D/V |
| **7.3.2** | **Verify that** the system scans every response for PII (like credit cards or emails) and automatically redacts it before display. | 1 | D/V |
| **7.3.3** | **Verify that** data labeled as "confidential" in the system remains blocked or redacted. | 2 | D |
| **7.3.4** | **Verify that** the system requires a human approval step or re-authentication if the model generates high-risk content. | 3 | D/V |
| **7.3.5** | **Verify that** safety filters can be configured differently based on the user's role or location (e.g., stricter filters for minors). | 3 | D/V |

---

## C7.4 Output & Action Limiting

Prevent the model from doing too much, too fast, or accessing things it should not.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.4.1** | **Verify that** the system enforces hard limits on requests and tokens per user to prevent cost spikes and denial of service. | 1 | D |
| **7.4.2** | **Verify that** the model cannot execute high-impact actions (like writing files, sending emails, or executing code) without explicit user confirmation. | 1 | D/V |
| **7.4.3** | **Verify that** the agent framework explicitly configures and enforces the maximum depth of recursive calls, delegation limits, and the list of allowed external tools. | 2 | D |

---

## C7.5 Explainability & Transparency

Ensure the user knows why a decision was made.

| # | Description | Level | Role |
| :-------: | ------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **7.5.1** | **Verify that** the UI displays a confidence score or "reasoning summary" to the user for critical decisions. | 2 | D/V |
| **7.5.2** | **Verify that** explanations provided to the user are sanitized to remove system prompts or backend data. | 2 | D/V |
| **7.5.3** | **Verify that** technical evidence of the model's decision (like attention maps or log-probs) are logged.| 3 | D |

---

## C7.6 Monitoring Integration

Ensure the application sends the right signals for security teams to watch.

| # | Description | Level | Role |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **7.6.1** | **Verify that** the system logs real-time metrics for safety violations (e.g., "Hallucination Detected", "PII Blocked").| 1 | D |
| **7.6.2** | **Verify that** the system triggers an alert if safety violation rates exceed a defined threshold within a specific time window. | 1 | V |
| **7.6.3** | **Verify that** logs include the specific model version and other details necessary to investigate potential abuse. | 2 | V |

---

## 7.7 Generative Media Safeguards

Prevent the creation of illegal or fake media.

| # | Description | Level | Role |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **7.7.1** | **Verify that** the system refuses to generate media (images/audio) that depicts real people without verified consent. | 1 | D/V |
| **7.7.2** | **Verify that** input filters block prompts requesting explicit or deepfake content before the model processes them. | 2 | D/V  |
| **7.7.3** | **Verify that** the system checks generated content for copyright violations before releasing it. | 2 | V |
| **7.7.4** | **Verify that** all generated media includes an invisible watermark or cryptographic signature to prove it was AI-generated. | 3 | D/V  |
| **7.7.5** | **Verify that** attempts to bypass filters are detected and logged as security events. | 3 | V |

## References

* [OWASP Top 10 for LLMs: LLM07: Insecure Output Handling](https://owasp.org/www-project-top-10-for-large-language-model-applications/#llm07-insecure-output-handling)
