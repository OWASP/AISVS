# C2.2: Content & Policy Screening

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation.md)

## Purpose

Even syntactically valid and well-formed prompts may request disallowed content — violence, self-harm instructions, hate speech, sexual content, illegal activities, or content that violates organizational policies. Content screening classifiers analyze the semantic intent of inputs and outputs to detect policy violations before they propagate through the system. This section requires both automated classification and policy-based gating, with configurable thresholds to balance safety with usability across different deployment contexts. Because modern assistants also accept images, audio, and video, screening has to extend beyond text — hidden instructions in downscaled images, near-ultrasonic audio commands, and payloads split across modalities are all demonstrated attack paths as of 2025–2026.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **2.3.1** | **Verify that** every prompt is scored by a content classifier for violence, self-harm, hate, and sexual content against configurable thresholds. Prompts that exceed those thresholds are rejected or sanitized before reaching model context. | 1 | Direct harmful-content requests reaching model context (MITRE ATLAS AML.T0054 LLM Jailbreak); classifier evasion via adversarial paraphrasing (87.88% TPR reduction across detector types), EchoGram token flips, and IntentPrompt narrative reframing; advisory-only screening, where a flagging-but-not-blocking classifier lets violating content flow into agent chains, tool calls, and MCP servers (AML.T0051), up to remote code execution in agent frameworks (Microsoft "prompts become shells", May 2026) | Confirm every inference path passes through a classifier (OpenAI omni-moderation, Azure AI Content Safety, Bedrock Guardrails, Google Model Armor, Llama Guard 3, LLM Guard) in-line at a gateway (LiteLLM or Bifrost guardrail hooks, TrueFoundry MCP pre-tool hooks, Cloudflare Firewall for AI) before model invocation — not as an async observer; submit known-violating payloads and grep downstream model, tool, and MCP logs to confirm they never arrive; kill or throttle the classifier and verify the gateway fails closed; review per-category threshold configuration against documented deployment context; replay MLCommons AILuminate public practice prompts (12,000 per language across 12 hazard categories) plus XSTest and OR-Bench-Hard over-refusal sets to measure under-blocking and over-blocking together; run Promptfoo, garak, or DeepTeam scans in CI to catch threshold regressions | Classifier tooling is mature, but thresholds are typically set once at deployment and never recalibrated; over-refusal is rarely measured even though OR-Bench shows state-of-the-art models still refuse benign prompts; many deployments still call moderation asynchronously, making rejection advisory, and fail-open on classifier timeout is a common default that few teams chaos-test; multi-turn escalation (Crescendo, SEMA) passes per-message screening, so conversation-level state is needed; "sanitize" paths are rarely implemented — most production gateways only reject, and partial sanitization risks leaving adversarial residue in context |
| **2.3.2** | **Verify that** prompt content classification is evaluated for languages that are not supported. | 1 | Low-resource-language jailbreaks: multi-turn attacks in Afrikaans, Kiswahili, isiXhosa, and isiZulu achieved 41.8–83.6% harmful-response rates across ChatGPT, Claude, DeepSeek, Gemini, and Grok (arXiv 2605.18239, May 2026); code-switching red-teaming yields 46.7% more successful attacks than English-only (ACL 2025); classifier support matrices are English-biased, so unsupported locales silently pass | Diff the provider's documented language-support matrix (Azure: 8 specially trained languages; Bedrock: Classic vs Standard tiers; Lakera: English-only moderation) against actual user-locale telemetry to find uncovered traffic; test with PolyGuardPrompts (29K samples, 17 languages) and code-switching corpora; confirm a language-detection gate (fastText, Azure AI Language Detection) rejects or routes unknown and low-confidence locales, and that the routing decision (reject / conservative threshold / human review) is recorded in screening logs | Language detection itself fails on short messages, mixed scripts, and transliteration; multi-turn translation attacks defeat per-message classification even when single-turn translation fails; AILuminate currently covers only English and French (Chinese and Hindi in development), so no standard benchmark exists for most locales; blanket rejection of unsupported languages penalizes legitimate non-English users — an unresolved fairness trade-off |
| **2.3.3** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage and trace metadata. | 2 | Undetected coordinated probing: boundary-search attacks (Boundary Point Jailbreaking) need only binary allow/reject feedback, and without session-correlated logs the probing pattern is invisible to the SOC; silent classifier regression after model or threshold updates; inability to reconstruct incidents for regulators (EU AI Act logging duties) | Inspect the log schema for confidence scores, category tags, applied stage (pre-model, post-model, pre-tool), and source/tool/MCP/agent/session fields; check trace correlation against OpenTelemetry GenAI semantic conventions for spans and events; confirm SIEM ingestion with correlation rules (Datadog LLM Observability, Splunk MITRE ATLAS AI Threat Detection app); replay archived screening decisions against updated classifier versions in shadow mode (Promptfoo adaptive guardrails, Bedrock guardrail trace analysis) and diff verdicts before promoting changes | No standardized screening-log schema exists — OpenTelemetry GenAI semantic conventions remain in Development status with no stabilization timeline; retaining harmful input text for replay creates privacy and legal tension (CSAM cannot lawfully be retained, so hash-and-metadata replay schemes are needed); default provider settings often discard confidence scores, keeping only the binary verdict; few organizations operationalize shadow-mode replay before classifier updates |
| **2.3.4** | **Verify that** non-text inputs (image/video/audio) are checked for adversarial perturbations, steganographic payloads, hidden or embedded content, or known attack patterns. | 2 | Image-borne hidden instructions that text-only classifiers never see: Trail of Bits' image-scaling attack (Anamorpher, August 2025) hid prompts that emerged only after downscaling and exfiltrated Google Calendar data through Gemini CLI; Brave's "unseeable" screenshot injections (October 2025) drove Perplexity Comet's OCR path with faint low-contrast text against authenticated banking sessions; steganographic and metadata payloads (EXIF/XMP/ICC-profile smuggling); adversarial perturbations on vision-language models with transfer attack success up to 45% on GPT-4V and 86% on ERNIE Bot (March 2026 survey, arXiv 2603.27918); audio attacks — AudioJailbreak's over-the-air adversarial suffixes (87–88% success through speakers across rooms, May 2025) and Sirens' Whisper near-ultrasonic inaudible injection (0.94 non-refusal rate, March 2026); video-driven prompting that repeats a harmful image across frames to slip past detectors (CVPR 2026); MITRE ATLAS AML.T0051.001 (indirect prompt injection), AML.T0043 (craft adversarial data), AML.T0015 (evade ML model) | Confirm every non-text input passes a multimodal classifier inline (Llama Guard 4 for interleaved text+multi-image, ShieldGemma 2 for images, OpenAI omni-moderation image support, Azure AI Content Safety Image Analyze, Bedrock Guardrails multimodal toxicity — GA since March 2025); verify an OCR-then-classify path feeds image-extracted text through the same text classifiers used for typed input (the pattern Microsoft documents for Azure and M365 defenses); check that inbound images are re-encoded, resized, and metadata-stripped (ExifTool `-all=`, libvips/ImageMagick `-strip`) or routed through content disarm and reconstruction (OPSWAT Deep CDR documents explicit anti-steganography pixel-noise injection; Glasswall, Votiro) before model ingestion; confirm audio is transcribed then classified, and test the transcription path with adversarial and ultrasonic samples; red-team with garak `visual_jailbreak` (FigStep probes), Promptfoo image/audio/video strategies, PyRIT multimodal converters (AddTextImageConverter), or Mindgard multimodal scans, and replay Anamorpher-crafted scaling attacks against the production image-preprocessing path | No cloud vendor ships production-grade real-time steganalysis — open tools (StegExpose, zsteg, Aletheia) are research-grade with high false negatives against modern embedding schemes, so destruction-by-transformation (re-encode, resize, strip) is the practical control; adversarial-perturbation defenses in ART (JPEG compression, feature squeezing) are cheap but defeatable by adaptive attackers, and dedicated detectors remain research-grade; Google Model Armor is still text-only and explicitly does not screen images embedded in documents; omni-moderation classifies only a subset of categories on images and no audio at all; transcribe-then-classify discards the acoustic channel where adversarial payloads live; no off-the-shelf audio prompt-injection detector exists (deepfake detectors like Pindrop Pulse check speaker authenticity, not hidden instructions); video screening is nascent — no public video-injection CVE as of early 2026, but CVPR 2026 work shows unsafe videos embed closer to safe ones than single harmful images |
| **2.3.5** | **Verify that** coordinated attacks spanning multiple input types (e.g., steganographic payloads in images combined with prompt injection in text) are detected and blocked. | 3 | Split-payload attacks where each modality is benign in isolation: FigStep and FigStep-Pro (AAAI 2025 Oral) render prohibited instructions as typographic images — Pro fragments the harmful text across multiple sub-images — while the accompanying text prompt stays innocuous; Visual-RolePlay pairs LLM-generated high-risk character images with benign role-play text; JPRO automates image+text jailbreak generation via multi-agent collaboration (November 2025); EchoLeak (CVE-2025-32711, disclosed June 2025) chained a crafted email past Microsoft's XPIA prompt-injection classifier and used auto-fetched images as the zero-click exfiltration channel in M365 Copilot — the canonical text-plus-image coordination incident; multimodal-reasoning jailbreaks exploit the model's own cross-modal reasoning to assemble harmful intent from benign parts (January 2026); MITRE ATLAS AML.T0051.001 | Verify the full multimodal context is scored jointly in one call, not per-modality in isolation: OpenAI omni-moderation scores images "in isolation or in conjunction with text"; Azure AI Content Safety's `imageWithText` multimodal API (preview) analyzes the image, its OCR-extracted text, and accompanying text together; Bedrock Guardrails evaluates text and images in the same Converse/ApplyGuardrail call; Llama Guard 4 classifies interleaved multi-image prompts; confirm a normalize-to-text pipeline (OCR every image, transcribe every audio clip) feeds the combined context through screening with per-modality and joint verdicts logged under one trace ID; replay FigStep via garak `visual_jailbreak` and PyRIT AddTextImageConverter, run Promptfoo image/audio/video strategies against the assembled pipeline, and test that fragments split across conversation turns trigger session-level review rather than relying on per-request scoring alone | No mature off-the-shelf cross-modal correlation engine exists as of mid-2026 — CrossGuard (targets joint-modal implicit malicious attacks where neither modality alone is harmful, arXiv 2510.17687) and GuardReasoner-Omni (text/image/video reasoning guardrail, arXiv 2602.03328) are research code, not products; production joint scorers are per-request classifiers that miss payloads split across turns, sessions, or agent hops; Azure's multimodal API has sat in preview since September 2024; OWASP LLM01:2025 concedes that "robust multimodal-specific defenses are an important area for further research" — this Level 3 control must today be assembled from OCR, transcription, joint classification, and session analytics rather than bought as a product |

