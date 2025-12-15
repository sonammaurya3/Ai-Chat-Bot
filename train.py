# train.py
import json
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Download NLTK data (first time only)
nltk.download('punkt')

# Step 1: Load the JSON data
with open("chatbot.json", "r") as file:
    data = json.load(file)

# Step 2: Prepare training data
sentences = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        sentences.append(pattern.lower())
        labels.append(intent["tag"])

# Step 3: Create a model pipeline (TF-IDF + Naive Bayes)
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Step 4: Train the model
model.fit(sentences, labels)

# Step 5: Save the trained model
with open("chatbot_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model training complete! File saved as chatbot_model.pkl")
