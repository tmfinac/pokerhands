from flask import Flask, render_template, session, redirect, url_for, jsonify
from flask_session import Session
from collections import Counter
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"

# サーバーサイドセッション設定
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# 全マーク・カードのリスト
marks = ["H", "D", "S", "C"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
cards = [m + n for m in marks for n in numbers]

# 初期化関数
def init_session():
    session["selected"] = []
    session["current_mark"] = None


# カードから画像ファイル名を作成
def card_filename(card):
    """カード文字列からPNGファイル名を返す"""
    mark = card[0]
    rank = card[1:]
    rank_map = {'A':'1','J':'11','Q':'12','K':'13'}
    rank_num = rank_map.get(rank, rank)
    return f"{rank_num}{mark}.png"

# テンプレートで使えるように登録
app.jinja_env.globals.update(card_filename=card_filename)


# 役判定関数
def judge_hand(selected):
    if len(selected) != 5:
        return ""
    suits = [card[0] for card in selected]
    ranks = []
    for card in selected:
        r = card[1:]
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
        cards=[],
        result=""
    )

# マーク選択
@app.route("/select_mark/<mark>")
def select_mark(mark):
    session["current_mark"] = mark
    mark_cards = [mark + n for n in numbers]
    # キャッシュ回避用に timestamp 付与
    mark_cards_images = [
        url_for('static', filename='cards/' + card_filename(card), t=int(time.time()))
        for card in mark_cards
    ]
    return render_template("index.html",
                           marks=marks,
                           current_mark=mark,
                           cards=mark_cards,
                           cards_images=mark_cards_images,
                           selected=session.get("selected"),
                           result="")

# カード選択（Ajax）
@app.route("/add_ajax/<card>")
def add_ajax(card):
    selected = session.get("selected", [])
    if len(selected) < 5 and card not in selected:
        selected.append(card)
    session["selected"] = selected
    result = judge_hand(selected)
    # 画像URLを追加（キャッシュ対策）
    selected_imgs = [url_for('static', filename=f'cards/{card_to_filename(c)}', t=int(time.time())) for c in selected]
    return jsonify({"selected": selected, "result": result, "selected_imgs": selected_imgs})

# リセット
@app.route("/reset")
def reset():
    init_session()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)