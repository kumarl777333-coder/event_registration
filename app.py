from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ─── Models ────────────────────────────────────────────────────────────────────

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')

    @property
    def spots_left(self):
        return self.capacity - len(self.registrations)

    @property
    def is_full(self):
        return self.spots_left <= 0

    def __repr__(self):
        return f'<Event {self.title}>'


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.name} for Event {self.event_id}>'


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('index.html', events=events)


@app.route('/events/new', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            event_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

            event = Event(
                title=request.form['title'],
                description=request.form['description'],
                date=event_date,
                location=request.form['location'],
                capacity=int(request.form['capacity']),
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error creating event: {str(e)}', 'danger')
    return render_template('create_event.html')


@app.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    registrations = Registration.query.filter_by(event_id=event_id).all()
    return render_template('event_detail.html', event=event, registrations=registrations)


@app.route('/events/<int:event_id>/register', methods=['GET', 'POST'])
def register(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        email = request.form['email']
        existing = Registration.query.filter_by(email=email, event_id=event_id).first()
        if existing:
            flash('You are already registered for this event.', 'warning')
            return redirect(url_for('event_detail', event_id=event_id))
        if event.is_full:
            flash('Sorry, this event is fully booked.', 'danger')
            return redirect(url_for('event_detail', event_id=event_id))
        try:
            reg = Registration(
                name=request.form['name'],
                email=email,
                phone=request.form.get('phone', ''),
                event_id=event_id,
            )
            db.session.add(reg)
            db.session.commit()
            flash(f'Successfully registered for "{event.title}"!', 'success')
            return redirect(url_for('event_detail', event_id=event_id))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
    return render_template('register.html', event=event)


@app.route('/events/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('index'))


@app.route('/api/events')
def api_events():
    events = Event.query.order_by(Event.date.asc()).all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'date': e.date.isoformat(),
        'location': e.location,
        'capacity': e.capacity,
        'spots_left': e.spots_left,
    } for e in events])


# ─── Init ──────────────────────────────────────────────────────────────────────

def seed_data():
    """Add sample events if the DB is empty."""
    if Event.query.count() == 0:
        samples = [
            Event(title='Tech Summit 2026', description='Annual technology conference featuring AI, cloud, and DevOps talks.', date=datetime(2026, 6, 15, 9, 0), location='Hyderabad Convention Centre', capacity=200),
            Event(title='Python Workshop', description='Hands-on workshop for beginners learning Python from scratch.', date=datetime(2026, 5, 20, 10, 0), location='JNTU Kakinada', capacity=50),
            Event(title='Startup Pitch Night', description='Local startups pitch their ideas to investors and the community.', date=datetime(2026, 7, 4, 18, 0), location='T-Hub, Hyderabad', capacity=100),
        ]
        db.session.add_all(samples)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
