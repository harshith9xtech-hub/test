from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def hello():
    return jsonify(
        message="✨ Welcome to Cloud with Harshith Lets GO build the pipeline ✨",
        tip="Built with Flask, shipped by Jenkins, running in Docker.",
        UI="this is my new ui"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
