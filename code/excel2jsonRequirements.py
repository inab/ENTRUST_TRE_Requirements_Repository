import json
from pathlib import Path
from collections import defaultdict

import pandas as pd
from jsonschema import validate, ValidationError


# ---------- Utility functions ----------

def load_schema(schema_path: Path) -> dict:
    """Load a JSON schema from disk."""
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def required_columns_from_schema(schema: dict) -> set:
    """Extract required column names from a JSON schema."""
    return set(schema.get("required", []))


def validate_required_columns(df: pd.DataFrame, required: set, sheet_name: str):
    """Ensure the Excel sheet contains all required schema fields."""
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Sheet '{sheet_name}' is missing required columns: {missing}"
        )


def write_json(obj: dict, path: Path):
    """Write a JSON object to disk, creating directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


# ---------- Main logic ----------

def main(
    excel_path: Path,
    requirement_schema_path: Path,
    evidence_schema_path: Path,
    output_dir: Path
):
    # ----- Load schemas -----
    req_schema = load_schema(requirement_schema_path)
    ev_schema = load_schema(evidence_schema_path)

    # ----- Load Excel -----
    xls = pd.ExcelFile(excel_path)

    if "Requirements" not in xls.sheet_names:
        raise ValueError("Missing 'Requirements' sheet")

    if "Evidences" not in xls.sheet_names:
        raise ValueError("Missing 'Evidences' sheet")

    req_df = xls.parse("Requirements").fillna("")
    ev_df = xls.parse("Evidences").fillna("")

    # ----- Validate required columns -----
    validate_required_columns(
        req_df, required_columns_from_schema(req_schema), "Requirements"
    )
    validate_required_columns(
        ev_df, required_columns_from_schema(ev_schema), "Evidences"
    )

    # ---------- Process evidences first ----------
    evidence_summary_by_requirement = defaultdict(list)

    for _, row in ev_df.iterrows():
        evidence = {
            key: row[key]
            for key in ev_schema["properties"].keys()
            if key in row
        }

        try:
            validate(evidence, ev_schema)
        except ValidationError as e:
            raise ValueError(
                f"Evidence {evidence.get('E#')} failed schema validation:\n{e}"
            )

        r_id = evidence.get("R#")
        if not r_id:
            raise ValueError(
                f"Evidence {evidence.get('E#')} is missing required R# reference"
            )

        # Write full evidence JSON
        output_path = output_dir / "evidences" / f"{evidence['E#']}.json"
        write_json(evidence, output_path)

        # Prepare summary for embedding
        summary = {
            "E#": evidence["E#"],
            "Evidence Artifact Example": evidence.get("Evidence Artifact Example", ""),
            "File": str(Path("../evidences") / f"{evidence['E#']}.json")
        }
        evidence_summary_by_requirement[r_id].append(summary)

        

    # ---------- Process requirements ----------
    for _, row in req_df.iterrows():
        requirement = {
            key: row[key]
            for key in req_schema["properties"].keys()
            if key in row
        }

        r_id = requirement.get("R#")
        if not r_id:
            raise ValueError("Requirement missing R# identifier")

        # Attach evidences (empty list if none)
        requirement["Evidence"] = evidence_summary_by_requirement.get(r_id, [])

        try:
            validate(requirement, req_schema)
        except ValidationError as e:
            raise ValueError(
                f"Requirement {r_id} failed schema validation:\n{e}"
            )

        output_path = output_dir / "requirements" / f"{r_id}.json"
        write_json(requirement, output_path)

    print("✔ JSON repository successfully generated")


# ---------- Entry point ----------

    if len(sys.argv) != 5:
        print(
            "Usage:\n"
            "  python excel_to_json_repo.py "
            "input.xlsx requirement.schema.json evidence.schema.json output_dir/"
        )
        sys.exit(1)

    main(
        Path(sys.argv[1]),
        Path(sys.argv[2]),
        Path(sys.argv[3]),
        Path(sys.argv[4])

    )
