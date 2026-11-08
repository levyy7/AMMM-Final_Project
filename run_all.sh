#!/usr/bin/env bash
# Usage: ./run_all.sh [data_dir]      (default data_dir: ./data)
# Optional: MODEL=path/to/model.mod ./run_all.sh data/

set -u

MODEL="${MODEL:-src/model.mod}"
CHECKER="src/checker.py"
DATA_DIR="${1:-data}"
OUT_DIR="output"

if ! command -v oplrun >/dev/null 2>&1; then
  echo "Error: oplrun not found in PATH" >&2
  exit 1
fi
[[ -f "$MODEL" ]]   || { echo "Error: model '$MODEL' not found" >&2; exit 1; }
[[ -f "$CHECKER" ]] || { echo "Error: checker '$CHECKER' not found" >&2; exit 1; }

mkdir -p "$OUT_DIR"

# collect project.<number>.dat files, sorted numerically
mapfile -t FILES < <(find "$DATA_DIR" -maxdepth 1 -type f -name 'project.*.dat' | sort -V)

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No project.*.dat files found in '$DATA_DIR'" >&2
  exit 1
fi

ok=0
bad=0

for dat in "${FILES[@]}"; do
  base=$(basename "$dat")

  if [[ ! $base =~ ^project\.([0-9]+)\.dat$ ]]; then
    echo "Skipping '$base' (name doesn't match project.<number>.dat)"
    continue
  fi
  i="${BASH_REMATCH[1]}"
   sol="$OUT_DIR/output.$i.sol"
  log="$OUT_DIR/log.$i.txt"

  echo "=== Instance $i: $base ==="

  if ! oplrun "$MODEL" "$dat" > "$log" 2>&1; then
    echo "  [ERROR] oplrun failed for instance $i (see $log)"
    bad=$((bad + 1))
    continue
  fi

  # Clean the output for the .sol file
  tr -d '\r' < "$log" | grep -E '^[0-9]+ [0-9]+$' > "$sol" || true

  # check the solution
  if python3 "$CHECKER" "$dat" "$sol"; then
    echo "  [OK] instance $i"
    ok=$((ok + 1))
  else
    echo "  [FAIL] checker rejected instance $i"
    bad=$((bad + 1))
  fi
done

echo
echo "Summary: $ok passed, $bad failed"
[[ $bad -eq 0 ]]
