# Contributing

## Introduction

### What is [OWASP](https://owasp.org/)?

The Open Worldwide Application Security Project (OWASP) is a nonprofit organization that works to improve the security of software. It has many programs to work towards this goal. One of those programs is the AISVS.

### What is the [AISVS](https://github.com/OWASP/www-project-artificial-intelligence-security-verification-standard-aisvs-docs)?

The OWASP Artificial Intelligence Security Verification Standard (AISVS) focuses on providing developers, architects, and security professionals with a structured framework to evaluate and verify the security and ethical considerations of AI-driven applications. Modeled after existing OWASP standards (such as the ASVS for web applications), AISVS defines categories of requirements across 14 chapters covering areas including model behavior, supply chain integrity, agentic orchestration, privacy, adversarial robustness, and human oversight.

### What is the Current Status of AISVS development?

**We are in the final stretch before the v1.0 requirement freeze.**

This is the most important moment to contribute. We are actively refining the control set to ensure every requirement is independently testable, clearly scoped, and useful to both implementers and auditors. Once the freeze lands, the control text is locked for the 1.0 release.

If you have security expertise in any of the 14 chapters and want to leave a mark on the first stable release of AISVS, now is the time.

## How can I help?

### High-priority contributions for the 1.0 release

The most valuable thing you can do right now is review the existing controls and ask:

- Is this requirement independently testable? Can a single auditor verify it with a single, specific piece of evidence?
- Is the scope clear? Could this control be confused with a control in a different chapter?
- Is anything missing? Are there attack surfaces, failure modes, or real-world AI security concerns that are not covered?
- Is anything duplicated? Do two controls in the same or different chapters say the same thing?

If you find issues, please open a GitHub issue first before submitting a pull request. Good issues describing the problem are just as valuable as PRs.

### Other ways to contribute

- **Review open PRs**: Help us catch scope overlap, wording ambiguity, or controls that are hard to test in practice.
- **Add missing controls**: If you know of a concrete, testable requirement that belongs in the standard and is not there yet, propose it.
- **Fix compound requirements**: Controls that bundle two distinct testable concerns into one should be split. See our existing split PRs for examples of the expected format.
- **Improve references**: Each chapter should reference the best available standards, frameworks, and research for its topic area.

Please first log ideas, issues, or questions here: <https://github.com/OWASP/AISVS/issues>.

We may also ask you to open a pull request, <https://github.com/OWASP/AISVS/pulls>, based on the discussion in the issue.

### Translations

We are looking for help with translations after v1.0 is released!
