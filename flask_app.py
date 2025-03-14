from flask import Flask, request, jsonify
from llm_response import LLMGenerator

app = Flask(__name__)
llm = LLMGenerator()

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    query = data.get("query", "")
    response = llm.generate_response(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
