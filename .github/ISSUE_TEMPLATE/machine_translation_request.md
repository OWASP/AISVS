---
name: Machine translation request
about: Request machine translation to a specific language afer forming a proofread team
title: 'MT Request:'
labels: 'machine_translation'
assignees: ''

---

**Language Code** (to be filled by requester)
One language code to run a machine translation such as "ja-JP"

**Proofread Team** (to be filled by requester)
Team Lead: (full name, ID on owasp.slack.com, gitthub ID (, linkedin (optional)
          e.g., John Doe, @johndoe, @JohnDoe_Github
Team Members: (full name, ID on owasp.slack.com(, linkedin or github ID (optional)

Notes:
- Team Lead github ID is required.
- 2 to 4 additional members for neutrality.
- When the English original is ready for localization, the project owner will announce localization readiness.
- With "mt" request, merge the MT'ed markdown and custom JSON files to language directory such as 1.0/blddoc/ja-JP.
- Then, the requester can retrieve the MT'ed files and start proofreading.
- When proofread is completed, the team lead can submit a pull request of the localized markdown files and custom JSON files to the language directory.
- When accepted, they will be merged to the main branch.
- When the project is ready for publish, W.I.P. watermark will be removed and PDF will be merged to main.
