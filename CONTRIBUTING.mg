# Contributing to the EOSC-ENTRUST Requirements Repository

Thank you for contributing to the EOSC-ENTRUST Requirements Repository.

This repository is governed by the EOSC-ENTRUST Requirements Management Process (RMP) and implements controlled versioning and change management for TRE requirements.


## 1. Who Can Contribute

Contributions are welcome from:
- TRE providers and operators
- EOSC-ENTRUST partners
- Technical, legal, and governance experts
- Contributors proposing requirements or improvements

All contributions are subject to review and approval.


## 2. Contribution Types

You may contribute by:
- Proposing new requirements
- Requesting changes to existing requirements
- Improving evidence examples
- Fixing errors or inconsistencies
- Improving documentation or tooling

## 3. Change Request Workflow

All changes to baselined requirements MUST follow this process:

1. Open a **Change Request issue** using the provided template.
2. Clearly identify:
   - Affected requirement(s)
   - Change type (clarification, correction, scope adjustment, etc.)
   - Rationale and expected impact
3. Participate in review discussions as needed.
4. Await approval decision.

No requirement changes will be merged without an approved Change Request.

## 4. Implementing Approved Changes

Approved changes are implemented via a pull request that:
- References the approved Change Request
- Updates structured artefacts in `requirements/` or `evidences_examples/`
- Passes schema validation checks
- Updates `CHANGELOG.md` if applicable

## 5. Review and Approval

Pull requests are reviewed by:
- Requirements Reviewers (technical and domain review)
- Requirements Maintainers (consistency and structure)
- Change Control Authority (for significant changes)

Approval requirements depend on the impact and scope of the change.


## 6. Versioning Rules

- Baseline releases are aligned with ENTRUST project milestones.
- Minor and patch versions reflect approved post-baseline changes.
- Contributors MUST NOT manually bump versions unless instructed.

Version identifiers are assigned as part of the release process.

## 7. Validation and Quality Checks

Contributors SHALL:
- Ensure JSON artefacts conform to the schemas in `schemas/`
- Use provided scripts in `code/` for validation
- Avoid breaking identifier consistency or traceability links

## 8. Code of Conduct

All contributors are expected to interact respectfully and professionally.
Harassment, discrimination, or disruptive behaviour will not be tolerated.


## 9. License and Reuse

By contributing, you agree that your contributions will be released under the repository’s license.


## 10. Questions and Support

For questions related to governance or requirements interpretation, contact the EOSC-ENTRUST Change Control Authority.
For technical issues, open an issue in the repository.
