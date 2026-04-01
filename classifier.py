# POEM - Classifier v0.1
# First machine learning component
# Learns category patterns from wrongness_log.txt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Step 1 - Load training data from wrongness log
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
        if current_question and current_category:
            questions.append(current_question)
            categories.append(current_category)
            current_question = None
            current_category = None

print(f"Loaded {len(questions)} training examples from wrongness log")
print(f"Categories found: {set(categories)}")

# Step 2 - Build and train the model
model = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB())
])

model.fit(questions, categories)
print("\nPOEM classifier trained successfully")

# Step 3 - Test it on new questions
test_questions = [
    "what is the tallest mountain on earth?",
    "why do humans sleep?",
    "should i learn python or javascript?",
    "where was napoleon born?",
    "how does gravity work?"
]

print("\n--- POEM Classifier Predictions ---")
for q in test_questions:
    prediction = model.predict([q])[0]
    print(f"Q: {q}")
    print(f"A: {prediction}\n")
