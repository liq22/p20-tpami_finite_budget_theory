#!/usr/bin/env python3
"""Generate the editable motivation diagram from the recorded control summary.

SVG text, boxes and arrows remain separate objects. The numerical footer reads
actual outputs, while the equality in panel c is a mathematical identity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=Path("paper/experiments/results/paired_control_summary.json"))
    parser.add_argument("--output", type=Path, default=Path("paper/assets/figures/motivation.svg"))
    args = parser.parse_args()
    result = json.loads(args.summary.read_text())
    budgets = result["budgets"]
    max_error = max(row["max_route_union_prediction_error"] for row in budgets.values())
    if result["evidence_kind"] != "controlled_synthetic_only":
        raise ValueError("this figure labels a controlled synthetic experiment")
    root = ET.Element(f"{{{NS}}}svg", {"viewBox": "0 0 1440 880", "width": "180mm", "height": "110mm", "role": "img"})
    ET.SubElement(root, f"{{{NS}}}title").text = "Coordinates, search and information must be separated"
    ET.SubElement(root, f"{{{NS}}}desc").text = "Three matched estimators share a fixed response problem. The union emulator duplicates a routed block without extra model queries."
    defs = ET.SubElement(root, f"{{{NS}}}defs")
    marker = ET.SubElement(defs, f"{{{NS}}}marker", {"id": "arrowhead", "markerWidth": "9", "markerHeight": "9", "refX": "8", "refY": "4", "orient": "auto", "markerUnits": "userSpaceOnUse"})
    ET.SubElement(marker, f"{{{NS}}}path", {"d": "M0,0 L8,4 L0,8 Z", "fill": "#304451"})

    def box(name: str, x: int, y: int, w: int, h: int, fill: str = "#ffffff") -> None:
        ET.SubElement(root, f"{{{NS}}}rect", {"id": name, "x": str(x), "y": str(y), "width": str(w), "height": str(h), "rx": "12", "fill": fill, "stroke": "#89979f", "stroke-width": "1.8"})

    def text(name: str, x: int, y: int, content: str, size: int = 27, weight: str = "normal", fill: str = "#172b37") -> None:
        node = ET.SubElement(root, f"{{{NS}}}text", {"id": name, "x": str(x), "y": str(y), "font-family": "DejaVu Sans, sans-serif", "font-size": str(size), "font-weight": weight, "fill": fill})
        node.text = content

    def arrow(name: str, x1: int, y1: int, x2: int, y2: int) -> None:
        ET.SubElement(root, f"{{{NS}}}line", {"id": name, "x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2), "stroke": "#304451", "stroke-width": "2.5", "marker-end": "url(#arrowhead)"})

    box("background", 0, 0, 1440, 880)
    text("title", 44, 59, "Separate coordinate gains from support-selection gains", 35, "bold")
    box("fixed-problem", 44, 90, 1352, 142, "#edf3f5")
    text("fixed-label", 68, 127, "FIXED EXPLANATORY PROBLEM", 23, "bold")
    text("fixed-response", 68, 173, "dₓ(v) = s(x) − s(x − v)", 31)
    text("fixed-semantics", 655, 168, "predictor s  ·  target  ·  intervention law μₓ", 25)
    text("fixed-information", 68, 213, "same k, Q  ·  development information D  ·  available context z  ·  fresh scoring displacements", 25)
    for i, x in enumerate([262, 720, 1178]):
        arrow(f"fixed-to-panel-{i}", x, 234, x, 270)
    panel_x = [44, 502, 960]
    for name, x in zip(["plain-union", "route", "matched-union"], panel_x):
        box(name, x, 281, 436, 337)
    text("a", 67, 325, "a   Plain union-OMP", 28, "bold")
    text("b", 525, 325, "b   Context route", 28, "bold")
    text("c", 983, 325, "c   Matched union", 28, "bold")
    text("union-dictionary", 68, 378, "Ψ(v) = [A₀v; …; A(J−1)v]", 26)
    text("union-search", 68, 424, "Search over all candidate atoms", 23)
    text("union-limit", 68, 463, "At most k nonzeros in total", 23)
    text("union-ambiguity-1", 68, 528, "Larger search space may change", 23)
    text("union-ambiguity-2", 68, 564, "finite-query estimation error", 23)
    text("route-selector", 527, 379, "(D, x, z, T_Q) → j, â", 27)
    text("route-prediction", 527, 428, "Response prediction: âᵀAⱼv", 24)
    text("route-support", 527, 468, "One block; at most k nonzeros", 23)
    text("route-fixed-gate", 527, 530, "Choose j before scoring v", 23)
    text("route-context", 527, 565, "Context constrains support", 23)
    text("emulate-padding", 985, 379, "ã = [0; …; â; …; 0]", 28)
    text("emulate-equality", 985, 429, "ãᵀΨ(v) = âᵀAⱼv", 31, "bold")
    text("emulate-support", 985, 472, "Same total k; same Q queries", 23)
    text("emulate-class-1", 985, 532, "Fixed dictionary does not mean", 23)
    text("emulate-class-2", 985, 566, "fixed support or coefficients", 23)
    arrow("route-to-emulator", 899, 642, 1163, 642)
    text("emulation-label", 561, 652, "same rule + information", 24)
    box("interpretation", 44, 682, 1352, 153, "#edf3f5")
    text("interpretation-title", 68, 720, "DECISIVE CONTROL", 23, "bold")
    text("interpretation-statement", 68, 758, "If b beats a but equals c, the contrast does not isolate an intrinsic routing advantage.", 25)
    q_values = ", ".join(budgets)
    text("recorded-outcome", 68, 801, f"Executed synthetic check: max |prediction(b) − prediction(c)| = {max_error:g};  Q = {q_values}.", 25)
    text("footer", 45, 861, "Class containment is exact; practical cost and real-data coordinate benefits require separate evidence.", 23)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(args.output, encoding="utf-8", xml_declaration=True)
    print(args.output)


if __name__ == "__main__":
    main()
