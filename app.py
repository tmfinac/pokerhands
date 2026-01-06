from flask import Flask, render_template, session, redirect, url_for, jsonify
from flask_session import Session
from collections import Counter

app = Flask(__name__)
app.secret_key = "supersecretkey"

# サーバーサイドセッション設定
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# マークと数字
marks = ["H", "D", "S", "C"]
numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
cards = [m + n for m in marks for n in numbers]

# セッション初期化
def init_session():
    session["selected"] = []
    session["current_mark"] = None

# カードコード → 画像ファイル名
def card_to_filename(card):
    number_map = {"A": "1", "J": "11", "Q": "12", "K": "13"}
    number = number_map.get(card[1:], card[1:])
    return f"{number}{card[0]}.png"

# 役判定
def judge_hand(selected):
    if len(selected) != 5:
        return ""
    suits = [c[0] for c in selected]
    ranks = []
    for c in selected:
        r = c[1:]
        if r == 'J':
            ranks.append(11)
        elif r == 'Q':
            ranks.append(12)
        elif r == 'K':
            ranks.append(13)
        elif r == 'A':
            ranks.append(14)
        else:
            ranks.append(int(r))
    ranks.sort()
    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)
    is_straight = ranks == list(range(ranks[0], ranks[0]+5))
    if set(ranks) == {14,2,3,4,5}:
        is_straight = True
    is_flush = len(set(suits)) == 1

    if is_straight and is_flush and max(ranks) == 14:
        return "ロイヤルストレートフラッシュ"
    if is_straight and is_flush:
        return "ストレートフラッシュ"
    if counts[0] == 4:
        return "フォーカード"
    if counts[0] == 3 and counts[1] == 2:
        return "フルハウス"
    if is_flush:
        return "フラッシュ"
    if is_straight:
        return "ストレート"
    if counts[0] == 3:
        return "スリーカード"
    if counts[0] == 2 and counts[1] == 2:
        return "ツーペア"
    if counts[0] == 2:
        return "ワンペア"
    return "ハイカード"

@app.context_processor
def utility_processor():
    return dict(card_to_filename=card_to_filename)

# ルート
@app.route("/")
def index():
    if "selected" not in session:
        init_session()
    return render_template(
        "index.html",
        marks=marks,
        current_mark=session.get("current_mark"),
        selected=session.get("selected"),
        result=""
    )

# マーク選択
@app.route("/select_mark/<mark>")
def select_mark(mark):
    session["current_mark"] = mark
    mark_cards = [mark + n for n in numbers]
    return render_template(
        "index.html",
        marks=marks,
        current_mark=mark,
        cards=mark_cards,
        selected=session.get("selected"),
        result=""
    )

# Ajaxカード追加
@app.route("/add_ajax/<card>")
def add_ajax(card):
    selected = session.get("selected", [])
    if len(selected) < 5 and card not in selected:
        selected.append(card)
    session["selected"] = selected
    result = judge_hand(selected)
    return jsonify({"selected": selected, "result": result})

# リセット
@app.route("/reset")
def reset():
    init_session()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)