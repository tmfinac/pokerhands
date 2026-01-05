from flask import Flask, render_template, redirect

app = Flask(__name__)

cards = ["1","2","3","4","5","6","7","8","9","10","J","Q","K"]
selected_cards = []

@app.route("/")
def index():
    return render_template(
        "index.html",
        cards=cards,
        selected=selected_cards,
        result=""
    )

@app.route("/add/<card>")
def add(card):
    if len(selected_cards) < 5:
        selected_cards.append(card)
    return redirect("/")

@app.route("/reset")
def reset():
    selected_cards.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
