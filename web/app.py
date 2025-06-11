#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Update these values with your actual DB instance info
DB_CONFIG = {
    'host': 'YOUR_DB_PRIVATE_IP',
    'user': 'ec2user',
    'password': 'yourpassword',
    'database': 'guestbook'
}

@app.route("/", methods=["GET", "POST"])
def index():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        cursor.execute("INSERT INTO entries (name, message) VALUES (%s, %s)", (name, message))
        conn.commit()

    cursor.execute("SELECT name, message, created_at FROM entries ORDER BY created_at DESC")
    entries = cursor.fetchall()
    conn.close()

    return render_template("index.html", entries=entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)