from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>5カードポーカー役判定</title>
  <style>
    body { font-family: system-ui, sans-serif; padding: 20px; }
    .slots, .cards { display: flex; gap: 12px; margin-bottom: 20px; }
    .card {
      width: 70px; height: 100px;
      border: 2px solid #222;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      font-weight: bold;
      background: white;
      cursor: pointer;
      box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    }
    .slot {
      background: #f0f0f0;
      cursor: default;
    }
    .result { font-size: 22px; font-weight: bold; margin-top: 20px; }
  </style>
</head>
<body>
<h1>5カードポーカー役判定</h1>

<!-- 選択されたカード表示 -->
<div class="slots">
  {% for i in range(5) %}
    <div class="card slot" id="slot{{i}}"></div>
  {% endfor %}
</div>

<!-- トランプカード（ランク） -->
<div class="cards">
  {% for c in cards %}
    <div class="card" onclick="addCard('{{c}}')">{{c}}</div>
  {% endfor %}
</div>

<div class="result" id="result"></div>

<script>
let slots = [];

function addCard(card) {
  if (slots.length >= 5) return;
  slots.push(card);
  document.getElementById('slot' + (slots.length - 1)).innerText = card;

  if (slots.length === 5) {
    fetch('/judge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cards: slots })
    })
    .then(r => r.json())
    .then(d => {
      document.getElementById('result').innerText = d.result;
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


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
