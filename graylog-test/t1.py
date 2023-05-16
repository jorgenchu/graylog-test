from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jorgenchu/Desktop/macC/db/ap_data.db'
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    macs = db.Column(db.String(255))

    def __init__(self, name, macs):
        self.name = name
        self.macs = macs


@app.route('/graylog_alert', methods=['POST'])
def graylog_alert():
    content = request.get_json()
    source = content.get('source')
    event_type = content.get('event_type')
    macs = content.get('mac')

    if source and event_type == 'sta_roam' and macs:
        room = Room.query.filter_by(name=source).first()
        if room:
            room.macs = macs
        else:
            room = Room(name=source, macs=macs)
            db.session.add(room)
        db.session.commit()

    return 'Data received successfully'


@app.route('/')
def index():
    rooms = Room.query.all()
    return render_template('index.html', rooms=rooms)


@app.route('/<name>')
def room_page(name):
    room = Room.query.filter_by(name=name).first()
    macs = room.macs if room else None
    return render_template('room.html', name=name, macs=macs)


if __name__ == '__main__':
    app.run(debug=True)
