#!/usr/bin/env python3
"""Parse the compact blocker DSL and emit blocker_registry.json + generation_memory.json.

DSL grammar (line oriented, '#' starts a comment, blank lines ignored):

    @meta
    round: <int>
    requested: mp=<int> ar=<int> cr=<int>
    halt: <reason>                         # optional, inferred when absent

    @candidate <candidate_id>
    source: baseline_extraction | golden_patch_reverse | test_patch_mining
    type: missing_parameter | ambiguous_requirement | contradictory_requirement
    mode: extraction | injection
    area: <area_token>
    selected: true | false
    rationale: <text>
    evidence: <text or baseline_only>
    reject: <reason or none>

    @blocker <id>
    type: <type>
    mode: <mode>
    area: <area_token>
    status: valid | repaired_valid
    repair: <text>                         # optional
    decision: <decision_point>
    fingerprint: <hidden_resolution_fingerprint>
    prohibited: term a | term b
    desc: <description>
    resolution: <resolution>
    q: <trigger question>                  # repeat for each question
    # ground truth, type specific:
    gt.omitted / gt.why                    # missing_parameter
    gt.element + gt.read: <reading> >> <impl>   # ambiguous_requirement (repeat gt.read)
    gt.a / gt.b / gt.why / gt.evidence     # contradictory_requirement

    @rejected
    type / mode / area / decision / gate / reason / checks / fingerprint / avoid / outcome

    @notes
    distribution: <text>
    independence: <text>
    pool: <text>
"""

import argparse
import json
import os
import sys

TYPE_ALIASES = {
    "mp": "missing_parameter",
    "ar": "ambiguous_requirement",
    "cr": "contradictory_requirement",
}
TYPE_ORDER = ["missing_parameter", "ambiguous_requirement", "contradictory_requirement"]
CHECK_FIELDS = [
    "realistic", "critical", "objective", "large_search_space", "single_blocker",
    "uncontaminated", "independent", "not_gotcha", "natural_and_subtle", "type_specific",
]


# Split raw DSL text into ordered (header, body_lines) records keyed by '@'.
def _split_records(text):
    records = []
    current = None
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("@"):
            parts = stripped[1:].split(None, 1)
            header = parts[0]
            name = parts[1].strip() if len(parts) > 1 else ""
            current = {"header": header, "name": name, "lines": []}
            records.append(current)
        elif current is not None:
            current["lines"].append(stripped)
    return records


# Split a body line into (key, value) on the first colon.
def _kv(line):
    if ":" not in line:
        return None, None
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


# Collect body lines into a dict, accumulating repeated keys into lists.
def _collect(lines, multi_keys=()):
    out = {}
    for line in lines:
        key, value = _kv(line)
        if key is None:
            continue
        if key in multi_keys:
            out.setdefault(key, []).append(value)
        else:
            out[key] = value
    return out


# Expand the 'requested' shorthand into a full per-type distribution dict.
def _parse_requested(value):
    dist = {t: 0 for t in TYPE_ORDER}
    for token in value.split():
        if "=" not in token:
            continue
        alias, count = token.split("=", 1)
        full = TYPE_ALIASES.get(alias.strip())
        if full:
            dist[full] = int(count.strip())
    return dist


# Build the type specific ground_truth_annotation block from a blocker dict.
def _ground_truth(btype, fields, reads, area):
    if btype == "missing_parameter":
        return {
            "omitted_element": fields.get("gt.omitted", ""),
            "component": area,
            "why_blocker": fields.get("gt.why", ""),
        }
    if btype == "ambiguous_requirement":
        interpretations = []
        for entry in reads:
            if ">>" in entry:
                reading, impl = entry.split(">>", 1)
            else:
                reading, impl = entry, ""
            interpretations.append({
                "reading": reading.strip(),
                "implementation": impl.strip(),
            })
        return {
            "ambiguous_element": fields.get("gt.element", ""),
            "component": area,
            "interpretations": interpretations,
        }
    comp_a, comp_b = (area.split("+", 1) + [area, area])[:2] if "+" in area else (area, area)
    return {
        "requirement_a": {"text": fields.get("gt.a", ""), "component": comp_a},
        "requirement_b": {"text": fields.get("gt.b", ""), "component": comp_b},
        "why_impossible": fields.get("gt.why", ""),
        "patch_evidence": fields.get("gt.evidence", "baseline_only"),
    }


