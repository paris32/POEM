# POEM - Scanner v0.5
# Reductive Inference Model - Shadow Path Implementation
import datetime

def run_scanner(question, threshold=1, attempt=1):

    factual_words = ["what", "when", "where", "who", "how many"]
    reasoning_words = ["why", "how", "explain"]
    opinion_words = ["should", "better", "best", "worst"]

    factual_matches = sum(1 for word in factual_words if word in question)
    reasoning_matches = sum(1 for word in reasoning_words if word in question)
    opinion_matches = sum(1 for word in opinion_words if word in question)
    total_matches = factual_matches + reasoning_matches + opinion_matches

    def explain_confidence(category, f, r, o, total):
        signals = []
        if f > 0:
            signals.append(f"{f} factual signal(s)")
        if r > 0:
            signals.append(f"{r} reasoning signal(s)")
        if o > 0:
            signals.append(f"{o} opinion signal(s)")
        if total == 0:
            return "no signals detected - question unrecognised"
        elif len(signals) == 1 and total == 1:
            return f"{signals[0]} detected - high certainty elimination"
        elif len(signals) == 1:
            return f"multiple {category.lower()} signals - very confident"
        else:
            conflict = " vs ".join(signals)
            return f"conflicting signals: {conflict} - proceeding carefully"

    # Detection with adjustable threshold
    if factual_matches >= threshold and factual_matches >= reasoning_matches and factual_matches >= opinion_matches:
        category = "FACTUAL"
        eliminated = "opinions, explanations, recommendations"
        confidence = round((factual_matches / max(total_matches, 1)) * 100)
        trigger = "factual keyword detected"
    elif reasoning_matches >= threshold and reasoning_matches >= factual_matches and reasoning_matches >= opinion_matches:
        category = "REASONING"
        eliminated = "facts, opinions, recommendations"
        confidence = round((reasoning_matches / max(total_matches, 1)) * 100)
        trigger = "reasoning keyword detected"
    elif opinion_matches >= threshold and opinion_matches >= factual_matches and opinion_matches >= reasoning_matches:
        category = "OPINION"
        eliminated = "facts, dates, names, numbers"
        confidence = round((opinion_matches / max(total_matches, 1)) * 100)
        trigger = "opinion keyword detected"
    else:
        category = "UNKNOWN"
        eliminated = "nothing yet - need more analysis"
        confidence = 0
        trigger = "no clear signal found"

    explanation = explain_confidence(
        category, factual_matches, reasoning_matches, opinion_matches, total_matches
    )

    if confidence < 50:
        safety_status = "WARNING: Low confidence - elimination conservative"
    else:
        safety_status = "Confidence sufficient - elimination proceeding"

    return {
        "category": category,
        "confidence": confidence,
        "explanation": explanation,
        "safety_status": safety_status,
        "eliminated": eliminated,
        "trigger": trigger,
        "attempt": attempt
    }


# Main program
question = input("Ask POEM a question: ")
question = question.lower()

print("\n--- POEM Scanner v0.5 Running ---")

# First attempt - strict threshold
result = run_scanner(question, threshold=1, attempt=1)

# Shadow path - if unknown or low confidence, try again with relaxed threshold
if result["category"] == "UNKNOWN" or result["confidence"] < 50:
    print(f"\nAttempt 1: {result['category']} at {result['confidence']}% confidence")
    print("Shadow path activated - backtracking with relaxed threshold...")

    result2 = run_scanner(question, threshold=0, attempt=2)

    if result2["category"] != "UNKNOWN":
        print(f"Shadow path recovered: {result2['category']} at {result2['confidence']}% confidence")
        result = result2
        result["shadow_path_used"] = True
    else:
        print("Shadow path exhausted - question genuinely ambiguous")
        result["shadow_path_used"] = True
else:
    result["shadow_path_used"] = False

print(f"\nQuestion received:   {question}")
print(f"Trigger signal:      {result['trigger']}")
print(f"Category detected:   {result['category']}")
print(f"Confidence score:    {result['confidence']}%")
print(f"Confidence reason:   {result['explanation']}")
print(f"Safety system:       {result['safety_status']}")
print(f"Shadow path used:    {result['shadow_path_used']}")
print(f"Eliminated:          {result['eliminated']}")
print("Possibility space reduced before deep thinking begins.")
print("\nPOEM v0.5 - Process Of Elimination Master")

# Log entry
log_entry = f"""
---
Timestamp: {datetime.datetime.now()}
Question: {question}
Attempt: {result['attempt']}
Category: {result['category']}
Confidence: {result['confidence']}%
Reason: {result['explanation']}
Shadow Path Used: {result['shadow_path_used']}
Eliminated: {result['eliminated']}
Trigger: {result['trigger']}
Safety: {result['safety_status']}
"""

with open("/Users/paris/wrongness_log.txt", "a") as log:
    log.write(log_entry)

print("Entry recorded to wrongness log.")
