#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-}" in
  theory) python -m unittest discover -s src/S04_Tests -p 'test_response_geometry.py' -v ;;
  test) python -m unittest discover -s src/S04_Tests -p 'test_response_*.py' -v ;;
  demo) shift; python src/S03_Scripts/run_response_basis.py --synthetic "$@" ;;
  study) shift; python src/S03_Scripts/run_response_basis.py "$@" ;;
  *) echo 'usage: bash scripts/run_response_basis.sh {theory|test|demo --output PATH|study --input DATA.npz --output PATH}' >&2; exit 2 ;;
esac