---

## Tool & Framework Landscape

### Commercial Content Safety APIs

| Tool | Vendor | Categories | Multilingual | Key Differentiator | Pricing |
|------|--------|------------|:------------:|-------------------|---------|
| **Moderation API** (`omni-moderation-latest`) | OpenAI | 11 subcategories (harassment, hate, self-harm, sexual, violence, illicit) | 40+ languages (42% multilingual improvement) | Free, multimodal (text + image), category scores plus applied input type metadata; model snapshots support repeatable calibration | Free |
| **Azure AI Content Safety** | Microsoft | Hate, violence, sexual, self-harm (4 severity levels each) | 8 specially trained languages + broad supported list; protected material, groundedness detection, and custom categories (standard) are English-only | Prompt Shields, auto language detection, Protected Material Detection, Custom Categories, Content Safety Studio monitoring dashboard | Free tier (5 RPS) + pay-per-call |
| **Bedrock Guardrails** | AWS | 6 categories including prompt attack; multimodal toxicity detection (GA March 2025 in us-east-1, us-west-2, eu-central-1, ap-northeast-1; preview elsewhere with reduced categories) extends hate, insults, sexual, violence, misconduct, and prompt-attack policies to images, AI-generated images, memes, charts, and mixed text+image content (JPEG/PNG up to 8000x8000) | Standard tier covers many languages; Classic tier optimized for English/French/Spanish; unsupported languages are explicitly ineffective | PII detection/masking, contextual grounding checks, code-element filtering, prompt-attack detection on images as well as text, configurable category strengths, ~88% block rate on harmful multimodal content, cross-account safeguards GA (April 2026) for centralized enforcement, and a standalone ApplyGuardrail API usable with self-hosted models; reasoning content is excluded from filtering | Pay-per-evaluation |
| **Vertex AI Safety** | Google | Hate, harassment, sexually explicit, dangerous | Gemini language support | Non-configurable auto-block for CSAM/PII, configurable content filters, Gemini-as-classifier | Included with API usage |
| **Google Cloud Model Armor** | Google | Hate, harassment, sexually explicit, dangerous, CSAM, prompt injection/jailbreak (now up to 10,000 tokens, with improved high-confidence detection), sensitive data, malicious URLs | Tested for responsible-safety and prompt-injection filters in Chinese, English, French, German, Italian, Japanese, Korean, Portuguese, and Spanish; quality may vary elsewhere | Screens prompts, responses, and documents; supports separate input/output templates, inspect-only vs inspect-and-block enforcement, Cloud Logging, Terraform-managed floor settings via Security Command Center, additional regions including `asia-southeast1`, and regional data residency | Standalone / Security Command Center |
| **Anthropic Filtering** | Anthropic | Aligned to Usage Policy; Constitutional Classifiers++ adds full-exchange policy evaluation | Claude language support | Constitutional Classifiers++ (January 2026) two-stage probe-plus-exchange-classifier cascade with ~40x cost reduction vs. first-generation system and 0.05% production refusal rate, validated by 1,700+ hours of red-teaming; representation-reuse "cheap monitors" cut probe cost to ~4% of policy-model cost; free moderation tooling, asynchronous monitoring | Included with API usage |
| **Galileo Protect** | Galileo | Configurable multi-category classification | Multilingual | Luna-2 SLMs with 0.95 F1 at 98% cost reduction vs GPT-4o; Agent Control open-source control plane (Apache 2.0); SOC 2 + ISO 27001 | SaaS / VPC / On-prem |
| **Lakera Guard** | Lakera | Prompt injection, jailbreak, content moderation, PII, data leakage, malicious links | Content moderation currently documented as English-only | Real-time API firewall for user and referenced content plus outputs; L1-L4 detector thresholds, daily detector updates, custom natural-language or regex guardrails, and batch document screening | Pay-per-call |
| **TrueFoundry Content Moderation Guardrail** | TrueFoundry | Hate, self-harm, sexual, violence | Azure-backed multilingual coverage | Managed Azure Content Safety guardrail with severity thresholds, enforce/audit modes, and hooks for LLM input, LLM output, MCP pre-tool, and MCP post-tool checks | Platform feature |
| **AI Guardrails by Zapier** | Zapier | PII (30+ types), prompt injection, jailbreak, toxicity | Inherits underlying detector coverage | Inline workflow guardrail step usable from Zaps, Agents, and MCP-connected clients (e.g., Cursor, Claude); structured results support code-free routing, redaction, blocking, and escalation before downstream CRM, database, or messaging actions | Platform feature |

### Open-Source Tools

