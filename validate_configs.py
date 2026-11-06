#!/usr/bin/env python3
"""
validate_configs.py
Validates all remote configuration JSON files in my-mobile_apps-configs.
Checks:
1. Valid JSON syntax.
2. Required fields (app_id, schema_version, early_access, trial, pricing).
3. Type safety (booleans, integers, numbers).
"""

import os
import json
import sys

DIR = os.path.dirname(os.path.abspath(__file__))

def validate_file(filename):
    filepath = os.path.join(DIR, filename)
    print(f"Validating {filename}...")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON SYNTAX ERROR in {filename}: {e}")
        return False

    # Check top-level keys
    required_keys = ["app_id", "schema_version", "early_access", "trial", "pricing"]
    for k in required_keys:
        if k not in data:
            print(f"  ❌ Missing required key '{k}' in {filename}")
            return False

    # Check early_access
    ea = data.get("early_access", {})
    if not isinstance(ea.get("active"), bool):
        print(f"  ❌ 'early_access.active' must be a boolean in {filename}")
        return False

    # Check trial
    tr = data.get("trial", {})
    if not isinstance(tr.get("duration_days"), int) or tr.get("duration_days") < 1:
        print(f"  ❌ 'trial.duration_days' must be an integer >= 1 in {filename}")
        return False

    # Check pricing
    pr = data.get("pricing", {})
    if not pr.get("lifetime_product_id") or not isinstance(pr.get("price_usd"), (int, float)):
        print(f"  ❌ Invalid 'pricing' block in {filename}")
        return False

    print(f"  ✅ {filename} is valid (App: {data.get('app_id')}, EarlyAccess: {ea.get('active')}, TrialDays: {tr.get('duration_days')})")
    return True

def main():
    print("=== Mobile Apps Remote Config Validator ===")
    all_ok = True
    for fname in os.listdir(DIR):
        if fname.endswith(".json") and fname != "schema.json":
            if not validate_file(fname):
                all_ok = False
    
    if all_ok:
        print("\n🎉 All configuration files are valid and production-ready!")
        sys.exit(0)
    else:
        print("\n💥 Some configuration files failed validation. Please fix errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
