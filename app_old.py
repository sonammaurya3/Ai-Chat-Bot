from flask import Flask, request, jsonify, render_template
import wikipedia

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    query = data.get('message')

    if not query:
        return jsonify({'reply': "Please ask something."})

    try:
        # Get summary of the query from Wikipedia (2 sentences)
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
        reply = summary
    except wikipedia.exceptions.DisambiguationError as e:
        # If multiple options, suggest first 3
        options = e.options[:3]
        reply = f"Your query is ambiguous. Did you mean: {', '.join(options)}?"
    except wikipedia.exceptions.PageError:
        reply = "Sorry, I couldn't find any information on that topic."
    except Exception:
        reply = "Sorry, something went wrong."

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)