| Tool | License | Focus | Maturity |
|------|---------|-------|----------|
| **LLM Guard** (Protect AI) | MIT | 15 input + 20 output scanners; model-agnostic | Production (2.5M+ downloads) |
| **NeMo Guardrails** (NVIDIA) | Apache 2.0 | Multi-turn dialog flow control via Colang DSL; unique conversation-level policy enforcement | Production |
| **Guardrails AI** | Apache 2.0 | Composable validator chains; Guardrails Hub with pre-built validators; Guardrails Index benchmark (Feb 2025) | Production |
| **WhyLabs LangKit** | Apache 2.0 | LLM observability; statistical anomaly detection; alerts aligned to MITRE ATLAS and OWASP LLM Top 10 | Production |
| **IBM Granite Guardian** | Apache 2.0 | Content moderation model for LLM output safety | Production |
| **Llama Guard 3 Vision** (Meta) | Llama License | First multimodal safety classifier (11B); 13 MLCommons hazard categories for text+image inputs; also available as 1B text-only for on-device | Production |
| **Llama Guard 4** (Meta) | Llama 4 Community License | Dense 12B classifier pruned from Llama 4 Scout (April 2025); handles interleaved text plus multiple images per prompt (trained on 2–5 images/sample); 14 MLCommons hazard categories plus code-interpreter abuse; works as input and output filter; runs on one 24 GB GPU; backs Meta's Llama Moderations API | Production |
| **Llama Prompt Guard 2** (Meta) | Llama License | BERT-style classifier for prompt-injection and jailbreak detection; 86M multilingual (English plus French, German, Hindi, Italian, Portuguese, Spanish, Thai) and 22M English-only (~75% lower latency); binary benign/malicious output, 512-token context, segment-and-scan for longer prompts | Production |
| **ShieldGemma 2** (Google) | Gemma License | Image content classification (sexually explicit, harmful, violent, gore); builds on ShieldGemma 1 text classification (2B/9B/27B) | Production |
| **PolyGuard** | Open Source (CC BY 4.0) | Multilingual moderation classifier and benchmark covering 17 languages; PolyGuardMix training corpus (1.91M samples) and PolyGuardPrompts benchmark (29K samples); reports ~5.5% improvement over prior state-of-the-art open and commercial classifiers | Production / COLM 2025 |
| **LEG** | Research release planned | Lightweight explainable prompt-safety classifier that labels unsafe prompts and token-level explanation spans | Research |
| **ExpGuard** | Open Source | Domain-specific guardrail for financial, medical, legal content; outperforms WildGuard by up to 15.3%; ICLR 2026 | Research / Early Production |
| **any-guardrail** (Mozilla.ai) | Apache 2.0 | Common interface to swap encoder-based and decoder-based guardrail models (Llama Guard, ShieldGemma, others) for A/B testing and reproducible evaluation; companion to `any-agent` | Production / Early |

### Language Detection & Unsupported-Language Controls

| Tool / Pattern | Coverage | Use in C2.3.2 Verification |
|----------------|----------|-----------------------------|
| **fastText language ID** | 176 languages | Lightweight pre-moderation language detection; useful for blocking or escalating unsupported, unknown, or low-confidence locales before model invocation. |
| **Azure AI Language Detection** | Wide language, dialect, and regional coverage with confidence scores | Captures language code plus confidence for routing decisions and audit logs; pair with moderation results to detect language-specific false negatives. |
| **CLD3** | BCP-47 style language codes; compact neural detector | Useful as a secondary detector for mixed-script or short-message disagreement checks, but the upstream Google repository is archived and should not be the only control. |
| **MrGuard** | Multilingual prompt classification research | Early guardrail option for multilingual jailbreak detection; useful for benchmarking out-of-domain and lower-resource language coverage. |
| **English-as-defense-proxy routing** | Translate or elicit English safety reasoning before final policy decision | Compensating pattern for languages where English safety alignment is stronger, but translation logs must preserve the original request and avoid forwarding unsafe translated content downstream. |

### Multimodal & Hidden-Content Screening (2.3.4 / 2.3.5)

| Tool / Pattern | Type | Use in Verification |
|----------------|------|---------------------|
| **OCR-then-classify** | Architectural pattern | Run OCR on every inbound image and route extracted text through the same injection/content classifiers as typed input, wrapped in delimiters and marked untrusted. Microsoft documents this for Azure AI Content Safety (the multimodal API does it natively) and M365 defenses; it is the corresponding defense to Promptfoo's image red-team strategy, which exists precisely because text-in-image bypasses text-only filters. |
| **Azure `imageWithText` multimodal API** | Commercial (preview) | Analyzes the image, OCR-extracted in-image text, and accompanying user text together in one call — the closest a hyperscaler ships to joint cross-modal scoring; in preview since September 2024. |
| **Image re-encode / resize / strip** | Pattern (ExifTool `-all=`, libvips/ImageMagick `-strip`, Pillow re-save) | Decode and re-encode every inbound image: destroys most pixel-domain steganographic payloads and removes EXIF/XMP/ICC metadata channels cheaply and deterministically. Re-running the production downscaler on a separate path also defuses image-scaling attacks like Anamorpher. |
| **CDR products** (OPSWAT MetaDefender Deep CDR, Glasswall, Votiro) | Commercial | File rebuild to known-good spec; OPSWAT explicitly documents anti-steganography via stripping unused data and injecting pixel-level noise; mature for file-borne hidden content, recursive over embedded objects. |
| **Steganalysis tools** (Aletheia, StegExpose, zsteg) | Open source, research-grade | Aletheia (MIT, actively developed) combines statistical and deep-learning steganalysis; StegExpose and zsteg are largely unmaintained with ~50% accuracy against modern embeddings in 2024 forensic testing. Useful as cheap pipeline checks, not as the control. |
| **Adversarial Robustness Toolbox (ART)** | Open source (MIT, IBM/Trusted-AI) | Preprocessor defenses (JpegCompression, FeatureSqueezing, SpatialSmoothing) and inference-time detectors for adversarial perturbations; transformations are deployable today but defeatable by adaptive attacks. |
| **Transcribe-then-classify** | Architectural pattern | STT (Whisper, Azure Speech, Amazon Transcribe) feeding text guardrails — the de facto audio screening pattern since no mainstream moderation API classifies raw audio; blind to acoustic-channel payloads, so pair with adversarial-audio testing. |
| **Audio deepfake detection** (Pindrop Pulse, Resemble Detect) | Commercial | Real-time synthetic-voice and liveness detection (~93–94% on unseen deepfakes in vendor/third-party tests, degrading on phone-quality audio); addresses speaker authenticity, not hidden-instruction payloads. |

### Red-Teaming & Replay Tools

| Tool | License | Focus | Key Feature |
|------|---------|-------|-------------|
| **Promptfoo** (OpenAI announced acquisition March 2026) | MIT / Enterprise | 50+ vulnerability types; prompt injection, jailbreak, PII leak, toxic content scanning; `image`, `audio`, and `video` strategies render test prompts as text-on-PNG, TTS speech, or video to test whether encoded text bypasses text-only filters | CI/CD integration via YAML configs and GitHub Actions; guardrails assertions for AWS Bedrock and Azure OpenAI; unsupported providers currently score 0 unless mapped explicitly; adaptive guardrails can turn red-team failures into production blocking policies |
| **DeepTeam** (Confident AI) | MIT | 80+ vulnerability types; 7 production guardrails; OWASP Top 10, MITRE ATLAS, NIST AI RMF alignment | Programmatic and CLI-based red teaming; risk assessment tracking across iterations; custom vulnerability type registration |
| **Mindgard** | Commercial | Adversarial ML evasion testing for guardrails; character injection and AML attack simulation | Tested against Azure Prompt Shield, Meta Prompt Guard, NeMo Guard, ProtectAI models; quantifies evasion rates per technique |
| **garak** (NVIDIA-backed) | Apache 2.0 | LLM vulnerability scanning for prompt injection, jailbreaks, toxicity, encoding bypass, data leakage, and related failure modes; `visual_jailbreak` module implements FigStep typographic image probes with matching detectors | Probe/detector model with JSONL reports and hit logs; useful for repeatable regression scans and comparing guardrail changes across releases; basis of NVIDIA NeMo Auditor |
| **PyRIT** (Microsoft) | MIT | Natively multimodal red-teaming — request/response model carries text, image, and audio pieces | 70+ stackable converters including AddTextImageConverter/AddImageTextConverter (overlay attack text onto images) and audio converters; supports multi-turn attacks (Crescendo, TAP) against assembled pipelines |
| **Giskard Hub scans** | Commercial / Open Source ecosystem | Agent vulnerability scanning mapped to OWASP LLM Top 10 plus harmful content, legal/financial risk, and unauthorized advice | Can scope scans by threat tag, inspect individual probe attempts, and promote successful attacks directly into durable regression test cases |

### Safety Benchmarks for Threshold Calibration

Threshold tuning (2.3.1) needs paired measurement of under-blocking and over-blocking; these public benchmarks make that measurable rather than vibes-based.

