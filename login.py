from flask import Flask, request, jsonify
import jwt
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

secret_key = "12345678901234567890"


@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = db.cursor()
    cursor.execute(
        "SELECT id, email FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    print(cursor)

    if user:
        payload = {"id": user[0]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Login gagal"}), 401


if __name__ == '__main__':
    app.run(debug=True)
