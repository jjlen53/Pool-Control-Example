import time

from datetime import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class tempReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.REAL, nullable=False)
    time = db.Column(db.REAL, nullable=False)

    def __repr__(self):
        return f'<Temperature Reading: {self.temperature}F at {datetime.fromtimestamp(self.time)}>'


@app.route('/')
def hello():
    return render_template("index.html", currenttime=datetime.fromtimestamp(time.time()))


@app.route('/recordtemp/<temp>')
def record_temp(temp):
    t = tempReading()
    try:
        t.temperature = float(temp)
    except ValueError:
        t.temperature = 0.0
    t.time = time.time()
    db.session.add(t)
    db.session.commit()
    return f"Got a temperature reading: {t}"

@app.route('/recordtemp/', methods=['GET'])
def record_temp_form():
    t = tempReading()
    try:
        t.temperature = float(request.args.get('temperature'))
    except ValueError:
        t.temperature = 0.0
    t.time = time.time()
    db.session.add(t)
    db.session.commit()
    return f"Got a temperature reading: {t.temperature}"



@app.route('/history')
def show_history():
    history = tempReading.query.all()
    response = "<table>"
    response += f"<tr><th>Temperature</th><th>Time</th></tr>"
    for t in history:
        response += f"<tr><td>{t.temperature}F</td><td>{datetime.fromtimestamp(t.time)}</td></tr>"
    response += "</table>"
    return response


if __name__ == '__main__':
    app.run(port=80)
