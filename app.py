from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# ---------------------------
# MongoDB Atlas Configuration
# ---------------------------
MONGO_URI = "mongodb+srv://dbusername:password@database.5mgbzog.mongodb.net/?appName=Database"

client = MongoClient(MONGO_URI)
db = client["mydatabase"]
collection = db["users"]

# API Route - Reads from backend file
@app.route("/api", methods=["GET"])
def get_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Frontend Form Route
@app.route("/")
def home():
    return render_template("form.html")

# Form Submission Route
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    try:
        if not name or not email:
            raise Exception("All fields are required!")

        data = {
            "name": name,
            "email": email
        }

        collection.insert_one(data)

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("form.html", error=str(e))

# Success Page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
