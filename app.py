from flask import Flask, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # セッションに必要

cards = ["1","2","3","4","5","6","7","8","9","10","J","Q","K"]

@app.route("/")
def index():
    selected = session.get("selected_cards", [])
    return render_template(
        "index.html",
        cards=cards,
        selected=selected
    )

@app.route("/add/<card>")
def add(card):
    if "selected_cards" not in session:
        session["selected_cards"] = []
    if len(session["selected_cards"]) < 5:
        session["selected_cards"].append(card)
        session.modified = True
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session["selected_cards"] = []
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

