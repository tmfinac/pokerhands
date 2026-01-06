from flask import Flask, render_template, redirect, session, url_for, jsonify
from collections import Counter

app = Flask(__name__)
app.secret_key = "super-secret-key"

cards = [
    "1H","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH",
    "1S","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS",
    "1D","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD",
    "1C","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC"
]
def judge_hand(selected):
    if len(selected) != 5:
        return ""
    count = Counter(selected)
    counts = sorted(count.values(), reverse=True)
    if counts == [4,1]:
        return "フォー・オブ・ア・カインド"
    elif counts == [3,2]:
        return "フルハウス"
    elif counts == [3,1,1]:
        return "スリー・オブ・ア・カインド"
    elif counts == [2,2,1]:
        return "ツーペア"
    elif counts == [2,1,1,1]:
        return "ワンペア"
    else:
        return "ハイカード"

@app.route("/")
def index():
    selected = session.get("selected_cards", [])
    result = judge_hand(selected)
    return render_template("index.html", cards=cards, selected=selected, result=result)

# Ajax 用のルート
@app.route("/add_ajax/<card>")
def add_ajax(card):
    if "selected_cards" not in session:
        session["selected_cards"] = []
    if len(session["selected_cards"]) < 5:
        session["selected_cards"].append(card)
        session.modified = True
    result = judge_hand(session["selected_cards"])
    return jsonify({"selected": session["selected_cards"], "result": result})

@app.route("/reset")
def reset():
    session["selected_cards"] = []
    session.modified = True
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
