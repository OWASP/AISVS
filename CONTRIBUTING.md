# Contributing to AISVS

Thank you for your interest in the OWASP Artificial Intelligence Security Verification Standard. This guide explains how to get involved and where your contributions will have the most impact.

---

## About the Project

The [Open Worldwide Application Security Project (OWASP)](https://owasp.org/) is a nonprofit organization that works to improve the security of software. The AISVS is one of its flagship verification standards.

The **Artificial Intelligence Security Verification Standard (AISVS)** provides developers, architects, and security professionals with a structured framework to evaluate and verify the security of AI-driven applications. Modeled after existing OWASP standards (such as the [ASVS](https://owasp.org/www-project-application-security-verification-standard/) for web applications), AISVS defines testable requirements across 14 chapters covering model behavior, supply chain integrity, agentic orchestration, privacy, adversarial robustness, human oversight, and more.

---

## Current Status

> **Requirements freeze: April 30, 2026.** After this date, no new requirements will be accepted for v1.0. Editorial fixes, clarifications, and wording improvements will continue to be accepted.
>
> **Target release: June 2026** at the OWASP Global AppSec conference in Vienna.

We are actively refining the control set to ensure every requirement is independently testable, clearly scoped, and useful to both implementers and auditors. Once the freeze lands, the control text is locked for the 1.0 release.

If you have security expertise in any of the 14 chapters and want to leave a mark on the first stable release of AISVS, now is the time.

---

## How to Contribute

### Before the Requirements Freeze (highest impact)

The most valuable thing you can do right now is review the existing controls and ask:

| Question | Why it matters |
| --- | --- |
| Is this requirement **independently testable**? | An auditor should be able to verify it with a single, specific piece of evidence. |
| Is the **scope clear**? | A control should not be confused with a control in a different chapter. |
| Is anything **missing**? | Are there attack surfaces, failure modes, or real-world AI security concerns that are not yet covered? |
| Is anything **duplicated**? | Two controls in the same or different chapters should not say the same thing. |

If you find issues, please **open a [GitHub issue](https://github.com/OWASP/AISVS/issues) first** before submitting a pull request. A well-written issue describing the problem is just as valuable as a PR.

### Other Ways to Contribute

- **Review open PRs** -- Help catch scope overlap, wording ambiguity, or controls that are hard to test in practice.
- **Add missing controls** -- If you know of a concrete, testable requirement that belongs in the standard and is not there yet, propose it before the April 30 freeze.
- **Fix compound requirements** -- Controls that bundle two distinct testable concerns into one should be split. See our existing split PRs for examples of the expected format.
- **Improve references** -- Each chapter should reference the best available standards, frameworks, and research for its topic area.

### After the Freeze

Once requirements are locked, we still welcome:

- Editorial and formatting fixes
- Clarifications to existing requirement language
- Improvements to appendices, glossary, and references
- Tooling, automation, and CI improvements

---

## Workflow

1. **Open an issue** at <https://github.com/OWASP/AISVS/issues> describing the problem or suggestion.
2. **Discuss** -- a project lead will respond and may refine the scope with you.
3. **Submit a pull request** at <https://github.com/OWASP/AISVS/pulls> if asked, referencing the issue number.

Please keep PRs focused on a single concern. Small, well-scoped changes are easier to review and merge quickly.

---

## Translations

We are looking for help with translations after v1.0 is released. If you are interested in translating AISVS into another language, please open an issue to let us know.

---

## License

All contributions to this project fall under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)**. By submitting a pull request, you agree that your contribution will be licensed under the same terms.
