import json
import sys
import time
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from llm_security.config import DATA_DIR
from llm_security.pipeline import defended_ask_llm


DATASET_PATH = DATA_DIR / "attack_dataset.json"
OUTPUT_PATH = DATA_DIR / "defended_results.json"


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    results = []

    for index, test in enumerate(test_cases):
        print(
            f"[{index + 1}/{len(test_cases)}] "
            f"{test['id']} — {test['category']}"
        )

        outcome = defended_ask_llm(test["prompt"])

        record = {
            "id": test["id"],
            "category": test["category"],
            "prompt": test["prompt"],
            "status": outcome["status"],
            "reason": outcome["reason"],
            "response": outcome["response"],
        }

        results.append(record)

        print(f"  Status: {outcome['status']}")
        print(f"  Reason: {outcome['reason']}")

        # Avoid making API calls too rapidly.
        # Input-blocked prompts never reach the API.
        if outcome["status"] in (
            "success",
            "blocked_output",
            "api_error",
        ):
            if index < len(test_cases) - 1:
                time.sleep(2)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    counts = Counter(item["status"] for item in results)

    print("\n=== Evaluation Summary ===")
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")

    print(f"\nTotal test cases: {len(results)}")
    print(f"Results saved to: {OUTPUT_PATH}")

    expected_ids = {item["id"] for item in test_cases}
    actual_ids = {item["id"] for item in results}

    if expected_ids != actual_ids:
        raise RuntimeError(
            "Some test cases are missing from the evaluation results."
        )


if __name__ == "__main__":
    main()