from flask import Flask, render_template, redirect, session, url_for, jsonify
from collections import Counter

app = Flask(__name__)
app.secret_key = "super-secret-key"

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["♠", "♥", "♦", "♣"]  # HTML上で表示
cards = [n + s for n in numbers for s in suits]

num_order = {n: i for i, n in enumerate(numbers, start=1)}


def judge_hand(selected):
    if len(selected) != 5:
        return ""

    nums = [card[:-1] for card in selected]
    suits_list = [card[-1] for card in selected]

    counts = Counter(nums)
    counts_values = sorted(counts.values(), reverse=True)

    is_flush = len(set(suits_list)) == 1
    num_indices = sorted([num_order[n] for n in nums])
    is_straight = all(num_indices[i] - num_indices[i - 1] == 1 for i in range(1, 5))

    if is_straight and is_flush:
        return "ストレートフラッシュ"
    elif counts_values == [4, 1]:
        return "フォー・オブ・ア・カインド"
    elif counts_values == [3, 2]:
        return "フルハウス"
    elif is_flush:
        return "フラッシュ"
    elif is_straight:
        return "ストレート"
    elif counts_values == [3, 1, 1]:
        return "スリー・オブ・ア・カインド"
    elif counts_values == [2, 2, 1]:
        return "ツーペア"
    elif counts_values == [2, 1, 1, 1]:
        return "ワンペア"
    else:
        return "ハイカード"


@app.route("/")
def index():
    selected = session.get("selected_cards", [])
    result = judge_hand(selected)
    return render_template("index.html", cards=cards, selected=selected, result=result)


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