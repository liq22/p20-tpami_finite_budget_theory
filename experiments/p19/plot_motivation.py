#!/usr/bin/env python3
"""Render two editable scientific diagrams; neither encodes experimental values.

The first defines the controlled problem. The second separates inherited fitting
operations, the proposed outer-objective intervention, selection and evaluation.
Each box, arrow and text line is an independent named SVG element.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


class Diagram:
    def __init__(self, title, height):
        self.root = ET.Element(f'{{{NS}}}svg', {
            'viewBox': f'0 0 1200 {height}', 'width': '180mm',
            'height': f'{height*.15:g}mm', 'role': 'img'})
        ET.SubElement(self.root, f'{{{NS}}}title').text = title
        defs = ET.SubElement(self.root, f'{{{NS}}}defs')
        marker = ET.SubElement(defs, f'{{{NS}}}marker', {
            'id': 'arrow', 'markerWidth': '8', 'markerHeight': '8',
            'refX': '7', 'refY': '4', 'orient': 'auto', 'markerUnits': 'userSpaceOnUse'})
        ET.SubElement(marker, f'{{{NS}}}path', {'d': 'M0,0 L8,4 L0,8 Z', 'fill': '#222222'})
        self.box('canvas', 0, 0, 1200, height, border=0)

    def box(self, name, x, y, w, h, border=1.5, dashed=False):
        attrs = {'id': name, 'x': str(x), 'y': str(y), 'width': str(w),
                 'height': str(h), 'fill': '#ffffff', 'stroke': '#222222',
                 'stroke-width': str(border)}
        if dashed:
            attrs['stroke-dasharray'] = '7 5'
        ET.SubElement(self.root, f'{{{NS}}}rect', attrs)

    def text(self, name, x, y, content, size=20, bold=False):
        ET.SubElement(self.root, f'{{{NS}}}text', {
            'id': name, 'x': str(x), 'y': str(y), 'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(size), 'font-weight': 'bold' if bold else 'normal',
            'fill': '#111111'}).text = content

    def lines(self, name, x, y, contents, size=20, gap=31):
        for i, text in enumerate(contents):
            self.text(f'{name}-{i}', x, y + gap*i, text, size)

    def arrow(self, name, points, dashed=False):
        attrs = {'id': name, 'points': ' '.join(f'{x},{y}' for x, y in points),
                 'fill': 'none', 'stroke': '#222222', 'stroke-width': '1.8',
                 'marker-end': 'url(#arrow)'}
        if dashed:
            attrs['stroke-dasharray'] = '7 5'
        ET.SubElement(self.root, f'{{{NS}}}polyline', attrs)

    def save(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.root)
        ET.ElementTree(self.root).write(path, encoding='utf-8', xml_declaration=True)
        print(path)


def problem():
    d = Diagram('Fixed-response problem and the controlled coordinate intervention', 770)
    d.text('title', 30, 40, 'What changes when explanation coordinates change?', 27, True)
    d.box('fixed-semantics', 30, 70, 1140, 100)
    d.text('fixed-label', 50, 100, 'FIXED SEMANTICS AND INFORMATION', 19, True)
    d.lines('fixed', 50, 130, [
        'Frozen score s  ·  target t  ·  original-space law μₓ  ·  development data D  ·  context z',
        'Coordinate budget k  ·  response-query budget Q  ·  same independent-unit split'], 20, 27)
    d.box('original-space', 30, 210, 330, 170)
    d.text('original-title', 50, 244, 'Original-space responses', 21, True)
    d.lines('original', 50, 283, ['Input x and displacement v', 'dₓ(v) = s(x) − s(x − v)', 'Same raw-space law for all A'])
    d.box('construction', 420, 210, 330, 170)
    d.text('construction-title', 440, 244, 'Construction transcript', 21, True)
    d.lines('construction', 440, 283, ['T_Q = {(v_q, dₓ(v_q))}', 'Q perturbed scalar responses', 'One reusable base score s(x)'])
    d.box('scoring', 810, 210, 360, 170)
    d.text('scoring-title', 830, 244, 'Independent scoring', 21, True)
    d.lines('scoring', 830, 283, ['Fresh v from the same μₓ', 'Separate scoring responses', 'Unavailable to online fitting'])
    d.arrow('response-to-fit', [(360, 290), (420, 290)])
    d.arrow('response-to-score', [(195, 210), (195, 193), (990, 193), (990, 210)])
    d.box('variable', 30, 432, 440, 165, border=3)
    d.text('variable-title', 50, 466, 'CONTROLLED INTERVENTION', 21, True)
    d.lines('variable', 50, 505, ['Coordinate-learning objective m', 'Common coordinate family + decoder', 'Common inputs, responses and budgets'])
    d.box('output', 540, 432, 630, 165)
    d.text('output-title', 560, 466, 'Fitted prediction and observed loss', 21, True)
    d.lines('output', 560, 505, ['A, selected support S, fitted coefficients â',
        'd̂ₓ(v) = âᵀAv       with at most k nonzeros', 'Unit loss Lᵤ; paired Δ = Lᵤ(m) − Lᵤ(m₀)'], 20, 31)
    d.arrow('transcript-to-output', [(585, 380), (585, 432)])
    d.arrow('score-to-output', [(1020, 380), (1020, 432)])
    d.arrow('intervention-to-output', [(470, 515), (540, 515)])
    d.box('gap', 30, 640, 1140, 100, dashed=True)
    d.text('gap-title', 50, 672, 'ATTRIBUTION GAP', 20, True)
    d.lines('gap', 50, 704, ['A lower fresh loss may reflect approximation, support identification, or coefficient estimation.',
        'Negative Δ favors the method; response fidelity alone does not establish physical meaning.'], 20, 26)
    return d


def method():
    d = Diagram('Shared-coordinate method: training, selection and frozen evaluation', 1030)
    d.text('title', 30, 40, 'Learn the shared basis; fit a new sparse decoder at each input', 25, True)
    d.text('legend', 30, 74, 'Thin outline: inherited operation   ·   Heavy outline: learning intervention   ·   Dashed arrow: update', 19)
    d.text('train-title', 30, 115, 'a  DEVELOPMENT TRAINING — no selection or test units', 22, True)
    d.box('train-data', 30, 143, 290, 354)
    d.text('train-data-title', 48, 177, 'Fixed response data', 20, True)
    d.lines('train-data', 48, 219, ['Actual input x', 'Fit table: V, d  (Q)'], 19, 36)
    d.text('outer-data-title', 48, 363, 'Fresh outer table', 20, True)
    d.lines('outer-data', 48, 405, ['Vᵒᵘᵗ, dᵒᵘᵗ  (R responses)', 'Training information only'], 19, 36)
    d.box('basis', 370, 143, 320, 170)
    d.text('basis-title', 388, 177, 'Shared orthogonal basis', 20, True)
    d.lines('basis', 388, 214, ['Aθ = exp(Sθ),  Sθ = −Sθᵀ', 'One basis across all inputs', 'Z = VAθᵀ; same raw response'])
    d.box('decoder', 740, 143, 430, 170)
    d.text('decoder-title', 758, 177, 'Inherited finite-query decoder', 20, True)
    d.lines('decoder', 758, 214, ['Normalized greedy support (at most k)', 'Restricted ridge coefficients â_S', 'Positive λ; not a population oracle'])
    d.arrow('training-data-flow', [(320, 230), (370, 230)])
    d.arrow('training-basis-flow', [(690, 230), (740, 230)])
    d.box('outer-objective', 370, 360, 800, 137, border=3)
    d.text('outer-title', 388, 394, 'RESPONSE-DRIVEN OUTER OBJECTIVE', 21, True)
    d.lines('outer', 388, 431, ['Fresh response error of the fitted Q-query decoder',
        'Update θ through the current support branch; predictor s remains frozen'], 20, 33)
    d.arrow('decoder-to-outer', [(960, 313), (960, 360)])
    d.arrow('outer-update', [(530, 360), (530, 313)], True)
    d.arrow('outer-responses', [(320, 425), (370, 425)])
    d.lines('proxies', 30, 533, ['Matched outer-loss replacements: actual-input reconstruction / coefficient concentration.',
        'All objectives retain the same downstream decoder and response-based selection.'], 19, 24)
    d.text('selection-title', 30, 580, 'b  INDEPENDENT SELECTION — one deployment criterion', 22, True)
    d.box('snapshots', 30, 606, 450, 112)
    d.text('snapshots-title', 48, 642, 'Frozen candidate trajectories', 21, True)
    d.lines('snapshots', 48, 678, ['Identity + prespecified checkpoints'], 19)
    d.box('selection', 550, 606, 620, 112)
    d.text('selection-box-title', 568, 642, 'Select by fresh response loss on separate units', 21, True)
    d.lines('selection', 568, 678, ['Same rule for learned and fixed families; identity wins ties'], 19)
    d.arrow('snapshot-to-selection', [(480, 663), (550, 663)])
    d.arrow('training-to-snapshots', [(1170, 476), (1185, 476), (1185, 594), (256, 594), (256, 606)])
    d.text('test-title', 30, 763, 'c  NEW INPUT / FINAL EVALUATION — no basis update', 22, True)
    d.box('freeze', 30, 790, 315, 138)
    d.text('freeze-title', 48, 825, 'Frozen basis A', 21, True)
    d.lines('freeze', 48, 862, ['New x and Q responses', 'Fit only support + coefficients'], 19)
    d.box('prediction', 400, 790, 325, 138)
    d.text('prediction-title', 418, 825, 'Response prediction', 20, True)
    d.lines('prediction', 418, 862, ['d̂ₓ(v) = âᵀAv', 'No evaluation-response access'], 19)
    d.box('evaluation', 780, 790, 390, 138)
    d.text('evaluation-title', 798, 825, 'Fresh scoring only', 21, True)
    d.lines('evaluation', 798, 862, ['Independent displacements → loss', 'Aggregate by unit → paired Δ'], 19)
    d.arrow('selected-to-test', [(1170, 678), (1185, 678), (1185, 778), (186, 778), (186, 790)])
    d.arrow('fit-to-predict', [(345, 855), (400, 855)])
    d.arrow('predict-to-evaluate', [(725, 855), (780, 855)])
    d.lines('footer', 30, 967, ['External control: âᵀAⱼv = ãᵀΨ(v), with ã = [0; …; â; …; 0] and the same (k, Q).',
        'Construction chooses the support; independent scoring measures response fidelity.'], 19, 29)
    return d


def main():
    output = Path('paper/assets/figures')
    problem().save(output/'motivation.svg')
    method().save(output/'method_overview.svg')


if __name__ == '__main__':
    main()
