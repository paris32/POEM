# POEM - Mini Scanner v0.2

question = input("Ask POEM a question: ")
question = question.lower()

# keywords for each category with weighted triggers
factual_words = ["what", "when", "where", "who", "how many"]
reasoning_words = ["why", "how", "explain"]
opinion_words =  ["should", "better", "best", "worst"]

# Count matches for confidence scoring
factual_matches = sum(1 for word in factual_words if word in question)
reasoning_matches = sum(1 for word in reasoning_words if word in question)
opinion_matches = sum(1 for word in opinion_words if word in question)

total_matches = factual_matches + reasoning_matches + opinion_matches

# Scanner elimination logic
print("\n--- POEM Scanner v0.2 Running ---")

if factual_matches > reasoning_matches and factual_matches > opinion_matches:
    category = "FACTUAL"
    eliminated = "opinions, explanations, recommendations"
    confidence = round((factual_matches / max(total_matches, 1)) * 100)
    trigger = "factual keyword detected"

elif reasoning_matches > factual_matches and reasoning_matches > opinion_matches:
    category = "REASONING"
    eliminated = "facts, opinions, recommendations"
    confidence = round((reasoning_matches / max(total_matches, 1)) * 100)
    trigger = "reasoning keyword detected"

elif opinion_matches > factual_matches and opinion_matches > reasoning_matches:
    category = "OPINION"
    eliminated = "facts, dates, names, numbers"
    confidence = round((opinion_matches / max(total_matches, 1)) * 100)
    trigger = "opinion keyword detected"

else:
    category = "UNKNOWN"
    eliminated = "nothing yet - need more analysis"
    confidence = 0
    trigger = "no clear signal found"

# Safety system - low confidence warning
if confidence < 50:
    safety_status = "WARNING: Low confidence - elimination conservative"

else:    
    safety_status = "Confidence sufficient - elimination proceeding"

print(f"Question received: {question}")
print(f"Trigger signal: {trigger}")
print(f"Category detected: {category}")
print(f"Confidence score: {confidence}%")
print(f"Safety system: {safety_status}")
print(f"Eliminated: {eliminated}")
print(f"Possibility space reduced before deep thinking begins.")
print("\nPOEM v0.2 - Process of Elimination Master")