import json
from pathlib import Path
from collections import defaultdict

import pandas as pd
from jsonschema import validate, ValidationError


# ---------- Utility functions ----------

def load_schema(schema_path: Path) -> dict:
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def write_json(obj: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def required_columns_from_schema(schema: dict) -> set:
    # Required JSON properties ≠ required Excel columns
    # We validate Excel columns manually where needed
    return set(schema.get("required", []))


def extract_index_fields(schema: dict) -> dict:
    """
    Extract all x-index annotated fields, regardless of enum / oneOf.
    Returns: { field_name: x-index metadata }
    """
    fields = {}
    for field, spec in schema.get("properties", {}).items():
        if "x-index" in spec:
            fields[field] = spec["x-index"]
    return fields


def extract_indexable_values(spec: dict) -> list:
    """
    Extract indexable values from enum or oneOf(const).
    """
    values = []

    if "enum" in spec:
        values = spec["enum"]

    elif "oneOf" in spec:
        for entry in spec["oneOf"]:
            if "const" in entry:
                values.append(entry["const"])

    return values


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

    # ----- Prepare evidence by reqruirement index -----
    evidences_by_requirement = defaultdict(list)
    
    # ----- Prepare index metadata -----
    index_fields = extract_index_fields(req_schema)

    indexes = {
        meta["id"]: {
            "_meta": meta,
            "data": defaultdict(list)
        }
        for meta in index_fields.values()
    }

    # ----- Load Excel -----
    xls = pd.ExcelFile(excel_path)

    req_df = xls.parse("Requirements").fillna("")
    ev_df = xls.parse("Evidences").fillna("")

    # ---------- Process evidences ----------
    #---Remove for now since we only have evidence examples 
    #---evidence_summary_by_requirement = defaultdict(list)
    evidence_index = []

    for _, row in ev_df.iterrows():
        evidence = {
            key: row.get(key, "")
            for key in ev_schema["properties"].keys()
        }

        if evidence.get("Related Requirements Summary") == "":
            evidence["Related Requirements Summary"] = []
        
        evidence["Related Requirement ID(s)"] = [evidence.get("Related Requirement ID(s)", "")] if evidence.get("Related Requirement ID(s)", "") != "" else []

        try:
            validate(evidence, ev_schema)
        except ValidationError as e:
            raise ValueError(
                f"Evidence {evidence.get('Evidence ID')} failed schema validation:\n{e}"
            )

        evidence_id = evidence["Evidence ID"]

        related_reqs = evidence.get("Related Requirement ID(s)", [])

        evidence_index.append({
            "Evidence ID": evidence_id,
            "Title": evidence.get("Title", "")
        })

        write_json(
            evidence,
            output_dir / "evidences" / f"{evidence_id}.json"
        )

        for r_id in related_reqs:
            evidences_by_requirement[r_id].append({
                "Evidence ID": evidence_id,
                "Title": evidence.get("Title", ""),
                "Description": evidence.get("Description", ""),
                "File": f"../evidences/{evidence_id}.json"
            })

    write_json(
        {"evidences": evidence_index},
        output_dir / "evidences" / "index.json"
    )

    write_json(
    {
        "by-requirement": evidences_by_requirement
    },
    output_dir / "indexes" / "evidences-by-requirement.json"
)

    # ---------- Process requirements ----------
    requirement_index = []

    for _, row in req_df.iterrows():
        requirement = {
            key: row.get(key, "")
            for key in req_schema["properties"].keys()
            if key not in ("Framework Mappings", "Evidences")
        }

        r_id = requirement.get("Requirement ID")
        if not r_id:
            raise ValueError("Requirement missing Requirement ID")

        # ----- Build Framework Mappings -----
        framework_mappings = [
            {
                "frameworkId": "SATRE",
                "value": row.get("SATRE", "")
            },
            {
                "frameworkId": "ENTRUST Blueprint",
                "value": row.get("ENTRUST Blueprint", "")
            }
        ]
        requirement["Framework Mappings"] = framework_mappings

        # ----- Attach evidences -----
        #---Remove for now since we only have evidence examples
        #---requirement["Evidences"] = evidence_summary_by_requirement.get(r_id, [])

        # ----- Populate indexes -----
        summary = {
            "Requirement ID": r_id,
            "Title": requirement.get("Title", "")
        }

        for field, meta in index_fields.items():
            value = requirement.get(field, "")
            if value == "":
                continue
            indexes[meta["id"]]["data"][value].append(summary)

        if requirement.get("Related Requirements", "") == "":
            requirement["Related Requirements"] = []
        if requirement.get("Priority", "") == "":
            requirement["Priority"] = 0
        
        requirement["Priority"] = round(requirement["Priority"])
    
        try:
            validate(requirement, req_schema)
        except ValidationError as e:
            raise ValueError(
                f"Requirement {r_id} failed schema validation:\n{e}"
            )

        write_json(
            requirement,
            output_dir / "requirements" / f"{r_id}.json"
        )

        requirement_index.append(summary)

    write_json(
        {"requirements": requirement_index},
        output_dir / "requirements" / "index.json"
    )

    # ---------- Write indexes + discovery ----------
    indexes_dir = output_dir / "indexes"
    indexes_dir.mkdir(parents=True, exist_ok=True)

    discovery = []

    for index_id, index_obj in indexes.items():
        filename = f"{index_id}.json"

        write_json(
            {
                "_meta": index_obj["_meta"],
                "data": index_obj["data"]
            },
            indexes_dir / filename
        )

        entry = dict(index_obj["_meta"])
        entry["file"] = filename
        discovery.append(entry)

    discovery.append({
        "id": "evidences-by-requirement",
        "title": "Evidences grouped by Requirement",
        "type": "evidence",
        "file": "evidences-by-requirement.json",
        "order": 99
    })

    discovery.sort(key=lambda x: x.get("order", 999))

    write_json(
        {"indexes": discovery},
        indexes_dir / "index.json"
    )

    print("JSON repository successfully generated")


# ---------- Entry point ----------

if __name__ == "__main__":
    main(
        Path("M8requirements.xlsx"),
        Path("requirement.schema.json"),
        Path("evidence.schema.json"),
        Path("./")
    )
