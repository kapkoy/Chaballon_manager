from ctypes import sizeof
import json
import os
from webbrowser import get
import globals as var
from modules import api
from warnings import warn

invalid_users = []
invalid_projects = []

def validate_user(user):
    """check if every mandatory elements are in user json file

    Args:
        user (_type_): _description_
    """
    mandatories = ["firstname", "lastname", "mail", "id"]
    for mandatory in mandatories:
        if mandatory not in user:
            warn(f"Invalid user: missing {mandatory} field")
            invalid_users.append(user)


def validate_project(project):
    """check if every mandatory elements are in project json file

    Args:
        project (_type_): _description_
    """
    mandatories = ["id", "time_start", "time_end", "status"]
    for mandatory in mandatories:
        if mandatory not in project:
            warn(f"Invalid project: missing {mandatory} field")
            invalid_projects.append(project) 

def get_infos(path):  
    """getting infos from json file

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        json_path = os.path.join(path, "infos.json")
        with open(json_path, "rb") as f:
            infos = json.load(f)
            f.close()
        return infos
    except Exception as e:
        print(e)
        return None
    
def getProject(proj_id):
    """get project from id

    Args:
        proj_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    for p in var.PROJS:
        if p["id"] == proj_id: 
            return p
    return None

def getUserFromProj(proj):
    """get user from projectid

    Args:
        proj (_type_): _description_

    Returns:
        _type_: _description_
    """
    for u in var.USERS:
        if u["id"] == proj["user_id"]:
            return u
        
def getUserFromID(id):
    for u in var.USERS:
        if u["id"] == id:
            return u
        
def sort_projects(keyword, invert):
    """sort project dict from keyword

    Args:
        keyword (_type_): _description_
        invert (_type_): _description_
    """
    if (keyword == "id"):
        var.PROJS = sorted(var.PROJS, key=lambda x: int(x[keyword]))
    else:
        var.PROJS = sorted(var.PROJS, key=lambda x: str(x[keyword]).lower())
    if invert:
        var.PROJS.reverse()

def getLatestId():
    latest = 1
    for p in var.PROJS:
        if p['id'] > latest:
            latest = p["id"]
    return latest+1

def getOtherUserProjs(user, current_proj):
    print('--------------------------------')
    print(current_proj)
    projs = []
    for p in var.PROJS:
        if p['user_id'] == user["id"]:
            if current_proj != p["id"]:
                this_proj = {"name": p["name"], "id": p["id"]}
                projs.append(this_proj)                
    return projs

def getTodos(proj_path):
    todos = []

    with open(f'{proj_path}\\todos.txt', "r") as f:
        for line in f.readlines():
            print(line)
            todo = {
                "text": line.replace("\\n","").replace("<checked>","").strip(),
                "checked": ("<checked>" in line)
                }
            todos.append(todo)
        f.close()
    return todos


def updateProject(data):
    id = int(data["id"])
    this_proj = getProject(id)

    this_proj["name"] = data['name']
    this_proj["time_start"] = data['start']
    this_proj["time_end"] = data['end']
    api.updateProject(this_proj.copy())
    
def updateStatus(status, proj_id):
    this_proj = getProject(int(proj_id))
    this_proj['status'] = status
    
    api.updateProject(this_proj.copy())    
    
def updatePaid(paid, proj_id):
    this_proj = getProject(int(proj_id))
    this_proj['paid'] = paid
    print(paid)
    api.updateProject(this_proj.copy())    

def updateUser(new, user):
    print(user)
    user["lastname"] = new["lastname"]
    user["firstname"] = new["firstname"]
    user["phone"] = new["phone"]
    user["mail"] = new["mail"]
    user["address"] = new["address"]
    user["id"] = ""
    user["id"] = api.newUserID(user)
    print(user)
    api.updateUser(user)

def build():
    """ builds database from folders
    """
    
    var.USERS = []
    var.PROJS = []
    
    """ build users"""
    for user_folder in os.listdir(var.PROJ_PATH):
        
        # This User
        user_path = os.path.join(var.PROJ_PATH, user_folder)
        print(user_folder)
        if os.path.isdir(user_path):
        
            user = get_infos(user_path)
            user['folder'] = user_folder
            validate_user(user)
            var.USERS.append(user)
                
            for proj_folder in os.listdir(user_path):
                proj_path = os.path.join(user_path, proj_folder)
                
                if os.path.isdir(proj_path):
                    project = get_infos(proj_path)
                    project["name"] = proj_folder
                    project["user"] = f'{user["firstname"]} {user["lastname"]}'
                    project["user_id"] = user["id"]
                    project["folder"] = proj_path
                    project["todos"] = getTodos(proj_path)
                    validate_project(project)
                    
                    var.PROJS.append(project)
                    
            var.PROJS = sorted(var.PROJS, key=lambda d: d['id'])
            var.PROJS.reverse()
          
