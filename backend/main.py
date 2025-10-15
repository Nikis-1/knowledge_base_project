from flask import Flask, request, jsonify
from .vector_store import query_pdf_store, load_pdf_to_store


app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = query_pdf_store(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