# Parse one @blocker record into a normalized blocker dict.
def _parse_blocker(record):
    fields = _collect(record["lines"], multi_keys=("q", "gt.read"))
    btype = fields.get("type", "")
    area = fields.get("area", "")
    prohibited = [p.strip() for p in fields.get("prohibited", "").split("|") if p.strip()]
    return {
        "id": record["name"],
        "type": btype,
        "mode": fields.get("mode", ""),
        "area_of_obstruction": area,
        "status": fields.get("status", "valid"),
        "repair_log": fields.get("repair", "none"),
        "decision_point": fields.get("decision", ""),
        "fingerprint": fields.get("fingerprint", ""),
        "prohibited_visible_terms": prohibited,
        "description": fields.get("desc", ""),
        "resolution": fields.get("resolution", ""),
        "trigger_questions": fields.get("q", []),
        "ground_truth": _ground_truth(btype, fields, fields.get("gt.read", []), area),
    }


# Parse one @candidate record into a candidate_pool entry.
def _parse_candidate(record):
    fields = _collect(record["lines"])
    return {
        "candidate_id": record["name"],
        "source": fields.get("source", ""),
        "preliminary_type": fields.get("type", ""),
        "mode": fields.get("mode", ""),
        "area": fields.get("area", ""),
        "rationale": fields.get("rationale", ""),
        "patch_evidence": fields.get("evidence", "baseline_only"),
        "selected": fields.get("selected", "false").lower() == "true",
        "rejection_reason": fields.get("reject", "none"),
    }


# Parse one @rejected record into a rejection_memory entry.
def _parse_rejected(record):
    fields = _collect(record["lines"])
    checks = [c.strip() for c in fields.get("checks", "").split("|") if c.strip()]
    return {
        "attempted_type": fields.get("type", ""),
        "attempted_mode": fields.get("mode", ""),
        "attempted_area_of_obstruction": fields.get("area", ""),
        "attempted_decision_point": fields.get("decision", ""),
        "failure_gate": fields.get("gate", ""),
        "failure_reason": fields.get("reason", ""),
        "failed_checks": checks,
        "failed_pattern_fingerprint": fields.get("fingerprint", ""),
        "avoid_in_future": fields.get("avoid", ""),
        "repair_outcome": fields.get("outcome", "discarded"),
    }


# Parse the full DSL text into structured sections.
def parse_dsl(text):
    parsed = {
        "round": 1,
        "requested": {t: 0 for t in TYPE_ORDER},
        "halt": None,
        "candidates": [],
        "blockers": [],
        "rejected": [],
        "notes": {},
    }
    for record in _split_records(text):
        header = record["header"]
        if header == "meta":
            fields = _collect(record["lines"])
            parsed["round"] = int(fields.get("round", "1"))
            parsed["requested"] = _parse_requested(fields.get("requested", ""))
            parsed["halt"] = fields.get("halt")
        elif header == "candidate":
            parsed["candidates"].append(_parse_candidate(record))
        elif header == "blocker":
            parsed["blockers"].append(_parse_blocker(record))
        elif header == "rejected":
            parsed["rejected"].append(_parse_rejected(record))
        elif header == "notes":
            parsed["notes"] = _collect(record["lines"])
    return parsed


# Count blockers per type inside an already built registry blocker list.
def _count_by_type(blockers):
    counts = {t: 0 for t in TYPE_ORDER}
    for blocker in blockers:
        btype = blocker.get("type")
        if btype in counts:
            counts[btype] += 1
    return counts


# Serialize one parsed blocker into the canonical registry entry.
def _registry_entry(blocker):
    return {
        "id": blocker["id"],
        "type": blocker["type"],
        "mode": blocker["mode"],
        "area_of_obstruction": blocker["area_of_obstruction"],
        "description": blocker["description"],
        "resolution": blocker["resolution"],
        "trigger_questions": blocker["trigger_questions"],
        "independence": {
            "decision_point": blocker["decision_point"],
            "hidden_resolution_fingerprint": blocker["fingerprint"],
            "prohibited_visible_terms": blocker["prohibited_visible_terms"],
        },
    }


# Build the cumulative blocker_registry object from parsed data and an existing registry.
def build_registry(parsed, existing):
    existing_blockers = existing.get("blockers", []) if existing else []
    new_blockers = [_registry_entry(b) for b in parsed["blockers"]]
    mode_counts = {"extraction": 0, "injection": 0}
    for blocker in parsed["blockers"]:
        if blocker["mode"] in mode_counts:
            mode_counts[blocker["mode"]] += 1
    notes = parsed["notes"].get("distribution", "")
    mode_line = "Mode split this round: {extraction} extraction, {injection} injection.".format(**mode_counts)
    distribution_notes = (notes + " " + mode_line).strip() if notes else mode_line
    return {
        "blockers": existing_blockers + new_blockers,
        "distribution_notes": distribution_notes,
    }


