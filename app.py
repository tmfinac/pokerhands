from flask import Flask, render_template, session, jsonify, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# カードリスト
suits = ['H','D','C','S']
numbers = ['1','2','3','4','5','6','7','8','9','10','J','Q','K']
cards = [num + suit for suit in suits for num in numbers]

# 役判定関数（簡易版）
def judge_hand(selected):
    # とりあえず枚数だけで返す簡易版
    if len(selected) < 5:
        return ""
    # ここに役判定ロジックを実装
    return "役サンプル"

@app.route('/')
def index():
    selected = session.get('selected', [])
    return render_template('index.html', selected=selected, result="", cards=cards)

@app.route('/add_ajax/<card>')
def add_ajax(card):
    if 'selected' not in session:
        session['selected'] = []
    if len(session['selected']) < 5 and card not in session['selected']:
        session['selected'].append(card)
    result = judge_hand(session['selected'])
    return jsonify(selected=session['selected'], result=result)

@app.route('/reset')
def reset():
    session['selected'] = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)