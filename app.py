from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import os

# ---------------- APP CONFIG ----------------

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flowboard'

# SocketIO for Render Deployment
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='gevent'
)

# ---------------- GLOBAL DATA ----------------

MEETING_LINK = "https://meet.google.com/wge-aofy-frc"

projects = []

# ---------------- HOME PAGE ----------------

@app.route('/')
def home():
    return render_template('index.html')

# ---------------- LOGIN PAGE ----------------

@app.route('/login')
def login():
    return render_template('login.html')

# ---------------- LOGIN FUNCTION ----------------

@app.route('/login', methods=['POST'])
def login_post():

    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # ---------------- MANAGER ----------------

    if (
        email == "manager@flowboard.com"
        and password == "manager123"
        and role == "Manager"
    ):
        return redirect('/manager')

    # ---------------- CLIENT ----------------

    elif (
        email == "client@flowboard.com"
        and password == "client123"
        and role == "Client"
    ):
        return redirect('/client')

    # ---------------- TEAM LEADER ----------------

    elif (
        email == "leader@flowboard.com"
        and password == "leader123"
        and role == "Team Leader"
    ):
        return redirect('/teamleader')

    # ---------------- TEAM MEMBER ----------------

    elif (
        email == "team@flowboard.com"
        and password == "team123"
        and role == "Team Member"
    ):
        return redirect('/teammember')

    return "Invalid Login"

# ---------------- CLIENT DASHBOARD ----------------

@app.route('/client')
def client():
    return render_template(
        'client.html',
        projects=projects,
        meeting_link=MEETING_LINK
    )

# ---------------- REGISTER PROJECT PAGE ----------------

@app.route('/register_project')
def register_project():
    return render_template('register_project.html')

# ---------------- SUBMIT PROJECT ----------------

@app.route('/submit_project', methods=['POST'])
def submit_project():

    project = {
        "name": request.form['project'],
        "description": request.form['description'],
        "status": "Pending",
        "assigned": "Not Assigned"
    }

    projects.append(project)

    return redirect('/client')

# ---------------- MANAGER DASHBOARD ----------------

@app.route('/manager')
def manager():
    return render_template(
        'manager.html',
        projects=projects,
        meeting_link=MEETING_LINK
    )

# ---------------- TEAM LEADER DASHBOARD ----------------

@app.route('/teamleader')
def teamleader():
    return render_template(
        'teamleader.html',
        projects=projects,
        meeting_link=MEETING_LINK
    )

# ---------------- TEAM MEMBER DASHBOARD ----------------

@app.route('/teammember')
def teammember():
    return render_template(
        'teammember.html',
        projects=projects,
        meeting_link=MEETING_LINK
    )

# ---------------- ASSIGN PROJECT ----------------

@app.route('/assign/<project_name>')
def assign(project_name):

    for project in projects:

        if project["name"] == project_name:

            project["status"] = "In Progress"
            project["assigned"] = "Team Leader"

    return redirect('/manager')

# ---------------- COMPLETE PROJECT ----------------

@app.route('/complete/<project_name>')
def complete(project_name):

    for project in projects:

        if project["name"] == project_name:

            project["status"] = "Completed"

    return redirect('/teamleader')

# ---------------- DELETE PROJECT ----------------

@app.route('/delete/<project_name>')
def delete(project_name):

    global projects

    projects = [
        project for project in projects
        if project["name"] != project_name
    ]

    return redirect('/manager')

# ---------------- CHAT SYSTEM ----------------

@socketio.on('message')
def handle_message(msg):

    emit('message', msg, broadcast=True)

# ---------------- MAIN ----------------

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    socketio.run(
        app,
        host='0.0.0.0',
        port=port
    )