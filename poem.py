# POEM v1.0
# Process Of Elimination Master
# First Complete Reductive Inference Model
# Scanner + Classifier working as one system

import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ─────────────────────────────────────────
# COMPONENT 1: TRAIN THE CLASSIFIER
# Learns from wrongness log automatically
# ─────────────────────────────────────────

def train_classifier():
    questions = []
    categories = []

    with open("/Users/paris/wrongness_log.txt", "r") as log:
        lines = log.readlines()

    current_question = None
    current_category = None

    for line in lines:
        line = line.strip()
        if line.startswith("Question:"):
            current_question = line.replace("Question:", "").strip()
        elif line.startswith("Category:"):
            current_category = line.replace("Category:", "").strip()
            if current_question and current_category != "UNKNOWN":
                questions.append(current_question)
                categories.append(current_category)
                current_question = None
                current_category = None

    model = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("classifier", MultinomialNB())
    ])

    model.fit(questions, categories)
    return model, len(questions)

# ─────────────────────────────────────────
# COMPONENT 2: THE SCANNER
# Fast first-pass elimination
# ─────────────────────────────────────────

def run_scanner(question, threshold=1, attempt=1):
    factual_words = ["what", "when", "where", "who", "how many", "is "]
    reasoning_words = ["why", "how", "explain"]
    opinion_words = ["should", "better", "best", "worst"]

    factual_matches = sum(1 for word in factual_words if word in question)
    reasoning_matches = sum(1 for word in reasoning_words if word in question)
    opinion_matches = sum(1 for word in opinion_words if word in question)
    total_matches = factual_matches + reasoning_matches + opinion_matches

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
        eliminated = "nothing yet"
        confidence = 0
        trigger = "no clear signal found"

    return {
        "category": category,
        "confidence": confidence,
        "eliminated": eliminated,
        "trigger": trigger,
        "attempt": attempt
    }

# ─────────────────────────────────────────
# COMPONENT 3: ANSWER SHAPE DETECTOR
# ─────────────────────────────────────────

def detect_answer_shape(category, question):
    number_hints = ["how many", "how much", "what year",
                    "how long", "how far", "when "]
    name_hints = ["who", "which person", "what person"]
    place_hints = ["where", "what city", "what country"]
    yesno_starters = ["is ", "are ", "was ", "were ",
                      "did ", "does ", "do ", "can ",
                      "could ", "would ", "should "]

    question_start = question.strip()

    if any(hint in question for hint in number_hints):
        return {"shape": "NUMBER/DATE", "eliminated_shapes": "names, places, yes/no, explanations"}
    elif any(hint in question for hint in name_hints):
        return {"shape": "PERSON NAME", "eliminated_shapes": "numbers, places, yes/no, explanations"}
    elif any(hint in question for hint in place_hints):
        return {"shape": "PLACE NAME", "eliminated_shapes": "numbers, names, yes/no, explanations"}
    elif any(question_start.startswith(s) for s in yesno_starters):
        return {"shape": "YES/NO", "eliminated_shapes": "numbers, names, places, explanations"}
    elif category == "REASONING":
        return {"shape": "EXPLANATION", "eliminated_shapes": "numbers, names, places, yes/no"}
    elif category == "OPINION":
        return {"shape": "RECOMMENDATION", "eliminated_shapes": "numbers, facts, dates, names"}
    else:
        return {"shape": "GENERAL", "eliminated_shapes": "nothing additional"}

# ─────────────────────────────────────────
# POEM v1.0 — MAIN SYSTEM
# ─────────────────────────────────────────

print("POEM v1.0 - Process Of Elimination Master")
print("Initialising...\n")

# Train classifier from wrongness log
classifier, training_count = train_classifier()
print(f"Classifier trained on {training_count} examples")
print("Scanner ready")
print("System online\n")

question = input("Ask POEM a question: ")
question_lower = question.lower()

print("\n--- POEM v1.0 Running ---")

# Stage 1 — Scanner first pass
scanner_result = run_scanner(question_lower, threshold=1, attempt=1)
classifier_used = False
shadow_path_used = False

# Stage 2 — If scanner uncertain, ask classifier
if scanner_result["confidence"] < 50 or scanner_result["category"] == "UNKNOWN":
    print(f"Scanner confidence: {scanner_result['confidence']}% — consulting classifier...")
    
    classifier_prediction = classifier.predict([question_lower])[0]
    classifier_used = True
    
    # Shadow path — try scanner again with relaxed threshold
    shadow_result = run_scanner(question_lower, threshold=0, attempt=2)
    shadow_path_used = True
    
    # Use classifier prediction as final category
    final_category = classifier_prediction
    final_confidence = 75
    final_trigger = f"classifier override — scanner was uncertain"
    final_eliminated = scanner_result["eliminated"]
    
    print(f"Classifier prediction: {classifier_prediction}")
    print(f"Shadow path attempted: yes")

else:
    final_category = scanner_result["category"]
    final_confidence = scanner_result["confidence"]
    final_trigger = scanner_result["trigger"]
    final_eliminated = scanner_result["eliminated"]

# Stage 3 — Answer shape detection
shape = detect_answer_shape(final_category, question_lower)

# Stage 4 — Safety assessment
if final_confidence < 50:
    safety = "WARNING: Low confidence — minimal elimination"
else:
    safety = "Confidence sufficient — elimination proceeding"

# Final output
print(f"\nQuestion:          {question}")
print(f"Category:          {final_category}")
print(f"Confidence:        {final_confidence}%")
print(f"Trigger:           {final_trigger}")
print(f"Safety:            {safety}")
print(f"Classifier used:   {classifier_used}")
print(f"Shadow path used:  {shadow_path_used}")
print(f"Eliminated:        {final_eliminated}")
print(f"Answer shape:      {shape['shape']}")
print(f"Shape eliminated:  {shape['eliminated_shapes']}")
print("\nPossibility space reduced before deep thinking begins.")
print("POEM v1.0 - Process Of Elimination Master")

# Log everything
log_entry = f"""
---
Timestamp: {datetime.datetime.now()}
Version: POEM v1.0
Question: {question}
Final Category: {final_category}
Confidence: {final_confidence}%
Trigger: {final_trigger}
Classifier Used: {classifier_used}
Shadow Path Used: {shadow_path_used}
Eliminated: {final_eliminated}
Shape: {shape['shape']}
Shape Eliminated: {shape['eliminated_shapes']}
Safety: {safety}
"""

with open("/Users/paris/wrongness_log.txt", "a") as log:
    log.write(log_entry)

print("\nEntry recorded to wrongness log.")
