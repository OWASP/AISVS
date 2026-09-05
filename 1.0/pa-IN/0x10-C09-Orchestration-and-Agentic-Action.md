<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md -->
<!-- Translator: GeeksikhSecurity -->

# C9 Orchestration & Agentic Security
# C9 ਆਰਕੈਸਟ੍ਰੇਸ਼ਨ (orchestration) ਅਤੇ ਏਜੰਟ-ਆਧਾਰਿਤ ਸੁਰੱਖਿਆ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses ensuring autonomous and multi-agent systems execute only authorized, intended, and bounded actions.

ਇਹ ਅਧਿਆਇ ਇਹ ਯਕੀਨੀ ਬਣਾਉਣ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਕਿ ਖ਼ੁਦਮੁਖ਼ਤਾਰ (autonomous) ਅਤੇ ਬਹੁ-ਏਜੰਟ ਸਿਸਟਮ ਸਿਰਫ਼ ਅਧਿਕਾਰਤ, ਇੱਛਤ, ਅਤੇ ਸੀਮਾਬੱਧ ਕਾਰਵਾਈਆਂ ਹੀ ਚਲਾਉਂਦੇ ਹਨ।

---

## C9.1 Execution Budgets, Loop Control, and Circuit Breakers
## C9.1 ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਬਜਟ, ਲੂਪ ਨਿਯੰਤਰਣ, ਅਤੇ ਸਰਕਟ ਬ੍ਰੇਕਰ

Runtime expansion (recursion, concurrency, cost) must be bounded, with safe halting on runaway behavior.

ਰਨਟਾਈਮ ਫੈਲਾਅ (ਰੀਕਰਸ਼ਨ, ਸਮਕਾਲੀਨਤਾ, ਲਾਗਤ) ਦਾ ਸੀਮਾਬੱਧ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਬੇਕਾਬੂ ਵਿਵਹਾਰ ਹੋਣ 'ਤੇ ਸਲਾਮਤ (safe) ਢੰਗ ਨਾਲ ਰੁਕਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **9.1.1** | **Verify that** per-tool quotas and timeouts (e.g., CPU, memory, disk, egress, and execution time) are enforced. | 1 |
| **9.1.2** | **Verify that** per-execution budgets (e.g., max recursion depth, token use, and monetary spend) are configured and enforced by the runtime. | 1 |
| **9.1.3** | **Verify that** a swarm-level kill-switch exists that can halt all active agent instances. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **9.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪ੍ਰਤੀ-ਟੂਲ ਕੋਟੇ ਅਤੇ ਟਾਈਮਆਊਟ (ਜਿਵੇਂ, CPU, ਮੈਮੋਰੀ, ਡਿਸਕ, ਬਾਹਰ ਜਾਣ ਵਾਲਾ ਟਰੈਫ਼ਿਕ (egress), ਅਤੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਸਮਾਂ) ਲਾਗੂ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **9.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪ੍ਰਤੀ-ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਬਜਟ (ਜਿਵੇਂ, ਵੱਧ ਤੋਂ ਵੱਧ ਰੀਕਰਸ਼ਨ ਡੂੰਘਾਈ, ਟੋਕਨ ਵਰਤੋਂ, ਅਤੇ ਵਿੱਤੀ ਖ਼ਰਚ) ਰਨਟਾਈਮ ਦੁਆਰਾ ਸੰਰਚਿਤ ਅਤੇ ਲਾਗੂ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **9.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇੱਕ ਸਵਾਰਮ-ਪੱਧਰੀ (swarm-level) kill-switch (ਤੁਰੰਤ-ਬੰਦ ਸਵਿੱਚ) ਮੌਜੂਦ ਹੈ ਜੋ ਸਾਰੇ ਸਰਗਰਮ ਏਜੰਟ ਇੰਸਟਾਂਸਾਂ ਨੂੰ ਰੋਕ ਸਕਦਾ ਹੈ। | 2 |

---

## C9.2 High-Impact Action Approval and Irreversibility Controls
## C9.2 ਉੱਚ-ਪ੍ਰਭਾਵ ਕਾਰਵਾਈ ਮਨਜ਼ੂਰੀ ਅਤੇ ਗ਼ੈਰ-ਉਲਟਾਉਣਯੋਗਤਾ ਨਿਯੰਤਰਣ

