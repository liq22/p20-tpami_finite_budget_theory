# Goal G0 — Data and Benchmark admission

Scientific question: Is there one real PHM task in the supplied local data that can support a leakage-safe, fixed-response experiment using the current Benchmark runtime?

Hypothesis: At least one dataset family has complete raw files, a declared classification target, a highest-level independent unit, a native reader and a split that can separate development-train, development-select and final-test units before windowing.

Estimand: None. G0 is an admission decision, not a performance experiment.

## Inputs

```text
dataset root: /home/user/data/PHMbenchdata/PHM-Vibench
metadata:     /home/user/data/PHMbenchdata/PHM-Vibench/metadata.xlsx
README:       /home/user/data/PHMbenchdata/PHM-Vibench/README.md
Benchmark:    PHMbench/PHM-Vibench current dev
candidate config: configs/demo/01_cross_domain/cwru_dg.yaml
```

## Fixed conditions

- Read-only inspection of local metadata/README/raw-file coverage before config design.
- Current `dev` is the only base; do not use `main` or an old paper submodule pointer.
- The public runtime is `phmfactory`; smoke and preflight use the same installation as the real experiment.
- Actual data boundary is `src/data_factory/`; no new DataPort, loader copy, manager or silent format repair.
- The current dense shared basis admits at most `p=256` coordinates.

## Changed variable

None. This Goal only determines whether and how one dataset/predictor configuration is admissible.

## Execution

1. Establish a clean topic branch and runtime:

```bash
export BENCH=/absolute/path/to/PHM-Vibench
export DATA_ROOT=/home/user/data/PHMbenchdata/PHM-Vibench
cd "$BENCH"
git fetch origin
git switch dev
git pull --ff-only origin dev
git status --short
git rev-parse HEAD
git switch -c feat/p20-response-falsification
python -m pip install -e .
phmfactory doctor
phmfactory preflight --config smoke
phmfactory demo
```

2. Verify dependency and source authority without assuming a submodule:

```bash
git ls-files .gitmodules
git submodule status || true
python - <<'PY'
import inspect, phmfactory
print(phmfactory.__file__)
PY
```

If a local `.gitmodules` or imported external data backend exists despite the audited remote state, record its exact role and stop until its revision/source authority is clear.

3. Verify the two user-supplied files and inspect their actual content:

```bash
test -f "$DATA_ROOT/metadata.xlsx"
test -f "$DATA_ROOT/README.md"
sed -n '1,260p' "$DATA_ROOT/README.md"
META="$DATA_ROOT/metadata.xlsx" python - <<'PY'
import os, pandas as pd
path=os.environ['META']
book=pd.ExcelFile(path)
print('sheets=', book.sheet_names)
for sheet in book.sheet_names:
    frame=pd.read_excel(path, sheet_name=sheet)
    print('\nSHEET', sheet, 'shape=', frame.shape)
    print('columns=', list(frame.columns))
    print(frame.head(5).to_string(index=False))
    print('null_counts=', frame.isna().sum().to_dict())
PY
```

4. Trace the selected dataset through the native reader and split code. Establish from source and a dry run:

```text
dataset family and source/license
raw-file locator columns
label and class mapping
operating-condition/domain fields
highest non-overlapping unit field
whether split occurs before or after windowing
normalization fit population
actual model input shape p
target-system/source-domain/target-domain semantics
```

Do not assume the CWRU demo is valid merely because the path exists. Its audited base uses `window_size: 4096`; do not override to `256` solely to satisfy the method.

5. Verify every metadata-selected raw file exists. Use the actual locator columns discovered in step 3; do not hard-code guessed `Name`/`File` fields.

6. Select one candidate dataset family and construct a proposed unit-disjoint split using metadata identifiers. Perform a prospective paired sample-size/power check from development units after defining a minimum scientifically relevant response-MSE effect. Do not inspect final-test outcomes.

7. Run native preflight with an untracked local machine config and no scientific shortcut:

```bash
phmfactory preflight \
  --config configs/experiments/p20/<dataset>_frozen_predictor.yaml \
  --local-config configs/local/p20_machine.yaml
```

## Validation

G0 passes only if all are true:

```text
smoke runtime passes
metadata and README are readable
selected raw files exist
reader resolves without dropped samples or fallback
label/task semantics are explicit
independent unit is identified before windowing
train/select/test units are disjoint
normalization uses development data only
actual input dimension is p<=256, or an already justified structured implementation exists
native checkpoint selection/test lifecycle is available
available unit count is adequate for the predeclared primary paired effect
```

## Required artifacts

```text
reports/p20/G0_ADMISSION.md
reports/p20/metadata_schema.txt
reports/p20/dataset_unit_split.csv
reports/p20/raw_file_coverage.csv
reports/p20/preflight.txt
reports/p20/smoke_command.txt
reports/p20/smoke_result_paths.txt
```

`G0_ADMISSION.md` must end with exactly one status: `ADMITTED`, `BLOCKED_DATA`, `BLOCKED_SPLIT`, `BLOCKED_DIMENSION`, or `BLOCKED_RUNTIME`.

## Acceptance criteria

- One dataset, task, predictor family, scalar score type and independent unit are admitted.
- No window-level leakage or unsupported dimensionality remains.
- The proposed experiment config resolves through the existing Benchmark runtime.

## Failure handling

If G0 fails, preserve the failed command, traceback and status. Do not switch datasets or shorten windows without a new scientific admission decision. Independent work that may continue: existing C1/C3 tests, documentation of the blocker, and source-level inspection of the structured-basis requirement.

## Sync

Commit only the validated admission report, bounded experiment config, focused tests and failure records. Push the topic branch and open a PR to Benchmark `dev`; do not merge until repository checks pass.
