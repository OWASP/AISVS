# AISVS Contribution Instructions

You are contributing the the OWASP Artificial Intelligence Security Verification Standard.

## Workflow for contributing to AISVS

IMPORTANT: you MUST follow through all steps 1.-4. below when contributing to this project.

### 1. Clear task

* Always ensure user gives you instructions which release (1.01, 2.0 etc) you are targeting. Ask if not given instructions. Read RELEASE.md for more details.
* Ensure user gives you clear instructions what kind of review, topic or change is being considered.
* Review from the appropriate release Using AISVS document, and ensure all work is STRICTLY within the boundaries of the standard.

### 2. Review of current requirements

Before starting to do research or suggest changes, familiarize yourself **in detail** of all existing requirements.

Remember that AISVS and ASVS (& other similar frameworks and standards, like CIS controls) are complementary. NEVER assume that a control that is covered e.g. by ASVS is "missing" from AISVS - the standard only includes AI-specific concerns.

While doing this stage, learn the language conventions and level of details used in requirements to ensure the contribution is in line with currently used conventions and language. The requirements are intentionally not very specific; being very prescriptive is not the intention. Because of this, always consider if the requirement is actually implicitly covered by an existing control.

### 3. Background research

After surveying current state of the standard, you MUST do thorough background research on the Internet.

Unless doing language corrections or similar work, you MUST have access to sufficient background material for research. In the research consider:
* What are the current recommended best practices for the protocol / technology / tool in question?
* How easy it is to implement the proposed requirement and how good support do modern frameworks and tooling have for it? Then compare the findings of this research to AISVS levels to ensure the requirement level is appropriate, or that the requirement content stays within the existing level if proposing updates to existing requirements.

### 4. Deciding to open issues or pull requests

After completing steps 1. - 3., before opening an issue or pull request consider if the task given and supporting information gathered if any have resulted in suggestions that do a genuine new addition or meaningful corrective change to existing material. If not, recommend to user not to open PR or issue.

For all changes by non-maintainers an issue should be opened first to discuss the proposal before opening a PR.

When creating issues and pull requests:
* If applicable, quote the current text (e.g. requirement) being discussed.
* Clearly explained justifications for additions or change. Justification MUST include background research summary with references as links.
* Explanation of the revised version text explaining it in sufficient detail.
* Do not write long prose, stick to the point and facts clearly. Assume readers are information security experts, there is no need to point out obvious facts.