Privileged, high-impact, or hard-to-reverse agent actions must require trusted approval checkpoints.

ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ, ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀਆਂ, ਜਾਂ ਔਖਿਆਈ ਨਾਲ ਉਲਟਾਈਆਂ ਜਾਣ ਵਾਲੀਆਂ ਏਜੰਟ ਕਾਰਵਾਈਆਂ ਲਈ ਭਰੋਸੇਯੋਗ ਮਨਜ਼ੂਰੀ ਚੈੱਕਪੁਆਇੰਟਾਂ ਦੀ ਲੋੜ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **9.2.1** | **Verify that** the agent runtime blocks execution of privileged, high-impact, or irreversible actions until explicit human approval is received and verified. | 1 |
| **9.2.2** | **Verify that** approval requests display canonicalized and complete action parameters, such as diffs, commands, recipients, amounts, resources, and scopes, without truncation or unsafe transformation. | 2 |
| **9.2.3** | **Verify that** each high-impact action has a trusted reversibility classification, such as read-only, reversible, externally reversible, or irreversible. | 2 |
| **9.2.4** | **Verify that** the agent runtime enforces reversibility classifications by blocking, requiring approval, or restricting actions based on their impact and ability to be reversed. | 2 |
| **9.2.5** | **Verify that** any self-modification capability (e.g., prompt rewriting, tool-list changes, parameter updates) is restricted by enforceable boundaries. | 2 |
| **9.2.6** | **Verify that** agentic systems include an AI-augmented review of planned high-risk actions before execution that adds to, and does not replace, the deterministic policy gate. | 2 |
| **9.2.7** | **Verify that** the AI-augmented review mechanism is protected against manipulation by adversarial inputs, and cannot be overridden or bypassed through prompt injection. | 2 |
| **9.2.8** | **Verify that** approvals are cryptographically bound to action parameters, requester identity, execution context, and a unique single-use nonce. | 3 |
| **9.2.9** | **Verify that** cryptographic key material or credentials used to issue approvals are isolated from the agent runtime. | 3 |
| **9.2.10** | **Verify that** approval gates for multi-step or multi-agent action chains enforce the highest-impact reversibility classification present anywhere in the chain. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **9.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਰਨਟਾਈਮ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ, ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀਆਂ, ਜਾਂ ਗ਼ੈਰ-ਉਲਟਾਉਣਯੋਗ ਕਾਰਵਾਈਆਂ ਦੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਨੂੰ ਉਦੋਂ ਤੱਕ ਰੋਕਦਾ ਹੈ ਜਦੋਂ ਤੱਕ ਸਪੱਸ਼ਟ ਮਨੁੱਖੀ ਮਨਜ਼ੂਰੀ ਪ੍ਰਾਪਤ ਅਤੇ ਤਸਦੀਕ ਨਹੀਂ ਹੋ ਜਾਂਦੀ। | 1 |
| **9.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਨਜ਼ੂਰੀ ਬੇਨਤੀਆਂ ਕਾਰਵਾਈ ਦੇ ਕੈਨੋਨੀਕਲਾਈਜ਼ ਕੀਤੇ ਅਤੇ ਸੰਪੂਰਨ ਪੈਰਾਮੀਟਰ — ਜਿਵੇਂ diff, ਕਮਾਂਡਾਂ, ਪ੍ਰਾਪਤਕਰਤਾ, ਰਕਮਾਂ, ਸਰੋਤ, ਅਤੇ ਸਕੋਪ — ਬਿਨਾਂ ਕਿਸੇ ਕਟੌਤੀ (truncation) ਜਾਂ ਗ਼ੈਰ-ਸਲਾਮਤ ਤਬਦੀਲੀ ਦੇ ਦਿਖਾਉਂਦੀਆਂ ਹਨ। | 2 |
| **9.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀ ਕਾਰਵਾਈ ਦਾ ਇੱਕ ਭਰੋਸੇਯੋਗ ਉਲਟਾਉਣਯੋਗਤਾ ਵਰਗੀਕਰਨ (reversibility classification) ਹੈ, ਜਿਵੇਂ ਸਿਰਫ਼-ਪੜ੍ਹਨਯੋਗ, ਉਲਟਾਉਣਯੋਗ, ਬਾਹਰੀ ਤੌਰ 'ਤੇ ਉਲਟਾਉਣਯੋਗ, ਜਾਂ ਗ਼ੈਰ-ਉਲਟਾਉਣਯੋਗ। | 2 |
| **9.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਰਨਟਾਈਮ ਕਾਰਵਾਈਆਂ ਦੇ ਪ੍ਰਭਾਵ ਅਤੇ ਉਹਨਾਂ ਦੇ ਉਲਟਾਏ ਜਾ ਸਕਣ ਦੀ ਸਮਰੱਥਾ ਦੇ ਆਧਾਰ 'ਤੇ ਉਹਨਾਂ ਨੂੰ ਰੋਕ ਕੇ, ਮਨਜ਼ੂਰੀ ਦੀ ਲੋੜ ਪਾ ਕੇ, ਜਾਂ ਸੀਮਤ ਕਰਕੇ ਉਲਟਾਉਣਯੋਗਤਾ ਵਰਗੀਕਰਨਾਂ ਨੂੰ ਲਾਗੂ ਕਰਦਾ ਹੈ। | 2 |
| **9.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕੋਈ ਵੀ ਸਵੈ-ਸੋਧ ਸਮਰੱਥਾ (ਜਿਵੇਂ, prompt ਨੂੰ ਮੁੜ-ਲਿਖਣਾ, ਟੂਲ-ਸੂਚੀ ਤਬਦੀਲੀਆਂ, ਪੈਰਾਮੀਟਰ ਅੱਪਡੇਟ) ਲਾਗੂਕਰਨਯੋਗ ਸੀਮਾਵਾਂ ਦੁਆਰਾ ਸੀਮਤ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **9.2.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ-ਆਧਾਰਿਤ ਸਿਸਟਮਾਂ ਵਿੱਚ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਤੋਂ ਪਹਿਲਾਂ ਯੋਜਨਾਬੱਧ ਉੱਚ-ਜੋਖਮ ਕਾਰਵਾਈਆਂ ਦੀ ਇੱਕ AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸਮੀਖਿਆ (AI-augmented review) ਸ਼ਾਮਲ ਹੁੰਦੀ ਹੈ, ਜੋ ਨਿਸ਼ਚਿਤ (deterministic) ਨੀਤੀ ਗੇਟ ਵਿੱਚ ਵਾਧਾ ਕਰਦੀ ਹੈ, ਉਸ ਦੀ ਥਾਂ ਨਹੀਂ ਲੈਂਦੀ। | 2 |
| **9.2.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸਮੀਖਿਆ ਵਿਧੀ ਵਿਰੋਧੀ ਇਨਪੁੱਟਾਂ ਦੁਆਰਾ ਹੇਰਾਫੇਰੀ ਤੋਂ ਸੁਰੱਖਿਅਤ ਹੈ, ਅਤੇ prompt ਇੰਜੈਕਸ਼ਨ ਰਾਹੀਂ ਇਸ ਨੂੰ ਓਵਰਰਾਈਡ ਜਾਂ ਬਾਈਪਾਸ ਨਹੀਂ ਕੀਤਾ ਜਾ ਸਕਦਾ। | 2 |
| **9.2.8** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਨਜ਼ੂਰੀਆਂ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਕਾਰਵਾਈ ਦੇ ਪੈਰਾਮੀਟਰਾਂ, ਬੇਨਤੀਕਰਤਾ ਦੀ ਪਛਾਣ, ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਸੰਦਰਭ, ਅਤੇ ਇੱਕ ਵਿਲੱਖਣ ਇੱਕ-ਵਾਰੀ-ਵਰਤੋਂ ਵਾਲੇ ਨੌਂਸ (nonce) ਨਾਲ ਬੰਨ੍ਹੀਆਂ ਜਾਂਦੀਆਂ ਹਨ। | 3 |
| **9.2.9** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਨਜ਼ੂਰੀਆਂ ਜਾਰੀ ਕਰਨ ਲਈ ਵਰਤੀ ਜਾਂਦੀ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਕੁੰਜੀ ਸਮੱਗਰੀ ਜਾਂ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਏਜੰਟ ਰਨਟਾਈਮ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਹਨ। | 3 |
| **9.2.10** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਬਹੁ-ਪੜਾਵੀ ਜਾਂ ਬਹੁ-ਏਜੰਟ ਕਾਰਵਾਈ ਲੜੀਆਂ ਲਈ ਮਨਜ਼ੂਰੀ ਗੇਟ ਲੜੀ ਵਿੱਚ ਕਿਤੇ ਵੀ ਮੌਜੂਦ ਸਭ ਤੋਂ ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲਾ ਉਲਟਾਉਣਯੋਗਤਾ ਵਰਗੀਕਰਨ ਲਾਗੂ ਕਰਦੇ ਹਨ। | 3 |

