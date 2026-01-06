from flask import Flask, session, render_template, redirect

app = Flask(__name__)
app.secret_key = "your_secret_key"

numbers = ["1","2","3","4","5","6","7","8","9","10","J","Q","K"]
suits = ["♥", "♦", "♠", "♣"]

def judge_hand(cards):
    if len(cards) != 5:
        return ""
    values = [c[:-1] for c in cards]
    counts = {v: values.count(v) for v in set(values)}
    if 3 in counts.values() and 2 in counts.values():
        return "フルハウス"
    elif 3 in counts.values():
        return "スリーカード"
    elif list(counts.values()).count(2) == 2:
        return "ツーペア"
    elif 2 in counts.values():
        return "ワンペア"
    else:
        return "ハイカード"

@app.route("/")
def index():
    selected_cards = session.get("selected_cards", [])
    selected_number = session.get("selected_number")
    result = judge_hand(selected_cards)
    return render_template("index.html",
                           selected_cards=selected_cards,
                           selected_number=selected_number,
                           numbers=numbers,
                           suits=suits,
                           result=result)

@app.route("/select_number/<num>")
def select_number(num):
    session["selected_number"] = num
    return redirect("/")

@app.route("/add_card/<suit>")
def add_card(suit):
    selected_number = session.get("selected_number")
    if not selected_number:
        return redirect("/")
    card = f"{selected_number}{suit}"
    if "selected_cards" not in session:
        session["selected_cards"] = []
    if len(session["selected_cards"]) < 5:
        session["selected_cards"].append(card)
    session["selected_number"] = None
    session.modified = True
    return redirect("/")

@app.route("/reset")
def reset():
    session.pop("selected_cards", None)
    session.pop("selected_number", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
