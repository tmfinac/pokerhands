from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>5カードポーカー役判定</title>
</head>
<body>
<h1>5カードポーカー役判定</h1>

<div id="slots"></div>

<div>
  {% for c in cards %}
    <button onclick="addCard('{{c}}')">{{c}}</button>
  {% endfor %}
</div>

<p id="result"></p>

<script>
let slots = [];

function addCard(card) {
  if (slots.length >= 5) return;
  slots.push(card);
  document.getElementById("slots").innerText = slots.join(" ");

  if (slots.length === 5) {
    fetch("/judge", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({cards: slots})
    }).then(r => r.json()).then(d => {
      document.getElementById("result").innerText = d.result;
    });
  }
}
</script>
</body>
</html>
"""

RANKS = [str(n) for n in range(1, 11)] + ["J", "Q", "K"]

@app.route("/")
def index():
    return render_template_string(HTML, cards=RANKS)

@app.route("/judge", methods=["POST"])
def judge():
    cards = request.json["cards"]
    return jsonify(result=judge_hand(cards))

def judge_hand(cards):
    from collections import Counter
    counts = sorted(Counter(cards).values(), reverse=True)

    if counts == [4, 1]:
        return "フォーカード"
    if counts == [3, 2]:
        return "フルハウス"
    if counts == [3, 1, 1]:
        return "スリーカード"
    if counts == [2, 2, 1]:
        return "ツーペア"
    if counts == [2, 1, 1, 1]:
        return "ワンペア"
    return "役ではありません"

if __name__ == "__main__":
    app.run()