---

## C9.3 Component Isolation and Tool Authorization
## C9.3 ਕੰਪੋਨੈਂਟ ਅਲੱਗ-ਥਲੱਗਤਾ ਅਤੇ ਟੂਲ ਅਧਿਕਾਰੀਕਰਨ

Tool and plugin execution, loading, and outputs must be constrained to prevent unauthorized system access and unsafe side effects.

ਅਣਅਧਿਕਾਰਤ ਸਿਸਟਮ ਪਹੁੰਚ ਅਤੇ ਗ਼ੈਰ-ਸਲਾਮਤ ਸਹਿ-ਪ੍ਰਭਾਵਾਂ (side effects) ਨੂੰ ਰੋਕਣ ਲਈ ਟੂਲ ਅਤੇ ਪਲੱਗਇਨ ਦੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ, ਲੋਡਿੰਗ, ਅਤੇ ਆਊਟਪੁੱਟ ਨੂੰ ਸੀਮਿਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **9.3.1** | **Verify that** each tool/plugin executes in a least-privilege sandbox or is otherwise isolated from model operations. | 1 |
| **9.3.2** | **Verify that** tool outputs are validated against schemas. | 1 |
| **9.3.3** | **Verify that** tool manifests declare required privileges, resource limits, and output validation requirements. | 2 |
| **9.3.4** | **Verify that** the runtime enforces the privileges, resource limits, and output-validation requirements declared in tool manifests. | 2 |
| **9.3.5** | **Verify that** components processing untrusted data are isolated from tool-calling capabilities, ensuring that compromised data processing cannot trigger unauthorized tool invocations. | 2 |
| **9.3.6** | **Verify that** there is architectural separation between processing of untrusted tool outputs and agent operations. | 2 |
| **9.3.7** | **Verify that** external resources named in model output are verified against an approved allow-list or registry before the agent installs or invokes them. | 2 |
| **9.3.8** | **Verify that** policy violations trigger automated tool containment. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **9.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਟੂਲ/ਪਲੱਗਇਨ ਘੱਟੋ-ਘੱਟ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ (least-privilege) ਸੈਂਡਬਾਕਸ ਵਿੱਚ ਚੱਲਦਾ ਹੈ ਜਾਂ ਕਿਸੇ ਹੋਰ ਢੰਗ ਨਾਲ ਮਾਡਲ ਕਾਰਵਾਈਆਂ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **9.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਟੂਲ ਆਊਟਪੁੱਟ ਨੂੰ ਸਕੀਮਾਵਾਂ ਦੇ ਵਿਰੁੱਧ ਪ੍ਰਮਾਣਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **9.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਟੂਲ ਮੈਨੀਫ਼ੈਸਟ (tool manifests) ਲੋੜੀਂਦੇ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰਾਂ, ਸਰੋਤ ਸੀਮਾਵਾਂ, ਅਤੇ ਆਊਟਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ ਲੋੜਾਂ ਦੀ ਘੋਸ਼ਣਾ ਕਰਦੇ ਹਨ। | 2 |
| **9.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਰਨਟਾਈਮ ਟੂਲ ਮੈਨੀਫ਼ੈਸਟਾਂ ਵਿੱਚ ਘੋਸ਼ਿਤ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰਾਂ, ਸਰੋਤ ਸੀਮਾਵਾਂ, ਅਤੇ ਆਊਟਪੁੱਟ-ਪ੍ਰਮਾਣਿਕਤਾ ਲੋੜਾਂ ਨੂੰ ਲਾਗੂ ਕਰਦਾ ਹੈ। | 2 |
| **9.3.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਡਾਟਾ ਦੀ ਪ੍ਰਕਿਰਿਆ ਕਰਨ ਵਾਲੇ ਕੰਪੋਨੈਂਟ ਟੂਲ-ਕਾਲ ਕਰਨ ਦੀਆਂ ਸਮਰੱਥਾਵਾਂ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਹਨ, ਜਿਸ ਨਾਲ ਇਹ ਯਕੀਨੀ ਬਣਦਾ ਹੈ ਕਿ ਸਮਝੌਤਾ ਹੋਈ ਡਾਟਾ ਪ੍ਰਕਿਰਿਆ ਅਣਅਧਿਕਾਰਤ ਟੂਲ ਸੱਦੇ (tool invocations) ਸ਼ੁਰੂ ਨਹੀਂ ਕਰ ਸਕਦੀ। | 2 |
| **9.3.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਟੂਲ ਆਊਟਪੁੱਟ ਦੀ ਪ੍ਰਕਿਰਿਆ ਅਤੇ ਏਜੰਟ ਕਾਰਵਾਈਆਂ ਵਿਚਕਾਰ ਆਰਕੀਟੈਕਚਰਲ ਵਿਭਾਜਨ ਮੌਜੂਦ ਹੈ। | 2 |
| **9.3.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਆਊਟਪੁੱਟ ਵਿੱਚ ਨਾਮਜ਼ਦ ਬਾਹਰੀ ਸਰੋਤਾਂ ਦੀ, ਏਜੰਟ ਦੁਆਰਾ ਉਹਨਾਂ ਨੂੰ ਸਥਾਪਤ ਕਰਨ ਜਾਂ ਸੱਦਣ ਤੋਂ ਪਹਿਲਾਂ, ਇੱਕ ਪ੍ਰਵਾਨਿਤ allow-list ਜਾਂ ਰਜਿਸਟਰੀ ਦੇ ਵਿਰੁੱਧ ਤਸਦੀਕ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **9.3.8** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਨੀਤੀ ਉਲੰਘਣਾਵਾਂ ਸਵੈਚਾਲਿਤ ਟੂਲ ਘੇਰਾਬੰਦੀ (tool containment) ਸ਼ੁਰੂ ਕਰਦੀਆਂ ਹਨ। | 3 |

