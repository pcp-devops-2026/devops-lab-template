#!/usr/bin/env bash
# setup.sh — verify the toolchain for the IBM DevOps cohort lab

set -u

echo "🔍 Verifying toolchain for devops-lab..."
echo

ok=0
fail=0

check() {
  local name="$1"
  local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    printf "  ✅ %-15s\n" "$name"
    ok=$((ok+1))
  else
    printf "  ❌ %-15s  (missing or broken)\n" "$name"
    fail=$((fail+1))
  fi
}

check "git"       "git --version"
check "docker"    "docker --version"
check "kubectl"   "kubectl version --client"
check "kind"      "kind --version"
check "oc"        "oc version --client"
check "helm"      "helm version --short"
check "python3"   "python3 --version"
check "pip"       "pip --version"
check "node"      "node --version"

echo
echo "Result: $ok ok, $fail missing/broken."
if [ "$fail" -gt 0 ]; then
  echo "👉 See the runbooks in mentoring-hub for install help."
  exit 1
fi
echo "🎉 You're all set."
