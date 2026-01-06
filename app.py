from flask import Flask, render_template, redirect, session, url_for, jsonify
from collections import Counter

app = Flask(__name__)
app.secret_key = "super-secret-key"

cards = ["1","2","3","4","5","6","7","8","9","10","J","Q","K"]

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
