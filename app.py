from flask import Flask, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # セッション用の秘密鍵

cards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


# カード役判定関数（5枚のカード）
def judge_hand(selected):
    if len(selected) != 5:
        return ""

    # 数字カードを変換（J=11, Q=12, K=13）
    values = []
    for c in selected:
        if c == "J":
            values.append(11)
        elif c == "Q":
            values.append(12)
        elif c == "K":
            values.append(13)
        else:
            values.append(int(c))

    values.sort()

    # ペア、スリーカード、フォーカードなどをカウント
    from collections import Counter
    counts = Counter(values)
    count_values = sorted(counts.values(), reverse=True)

    if count_values == [4, 1]:
        return "フォーカード"
    elif count_values == [3, 2]:
        return "フルハウス"
    elif count_values == [3, 1, 1]:
        return "スリーカード"
    elif count_values == [2, 2, 1]:
        return "ツーペア"
    elif count_values == [2, 1, 1, 1]:
        return "ワンペア"
    elif values == list(range(values[0], values[0] + 5)):
        return "ストレート"
    else:
        return "ハイカード（役ではありません）"


@app.route("/")
def index():
    selected = session.get("selected_cards", [])
    result = judge_hand(selected)
    return render_template("index.html", cards=cards, selected=selected, result=result)


@app.route("/add/<card>")
def add(card):
    if "selected_cards" not in session:
        session["selected_cards"] = []
    if len(session["selected_cards"]) < 5:
        session["selected_cards"].append(card)
        session.modified = True
    return redirect("/")


@app.route("/reset")
def reset():
    session["selected_cards"] = []
    session.modified = True
    return redirect("/")


# ローカル起動用
if __name__ == "__main__":
    app.run(debug=True)