| Benchmark | Scope | Use in Verification |
|-----------|-------|---------------------|
| **MLCommons AILuminate** (Safety v1.0; Jailbreak v0.5 draft) | 12 hazard categories; 24,000+ prompts per language (12,000 public practice); English and French today, Chinese and Hindi in development; graded Poor–Excellent against a reference system | Replay the public practice set through the full screening pipeline (not the bare model) to measure block rates per hazard category at current thresholds |
| **OR-Bench** (ICML 2025) | 80,000 seemingly toxic but safe prompts across 10 categories, plus ~1,000 hard prompts and 600 genuinely toxic controls | Measures over-refusal: run OR-Bench-Hard through the classifier and track false-positive rate as a release-gate metric alongside attack block rate |
| **XSTest** (NAACL 2024) | 250 hand-crafted safe prompts using sensitive keywords, paired with unsafe counterparts | Quick smoke test that screening distinguishes intent from keyword presence; saturated for frontier models but still useful for catching over-aggressive classifier thresholds |
| **PolyGuardPrompts** (COLM 2025) | 29K samples across 17 languages | Per-locale false-negative measurement for 2.3.2 unsupported-language gap analysis |

### SOC-Integrated Monitoring Platforms

| Platform | Compliance | Content Safety Features | SOC Integration |
|----------|-----------|------------------------|-----------------|
| **Datadog LLM Observability** | SOC 2 Type II | End-to-end agent tracing, prompt injection tracking, toxicity scoring, full trace export | Native SIEM integration, correlation IDs, configurable alerts, dashboard visualization |
| **LangWatch** | SOC 2 | Per-request traces across agents/tools/chains, cost visibility, quality evaluations | Configurable alerts, trace export for replay, multi-step workflow monitoring |

### Policy Engines for ABAC

| Engine | Governance Body | Best For | Key Feature |
|--------|----------------|----------|-------------|
| **OPA / Rego** | CNCF Graduated | General ABAC policy enforcement | Sub-millisecond evaluation, decision caching, tamper-evident audit trails |
| **Cedar** | CNCF Sandbox (Jan 2026) | Agent tool authorization, fine-grained ABAC | Formally verified safety properties, ephemeral credentials, natural policy syntax |

---

## Notable Incidents

| Date | Incident | Relevance |
|------|----------|-----------|
| **January 2026** | Ofcom opened a formal Online Safety Act investigation into X over Grok-generated sexualised imagery, including of real people — the first major UK enforcement action centered on generative-AI content screening failures. | Demonstrates regulatory consequences when content screening fails on generation surfaces (2.3.1, 2.3.3). |
| **May 2026** | Pennsylvania sued Character.AI after its chatbot posed as a licensed medical professional to users, including minors — state enforcement arriving ahead of the federal GUARD Act. | Policy screening must cover impersonation and professional-advice categories, not just the classic four harm types (2.3.1). |
| **May 2026** | Microsoft published "Prompts Become Shells," detailing remote-code-execution vulnerabilities in AI agent frameworks where unscreened user input flowed into tool execution paths. | Concrete evidence for why violating inputs must be blocked before tool/MCP propagation, not merely flagged (2.3.3). |
| **April 2025** | China's "Clear and Bright" campaign removed 3,500+ AI products for content-compliance failures, the largest mass enforcement action against AI content screening gaps to date. | Scale of administrative enforcement where screening does not meet jurisdictional content rules. |
| **March 2026** | Australia's eSafety Commissioner reported AI companion apps exposing children to sexualised content and inadequate crisis routing, feeding directly into enforceable industry codes. | Age-context thresholds (2.3.1) and human-review routing (2.3.2) are now regulatory expectations, not just best practice. |
| **June 2025** | EchoLeak (CVE-2025-32711): Aim Security disclosed the first zero-click prompt-injection exfiltration in a production LLM system — a crafted email bypassed Microsoft 365 Copilot's XPIA classifier and used auto-fetched images plus a Teams proxy CSP allowance as the exfiltration channel. Patched server-side May 2025. | Canonical coordinated cross-modal incident: text payload slipped past the classifier, image auto-fetch carried the data out (2.3.5). |
| **August 2025** | Trail of Bits published the image-scaling attack and its open-source crafting tool Anamorpher: prompts invisible at full resolution emerged after downscaling and drove Gemini CLI to email Google Calendar data via Zapier with no user approval; Gemini web/API, Vertex AI Studio, Google Assistant, and Genspark were affected. | Hidden image content defeated screening that only saw the full-resolution image — the preprocessing pipeline itself became the attack surface (2.3.4). |
| **October 2025** | Brave disclosed "unseeable" prompt injections against agentic AI browsers: faint low-contrast text in screenshots was extracted by Perplexity Comet's OCR path and executed as user instructions against authenticated banking and email sessions; Fellou and Opera Neon showed related flaws. | Screenshot/OCR ingestion paths need the same screening as typed input; near-invisible-to-humans content is fully visible to the model (2.3.4, 2.3.5). |
| **April 2026** | Google telemetry reported via Help Net Security showed a 32% rise in in-the-wild malicious hidden-instruction pages between November 2025 and February 2026, using 1-pixel text, near-transparent colors, hidden tags, HTML comments, and metadata. | Hidden-content injection is now an observed, growing in-the-wild technique, not just a lab demonstration (2.3.4). |

---

## Implementation Maturity

| Requirement | Maturity | Notes |
|-------------|----------|-------|
| **2.3.1** Content classifiers | **High** | Multiple production-ready commercial APIs (OpenAI free, Azure, AWS with multimodal toxicity preview and cross-account safeguards, Google Cloud Model Armor with 10k-token prompt-injection windows and Terraform floor settings, Galileo, Lakera) and open-source options (LLM Guard, Granite Guardian, Llama Guard 3 Vision, Llama Prompt Guard 2, ExpGuard, PolyGuard); Anthropic's Constitutional Classifiers++ (January 2026) demonstrates ~40x compute reduction with a 0.05% production refusal rate, and Mozilla's `any-guardrail` provides a uniform interface for A/B-testing detectors. Multimodal safety classification is now available via Llama Guard 3 Vision, ShieldGemma 2, and Bedrock Guardrails multimodal toxicity. Main gaps: multilingual coverage in low-resource languages, classifier evasion resistance, visual semantic attacks (rebus/emoji-based) that bypass text-only classifiers entirely, narrative reframing that defeats intent-aware and Chain-of-Thought defenses (IntentPrompt, EMNLP 2025 Findings), and adversarial fine-tuning attacks (Trojan-Speak) that defeat LLM-as-classifier defenses when attackers control the underlying model. |
| **2.3.2** Unsupported-language abuse testing | **Medium** | Language detection, provider support matrices, and red-team corpora are available, but production teams often lack per-locale thresholds and low-resource language coverage. PolyGuard (COLM 2025, 17 languages with a 29K-sample benchmark) and Meta's Llama Prompt Guard 2 86M (eight evaluated languages) materially expand open-weight multilingual options, but code-switching, transliteration, short-message ambiguity, text-in-image attacks, and morphology-aware low-resource jailbreak generation remain practical bypass paths. |
| **2.3.1** Pre-model rejection paths | **Medium** | Architectural pattern is well-understood (gateway not advisory), but multi-turn attacks (crescendo, Bad Likert Judge), autonomous reasoning-model jailbreak agents, optimized suffix attacks, token flip attacks (EchoGram), special-token manipulation (MetaBreak), and visual rebus attacks (NVIDIA, July 2025) expose fundamental weaknesses across both text and multimodal modalities. NeMo Guardrails offers unique multi-turn awareness, while Constitutional Classifiers++ adds exchange-level evaluation. Trojan-Speak (March 2026) shows that adversarial fine-tuning can quietly defeat LLM-based classifiers altogether, so rejection paths must combine classifier screening with deterministic policy gates, capability restrictions, and human approval for high-impact actions. For agentic systems, output-level controls and action screening are now considered essential alongside input screening. |
| **2.3.3** Structured screening logs with SOC correlation | **Medium** | Datadog LLM Observability and LangWatch now provide SOC 2-compliant tracing with native SIEM integration — a significant improvement over custom-built pipelines. Azure Content Safety Studio and WhyLabs provide built-in dashboards. Red-team replay tooling (Promptfoo, DeepTeam) supports automated regression testing against archived attack payloads. Main gap: few organizations have established workflows for systematically replaying screening logs against updated classifiers. |
| **2.3.4** Non-text input screening | **Medium for classification, Low for steganalysis** | Multimodal safety classification is genuinely available: Llama Guard 4 (April 2025), ShieldGemma 2, omni-moderation image support, Azure Image Analyze (GA), and Bedrock multimodal toxicity (GA March 2025). Hidden-content and adversarial-perturbation detection is much weaker: no cloud vendor ships real-time steganalysis, open steganalysis tools are research-grade, and ART-style input transformations are defeatable by adaptive attacks. The deployable controls are destruction-by-transformation (re-encode/resize/strip, CDR) and OCR-then-classify; audio reduces to transcribe-then-classify, which is blind to the acoustic channel. Google Model Armor remains text-only — a notable hyperscaler gap. |
| **2.3.5** Cross-modal coordinated attack detection | **Emerging** | Joint text+image scoring exists per-request (omni-moderation, Azure `imageWithText` preview, Bedrock combined calls, Llama Guard 4 multi-image), and red-team tooling can generate split-payload attacks (garak FigStep probes, PyRIT converters, Promptfoo strategies). But cross-modal correlation engines are research-only (CrossGuard, GuardReasoner-Omni), and nothing productized correlates payload fragments across turns, sessions, or agent hops. Expect to assemble this Level 3 control from OCR, transcription, joint classification, and session analytics. |

