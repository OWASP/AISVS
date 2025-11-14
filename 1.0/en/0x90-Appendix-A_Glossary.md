# Appendix A: Glossary

> *This comprehensive glossary provides definitions of key AI, ML, and security terms used throughout the AISVS to ensure clarity and common understanding.*

* **Adversarial Example**: An input deliberately crafted to cause an AI model to make a mistake, often by adding subtle perturbations imperceptible to humans.

* **Adversarial Robustness** – Adversarial robustness in AI refers to a model's ability to maintain its performance and resist being fooled or manipulated by intentionally crafted, malicious inputs designed to cause errors.

* **Agent** – AI agents are software systems that use AI to pursue goals and complete tasks on behalf of users. They show reasoning, planning, and memory and have a level of autonomy to make decisions, learn, and adapt.

* **Agentic AI**: AI systems that can operate with some degree of autonomy to achieve goals, often making decisions and taking actions without direct human intervention.

* **Attribute-Based Access Control (ABAC)**: An access control paradigm where authorization decisions are based on attributes of the user, resource, action, and environment, evaluated at query time.

* **Backdoor Attack**: A type of data poisoning attack where the model is trained to respond in a specific way to certain triggers while behaving normally otherwise.

* **Bias**: Systematic errors in AI model outputs that can lead to unfair or discriminatory outcomes for certain groups or in specific contexts.

* **Bias Exploitation**: An attack technique that takes advantage of known biases in AI models to manipulate outputs or outcomes.

* **Cedar**: Amazon's policy language and engine for fine-grained permissions used in implementing ABAC for AI systems.

* **Chain of Thought**: A technique for improving reasoning in language models by generating intermediate reasoning steps before producing a final answer.

* **Circuit Breakers**: Mechanisms that automatically halt AI system operations when specific risk thresholds are exceeded.

* **Confidential Inference Service**: An inference service that runs AI models inside a trusted execution environment (TEE) or equivalent confidential computing mechanism, ensuring model weights and inference data remain encrypted, sealed, and protected from unauthorized access or tampering.

* **Confidential Workload**: An AI workload (e.g., training, inference, preprocessing) executed inside a trusted execution environment (TEE) with hardware-enforced isolation, memory encryption, and remote attestation to protect code, data, and models from host or co-tenant access.

* **Data Leakage**: Unintended exposure of sensitive information through AI model outputs or behavior.

* **Data Poisoning**: The deliberate corruption of training data to compromise model integrity, often to install backdoors or degrade performance.

* **Differential Privacy** – Differential privacy is a mathematically rigorous framework for releasing statistical information about datasets while protecting the privacy of individual data subjects. It enables a data holder to share aggregate patterns of the group while limiting information that is leaked about specific individuals.

* **Embeddings**: Dense vector representations of data (text, images, etc.) that capture semantic meaning in a high-dimensional space.

* **Explainability** – Explainability in AI is the ability of an AI system to provide human-understandable reasons for its decisions and predictions, offering insights into its internal workings.

* **Explainable AI (XAI)**: AI systems designed to provide human-understandable explanations for their decisions and behaviors through various techniques and frameworks.

* **Federated Learning**: A machine learning approach where models are trained across multiple decentralized devices holding local data samples, without exchanging the data itself.

* **Formulation**: The recipe or method used to produce an artifact or dataset, such as hyperparameters, training configuration, preprocessing steps, or build scripts.

* **Guardrails**: Constraints implemented to prevent AI systems from producing harmful, biased, or otherwise undesirable outputs.

* **Hallucination** – An AI hallucination refers to a phenomenon where an AI model generates incorrect or misleading information that is not based on its training data or factual reality.

* **Human-in-the-Loop (HITL)**: Systems designed to require human oversight, verification, or intervention at crucial decision points.

* **Infrastructure as Code (IaC)**: Managing and provisioning infrastructure through code instead of manual processes, enabling security scanning and consistent deployments.

* **Jailbreak**: Techniques used to circumvent safety guardrails in AI systems, particularly in large language models, to produce prohibited content.

* **Least Privilege**: The security principle of granting only the minimum necessary access rights for users and processes.

* **LIME (Local Interpretable Model-agnostic Explanations)**: A technique to explain the predictions of any machine learning classifier by approximating it locally with an interpretable model.

* **MCP (Model Context Protocol)**: A protocol that enables AI models and agents to access external tools, data sources, and resources by exchanging structured, typed requests and responses over a defined transport.

* **Membership Inference Attack**: An attack that aims to determine whether a specific data point was used to train a machine learning model.

* **MITRE ATLAS**: Adversarial Threat Landscape for Artificial-Intelligence Systems; a knowledge base of adversarial tactics and techniques against AI systems.

* **Model Card** – A model card is a document that provides standardized information about an AI model's performance, limitations, intended uses, and ethical considerations to promote transparency and responsible AI development.

* **Model Extraction**: An attack where an adversary repeatedly queries a target model to create a functionally similar copy without authorization.

* **Model Inversion**: An attack that attempts to reconstruct training data by analyzing model outputs.

* **Model Lifecycle Management** – AI Model Lifecycle Management is the process of overseeing all stages of an AI model's existence, including its design, development, deployment, monitoring, maintenance, and eventual retirement, to ensure it remains effective and aligned with objectives.

* **Model Poisoning**: Introducing vulnerabilities or backdoors directly into a model during the training process.

* **Model Stealing/Theft**: Extracting a copy or approximation of a proprietary model through repeated queries.

* **Multi-agent System**: A system composed of multiple interacting AI agents, each with potentially different capabilities and goals.

* **OPA (Open Policy Agent)**: An open-source policy engine that enables unified policy enforcement across the stack.

* **Privacy-Preserving Machine Learning (PPML)**: Techniques and methods to train and deploy ML models while protecting the privacy of the training data.

* **Prompt Injection**: An attack where malicious instructions are embedded in inputs to override a model's intended behavior.

* **RAG (Retrieval-Augmented Generation)**: A technique that enhances large language models by retrieving relevant information from external knowledge sources before generating a response.

* **Red-Teaming**: The practice of actively testing AI systems by simulating adversarial attacks to identify vulnerabilities.

* **SBOM (Software Bill of Materials)**: A formal record containing the details and supply chain relationships of various components used in building software or AI models.

* **SHAP (SHapley Additive exPlanations)**: A game theoretic approach to explain the output of any machine learning model by computing the contribution of each feature to the prediction.

* **Strong Authentication**: Authentication that resists credential theft and replay by requiring at least two factors (knowledge, possession, inherence) and phishing-resistant mechanisms such as FIDO2/WebAuthn, certificate-based service auth, or short-lived tokens.

* **Supply Chain Attack**: Compromising a system by targeting less-secure elements in its supply chain, such as third-party libraries, datasets, or pre-trained models.

* **Transfer Learning**: A technique where a model developed for one task is reused as the starting point for a model on a second task.

* **Vector Database**: A specialized database designed to store high-dimensional vectors (embeddings) and perform efficient similarity searches.

* **Vulnerability Scanning**: Automated tools that identify known security vulnerabilities in software components, including AI frameworks and dependencies.

* **Watermarking**: Techniques to embed imperceptible markers in AI-generated content to track its origin or detect AI generation.

* **Zero-Day Vulnerability**: A previously unknown vulnerability that attackers can exploit before developers create and deploy a patch.
