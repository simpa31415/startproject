from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Hämta database URL från environment variable (Render sätter DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Skapa tabell
class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

# Route för formulär
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        num = request.form.get("number")
        if num:
            new_num = Number(value=int(num))
            db.session.add(new_num)
            db.session.commit()
        return redirect("/")
    numbers = Number.query.all()
    return render_template("index.html", numbers=numbers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    db.create_all()  # skapar tabeller
    app.run(host="0.0.0.0", port=port)