---

## C9.4 Agent and Orchestrator Identity
## C9.4 ਏਜੰਟ ਅਤੇ ਆਰਕੈਸਟ੍ਰੇਟਰ (orchestrator) ਪਛਾਣ

Every action must be attributable and every mutation detectable.

ਹਰ ਕਾਰਵਾਈ ਦਾ ਸਰੋਤ-ਨਿਰਧਾਰਨਯੋਗ ਹੋਣਾ ਅਤੇ ਹਰ ਪਰਿਵਰਤਨ (mutation) ਦਾ ਪਤਾ ਲਗਾਉਣਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **9.4.1** | **Verify that** each agent instance has a unique cryptographic identity and authenticates as a first-class principal to downstream systems. | 2 |
| **9.4.2** | **Verify that** agent-initiated actions are cryptographically bound to each step of the execution chain for non-repudiation. | 2 |
| **9.4.3** | **Verify that** agent identity credentials rotate on a defined schedule. | 3 |
| **9.4.4** | **Verify that** agent state persisted between invocations is integrity-protected. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **9.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਏਜੰਟ ਇੰਸਟਾਂਸ ਦੀ ਇੱਕ ਵਿਲੱਖਣ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਪਛਾਣ ਹੈ ਅਤੇ ਉਹ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਲਈ ਇੱਕ ਪਹਿਲੇ-ਦਰਜੇ ਦੀ ਪਛਾਣ-ਇਕਾਈ (first-class principal) ਵਜੋਂ ਪ੍ਰਮਾਣੀਕਰਨ ਕਰਦਾ ਹੈ। | 2 |
| **9.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਦੁਆਰਾ ਸ਼ੁਰੂ ਕੀਤੀਆਂ ਕਾਰਵਾਈਆਂ ਗ਼ੈਰ-ਇਨਕਾਰਯੋਗਤਾ (non-repudiation) ਲਈ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਲੜੀ ਦੇ ਹਰ ਪੜਾਅ ਨਾਲ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਬੰਨ੍ਹੀਆਂ ਜਾਂਦੀਆਂ ਹਨ। | 2 |
| **9.4.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਪਛਾਣ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਸਮਾਂ-ਸਾਰਣੀ ਅਨੁਸਾਰ ਬਦਲੇ (rotate) ਜਾਂਦੇ ਹਨ। | 3 |
| **9.4.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸੱਦਿਆਂ ਵਿਚਕਾਰ ਸਥਾਈ ਰੱਖੀ ਗਈ ਏਜੰਟ ਸਥਿਤੀ ਅਖੰਡਤਾ-ਸੁਰੱਖਿਅਤ ਹੈ। | 3 |

