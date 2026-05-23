#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    es = Event.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'location': e.location
    } for e in es]), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    e = Event.query.get(id)
    if not e:
        return jsonify({'error': 'Event not found'}), 404
    
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'start_time': s.start_time.isoformat()
    } for s in e.sessions]), 200


@app.route('/speakers')
def get_speakers():
    sp=Speaker.query.all()
    return jsonify([{
        'id':s.id,
        'name':s.name
    }for s in sp]),200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    sp=Speaker.query.get(id)
    if not sp:
        return jsonify({'error':'Speaker not found'}),404
    bt=sp.bio.bio_text if sp.bio else "No bio available"
    return jsonify({
        'id':sp.id,
        'name':sp.name,
        'bio_text':bt
    }),200
    


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    ss = Session.query.get(id)
    if not ss:
        return jsonify({'error': 'Session not found'}), 404

    return jsonify([{
        'id': s.id,
        'name': s.name,
        'bio_text': s.bio.bio_text if s.bio else "No bio available"
    } for s in ss.speakers]), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)