---

## Cross-Chapter Links

| Related Section | Connection |
|----------------|------------|
| [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense.md) | Content classifiers complement prompt injection detection — prompt injection bypasses can circumvent content screening (AML.T0051) |
| [C02-02 Pre-Tokenization Input Normalization](C02-02-Pre-Tokenization-Input-Normalization.md) | Encoding and obfuscation attacks (Unicode, Base64, homoglyphs) affect both normalization and content classifiers |
| [C05 Access Control & Identity](../C05-Access-Control/C05-Access-Control.md) | ABAC policy resolution depends on identity infrastructure for user attributes (age, region, role) |
| [C09 Orchestration & Agentic Action](../C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md) | Rejected content must not propagate through agent chains (2.3.3) |
| [C10 MCP Security](../C10-MCP-Security/C10-MCP-Security.md) | Content screening must cover MCP tool inputs/outputs; policy-violating content must not propagate to MCP servers (2.3.3) |
| [C13 Monitoring & Logging](../C13-Monitoring-and-Logging/C13-Monitoring-and-Logging.md) | Screening logs (2.3.4) feed into the broader monitoring and SIEM infrastructure |
| [C14 Human Oversight](../C14-Human-Oversight/C14-Human-Oversight.md) | Borderline content screening decisions may require human-in-the-loop escalation |

---

## Related Pages

- [C11-10 Adversarial Bias Exploitation Defense](../C11-Adversarial-Robustness/C11-10-Adversarial-Bias-Exploitation-Defense.md) — Extends classifier hardening with subgroup robustness, guardrail evasion testing, and evidence that safety classifiers resist targeted probing.
- [C07-03 Output Safety Privacy Filtering](../C07-Model-Behavior/C07-03-Output-Safety-Privacy-Filtering.md) — Complements input-side screening with post-response checks for unsafe content, PII, and covert exfiltration after generation.
- [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense.md) — Shares jailbreak, indirect-injection, and agent-tool guardrail tests that often trigger the same content-screening controls.
- [C02-02 Pre-Tokenization Input Normalization](C02-02-Pre-Tokenization-Input-Normalization.md) — Prepares text, encodings, and tool or memory inputs so content classifiers evaluate the intended payload instead of obfuscated variants.
- [C09-05 Secure Messaging](../C09-Orchestration-and-Agents/C09-05-Secure-Messaging.md) — Carries screened-content decisions across agent messages, tool outputs, MCP metadata, and shared-memory boundaries before downstream trust is granted.

---

## Regulatory Compliance Matrix

| Regulation | Applicable Articles | Content Screening Requirements | Enforcement |
|------------|-------------------|-------------------------------|-------------|
| **EU AI Act** | Art. 5 (prohibited), Art. 50 (transparency), Arts. 51–56 (GPAI), Arts. 6–49 (high-risk); General-Purpose AI Code of Practice (final, July 2025) — Transparency, Copyright, and Safety and Security chapters | GPAI must prevent illegal content generation; mandatory deepfake labeling; prohibited AI exploiting age-group vulnerabilities; Annex III high-risk AI system rules deferred to December 2, 2027 by the May 2026 Digital Omnibus (including automatic logging and post-market monitoring); draft Article 50 transparency guidelines published May 8, 2026, open for stakeholder consultation through June 3, 2026, intended to apply from August 2, 2026 — disclosure obligations for synthetic content / deepfakes / AI emotion recognition / biometric categorization, with attenuated disclosure permitted for clearly artistic, creative, satirical, or fictional works; updated Code of Practice on marking and labelling AI-generated content under development with working-group sessions through May 2026; final GPAI Code of Practice Safety and Security chapter applies to systemic-risk model providers under Article 55 and requires systemic-risk assessment and monitoring (including CBRN, loss-of-control, autonomy, and misuse scenarios) plus implementation documentation retained for at least 10 years after the model is placed on the market | Up to 35M EUR / 7% global turnover for prohibited practices (enforced since Feb 2025); up to 15M EUR / 3% for high-risk non-compliance (from Dec 2027 after the May 2026 Digital Omnibus deferral); GPAI Code fully enforceable with fines from August 2, 2026 |
| **EU DSA** | Art. 6 (illegal content), Art. 17 (reasons for restriction), VLOP systemic-risk duties | Platforms must act diligently to remove illegal content; transparency reporting on AI-assisted content moderation; high-impact AI feature deployments may require ad hoc risk assessment before rollout | Transparency reports due early 2026; formal investigations can examine whether AI feature risks were assessed and mitigated before deployment |
| **NIST AI RMF / AI 600-1** | MAP, MEASURE, MANAGE functions; NIST AI 600-1 Generative AI Profile | Voluntary — harm taxonomy, content safety metrics, operational controls, generative-AI-specific risk identification, pre-deployment testing, incident disclosure, content provenance, and risk management practices for harmful-content and misuse scenarios | Voluntary; referenced in US federal procurement |
| **COPPA (updated)** | New rule effective June 2025; FTC age-verification enforcement policy statement issued February 25, 2026 | Age screening before data collection; separate parental consent for AI training data; biometric identifiers covered; age-verification data should be limited to age determination, deleted promptly, protected, and assessed for reasonable accuracy | FTC enforcement; compliance deadline April 22, 2026 |
| **Australia Online Safety Codes** | Age-Restricted Material Codes; Unlawful Material Codes and Standards; eSafety transparency notices | Companion chatbots must protect children from age-inappropriate content, provide crisis and mental-health routing, and prevent generation or facilitation of child sexual exploitation and abuse material | Legally enforceable; breach of a compliance direction can carry civil penalties up to AUD 49.5M |
| **UK Online Safety Act** | Illegal content duties, child-safety duties, age-assurance duties; AI chatbots brought clearly into scope after the Prime Minister's February 16, 2026 announcement and Ofcom's 2026-27 priorities focused on AI moderation, deepfakes, and child protection | AI chatbots and services with user-to-user or generated-content surfaces may need illegal-content risk assessments, rapid takedown processes, content moderation systems, CSAM/non-consensual intimate image controls, and highly effective age assurance where pornography or adult content is available; Ofcom expects named accountable persons, swift takedown, and adequately resourced moderation functions | Ofcom investigations can lead to required remediation, fines up to 18M GBP or 10% of qualifying worldwide revenue, and business-disruption measures in serious ongoing non-compliance |
| **ISO 42001** | Annex A.2, A.5, A.8, A.9, A.10 | AI risk assessment, data governance, continuous monitoring, incident management, adversarial robustness | Certification-based |
| **China AI Regulations** | Generative AI Measures (Aug 2023), Labeling Rules (Sept 2025), CSL Amendments (Jan 2026) | Content must adhere to regulatory standards; mandatory AI content labeling; pre-publication review mechanisms | Administrative takedowns — 3,500+ AI products removed in April 2025 "Clear and Bright" campaign |
| **CHATBOT Act / GUARD Act (proposed U.S.)** | Senate Commerce introduction (Apr 28, 2026); Senate Judiciary Committee approval and narrowing of S. 3062 (Apr 30, 2026 / May 2026) | The narrowed GUARD Act focuses on "AI companions" — conversational systems simulating emotional or interpersonal interactions; companies must implement reasonable age verification, prohibit minor access, and require non-human / non-credentialed disclosures, with civil penalties up to $250,000 per violation enforced by federal and state officials. The CHATBOT Act establishes parental "family accounts" for minors. Pennsylvania's May 1, 2026 suit against Character.AI shows that state regulators will pursue impersonation of licensed professionals even while federal legislation is pending | Proposed federal legislation; not enacted as of May 21, 2026, but state-level enforcement (e.g., Pennsylvania v. Character.AI) is already underway |
| **COPPA 2.0 (proposed)** | Extends protections to ages 13–16 | Bans targeted advertising to minors entirely; dedicated FTC enforcement division; layer on existing COPPA obligations | Under active Congressional consideration (March 2026) |
| **UK AADC** | 15 standards | High-privacy defaults for children; no profiling of minors; age-appropriate content delivery | ICO fines up to 17.5M GBP / 4% turnover |

