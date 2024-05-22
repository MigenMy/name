from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    username = session.get('username', 'Anonymous')
    messages.append({'username': username, 'message': message})
    emit('message', {'username': username, 'message': message}, broadcast=True)

@app.route('/chat')
def chat():
    username = session.get('username', 'Anonymous')
    return render_template('chat.html', username=username, messages=messages)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('chat'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
