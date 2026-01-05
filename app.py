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
    .slots, .cards { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
    .card {
      width: 70px; height: 100px;
      border-radius: 8px;
      cursor: pointer;
      box-shadow: 2px 2px 6px rgba(0,0,0,0.25);
    }
    .slot {
      background: #eaeaea;
    }
    .result { font-size: 22px; font-weight: bold; margin-top: 20px; }
  </style>
</head>
<body>
<h1>5カードポーカー役判定</h1>

<!-- 選択されたカード -->
<div class="slots">
  {% for i in range(5) %}
    <img class="card slot" id="slot{{i}}" />
  {% endfor %}
</div>

<!-- トランプ画像カード -->
<div class="cards">
  {% for c in cards %}
    <img class="card" src="{{ url_for('static', filename='cards/' + c + '.png') }}"
         onclick="addCard('{{c}}')" />
  {% endfor %}
</div>

<div class="result" id="result"></div>

<script>
let slots = [];

function addCard(card) {
  if (slots.length >= 5) return;
  slots.push(card);

  const img = document.getElementById('slot' + (slots.length - 1));
  img.src = '/static/cards/' + card + '.png';

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

# PNGファイル名に対応するランク
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
