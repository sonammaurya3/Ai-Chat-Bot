from flask import Flask, request, jsonify, render_template
import wikipedia
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

# Load SerpAPI key from .env
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

app = Flask(__name__)

def is_hindi(text):
    """Detect if text contains Hindi characters"""
    return any("\u0900" <= c <= "\u097F" for c in text)

def search_google(query, lang="en"):
    """Fallback search using SerpAPI"""
    try:
        params = {
            "engine": "google",
            "q": query,
            "hl": lang,
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if "organic_results" in results and len(results["organic_results"]) > 0:
            snippet = results["organic_results"][0].get("snippet")
            if snippet:
                return snippet
        return None
    except Exception as e:
        print("Google search error:", e)
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    
    # Detect language
    if is_hindi(user_msg):
        wikipedia.set_lang("hi")
        lang = "hi"
    else:
        wikipedia.set_lang("en")
        lang = "en"
    
    # Try Wikipedia first
    try:
        search_results = wikipedia.search(user_msg)
        if search_results:
            page = wikipedia.page(search_results[0])
            answer = page.summary[:500]  # first 500 chars
        else:
            answer = None
    except Exception as e:
        print("Wikipedia error:", e)
        answer = None
    
    # Fallback to Google
    if not answer:
        answer = search_google(user_msg, lang=lang)
    
    # Final fallback message
    if not answer:
        answer = "Sorry, I couldn't find a reliable answer. 🙁"
    
    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(debug=True)


