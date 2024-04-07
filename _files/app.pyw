import logging
from flask import Flask, render_template, send_file, request, make_response
from urllib.parse import quote_plus
import os
import time
from flask_socketio import SocketIO, emit

from modules import db, api, ui
import globals as var


app = Flask(__name__, static_folder='static')
app.jinja_env.filters['quote_plus'] = quote_plus
app.config['FLASK_ENV'] = 'development'
app.config['FLASK_APP'] = "Chaballon Manager"
app.config['FLASK_DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True, async_mode='threading')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)


@socketio.on("refresh_projects")
def refresh_projects():
    socketio.emit("refresh_projs", render_template(
        "projects.html", projects=var.PROJS))


@app.route("/")
def home():
    print("Welcome Chaton <3")
    bg = api.get_random_bg()
    refresh_projects()
    return render_template("index.html", projects=var.PROJS, bg=bg, proj={"status": "Cancel"}, status=var.STATUS)


@socketio.on("first_connect")
def on_connection():
    db.build()
    refresh_projects()


@socketio.on("sort_projects")
def sort_projects(key, invert):
    db.sort_projects(key, invert)
    refresh_projects()


@socketio.on("new_proj_req")
def new_proj_req(proj_id):
    if not proj_id:
        latest = db.getLatestId()
        return render_template("new_proj.html", users=var.USERS, latest=latest, user={}, new=True, proj={})
    else:
        proj = db.getProject(int(proj_id))
        user = db.getUserFromID(proj["user_id"])
        return render_template("new_proj.html", users=var.USERS, user=user, latest=proj_id, new=False, proj=proj)


@socketio.on("new_proj")
def new_proj(data):
    if data["edit"]:
        db.updateProject(data)
        
        if data["new_user"] is not None:
            print("------------------------ NEW USER ---------------------")
            user = db.getUserFromID(db.getProject(int(data["id"]))["user_id"])
            db.updateUser(data["new_user"], user)
        db.build()
    else:
        api.create_project(data)
        
    refresh_projects()
    return view_project(int(data["id"]))



@socketio.on('view_project')
def view_project(proj_id):
    this_proj = db.getProject(proj_id)
    this_user = db.getUserFromProj(this_proj)
    other_p = db.getOtherUserProjs(this_user, proj_id)
    print(this_proj)
    return render_template("viewer.html", proj=this_proj, users=var.USERS, user=this_user, other_p=other_p, status=var.STATUS)


@socketio.on('new_todo')
def new_todo(data, proj_id):
    proj_id = int(proj_id)
    api.updateTodos(data, proj_id)
    return "yeah"


@socketio.on("open_files")
def open_files(id):
    api.openFiles(int(id))


@socketio.on("update_status")
def update_status(status, proj_id):
    db.updateStatus(status, proj_id)
    refresh_projects()
    
@socketio.on("update_paid")
def update_paid(paid, proj_id):
    db.updatePaid(paid, proj_id)
    refresh_projects()
    


@socketio.on("edit_project_req")
def edit_project_req(proj_id):
    return proj_id


if __name__ == "__main__":
    db.build()
    api.getStatus()
    ui.init()
    app.run(threaded=True, host="0.0.0.0", port=8000)
    socketio.run(app, allow_unsafe_werkzeug=True,
                 port=5009, threaded=True)
    
# NTH add sorting when searching ?
# TODO sort by status
# TODO add paid button