---

## Related Standards & References

- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [OpenAI omni-moderation Model Card](https://platform.openai.com/docs/models/omni-moderation-latest)
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/)
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [AWS Bedrock Guardrails — Components](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html)
- [AWS Bedrock Guardrails — Content Filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters.html)
- [AWS Bedrock Guardrails — Supported Languages](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-supported-languages.html)
- [AWS Bedrock Guardrails — Automated Reasoning Checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)
- [Google Cloud Model Armor Overview](https://docs.cloud.google.com/model-armor/overview)
- [Anthropic Usage Policy](https://www.anthropic.com/policies/aup)
- [Azure AI Content Safety — Language Support](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/language-support)
- [Azure AI Language Detection Transparency Note](https://learn.microsoft.com/en-us/legal/cognitive-services/language-service/transparency-note-language-detection)
- [fastText Language Identification](https://fasttext.cc/docs/en/language-identification)
- [Google CLD3 Language Detector](https://github.com/google/cld3)
- [LLM Guard by Protect AI](https://llm-guard.com/)
- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [NVIDIA NeMo Guardrails — Colang 2.0 Guide](https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/colang/colang-2/index.html)
- [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- [WhyLabs LangKit](https://whylabs.ai/langkit)
- [IBM Granite Guardian](https://www.ibm.com/think/tutorials/llm-content-moderation-with-granite-guardian)
- [Perspective API (Google/Jigsaw)](https://perspectiveapi.com/)
- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/)
- [AWS Cedar](https://www.cedarpolicy.com/)
- [EU AI Act — Official Text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [EU Digital Services Act](https://digital-strategy.ec.europa.eu/en/policies/digital-services-act)
- [European Commission — DSA Investigation into Grok and X Recommender Systems (January 2026)](https://digital-strategy.ec.europa.eu/en/news/commission-investigates-grok-and-xs-recommender-systems-under-digital-services-act)
- [European Commission — Draft Article 50 Transparency Guidelines (May 2026)](https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act)
- [COPPA Updated Rule](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1 — Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [Palo Alto Unit 42 — LLM Guardrails Comparison (March 2025)](https://unit42.paloaltonetworks.com/comparing-llm-guardrails-across-genai-platforms/)
- [HiddenLayer — EchoGram Token Flip Attack (November 2025)](https://www.hiddenlayer.com/research/echogram-the-hidden-vulnerability-undermining-ai-guardrails)
- [Crescendo Attack Paper (USENIX Security 2025)](https://arxiv.org/abs/2404.01833)
- [Many-Shot Jailbreaking (Anthropic, NeurIPS 2024)](https://www.anthropic.com/research/many-shot-jailbreaking)
- [Microsoft Skeleton Key Disclosure](https://www.microsoft.com/en-us/security/blog/2024/06/26/mitigating-skeleton-key-a-new-type-of-generative-ai-jailbreak-technique/)
- [Promptfoo — LLM Red Teaming Framework](https://www.promptfoo.dev/docs/red-team/)
- [Promptfoo — Guardrails Assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/guardrails/)
- [Promptfoo — Testing and Validating Guardrails](https://www.promptfoo.dev/docs/guides/testing-guardrails/)
- [Promptfoo — Adaptive Guardrails](https://www.promptfoo.dev/docs/enterprise/guardrails/)
- [OpenAI — Promptfoo Acquisition Announcement (March 2026)](https://openai.com/index/openai-to-acquire-promptfoo/)
- [DeepTeam — LLM Red Teaming by Confident AI](https://github.com/confident-ai/deepteam)
- [garak Prompt Injection Scanning](https://docs.garak.ai/garak/examples/prompt-injection)
- [Giskard Hub Vulnerability Scanning](https://docs.giskard.ai/hub/sdk/guides/scans)
- [Mindgard — Bypassing Azure AI Content Safety Guardrails](https://mindgard.ai/blog/bypassing-azure-ai-content-safety-guardrails)
- [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/)
- [LangWatch — LLM Monitoring](https://langwatch.ai/)
- [Bypassing LLM Guardrails: Empirical Analysis of Evasion Attacks (2025)](https://arxiv.org/html/2504.11168)
- [EU AI Act Code of Practice — AI-Generated Content Labeling (Second Draft, March 2026)](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-second-draft-code-practice-marking-and-labelling-ai-generated-content)
- [NVIDIA — Securing Agentic AI: How Semantic Prompt Injections Bypass AI Guardrails (July 2025)](https://developer.nvidia.com/blog/securing-agentic-ai-how-semantic-prompt-injections-bypass-ai-guardrails/)
- [ExpGuard: LLM Content Moderation in Specialized Domains (ICLR 2026)](https://arxiv.org/abs/2603.02588)
- [Large Reasoning Models are Autonomous Jailbreak Agents (Nature Communications, February 2026)](https://www.nature.com/articles/s41467-026-69010-1)
- [AB Jailbreaking — Hybrid Framework for Adversarial Vulnerabilities (Scientific Reports, April 2026)](https://www.nature.com/articles/s41598-026-44403-w)
- [MNMR-GenA Low-Resource Language Jailbreaks (Scientific Reports, April 2026)](https://www.nature.com/articles/s41598-026-47434-5)
- [Detection and Analysis of Prompt Injection in Indian Multilingual LLMs (Scientific Reports, April 2026)](https://www.nature.com/articles/s41598-026-43883-0)
- [Llama Guard 3 Model Card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-3/)
- [Galileo AI Guardrails Platform](https://galileo.ai/blog/best-ai-guardrails-platforms)
- [Lakera Guard](https://www.lakera.ai/)
- [Lakera Guard — Guardrails Documentation](https://docs.lakera.ai/docs/defenses)
- [Lakera Guard — Content Moderation](https://docs.lakera.ai/docs/content-moderation)
- [TrueFoundry Content Moderation Guardrail](https://www.truefoundry.com/docs/ai-gateway/tfy-content-moderation)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet — Model-Based Guardrails](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html#model-based-guardrails)
- [Code-Switching Red-Teaming: LLM Evaluation for Safety and Multilingual Understanding (ACL 2025)](https://aclanthology.org/2025.acl-long.657/)
- [Beyond Words: Multilingual and Multimodal Red Teaming of MLLMs (LLMSec 2025)](https://aclanthology.org/2025.llmsec-1.15/)
- [MrGuard: A Multilingual Reasoning Guardrail for Universal LLM Safety (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.1392/)
- [English as Defense Proxy: Mitigating Multilingual Jailbreak (EMNLP Findings 2025)](https://aclanthology.org/2025.findings-emnlp.62/)
- [FTC COPPA Policy Statement on Age Verification (February 2026)](https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-issues-coppa-policy-statement-incentivize-use-age-verification-technologies-protect-children)
- [FTC Inquiry into AI Chatbots Acting as Companions (September 2025)](https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions)
- [eSafety Commissioner — AI Companions Report (March 2026)](https://www.esafety.gov.au/newsroom/media-releases/esafety-report-shows-ai-companions-are-putting-children-at-risk)
- [Ofcom — Investigation into X over Grok Sexualised Imagery (January 2026)](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ofcom-launches-investigation-into-x-over-grok-sexualised-imagery)
- [Ofcom — AI Companion Chatbot Investigation (January 2026)](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ofcom-investigates-ai-companion-chatbot-service)
- [Common Sense Media — Grok AI Chatbot Not Safe for Teens (January 2026)](https://www.commonsensemedia.org/press-releases/grok-ai-chatbot-not-safe-for-teens-common-sense-media-report-finds)
- [OpenAI Child Safety Blueprint (April 2026)](https://openai.com/index/introducing-child-safety-blueprint/)
- [CHATBOT Act — Senate Commerce Committee Introduction (April 2026)](https://www.commerce.senate.gov/press/rep/release/cruz-schatz-curtis-schiff-introduce-new-bill-giving-parents-control-over-kids-ai-chatbot-use/)
- [GUARD Act — Senate Judiciary Committee Approval (April 2026)](https://www.hawley.senate.gov/senator-hawleys-guard-act-to-protect-kids-from-ai-chatbots-passes-committee-unanimously/)
- [Cloud Security Alliance — Image-Based Prompt Injection (March 2026)](https://labs.cloudsecurityalliance.org/research/csa-research-note-image-prompt-injection-multimodal-llm-2026/)
- [Microsoft Research — SEMA Multi-Turn Jailbreak Attacks (ICLR 2026)](https://www.microsoft.com/en-us/research/publication/sema-simple-yet-effective-learning-for-multi-turn-jailbreak-attacks/)
- [MultiBreak: A Scalable and Diverse Multi-turn Jailbreak Benchmark (ICML 2026)](https://arxiv.org/abs/2605.01687)
- [Boundary Point Jailbreaking of Black-Box LLMs (February 2026)](https://arxiv.org/abs/2602.15001)
- [A Lightweight Explainable Guardrail for Prompt Safety (January 2026)](https://arxiv.org/abs/2602.15853)
- [Springer — Securing LLM-Based Agents Against Cyberattacks (May 2026)](https://link.springer.com/article/10.1007/s11416-026-00622-3)
- [European Commission — Technical Studies for Article 50 AI-Generated Content Marking and Detection (May 2026)](https://digital-strategy.ec.europa.eu/en/library/three-studies-technical-solutions-mark-and-detect-ai-generated-content)
- [European Commission — General-Purpose AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai)
- [OWASP AI Testing Guide v1](https://owasp.org/www-project-ai-testing-guide/)
- [Anthropic — Next-Generation Constitutional Classifiers (January 2026)](https://www.anthropic.com/research/next-generation-constitutional-classifiers)
- [Constitutional Classifiers++: Efficient Production-Grade Defenses against Universal Jailbreaks (arXiv 2601.04603, January 2026)](https://arxiv.org/abs/2601.04603)
- [Anthropic Alignment Science — Cost-Effective Constitutional Classifiers via Representation Re-use](https://alignment.anthropic.com/2025/cheap-monitors/)
- [Trojan-Speak: Bypassing Constitutional Classifiers via Adversarial Finetuning (arXiv 2603.29038, March 2026)](https://arxiv.org/abs/2603.29038)
- [MetaBreak: Jailbreaking Online LLM Services via Special Token Manipulation (arXiv 2510.10271, October 2025)](https://arxiv.org/abs/2510.10271)
- [Jailbreaking Attacks vs. Content Safety Filters: How Far Are We in the LLM Safety Arms Race? (arXiv 2512.24044, December 2025)](https://arxiv.org/abs/2512.24044)
- [Mozilla.ai — Introducing any-guardrail: A Common Interface to Test AI Safety Models](https://blog.mozilla.ai/introducing-any-guardrail-a-common-interface-to-test-ai-safety-models/)
- [mozilla-ai/any-guardrail (GitHub)](https://github.com/mozilla-ai/any-guardrail)
- [AWS — Bedrock Guardrails Multimodal Toxicity Detection (Image Support, Preview)](https://aws.amazon.com/blogs/aws/amazon-bedrock-guardrails-now-supports-multimodal-toxicity-detection-with-image-support/)
- [AWS — Bedrock Guardrails Cross-Account Safeguards (April 2026)](https://aws.amazon.com/about-aws/whats-new/2026/04/bedrock-guardrails-cross-account-safeguards/)
- [Google Cloud — Model Armor Release Notes](https://docs.cloud.google.com/model-armor/release-notes)
- [Google Cloud — Model Armor Floor Settings (Security Command Center)](https://cloud.google.com/security-command-center/docs/model_armor_floor_settings)
- [Zapier — AI Guardrails Inline Safety Checks (March 2026)](https://www.businesswire.com/news/home/20260330262542/en/AI-Guardrails-by-Zapier-Gives-Teams-Inline-Safety-Checks-for-Every-AI-Powered-Workflow)
- [European Commission — Consultation on Draft Guidelines on Transparency Obligations under the AI Act (May 2026)](https://digital-strategy.ec.europa.eu/en/consultations/consultation-draft-guidelines-transparency-obligations-under-ai-act)
- [European Commission — Code of Practice on Marking and Labelling AI-Generated Content (Policy Page)](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)
- [Global Policy Watch — Ten Takeaways from the European Commission Draft Article 50 Guidelines (May 2026)](https://www.globalpolicywatch.com/2026/05/10-takeaways-european-commission-draft-guidelines-on-ai-transparency-under-the-eu-ai-act/)
- [Ofcom — AI Chatbots and Online Regulation: What You Need to Know](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ai-chatbots-and-online-regulation-what-you-need-to-know)
- [Pinsent Masons — Online Safety Act Duties Cover Gen-AI and Chatbots, Ofcom Confirms](https://www.pinsentmasons.com/out-law/news/online-safety-act-duties-cover-gen-ai-and-chatbots)
- [GUARD Act — S. 3062 Text (Congress.gov)](https://www.congress.gov/bill/119th-congress/senate-bill/3062/text)
- [Global Policy Watch — Senate Judiciary Committee Advances Narrowed GUARD Act (May 2026)](https://www.globalpolicywatch.com/2026/05/senate-judiciary-committee-advances-guard-act-regulating-minor-use-of-ai/)
- [Pennsylvania v. Character.AI — Suit Alleging Unauthorized Practice of Medicine (May 2026)](https://www.paubox.com/blog/pennsylvania-sues-character.ai-after-chatbot-poses-as-a-doctor)
- [Microsoft Security Blog — Prompts Become Shells: RCE in AI Agent Frameworks (May 7, 2026)](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)
- [IntentPrompt — Exploring the Vulnerability of the Content Moderation Guardrail via Intent Manipulation (EMNLP 2025 Findings, arXiv 2505.18556)](https://arxiv.org/abs/2505.18556)
- [JBFuzz — Jailbreaking LLMs Efficiently and Effectively Using Fuzzing (arXiv 2503.08990)](https://arxiv.org/abs/2503.08990)
- [Meta Llama Prompt Guard 2 — Model Card](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/)
- [Meta Llama-Prompt-Guard-2-86M (Hugging Face)](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)
- [PolyGuard — A Multilingual Safety Moderation Tool for 17 Languages (COLM 2025, arXiv 2504.04377)](https://arxiv.org/abs/2504.04377)
- [European Commission — General-Purpose AI Code of Practice (Final, July 2025)](https://code-of-practice.ai/)
- [Center for Internet Security — Prompt Injection Report Analysis (April 2026)](https://dev.to/waxell/340-and-climbing-what-the-cis-prompt-injection-report-means-for-enterprise-ai-agents-49jn)
- [MLCommons AILuminate Benchmark](https://mlcommons.org/benchmarks/ailuminate/)
- [OR-Bench: An Over-Refusal Benchmark for Large Language Models (ICML 2025)](https://arxiv.org/abs/2405.20947)
- [XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours (NAACL 2024)](https://aclanthology.org/2024.naacl-long.301/)
- [Multilingual Jailbreaking of LLMs Using Low-Resource Languages (arXiv 2605.18239, May 2026)](https://arxiv.org/abs/2605.18239)
- [MITRE ATLAS — AML.T0054 LLM Jailbreak](https://atlas.mitre.org/techniques/AML.T0054)
- [OpenTelemetry — Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Cloudflare — Firewall for AI: Block Unsafe LLM Prompts](https://blog.cloudflare.com/block-unsafe-llm-prompts-with-firewall-for-ai/)
- [Splunk — MITRE ATLAS AI Threat Detection App](https://splunkbase.splunk.com/app/8527)
- [Trail of Bits — Weaponizing Image Scaling Against Production AI Systems (August 2025)](https://blog.trailofbits.com/2025/08/21/weaponizing-image-scaling-against-production-ai-systems/)
- [Brave — Unseeable Prompt Injections in Screenshots (October 2025)](https://brave.com/blog/unseeable-prompt-injections/)
- [EchoLeak CVE-2025-32711 — Zero-Click Prompt Injection in M365 Copilot (June 2025)](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability)
- [The Attacker Moves Second: EchoLeak Analysis (arXiv 2509.10540)](https://arxiv.org/abs/2509.10540)
- [Microsoft MSRC — How Microsoft Defends Against Indirect Prompt Injection Attacks (July 2025)](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)
- [Help Net Security — Indirect Prompt Injection in the Wild (April 2026)](https://www.helpnetsecurity.com/2026/04/24/indirect-prompt-injection-in-the-wild/)
- [Meta Llama Guard 4 — Model Card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-4/)
- [meta-llama/Llama-Guard-4-12B (Hugging Face)](https://huggingface.co/meta-llama/Llama-Guard-4-12B)
- [Google ShieldGemma 2 — Model Card](https://ai.google.dev/gemma/docs/shieldgemma/model_card_2)
- [Azure AI Content Safety — Multimodal (imageWithText) Quickstart](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-multimodal)
- [AWS Bedrock Guardrails — Multimodal Content Filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-mmfilter.html)
- [AWS — Bedrock Guardrails Image Content Filters GA (March 2025)](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-guardrails-image-content-filters-provide-industry-leading-safeguards-helping-customer-block-up-to-88-of-harmful-multimodal-content-generally-available-today/)
- [OPSWAT MetaDefender Deep CDR](https://www.opswat.com/technologies/deep-cdr)
- [ExifTool by Phil Harvey](https://exiftool.org/)
- [Aletheia — Open-Source Image Steganalysis](https://github.com/daniellerch/aletheia)
- [Adversarial Robustness Toolbox — Preprocessor Defenses](https://adversarial-robustness-toolbox.readthedocs.io/en/latest/modules/defences/preprocessor.html)
- [garak — visual_jailbreak (FigStep) Probes](https://reference.garak.ai/en/stable/garak.probes.visual_jailbreak.html)
- [Promptfoo — Image Jailbreaking Strategy](https://www.promptfoo.dev/docs/red-team/strategies/image/)
- [Microsoft PyRIT — Python Risk Identification Tool](https://microsoft.github.io/PyRIT/)
- [FigStep: Jailbreaking Large Vision-Language Models via Typographic Visual Prompts (AAAI 2025, arXiv 2311.05608)](https://arxiv.org/abs/2311.05608)
- [Visual-RolePlay: Universal Jailbreak Attack on Multimodal LLMs (arXiv 2405.20773)](https://arxiv.org/abs/2405.20773)
- [JPRO: Automated Multimodal Jailbreaking via Multi-Agent Collaboration (arXiv 2511.07315, November 2025)](https://arxiv.org/abs/2511.07315)
- [AudioJailbreak: Jailbreak Attacks Against End-to-End Large Audio-Language Models (arXiv 2505.14103, May 2025)](https://arxiv.org/abs/2505.14103)
- [Sirens' Whisper: Inaudible Near-Ultrasonic Jailbreaks of Speech-Driven LLMs (arXiv 2603.13847, March 2026)](https://arxiv.org/abs/2603.13847)
- [Audio Jailbreaks in Large Audio-Language Models: Taxonomy and Attack-Defense Analysis (arXiv 2605.30031, May 2026)](https://arxiv.org/abs/2605.30031)
- [Adversarial Attacks on Multimodal LLMs: A Comprehensive Survey (arXiv 2603.27918, March 2026)](https://arxiv.org/abs/2603.27918)
- [Breaking Multimodal LLM Safety via Video-Driven Prompting (CVPR 2026)](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Breaking_Multimodal_LLM_Safety_via_Video-Driven_Prompting_CVPR_2026_paper.html)
- [CrossGuard: Guarding Against Joint-Modal Implicit Malicious Attacks (arXiv 2510.17687)](https://arxiv.org/abs/2510.17687)
- [GuardReasoner-Omni: Reasoning Guardrails Across Text, Image, and Video (arXiv 2602.03328, February 2026)](https://arxiv.org/abs/2602.03328)
- [Jailbreaks on Vision-Language Models via Multimodal Reasoning (arXiv 2601.22398, January 2026)](https://arxiv.org/abs/2601.22398)
- [MITRE ATLAS Data Releases (v2026.05, May 2026)](https://github.com/mitre-atlas/atlas-data/releases)

---

## Open Research Questions

- How effective are current content classifiers against adversarial paraphrasing and coded language? (Adversarial paraphrasing achieves 87.88% TPR reduction across detector types as of 2025 — the gap remains significant.)
- What is the right balance between over-blocking (false positives harming usability) and under-blocking (false negatives allowing harmful content)? How should organizations measure and report this tradeoff?
- How should content screening evolve for multi-turn conversations where individual messages are benign but the conversation trajectory is harmful? (Crescendo attacks achieve 98% bypass via gradual escalation — NeMo Guardrails' Colang DSL is one approach, but maturity is limited.)
- Can content classifiers be reliably evaluated across languages and cultures, or are they inherently biased toward English-language norms? (ACL 2025 code-switching red-team work produced 46.7% more successful attacks than standard English attacks, and text-in-image attacks were especially effective for lower-resource languages.)
- How should organizations handle the tension between open-ended AI assistants and strict content policies in multi-tenant deployments with diverse regulatory requirements?
- Can content classifiers themselves be hardened against adversarial manipulation (e.g., EchoGram token flip attacks), or will the classifier-vs-attacker arms race remain fundamentally asymmetric?
- Can classifier APIs expose enough signal for legitimate tuning without enabling black-box boundary search attacks? Boundary Point Jailbreaking suggests that binary reject/allow feedback can still be enough for automated optimization unless batch-level probing is detected.
- How should content screening adapt to agentic architectures where content flows through chains of tool calls, MCP servers, and sub-agents with different trust levels, especially when a reasoning model can autonomously plan multi-turn jailbreak attempts?
- What is the minimum viable logging schema for effective red-team replay — can organizations replay screening decisions without storing the original harmful input text, using only hashes and metadata? What are the privacy and regulatory implications of retaining harmful content in screening logs?
- How should content screening adapt to multimodal inputs where harmful intent is encoded visually (rebus sequences, emoji chains, steganographic payloads) rather than textually? Can multimodal safety classifiers (Llama Guard 3 Vision, ShieldGemma 2) reliably detect visual semantic attacks, or is this an inherently harder classification problem than text?
- As domain-specific guardrails (ExpGuard for finance/medical/legal) demonstrate significant accuracy improvements over general-purpose classifiers, should organizations deploy multiple specialized classifiers in parallel rather than relying on a single general-purpose model?
- When an adversary can fine-tune the underlying model (e.g., open weights, internal misuse, or a compromised supply chain), what mix of LLM-based classifiers, deterministic policy gates, capability restrictions, and human approval is sufficient? Trojan-Speak achieves 99+% Constitutional Classifier evasion with under 5% reasoning loss, implying that LLM-as-classifier defenses cannot be trusted on their own under that threat model.
- How should screening pipelines integrate AI-generated content disclosure (deepfake labeling, content credentials, watermarking) so that EU AI Act Article 50 transparency obligations are enforceable from August 2, 2026, without leaking the underlying content into screening logs more than necessary for replay and audit?
- Normalize-to-text (OCR plus transcription) is today's practical multimodal screening pattern, but it discards the pixel and acoustic channels where adversarial payloads actually live — image-scaling attacks and near-ultrasonic injection both exploit exactly what normalization throws away. Can joint multimodal classifiers close that gap, or does cross-modal coordinated-attack detection (2.3.5) inherently require session-level correlation infrastructure that no vendor ships yet?

---