# Reconstruct the slimmed validation block from a blocker status.
def _validation(blocker):
    return {"status": blocker["status"], "repair_log": blocker["repair_log"]}


# Serialize one parsed blocker into the slimmed generation_memory blocker entry.
def _memory_blocker(blocker):
    return {
        "id": blocker["id"],
        "type": blocker["type"],
        "mode": blocker["mode"],
        "area_of_obstruction": blocker["area_of_obstruction"],
        "ground_truth_annotation": blocker["ground_truth"],
        "validation": _validation(blocker),
        "independence": {
            "decision_point": blocker["decision_point"],
            "hidden_resolution_fingerprint": blocker["fingerprint"],
            "prohibited_visible_terms": blocker["prohibited_visible_terms"],
            "overlaps_prior_registry": False,
            "overlap_notes": "none",
        },
    }


# Infer the halt reason when the DSL leaves it unset.
def _infer_halt(parsed, deficit, achieved_total):
    if parsed["halt"]:
        return parsed["halt"]
    if all(v == 0 for v in deficit.values()):
        return "distribution_already_satisfied"
    if achieved_total == parsed["requested"]:
        return "distribution_satisfied"
    if parsed["round"] >= 3:
        return "budget_exhausted"
    return "continue"


# Build the cumulative generation_memory object from parsed data and prior loop state.
def build_generation_memory(parsed, existing, prior_rejection):
    existing_counts = _count_by_type(existing.get("blockers", [])) if existing else {t: 0 for t in TYPE_ORDER}
    deficit = {t: parsed["requested"][t] - existing_counts[t] for t in TYPE_ORDER}
    achieved_round = _count_by_type(parsed["blockers"])
    achieved_total = {t: existing_counts[t] + achieved_round[t] for t in TYPE_ORDER}
    mode_counts = {"extraction": 0, "injection": 0}
    for blocker in parsed["blockers"]:
        if blocker["mode"] in mode_counts:
            mode_counts[blocker["mode"]] += 1
    halt_reason = _infer_halt(parsed, deficit, achieved_total)
    rejection_memory = list(prior_rejection or []) + list(parsed["rejected"])
    return {
        "halt": {
            "reason": halt_reason,
            "round": parsed["round"],
            "achieved_total": achieved_total,
            "requested": parsed["requested"],
        },
        "blocker_dataset": {
            "round": parsed["round"],
            "requested_distribution": parsed["requested"],
            "deficit_distribution": deficit,
            "candidate_pool": parsed["candidates"],
            "blockers": [_memory_blocker(b) for b in parsed["blockers"]],
            "rejected_blockers": parsed["rejected"],
            "batch_audit": {
                "status": "valid",
                "achieved_distribution": achieved_round,
                "mode_distribution": mode_counts,
                "distribution_notes": parsed["notes"].get("distribution", ""),
                "independence_summary": parsed["notes"].get("independence", ""),
                "candidate_pool_summary": parsed["notes"].get("pool", ""),
            },
        },
        "rejection_memory": rejection_memory,
    }


# Load a JSON file when a path is given, otherwise return the fallback.
def _load_json(path, fallback):
    if not path:
        return fallback
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


# Parse CLI arguments, run the build, and write both output files.
def main():
    parser = argparse.ArgumentParser(description="Build blocker JSON files from the blocker DSL.")
    parser.add_argument("dsl", help="Path to the blocker DSL file.")
    parser.add_argument("--existing", help="Path to the previous round blocker_registry.json.", default=None)
    parser.add_argument("--rejection-memory", help="Path to the previous round rejection_memory JSON array.", default=None)
    parser.add_argument("--out-dir", help="Directory where the JSON files are written.", default=".")
    args = parser.parse_args()

    with open(args.dsl, "r", encoding="utf-8") as handle:
        text = handle.read()

    parsed = parse_dsl(text)
    existing = _load_json(args.existing, {})
    prior_rejection = _load_json(args.rejection_memory, [])

    registry = build_registry(parsed, existing)
    memory = build_generation_memory(parsed, existing, prior_rejection)

    os.makedirs(args.out_dir, exist_ok=True)
    registry_path = os.path.join(args.out_dir, "blocker_registry.json")
    memory_path = os.path.join(args.out_dir, "generation_memory.json")
    with open(registry_path, "w", encoding="utf-8") as handle:
        json.dump(registry, handle, indent=2, ensure_ascii=False)
    with open(memory_path, "w", encoding="utf-8") as handle:
        json.dump(memory, handle, indent=2, ensure_ascii=False)

    print("wrote {} ({} blockers)".format(registry_path, len(registry["blockers"])))
    print("wrote {} (halt: {})".format(memory_path, memory["halt"]["reason"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
