from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def hello():
    return jsonify(
        message="🚀 FEATURE BRANCH UI UPDATE BY HARSHITH",
        status="Feature branch is running",
        new_ui="✨ DARK MODE ENABLED (SIMULATED)",
        version="feature/ui-v1"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
