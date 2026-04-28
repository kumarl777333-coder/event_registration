# ⬡ EventHub — Flask Event Registration App

A clean, full-featured event registration web application built with **Python + Flask** and **SQLite**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)

---

## Features

- 📅 **Browse Events** — view all upcoming events with dates, locations & availability
- ✏️ **Create Events** — add title, description, date/time, location, and capacity
- 📝 **Register** — register for any event with name, email & phone
- 🚫 **Duplicate prevention** — one registration per email per event
- 🔴 **Capacity tracking** — real-time spots remaining with sold-out state
- 🗑️ **Delete events** — remove events and all registrations
- 🔌 **REST API** — `/api/events` endpoint returns JSON
- 💾 **SQLite** — zero-config database, works out of the box

---

## Project Structure

```
event_registration/
├── app.py                  # Main Flask application
├── requirements.txt
├── .gitignore
├── README.md
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── create_event.html
    ├── event_detail.html
    └── register.html
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/event-registration.git
cd event-registration
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser. Sample events will be loaded automatically.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key-...` | Flask session secret — **change in production** |
| `DATABASE_URL` | `sqlite:///events.db` | Database connection string |

---

## API

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | List all events |
| `/events/new` | GET/POST | Create a new event |
| `/events/<id>` | GET | Event detail + registrations |
| `/events/<id>/register` | GET/POST | Register for an event |
| `/events/<id>/delete` | POST | Delete an event |
| `/api/events` | GET | JSON list of all events |

---

## Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: Jinja2 templates, vanilla CSS & JS
- **Fonts**: DM Serif Display + DM Sans (Google Fonts)

---

## License

MIT — free to use and modify.
