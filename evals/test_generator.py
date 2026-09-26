import json

from quiz_engine import generate_quiz
from evals.groundedness import evaluate_groundedness


passage = """
Past experiences do not determine a person's future.
What matters is the meaning the person gives to those experiences.
A person may interpret the same experience differently from another person.
"""


quiz = generate_quiz(passage)


grounded_count = 0

for question in quiz.questions:

    is_grounded = evaluate_groundedness(
        passage,
        question.question
    )

    print(f"\nQuestion: {question.question}")
    print(f"Grounded: {is_grounded}")

    if is_grounded:
        grounded_count += 1


score = grounded_count / len(quiz.questions)

result = {
    "groundedness_score": score,
    "grounded_questions": grounded_count,
    "total_questions": len(quiz.questions)
}


with open("evals/result.json", "w") as file:
    json.dump(result, file, indent=2)


print(f"\nGroundedness score: {score:.0%}")
print("Results saved to evals/result.json")
