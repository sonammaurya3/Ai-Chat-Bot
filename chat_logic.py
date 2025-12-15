import google.generativeai as genai
import os

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

# Language detection (simple WhatsApp style)
def detect_language(text):
    text = text.lower()

    hinglish_words = ["kya", "kaise", "kyu", "kr", "kro", "muje", "mujhe", "acha", "accha", "hn", "nhi", "tu", "tum"]
    english_words = ["what", "how", "why", "hello", "please", "explain", "help"]

    h_count = sum(w in text for w in hinglish_words)
    e_count = sum(w in text for w in english_words)

    if h_count >= e_count:
        return "hinglish"
    return "english"


def generate_response(user_msg):
    lang = detect_language(user_msg)

    if lang == "hinglish":
        system_prompt = (
            "You are Sonam AI — a cute, friendly WhatsApp-style assistant. "
            "Reply in Hinglish, short, natural, and human-like. "
            "Use light emojis sometimes 😄✨🥰. "
            "Tone should feel like a helpful friend, not too formal, not too robotic. "
            "Keep answers easy, simple, thoda casual."
        )
    else:
        system_prompt = (
            'You are Sonam AI — a friendly assistant. '
            'Reply in simple English, easy to understand, conversational, short, and helpful. '
            'Use 1 simple emoji sometimes, but not too many.'
        )

    prompt = f"{system_prompt}\nUser: {user_msg}\nSonam AI:"

    response = model.generate_content(prompt)

    return response.text


