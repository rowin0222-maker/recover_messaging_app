from flask import Flask, render_template, jsonify, request
from models import db, Message
import os

# Define base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Create the app
app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return render_template("recover.html")

@app.route("/messages")
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    data = [
        {
            "dir": m.direction,
            "text": m.text,
            "time": m.timestamp.strftime("%Y-%m-%d %H:%M")
        }
        for m in messages
    ]
    return jsonify(data)

@app.route("/api/add", methods=["POST"])
def add_message():
    data = request.json
    msg = Message(direction=data["dir"], text=data["text"])
    db.session.add(msg)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/delete/<int:id>", methods=["POST"])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    msg.deleted = True
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)