---

## C9.5 Agent Authorization, Delegation, and Continuous Enforcement
## C9.5 ਏਜੰਟ ਅਧਿਕਾਰੀਕਰਨ, ਸੌਂਪਣੀ, ਅਤੇ ਨਿਰੰਤਰ ਲਾਗੂਕਰਨ

Every action must be authorized at execution time and constrained by scope.

ਹਰ ਕਾਰਵਾਈ ਦਾ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਦੇ ਸਮੇਂ ਅਧਿਕਾਰੀਕਰਨ ਹੋਣਾ ਅਤੇ ਸਕੋਪ ਦੁਆਰਾ ਸੀਮਿਤ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **9.5.1** | **Verify that** agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, and which parameter values it may supply. | 2 |
| **9.5.2** | **Verify that** when an agent acts on a user's behalf, the runtime propagates an integrity-protected, scope-limited token that carries the user's authorization context and is enforced at every downstream call. | 2 |
| **9.5.3** | **Verify that** all access control decisions are enforced by application logic or a policy engine, never by the AI model itself. | 2 |
| **9.5.4** | **Verify that** secrets and credentials required by an agent at runtime are not exposed within the model's observable context, including the context window, system prompts, or tool call parameters. | 2 |
| **9.5.5** | **Verify that** inter-agent task delegation is restricted by an explicit authorization policy. | 2 |
| **9.5.6** | **Verify that** long-running agent sessions re-evaluate current backend authorization policy on every privileged action. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **9.5.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਕਾਰਵਾਈਆਂ ਦਾ ਰਨਟਾਈਮ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੀਆਂ ਬਾਰੀਕ-ਪੱਧਰੀ ਨੀਤੀਆਂ ਦੇ ਵਿਰੁੱਧ ਅਧਿਕਾਰੀਕਰਨ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਜੋ ਇਹ ਸੀਮਤ ਕਰਦੀਆਂ ਹਨ ਕਿ ਇੱਕ ਏਜੰਟ ਕਿਹੜੇ ਟੂਲ ਸੱਦ ਸਕਦਾ ਹੈ, ਅਤੇ ਕਿਹੜੇ ਪੈਰਾਮੀਟਰ ਮੁੱਲ ਦੇ ਸਕਦਾ ਹੈ। | 2 |
| **9.5.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਦੋਂ ਕੋਈ ਏਜੰਟ ਕਿਸੇ ਉਪਭੋਗਤਾ ਵੱਲੋਂ ਕਾਰਵਾਈ ਕਰਦਾ ਹੈ, ਤਾਂ ਰਨਟਾਈਮ ਇੱਕ ਅਖੰਡਤਾ-ਸੁਰੱਖਿਅਤ, ਸਕੋਪ-ਸੀਮਿਤ ਟੋਕਨ ਅੱਗੇ ਸੰਚਾਰਿਤ ਕਰਦਾ ਹੈ ਜੋ ਉਪਭੋਗਤਾ ਦਾ ਅਧਿਕਾਰੀਕਰਨ ਸੰਦਰਭ ਲੈ ਕੇ ਜਾਂਦਾ ਹੈ ਅਤੇ ਹਰ ਡਾਊਨਸਟ੍ਰੀਮ ਕਾਲ 'ਤੇ ਲਾਗੂ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **9.5.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਰੇ ਪਹੁੰਚ ਕੰਟਰੋਲ ਫ਼ੈਸਲੇ ਐਪਲੀਕੇਸ਼ਨ ਤਰਕ ਜਾਂ ਇੱਕ ਨੀਤੀ ਇੰਜਣ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਕਦੇ ਵੀ AI ਮਾਡਲ ਦੁਆਰਾ ਖ਼ੁਦ ਨਹੀਂ। | 2 |
| **9.5.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਰਨਟਾਈਮ 'ਤੇ ਕਿਸੇ ਏਜੰਟ ਨੂੰ ਲੋੜੀਂਦੇ ਗੁਪਤ ਭੇਦ ਅਤੇ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਮਾਡਲ ਦੇ ਦੇਖਣਯੋਗ ਸੰਦਰਭ ਵਿੱਚ ਜ਼ਾਹਰ ਨਹੀਂ ਹੁੰਦੇ, ਜਿਸ ਵਿੱਚ ਸੰਦਰਭ ਵਿੰਡੋ, system prompt, ਜਾਂ ਟੂਲ ਕਾਲ ਪੈਰਾਮੀਟਰ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **9.5.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟਾਂ ਵਿਚਕਾਰ ਕਾਰਜ ਸੌਂਪਣੀ (task delegation) ਇੱਕ ਸਪੱਸ਼ਟ ਅਧਿਕਾਰੀਕਰਨ ਨੀਤੀ ਦੁਆਰਾ ਸੀਮਤ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **9.5.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਲੰਬੇ ਸਮੇਂ ਤੱਕ ਚੱਲਣ ਵਾਲੇ ਏਜੰਟ ਸੈਸ਼ਨ ਹਰ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ ਕਾਰਵਾਈ 'ਤੇ ਮੌਜੂਦਾ ਬੈਕਐਂਡ ਅਧਿਕਾਰੀਕਰਨ ਨੀਤੀ ਦਾ ਮੁੜ-ਮੁਲਾਂਕਣ ਕਰਦੇ ਹਨ। | 3 |

