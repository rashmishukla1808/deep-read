import json

from groundedness import evaluate_groundedness


with open("evals/test_cases.json", "r") as file:
    test_cases = json.load(file)


for test in test_cases:

    actual = evaluate_groundedness(
    test["passage"],
    test["question"]
)
    expected = test["expected_grounded"]

    result = "PASS" if actual == expected else "FAIL"

    print(
        f"{test['id']}: "
        f"Expected={expected}, "
        f"Actual={actual} → {result}"
    )
