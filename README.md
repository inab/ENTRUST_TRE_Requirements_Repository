# EOSC-ENTRUST Requirements Repository

This repository hosts the authoritative, version-controlled catalogue of requirements defined within the EOSC-ENTRUST project for Trusted Research Environments (TREs).

The repository supports the EOSC-ENTRUST Requirements Management Process (RMP) by enabling structured storage, controlled evolution, traceability, and public accessibility of requirements and supporting artefacts.


## Purpose and Scope

The purpose of this repository is to:
- Maintain a controlled baseline of validated EOSC-ENTRUST TRE requirements
- Support consistent interpretation, adoption, and assessment of requirements
- Enable traceability to evidence, mappings, and external frameworks
- Provide a transparent and reusable reference for stakeholders

The repository represents a **living artefact** that evolves through formally governed change control.


## Repository Structure

The repository is organised as follows:

```text
requirements/           Structured requirement artefacts (one file per requirement)
evidences_examples/     Structured examples of evidence artefacts
schemas/                JSON schemas for requirements and evidence validation
mappings/               Traceability matrices and mapping templates
code/                   Scripts supporting import, validation, and publication
docs/                    Material used to generate a human-readable catalogue
CHANGELOG.md            Record of approved requirement changes
CONTRIBUTING.md         Contribution and change governance guidelines
CODE_OF_CONDUCT.md      Behavioural expectations for contributors
NOTICE.md               Project attribution and funding acknowledgement
LICENSE                 Terms for reuse of repository contents
```
## Access to the Requirements Catalogue

To support transparency and adoption requirements are made available through a human-readable catalogue autoamtically derived from  structured requirement artefacts
  (i.e.`requirements/` entries).

*Requirements Catalogue:* [Requirements Catalogue]()

Details on catalogue generation are maintained in the doc/ directory.


## Requirements Lifecycle and Governance

Requirements in this repository follow the EOSC-ENTRUST lifecycle:
1. Stakeholder Elicitation and analysis
2. Verifiability assessment
3. Stakeholder validation
4. Baseline registration under version control
5. Controlled change and maintenance

Changes to baselined requirements SHALL follow the formal Change Control process defined in the RMP. No modification is applied without an approved Change Request

## Versioning Policy

The repository follows a milestone-anchored semantic versioning scheme:
`project-milestone>.<minor>.<patch>`
Examples:
- `milestone8.0.0` – Initial baseline aligned with Milestone 8
- `milestone8.1.0` – Approved clarifications and corrections
- `milestone8.1.1` – Editorial or metadata-only fixes

Version identifiers are assigned as part of the release process in the `version` attribute of the requirement formal definition and recorded in CHANGELOG.md.

## Contributing
Contributions are welcome and encouraged. All contributions are subject to review and approval under the EOSC-ENTRUST Change Control process. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting:

- New requirements
- Change requests
- Documentation improvements
- Tooling enhancements

## Contact and Governance

This repository is governed under the EOSC-ENTRUST Requirements Management Process. For governance questions, clarification requests, or disputes related to requirements, please contact the designated EOSC-ENTRUST Change Control Authority via [eosc-entrust-coordination@elixir-europe.org](eosc-entrust-coordination@elixir-europe.org).