---

## C9.6 Shutdown and Graceful Degradation
## C9.6 ਬੰਦ ਕਰਨਾ ਅਤੇ ਸੁਚੱਜੀ ਗਿਰਾਵਟ

Shutdown and graceful degradation paths must remain under human control, with mechanisms that stay reliable and are exercised over time.

ਬੰਦ ਕਰਨ ਅਤੇ ਸੁਚੱਜੀ ਗਿਰਾਵਟ (graceful degradation) ਦੇ ਰਾਹਾਂ ਦਾ ਮਨੁੱਖੀ ਨਿਯੰਤਰਣ ਹੇਠ ਰਹਿਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਇਹਨਾਂ ਦੀਆਂ ਵਿਧੀਆਂ ਦਾ ਭਰੋਸੇਯੋਗ ਬਣੇ ਰਹਿਣਾ ਅਤੇ ਸਮੇਂ ਦੇ ਨਾਲ-ਨਾਲ ਪਰਖੇ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **9.6.1** | **Verify that** a manual kill-switch mechanism exists to immediately halt AI model inference and outputs. | 1 |
| **9.6.2** | **Verify that** when a human-approval gate is not satisfied within the defined approval time, the system blocks the pending action. | 2 |
| **9.6.3** | **Verify that** kill-switch commands are implemented through an out-of-band channel that is isolated from the agent runtime. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **9.6.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਮਾਡਲ ਦੇ ਇਨਫ਼ਰੈਂਸ ਅਤੇ ਆਊਟਪੁੱਟ ਨੂੰ ਤੁਰੰਤ ਰੋਕਣ ਲਈ ਇੱਕ ਹੱਥੀਂ ਚਲਾਈ ਜਾਣ ਵਾਲੀ kill-switch ਵਿਧੀ ਮੌਜੂਦ ਹੈ। | 1 |
| **9.6.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਦੋਂ ਪਰਿਭਾਸ਼ਿਤ ਮਨਜ਼ੂਰੀ ਸਮੇਂ ਦੇ ਅੰਦਰ ਮਨੁੱਖੀ-ਮਨਜ਼ੂਰੀ ਗੇਟ ਪੂਰਾ ਨਹੀਂ ਹੁੰਦਾ, ਤਾਂ ਸਿਸਟਮ ਬਕਾਇਆ ਕਾਰਵਾਈ ਨੂੰ ਰੋਕ ਦਿੰਦਾ ਹੈ। | 2 |
| **9.6.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** kill-switch ਕਮਾਂਡਾਂ ਇੱਕ ਆਊਟ-ਆਫ਼-ਬੈਂਡ (out-of-band) ਚੈਨਲ ਰਾਹੀਂ ਲਾਗੂ ਕੀਤੀਆਂ ਜਾਂਦੀਆਂ ਹਨ ਜੋ ਏਜੰਟ ਰਨਟਾਈਮ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਹੈ। | 3 |

---

## References
## ਹਵਾਲੇ

* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [NIST AI 100-1: AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [Regulation (EU) 2024/1689 (EU AI Act), Article 14: Human Oversight](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
