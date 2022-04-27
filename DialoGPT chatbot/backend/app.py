import json

from model import ChatModel

from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"

# Enable cors requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Initiate model
clf = ChatModel()


@app.route("/")
@cross_origin(origin="*")
def index():
    """Check if api is working."""
    return json.dumps({"status": "OK"})


@app.route("/query", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def query():
    """Endpoint for receiving bot response"""
    print(request)
    query = request.json
    print(query)
    conversations = query["lastConversations"]
    # Get dialog in format according to documentation
    # input_data = "    ".join(conversations)
    bot_answer = clf.get_reply(conversations)
    return json.dumps({"botResponse": bot_answer})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=80, debug=True,
    )
