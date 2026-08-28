from flask import Flask, request

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()

    print("Received:", data)

    return {"status": "ok"}


app.run(host="0.0.0.0", port=5000)

#WORKING properly 