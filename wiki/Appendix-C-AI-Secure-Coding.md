# Appendix C: AI-Assisted Secure Coding

> **Source:** [`1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)
> **Requirements:** 27 | **Sections:** 9
> **Last Researched:** 2026-03-22

## Overview

Controls for the safe use of AI-assisted coding tools, covering workflow security, tool qualification, prompt management, code validation, and deployment controls.

### AI-Generated Code Vulnerability Landscape (2024-2026)

The security properties of AI-generated code have been extensively studied. Key findings:

- **Overall vulnerability rate: 25.1%** across 534 AI-generated code samples from 6 major LLMs (AppSec Santa 2026). Safest model (GPT-5.2): 19.1%; three models tied at 29.2%.
- **Copilot-specific:** 32.8% of Python and 24.5% of JavaScript snippets contained security issues ([ACM TOSEM 2025](https://dl.acm.org/doi/10.1145/3716848)). NYU found ~40% of Copilot-generated programs contained vulnerabilities.
- **Veracode 2025:** 45% of AI-generated code contains security flaws when tested across 100+ LLMs.
- **GitHub Copilot generates ~46% of code** in files where enabled, making the audit surface substantial.
- **Trust gap is the primary risk:** Per-line vulnerability rates are comparable to human code, but developers review AI output less carefully, amplifying risk.

**Most common CWEs in AI-generated code (2026 data):**

| CWE | Description | Frequency |
|-----|-------------|-----------|
| CWE-918 | Server-Side Request Forgery (SSRF) | Most frequent (32 instances in 534 samples) |
| CWE-215 | Debug Information Leak | 18 instances |
| CWE-502 | Insecure Deserialization | 14 instances |
| CWE-79 | Cross-Site Scripting (XSS) | Common across all models |
| CWE-89 | SQL Injection | String concatenation pattern |
| CWE-798 | Hardcoded Credentials | Persistent across models |
| CWE-78 | OS Command Injection | Common in system utility code |
| CWE-22 | Path Traversal | Missing canonicalization |

**Critical SAST finding:** 78% of confirmed vulnerabilities were caught by only one scanning tool, meaning multiple scanners are necessary for adequate coverage of AI-generated code.

### AI Coding Agent Security: End-to-End Testing (March 2026)

As of March 2026, DryRun Security published results from testing three major AI coding agents — Claude Code (Sonnet 4.6), OpenAI Codex (GPT 5.2), and Google Gemini (2.5 Pro) — building two realistic applications from scratch. Key findings:

- **87% of pull requests contained at least one vulnerability** (26 of 30 PRs), with 143 total security issues across 38 scans.
- **Broken access control was universal** across all three agents: unauthenticated endpoints on destructive operations, missing authorization checks, client-side-only validation.
- **Business logic flaws dominated:** OAuth implementation failures (missing state parameters), missing WebSocket authentication, inadequate rate limiting, and weak JWT secret management (hardcoded fallbacks).
- **Pattern-based SAST caught only 12% of seeded vulnerabilities** vs. 88% for contextual analysis tools, highlighting a major gap in traditional static analysis for AI-generated code.

This is significant because it demonstrates that AI coding agents do not just reproduce known-bad patterns — they introduce novel logic-level flaws that require semantic understanding to detect.

### AI Code Review Tools: Capabilities and Limitations (2025-2026)

| Tool | Status | Security Capability |
|------|--------|-------------------|
| **GitHub Copilot Code Review** | GA April 2025; 1M users in first month; CodeQL + ESLint integration Oct 2025 | Failed to flag any OWASP Top 10 vulnerabilities in WebGoat testing; cannot reason about cross-function data flow |
| **CodeRabbit** | Most-installed AI code review on GitHub/GitLab; 2M+ repos, 13M+ PRs | Broad coverage; not security-specialized |
| **Aegis** | Purpose-built for AI-generated code security | Specialized for AI-specific vulnerability patterns |
| **GitHub Advanced Security** | Code scanning + secret scanning + Dependabot + Copilot Autofix | Comprehensive but requires GitHub Enterprise |
| **Endor Labs AI Security Review** | Launched 2025 | Focus on dependency and supply chain risks |
| **Semgrep Multimodal** | Launched March 2026 | Combines deterministic SAST with LLM reasoning; claims 8x more true positives and 50% less noise; detects IDOR, broken authorization, and business logic flaws that traditional SAST misses |
| **DryRun Security** | Contextual code review for AI agents | PR-native enforcement; caught 88% of AI coding agent vulnerabilities vs. 12% for pattern-based SAST; integrates with Claude Code, Cursor, Codex |

**Key limitation:** Copilot's code review reviewed only 6 of 9 XSS-vulnerable files and 4 of 9 SQL injection files in testing, making no security comments on any. Cross-function data flow analysis remains a fundamental weakness of current AI code reviewers. As of March 2026, Semgrep Multimodal is the first major SAST vendor to combine LLM reasoning with rule-based analysis to address this gap.

### Security Vulnerabilities in AI Coding Tools (2025-2026)

AI coding tools themselves have become a significant attack surface. The "IDEsaster" research (Ari Marzouk, December 2025) disclosed 30+ vulnerabilities across 8 major AI IDEs, resulting in 24 CVEs. Affected tools include Cursor, Windsurf, GitHub Copilot, Zed.dev, Roo Code, Kiro.dev, JetBrains Junie, and Claude Code.

**GitHub Copilot / Cursor CVEs:**
- **CVE-2025-62453:** Improper validation of generative AI output in Copilot code suggestions
- **CVE-2025-53773:** Exploits Copilot's ability to modify project configuration files, enabling arbitrary command execution
- **CVE-2025-54130, CVE-2025-64660, CVE-2025-61590:** Additional Copilot/Cursor vulnerabilities from IDEsaster disclosure
- **"Affirmation jailbreak":** Simple agreeing words tricked Copilot into producing disallowed code
- **Proxy hijack:** Exploited Copilot's proxy settings to steal API tokens

**Claude Code CVEs (Check Point Research, February 2026):**
- **CVE-2025-59536** (CVSS 8.7): Code injection via `.mcp.json` and `claude/settings.json` files, enabling arbitrary shell command execution on tool initialization. Fixed in version 1.0.111 (October 2025).
- **CVE-2026-21852** (CVSS 5.3): Information disclosure in project-load flow; a malicious repository could redirect `ANTHROPIC_BASE_URL` to an attacker-controlled endpoint, exfiltrating API keys before the trust prompt appeared. Fixed in version 2.0.65 (January 2026).
- A third vulnerability (CVSS 8.7) allowed user consent bypass via project hooks in `.claude/settings.json`, enabling arbitrary code execution without confirmation. Fixed in version 1.0.87 (September 2025).

**Cross-cutting attack patterns:**
- **Prompt injection via repository context:** Malicious `.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`, or MCP configuration files can inject instructions into AI coding assistants (Pillar Security, 2025; Check Point, 2026)
- **Auto-approved agent tool calls:** Several IDEsaster vulnerabilities exploited auto-approved tool invocations that required no user interaction
- **Configuration file weaponization:** Opening an untrusted repository is now sufficient to trigger RCE or data exfiltration in multiple AI coding tools

---

## AC.1 AI-Assisted Secure-Coding Workflow

Integrate AI tooling into the organization's secure-software-development lifecycle (SSDLC) without weakening existing security gates.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.1.1** | **Verify that** a documented workflow describes when and how AI tools may generate, refactor, or review code. | 1 | D/V | Ad-hoc, ungoverned use of AI coding tools leading to inconsistent security posture; shadow AI usage where developers use unapproved tools without oversight. | Review the organization's SSDLC documentation for explicit AI tool usage policies. Confirm the policy addresses acceptable use cases (generation, refactoring, review) and prohibited contexts (e.g., classified systems). Interview developers to confirm awareness. | Many organizations have no formal policy yet. Even a lightweight "acceptable use" document satisfies this. The policy should name specific approved tools (Copilot, Claude Code, Cursor, etc.) and be versioned. |
| **AC.1.2** | **Verify that** the workflow maps to each SSDLC phase (design, implementation, code review, testing, deployment). | 2 | D | Gaps in coverage where AI-generated code bypasses security gates designed for human-authored code; AI suggestions accepted during design that skip threat modeling. | Examine workflow documentation for explicit mapping of AI tool usage to each SSDLC phase. Confirm that security gates (e.g., design review, code review checklist, test coverage thresholds) apply equally to AI-generated artifacts. | Most current AI coding tool integrations focus on the implementation phase. Coverage of design (e.g., AI-generated architecture) and deployment phases is less mature. Organizations may need to extend existing SSDLC checklists rather than create parallel processes. |
| **AC.1.3** | **Verify that** metrics (e.g., vulnerability density, mean-time-to-detect) are collected on AI-produced code and compared to human-only baselines. | 3 | D/V | Inability to detect whether AI tooling is improving or degrading code security over time; management decisions about AI adoption made without evidence. | Review dashboards or reports that segment security metrics by code origin (AI-generated vs. human-written). Confirm that vulnerability density, defect escape rate, and MTTD are tracked. Compare trends over at least two reporting periods. | Requires reliable attribution of code origin, which is hard in practice. Git metadata, commit tags, or IDE telemetry can approximate this. Research from Stanford (2023) and GitClear (2024) suggests AI-generated code may have higher churn rates, but vulnerability density data is still limited. |

---

## AC.2 AI Tool Qualification & Threat Modeling

Ensure AI coding tools are evaluated for security capabilities, risk, and supply-chain impact before adoption.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.2.1** | **Verify that** a threat model for each AI tool identifies misuse, model-inversion, data leakage, and dependency-chain risks. | 1 | D/V | Unvetted AI tools exfiltrating proprietary source code to third-party servers; model-inversion attacks recovering training data; dependency confusion from AI-suggested packages that do not exist (package hallucination). The IDEsaster disclosure (December 2025) showed 30+ exploitable vulnerabilities across 8 major AI IDEs, making tool-level threat modeling essential. | Review threat model documents for each approved AI coding tool. Confirm coverage of data flow (what code/context leaves the developer's machine), authentication model, API endpoint security, and known attack vectors. ISACA's four-phase framework (2026) provides a structured approach: Discovery, Risk Classification, Layered Controls, Continuous Monitoring. Verify the threat model is signed off by a security reviewer. | Package hallucination is a documented risk: AI models suggest non-existent packages that attackers can then register (Lanyado, Vulcan Cyber, 2023). Threat models should now also cover configuration file weaponization (CVE-2025-59536, CVE-2026-21852) and auto-approved tool calls. SaaS-hosted models (Copilot, ChatGPT) have different data-flow risks than local models (Ollama, llama.cpp). ISACA research indicates discovery sweeps typically reveal 15-20% of tools requiring blocking and 30-40% needing monitoring. |
| **AC.2.2** | **Verify that** tool evaluations include static/dynamic analysis of any local components and assessment of SaaS endpoints (TLS, authentication/authorization, logging). | 2 | D | Compromised IDE extensions acting as backdoors; insecure API connections leaking source code in transit; insufficient logging preventing incident response. | For local components (VS Code extensions, CLI tools): review SAST scan results and dependency audit (npm audit, pip audit). For SaaS endpoints: verify TLS 1.2+ enforcement, OAuth/API key authentication, and confirm that audit logs capture prompt/response metadata. | IDE extensions for Copilot, Cursor, and Continue run with broad filesystem access. Extension marketplaces have had supply-chain attacks (e.g., malicious VS Code extensions). Evaluate extension permissions and update cadence. Amazon Q Developer and Copilot Enterprise offer VPC/private deployment options that reduce SaaS endpoint risk. |
| **AC.2.3** | **Verify that** evaluations follow a recognized framework and are re-performed after major version changes. | 3 | D/V | Stale risk assessments that do not reflect current tool capabilities or vulnerabilities; model updates that change security-relevant behavior silently. | Confirm evaluations reference a recognized framework (NIST AI RMF, ISO 42001, OWASP AI Exchange). Check re-evaluation records triggered by major version changes. Verify that re-evaluation includes regression testing of previously identified risks. | AI coding tools update frequently (Copilot model changes, Cursor version bumps). Defining what constitutes a "major version change" requiring re-evaluation is non-trivial. Consider tying re-evaluation to model changes (e.g., GPT-4 to GPT-4o) rather than minor IDE plugin updates. |

---

## AC.3 Secure Prompt & Context Management

Prevent leakage of secrets, proprietary code, and personal data when constructing prompts or contexts for AI models.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.3.1** | **Verify that** written guidance prohibits sending secrets, credentials, or classified data in prompts. | 1 | D/V | Developers pasting API keys, database passwords, or PII into AI chat interfaces; secrets persisted in AI provider logs and potentially recoverable by third parties. ISACA research (2026) indicates 38% of workers admit sharing confidential information with AI tools. | Review acceptable use policy for explicit prohibition of secrets in prompts. Confirm developers receive training on what constitutes sensitive data in the context of AI prompts. Check for documented examples of prohibited prompt content. | This is a policy control, not a technical one. Developers routinely copy-paste code containing hardcoded credentials. Tools like GitHub Copilot Chat transmit the active editor buffer, which may contain secrets. CVE-2026-21852 demonstrated that even API keys used by the coding tool itself can be exfiltrated via malicious repository configuration. Policy alone is necessary but insufficient without AC.3.2 technical controls. |
| **AC.3.2** | **Verify that** technical controls (client-side redaction, approved context filters) automatically strip sensitive artifacts. | 2 | D | Accidental inclusion of secrets in AI context windows; .env files, private keys, or configuration files with credentials sent as part of repository-wide context. | Verify that client-side filtering is configured (e.g., .copilotignore, .cursorignore, .claudeignore files). Test by placing a known secret pattern in a file and confirming it is excluded from AI context. Review filter rules for completeness. | .copilotignore and .cursorignore support gitignore syntax. Claude Code respects .claudeignore. However, filter effectiveness depends on correct configuration. Many tools send surrounding file context automatically, making it hard to guarantee exclusion. Pre-commit hooks with tools like detect-secrets or gitleaks provide a complementary layer. |
| **AC.3.3** | **Verify that** prompts and responses are tokenized, encrypted in transit and at rest, and retention periods comply with data-classification policy. | 3 | D/V | Long-term persistence of proprietary code in AI provider infrastructure; regulatory violations from retaining PII in prompt logs beyond allowed periods; forensic inability to determine what data was sent to AI providers. | Review AI tool vendor data processing agreements for encryption and retention commitments. Verify TLS in transit. For self-hosted models, audit storage encryption configuration. Confirm retention periods align with organizational data classification (e.g., 30 days for internal, no retention for confidential). | GitHub Copilot Business/Enterprise offers zero data retention. OpenAI API offers opt-out of training data use. Self-hosted models (via Ollama, vLLM) eliminate third-party retention concerns entirely. Tokenization of prompts before logging can enable audit without storing raw proprietary code. |

---

## AC.4 Validation of AI-Generated Code

Detect and remediate vulnerabilities introduced by AI output before the code is merged or deployed.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.4.1** | **Verify that** AI-generated code is always subjected to human code review. | 1 | D/V | Subtly insecure code patterns accepted without scrutiny (e.g., SQL concatenation instead of parameterized queries, weak random number generation, missing authorization checks); over-trust in AI output. | Examine pull request history for evidence that AI-generated code receives human review. Check for branch protection rules requiring at least one human approval. Interview developers about review practices for AI suggestions. | Research consistently shows AI-generated code contains vulnerabilities. A Stanford study (2022) found developers using Copilot produced less secure code. The challenge is reviewer fatigue when large volumes of AI-generated code require review. Smaller, incremental AI-generated changes are easier to review effectively. |
| **AC.4.2** | **Verify that** automated scanners (SAST/IAST/DAST) run on every pull request containing AI-generated code and block merges on critical findings. | 2 | D | Known vulnerability patterns (injection, XSS, path traversal, insecure deserialization) in AI-generated code reaching production; AI models reproducing vulnerable patterns from training data. DryRun Security testing (March 2026) found 87% of AI agent PRs contained vulnerabilities. | Verify CI/CD pipeline includes SAST (Semgrep, CodeQL, SonarQube) and confirm it runs on all PRs. Check that merge is blocked on critical/high severity findings. Review scanner rule sets for coverage of OWASP Top 10. Consider contextual analysis tools (DryRun Security, Semgrep Multimodal) alongside pattern-based SAST, since pattern-based tools caught only 12% of AI coding agent vulnerabilities in controlled testing. | AI-generated code is particularly susceptible to CWE-78 (OS command injection), CWE-89 (SQL injection), and CWE-79 (XSS) based on published benchmarks, but broken access control and business logic flaws now dominate in agent-generated code (March 2026 data). Semgrep Multimodal (launched March 2026) combines LLM reasoning with rule-based analysis to address logic-level flaws like IDOR and authorization bypasses. Multiple scanners remain essential — 78% of vulnerabilities caught by only one tool. |
| **AC.4.3** | **Verify that** differential fuzz testing or property-based tests prove security-critical behaviors (e.g., input validation, authorization logic). | 3 | D/V | Logic errors and edge-case vulnerabilities that pass static analysis but fail under adversarial inputs; AI-generated input validation that appears correct but misses boundary conditions or Unicode edge cases. | Review test suites for property-based tests (Hypothesis for Python, fast-check for JS/TS, QuickCheck for Haskell) or fuzz testing (AFL, libFuzzer, Jazzer). Confirm security-critical code paths (auth, input validation, crypto) have fuzz or property-based coverage. | AI models can generate property-based tests themselves, but these tests must be reviewed for correctness. An AI-generated property test that asserts trivially true properties provides false assurance. Differential fuzzing (comparing AI-generated implementation against a reference implementation) is especially valuable but requires a trusted reference. |

---

## AC.5 Explainability & Traceability of Code Suggestions

Provide auditors and developers with insight into why a suggestion was made and how it evolved.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.5.1** | **Verify that** prompt/response pairs are logged with commit IDs. | 1 | D/V | Inability to trace the origin of vulnerable code back to a specific AI interaction; lack of forensic evidence during incident response; no audit trail for compliance. | Check for logging infrastructure that captures AI interactions. Verify logs include timestamps, prompt text (or hash), response text (or hash), and associated commit SHA. Confirm logs are retained per organizational retention policy. | Claude Code logs interactions locally in JSONL format. Copilot Enterprise provides an audit log API. For other tools, organizations may need to build custom logging via proxy or IDE extension hooks. Logging full prompt/response pairs may conflict with AC.3.3 data minimization goals; hashing or summarizing may be a compromise. |
| **AC.5.2** | **Verify that** developers can surface model citations (training snippets, documentation) supporting a suggestion. | 2 | D | Acceptance of AI-generated code that closely replicates copyrighted or GPL-licensed training data without attribution; use of code patterns from vulnerable or deprecated libraries. | Verify the AI tool provides citation or reference information (e.g., Copilot's code referencing filter, Sourcegraph Cody's context sources). Test by requesting code for a well-known library and checking whether the tool surfaces the source. | GitHub Copilot has a "matching public code" filter that blocks suggestions closely matching public repositories. Claude Code surfaces file context references. True training data attribution (identifying which training examples influenced a suggestion) remains an unsolved research problem. Current tools provide repository-level references at best. |
| **AC.5.3** | **Verify that** explainability reports are stored with design artifacts and referenced in security reviews, satisfying ISO/IEC 42001 traceability principles. | 3 | D/V | Non-compliance with AI governance standards (ISO 42001, EU AI Act); inability to demonstrate due diligence in AI-assisted development during audits or litigation. | Review design documentation repositories for explainability reports. Confirm security review records reference AI tool usage and traceability data. Verify alignment with ISO/IEC 42001 clause 6.1.2 (AI risk assessment) and Annex A controls. | ISO 42001 certification is still emerging, with few organizations certified as of 2025. Explainability reports for coding tools are not well-standardized. Organizations may need to define their own format covering: tool used, model version, prompt summary, review outcome, and risk assessment. |

---

## AC.6 Continuous Feedback & Model Fine-Tuning

Improve model security performance over time while preventing negative drift.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.6.1** | **Verify that** developers can flag insecure or non-compliant suggestions, and that flags are tracked. | 1 | D/V | Repeated generation of known-insecure patterns with no mechanism for correction; developer frustration leading to workarounds that bypass security controls. | Confirm a feedback mechanism exists (e.g., thumbs-down in Copilot, feedback forms, issue tracker labels). Verify flags are aggregated and reviewed periodically. Check that high-severity flags trigger investigation. | GitHub Copilot and Cursor both support inline feedback. For CLI tools like Claude Code, feedback may need to be captured via separate channels (Slack, issue trackers). The key is that feedback is actionable, not just collected. Track resolution rates and time-to-fix for flagged patterns. |
| **AC.6.2** | **Verify that** aggregated feedback informs periodic fine-tuning or retrieval-augmented generation with vetted secure-coding corpora (e.g., OWASP Cheat Sheets). | 2 | D | AI models persistently suggesting insecure patterns because feedback is not incorporated; missed opportunity to improve model output using organization-specific secure coding standards. | Review evidence that feedback data is used in model improvement cycles (fine-tuning logs, RAG corpus updates). For RAG-based systems, verify the retrieval corpus includes vetted sources (OWASP, CWE, organization-specific secure coding guides). Confirm update cadence (at least quarterly). The [OpenSSF Security-Focused Guide for AI Code Assistant Instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) provides a baseline for secure instruction files. | Most organizations cannot fine-tune commercial models (Copilot, Claude) directly. RAG is the practical alternative: maintain a curated knowledge base of secure coding patterns that the AI tool references. Cursor supports `.cursorrules`, Claude Code supports `CLAUDE.md`, Copilot supports `.github/copilot-instructions.md`. The OpenSSF guide (2025) recommends Recursive Criticism and Improvement (RCI) — instructing the AI to review and improve its own output iteratively — as a practical security enhancement. These instruction files serve as lightweight RAG mechanisms but must themselves be protected against prompt injection (see IDEsaster CVEs). |
| **AC.6.3** | **Verify that** a closed-loop evaluation harness runs regression tests after every fine-tune; security metrics must meet or exceed prior baselines before deployment. | 3 | D/V | Model fine-tuning introducing regressions where previously secure patterns become insecure; degraded security performance going undetected after model updates. | Review the evaluation harness design. Confirm it includes a benchmark suite of security-relevant code generation tasks (e.g., generate parameterized SQL, generate CSRF-protected forms). Verify pass/fail criteria and evidence that deployment is gated on results. | Benchmarks like CyberSecEval (Meta), SecurityEval, and SVEN provide standardized security evaluation for code-generating models. Organizations using self-hosted fine-tuned models should run these benchmarks before and after fine-tuning. For commercial tool users, this control is largely dependent on the vendor's internal processes. |

---

## AC.7 AI-Generated Infrastructure & Pipeline Artifacts

Ensure that AI-generated infrastructure-as-code (IaC), CI/CD workflows, deployment configurations, and security policy artifacts are subject to appropriate validation and governance controls.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.7.1** | **Verify that** AI-generated infrastructure-as-code, CI/CD workflows, and security policy artifacts are clearly identified and tracked. | 1 | D/V | AI-generated Terraform, CloudFormation, or Kubernetes manifests deployed without awareness of their origin; inability to prioritize security review for machine-generated infrastructure changes. | Check version control for labeling conventions (commit message tags, PR labels, file headers) that identify AI-generated IaC. Verify an inventory or registry tracks which infrastructure artifacts were AI-generated. | Convention-based tracking (e.g., commit messages containing "[ai-generated]" or "Co-Authored-By: Claude") is the most practical approach. Automated enforcement via pre-commit hooks or CI checks can validate that AI-generated artifacts are properly labeled. |
| **AC.7.2** | **Verify that** AI-generated infrastructure and pipeline configurations require appropriate review and approval prior to execution. | 2 | D | AI-generated IaC with overly permissive IAM policies, open security groups, unencrypted storage, or disabled logging reaching production without scrutiny. | Verify branch protection or pipeline gates require human approval for IaC changes. Confirm review checklists include IaC-specific security checks (least privilege, encryption, network segmentation). Check that Terraform plan / CloudFormation changeset review is mandatory. | AI models frequently generate IaC with insecure defaults: public S3 buckets, wildcard IAM policies, security groups open to 0.0.0.0/0. Tools like Checkov, tfsec, and KICS should run in CI to catch these. Review should be performed by someone with infrastructure security expertise, not just application developers. |
| **AC.7.3** | **Verify that** AI-generated infrastructure and workflow changes are subject to security validation, configuration checks, and policy enforcement equivalent to or stricter than application code. | 3 | D/V | IaC treated as second-class artifact with weaker security gates than application code; AI-generated GitHub Actions workflows with excessive permissions or unsafe third-party action references. | Verify that IaC scanning tools (Checkov, tfsec, KICS, Bridgecrew) run in CI with blocking policies. Confirm policy-as-code frameworks (OPA/Rego, Sentinel) enforce organizational security baselines. Verify coverage parity with application code scanning. | CI/CD workflow files (GitHub Actions, GitLab CI) are a particularly high-value target because they execute with elevated permissions. AI-generated workflow files should be reviewed for: pinned action versions (not @main), minimal GITHUB_TOKEN permissions, no secrets in logs, and restricted workflow triggers. |

---

## AC.8 Autonomous Agent Change Control Constraints

Ensure that autonomous AI agents involved in code or configuration generation are subject to appropriate separation of duties and cannot independently approve or promote their own changes.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.8.1** | **Verify that** autonomous agents cannot approve, merge, sign, or deploy artifacts that they have generated. | 1 | D/V | AI agent autonomously generating and deploying malicious or vulnerable code without human oversight; compromised agent credentials used to push unauthorized changes to production. | Review repository permissions and CI/CD configurations to confirm AI agent accounts lack merge/approve/deploy permissions. Test by attempting agent self-approval in a staging environment. Verify branch protection rules exclude agent identities from approvers. | This is critical for tools like Claude Code (with GitHub integration), Devin, SWE-agent, and similar autonomous coding agents. GitHub branch protection rules can enforce this by requiring review from specific teams that exclude bot accounts. The key principle is that no single identity (human or AI) should both generate and approve a change. |
| **AC.8.2** | **Verify that** AI systems operate with scoped identities and permissions that prevent self-promotion of generated artifacts across environments. | 2 | D | Privilege escalation where an AI agent with write access to a development environment also has access to staging or production; lateral movement from compromised agent credentials. | Audit AI agent service accounts for least-privilege permissions. Verify separate credentials per environment (dev/staging/prod). Confirm no shared secrets or cross-environment access. Review IAM policies for AI agent roles. | AI agents should use dedicated service accounts (not developer personal tokens). GitHub Apps with scoped repository permissions are preferred over personal access tokens. Environment-specific credentials prevent a compromised dev agent from reaching production. Consider short-lived tokens (GitHub App installation tokens expire after 1 hour). |
| **AC.8.3** | **Verify that** separation of duties is enforced between artifact generation, review, approval, and deployment stages for AI-generated changes. | 3 | D/V | Complete bypass of change management when an AI agent controls the full pipeline from code generation through deployment; audit failures due to lack of independent verification at each stage. | Map the end-to-end change pipeline and verify distinct identities at each stage (generation, review, approval, deployment). Confirm no single identity participates in more than one stage. Review audit logs for evidence of multi-party involvement. | Full four-way separation of duties is aspirational for many organizations. A practical minimum is two-way separation: AI generates, human approves. Three-way separation (AI generates, human reviews, different human/system deploys) is more realistic for mature organizations. Enforce via CODEOWNERS, required reviewers, and deployment approval gates. |

---

## AC.9 AI Provenance-Aware Deployment Controls

Ensure that deployment and promotion pipelines incorporate provenance-aware validation for AI-generated artifacts.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **AC.9.1** | **Verify that** AI-generated artifacts include provenance metadata identifying the generating system, generation context, and associated traceability records. | 1 | D/V | Deployed artifacts with unknown origin making incident response and root cause analysis difficult; inability to determine whether a vulnerability was introduced by human or AI, hindering targeted remediation. | Inspect AI-generated artifacts for provenance metadata (e.g., commit message annotations, file headers, SLSA provenance attestations). Verify metadata includes: generating tool name/version, model identifier, timestamp, and link to prompt/response logs. | SLSA (Supply-chain Levels for Software Artifacts) provides a framework for provenance attestations. For AI-generated code, provenance should minimally include: tool (e.g., "Claude Code 1.x"), model (e.g., "claude-sonnet-4-20250514"), and a reference to the interaction log. Git trailers ("Co-Authored-By:", "Generated-By:") are a lightweight implementation. |
| **AC.9.2** | **Verify that** deployment pipelines validate the presence and integrity of provenance metadata for AI-generated artifacts prior to promotion. | 2 | D | Artifacts with missing or tampered provenance metadata reaching production; circumvention of provenance requirements by stripping metadata before deployment. | Review CI/CD pipeline configuration for provenance validation steps. Test by submitting an artifact without provenance metadata and confirming it is rejected. Verify integrity checks (e.g., signed provenance attestations, hash verification). | Sigstore/cosign can sign and verify provenance attestations. In-toto provides a framework for supply chain integrity verification. For most organizations, a CI check that validates commit message format (requiring AI attribution tags) is a practical starting point before implementing full cryptographic attestation. |
| **AC.9.3** | **Verify that** artifacts lacking required provenance information, or originating from untrusted generation environments, can be rejected during deployment. | 3 | D/V | Artifacts generated by unauthorized or compromised AI tools entering the deployment pipeline; shadow AI usage where developers use unapproved tools and strip provenance to avoid detection. | Verify deployment pipeline includes a rejection mechanism for missing provenance. Test with artifacts from an untrusted source. Confirm rejected artifacts generate alerts. Review the approved tool allowlist and confirm it is enforced. | Maintaining an allowlist of trusted generation environments requires ongoing governance. "Untrusted" should be defined clearly: is it any tool not on the approved list, or specifically tools without data retention agreements? Consider a graduated approach: warn on missing provenance at Level 1, block at Level 2, require cryptographic attestation at Level 3. |

---

## Threat Landscape

- AI-generated code introducing subtle vulnerabilities (SQL injection, XSS, insecure defaults) -- 25.1% overall vulnerability rate (2026 data)
- Prompt injection through repository context (malicious CLAUDE.md, .cursorrules files) -- demonstrated as practical attack vector by Pillar Security (2025)
- Over-reliance on AI-generated code without human review -- the "trust gap" is the primary risk amplifier; developers review AI output less carefully
- Leaked secrets or PII in prompts sent to cloud-hosted coding assistants
- AI-generated infrastructure-as-code with insecure defaults (overly permissive IAM, public S3, open security groups)
- Package hallucination: AI models suggest non-existent packages that attackers register (Lanyado, Vulcan Cyber, 2023)
- Autonomous agents with excessive permissions bypassing change control
- Supply-chain attacks via compromised IDE extensions
- Direct exploitation of AI coding tools: CVE-2025-62453 (improper output validation), CVE-2025-53773 (config file manipulation leading to RCE)
- Jailbreak attacks on coding assistants: "affirmation jailbreak" bypasses safety filters with simple agreeing words
- SSRF (CWE-918) as dominant AI-generated vulnerability: most frequent single weakness in 2026 benchmarks, surpassing traditional injection categories
- AI code review tool limitations: Copilot Code Review failed to flag OWASP Top 10 in controlled testing; cannot reason about cross-function data flow
- **[New]** IDEsaster disclosure (December 2025): 30+ vulnerabilities across 8 AI IDEs (Cursor, Windsurf, Copilot, Zed, Roo Code, Kiro, JetBrains Junie, Claude Code); 24 CVEs assigned. Attack patterns include prompt injection, auto-approved tool calls, and configuration file weaponization.
- **[New]** Claude Code CVEs (February 2026): CVE-2025-59536 (CVSS 8.7, RCE via MCP config) and CVE-2026-21852 (CVSS 5.3, API key exfiltration via malicious repo). Demonstrated that opening an untrusted repository is sufficient for exploitation.
- **[New]** AI coding agents fail at access control: DryRun Security testing (March 2026) found 87% of PRs from Claude Code, Codex, and Gemini contained vulnerabilities — broken access control was universal, and pattern-based SAST caught only 12% of issues.
- **[New]** Shadow AI risk quantified: ISACA framework (2026) reports 38% of workers admit sharing confidential information with AI tools; discovery sweeps typically find 15-20% of tools need blocking.

## Tooling & Implementation

- **Coding assistants:** GitHub Copilot, Cursor, Claude Code, Amazon Q Developer, Windsurf
- **AI code review:** GitHub Copilot Code Review (GA Apr 2025; CodeQL integration Oct 2025), CodeRabbit (2M+ repos), Aegis (AI-code-specialized), Qodo (formerly CodiumAI), DryRun Security (contextual code review for AI agents)
- **Code scanning:** Semgrep (including Multimodal, launched March 2026), CodeQL, Snyk Code, SonarQube -- note: 78% of AI-generated vulnerabilities caught by only one tool, so run multiple scanners. Semgrep Multimodal combines LLM reasoning with rule-based SAST for business logic flaws.
- **IaC scanning:** Checkov, tfsec, KICS, Bridgecrew
- **Provenance tracking:** Git metadata, AI attribution in commit messages, SLSA attestations, Sigstore/cosign
- **Sandbox testing:** CI/CD gates for AI-generated code, pre-commit hooks
- **Secret detection:** detect-secrets, gitleaks, TruffleHog
- **Property/fuzz testing:** Hypothesis, fast-check, AFL, libFuzzer
- **Policy-as-code:** OPA/Rego, HashiCorp Sentinel
- **Security benchmarks for code LLMs:** CyberSecEval (Meta), SecurityEval, SVEN, [AppSec Santa AI Code Security Benchmark](https://appsecsanta.com/api-ai-security/ai-code-security)
- **Secure instruction guides:** [OpenSSF Security-Focused Guide for AI Code Assistant Instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) — covers secure defaults, supply chain safety, language-specific guidance
- **Assessment frameworks:** [ISACA AI Coding Assistant Vulnerability Framework (2026)](https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2026/securing-the-ai-frontier-a-practical-framework-for-assessing-ai-coding-assistant-vulnerabilities) — four-phase discovery, classification, controls, monitoring
- **Standards:** NIST SP 800-218A (Secure Software Development for Generative AI); NIST AI Agent Standards Initiative (February 2026); ISO 42001

## Open Research Questions

- [x] What percentage of AI-generated code contains security vulnerabilities in practice? **Answered (2026):** ~25% overall; 19-29% depending on model; comparable per-line to human code but amplified by reduced review scrutiny.
- [ ] How should organizations track and audit AI-generated vs. human-written code? Git metadata and commit tags remain the most practical approach, but no standard has emerged.
- [ ] What constitutes adequate review of AI-generated infrastructure-as-code?
- [ ] How do autonomous coding agents change the threat model for SDLC security? Prompt injection via repository context files is now a demonstrated attack vector.
- [x] How effective are current SAST tools at detecting AI-specific vulnerability patterns? **Partially answered (2026):** 78% of vulnerabilities caught by only one tool; no single scanner is sufficient. SSRF (CWE-918) is now the top AI-generated vulnerability but is poorly covered by many SAST tools.
- [ ] What is the optimal human review depth for high-volume AI-generated code? Copilot generates ~46% of code where enabled; Copilot Code Review failed to flag OWASP Top 10 in testing, so human review remains essential.
- [ ] How should AI coding tool CVEs (e.g., CVE-2025-62453, CVE-2025-53773, CVE-2026-21852) be tracked and managed differently from traditional software CVEs? The IDEsaster disclosure (24 CVEs across 8 IDEs) suggests the attack surface is broader than initially expected.
- [x] Can AI code review tools be made to reason about cross-function and cross-file data flow? **Partially answered (March 2026):** Semgrep Multimodal combines LLM reasoning with rule-based analysis, claiming 8x more true positives for logic flaws. DryRun Security's contextual analysis caught 88% of AI agent vulnerabilities vs. 12% for pattern-based SAST. Early results are promising but independent validation is pending.
- [ ] What is the security impact of prompt injection attacks via repository context files (.cursorrules, CLAUDE.md) at scale? Check Point's Claude Code research (February 2026) demonstrated practical exploitation; IDEsaster showed this is not tool-specific.
- [ ] **[New]** How should organizations implement the NIST AI Agent Standards Initiative (February 2026) for AI coding agents that operate autonomously in CI/CD pipelines?
- [ ] **[New]** What is the optimal combination of pattern-based SAST and contextual/LLM-powered analysis for AI-generated code? Early data (12% vs. 88% detection rates) suggests fundamental rethinking of scanner strategy is needed.

---

## References (2024-2026 Research)

- [Security Weaknesses of Copilot-Generated Code (ACM TOSEM, 2025)](https://dl.acm.org/doi/10.1145/3716848) -- empirical study of vulnerability rates in Copilot output
- [Copilot Code Review: Can AI Spot Security Flaws? (arXiv, 2025)](https://arxiv.org/html/2509.13650v1) -- WebGoat testing showing failure to detect OWASP Top 10
- [AI-Generated Code Security: Risks & Testing (AppSec Santa, 2026)](https://appsecsanta.com/api-ai-security/ai-code-security) -- 534-sample benchmark across 6 LLMs
- [Vulnerability in Copilot and Cursor: Weaponizing Code Agents (Pillar Security, 2025)](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)
- [GitHub Copilot RCE via Prompt Injection (CybersecurityNews, 2025)](https://cybersecuritynews.com/github-copilot-rce-vulnerability/)
- [OWASP Gen AI Incident Round-up, Jan-Feb 2025](https://genai.owasp.org/2025/03/06/owasp-gen-ai-incident-exploit-round-up-jan-feb-2025/)
- [GitHub Copilot Security Risks: Enterprise Guide (MintMCP)](https://www.mintmcp.com/blog/github-copilot-security-risks)
- [AI Code Security Explained (Wiz Academy)](https://www.wiz.io/academy/application-security/ai-code-security)
- [Endor Labs: AI Security Code Review (2025)](https://www.endorlabs.com/learn/introducing-ai-security-code-review)
- [AI Coding Agents Keep Repeating Decade-Old Security Mistakes (Help Net Security, March 2026)](https://www.helpnetsecurity.com/2026/03/13/claude-code-openai-codex-google-gemini-ai-coding-agent-security/) -- DryRun Security testing of Claude Code, Codex, Gemini; 87% vulnerability rate in PRs
- [Claude Code Flaws Allow RCE and API Key Exfiltration (Check Point Research, February 2026)](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) -- CVE-2025-59536 and CVE-2026-21852
- [IDEsaster: 30+ Flaws in AI Coding Tools (The Hacker News, December 2025)](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html) -- 24 CVEs across 8 AI IDEs
- [Semgrep Multimodal: AI Reasoning Meets Rule-Based Analysis (Help Net Security, March 2026)](https://www.helpnetsecurity.com/2026/03/20/semgrep-multimodal-code-security/) -- combines LLM reasoning with deterministic SAST
- [OpenSSF Security-Focused Guide for AI Code Assistant Instructions (2025)](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) -- secure defaults for AI coding assistant configuration
- [ISACA: Securing the AI Frontier — Framework for AI Coding Assistant Vulnerabilities (2026)](https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2026/securing-the-ai-frontier-a-practical-framework-for-assessing-ai-coding-assistant-vulnerabilities) -- four-phase assessment framework
- [NIST AI Agent Standards Initiative (February 2026)](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) -- standards for secure, interoperable AI agents
- [Top 10 AI SAST Tools for 2026 (DryRun Security)](https://www.dryrun.security/blog/top-ai-sast-tools-2026) -- comparative analysis of AI-aware SAST tools

## Community Notes

_Discussion about AI-assisted coding security practices._

---
