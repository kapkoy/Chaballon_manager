import os
import globals as var
from modules import db
import random, json
import subprocess
import openpyxl

def get_random_bg():
    return random.choice(os.listdir(var.BG_PATH))

def newUserID(user):
    fname_split = user['firstname'].split(' ')
    if len(fname_split) == 1:
        fname_split = fname_split[0].split('-')
    if len(fname_split) > 1:
        fname_init = fname_split[0][0].upper() + fname_split[1][0].upper()
    else:
        fname_init = fname_split[0][0].upper() + fname_split[0][1].upper()

    id = fname_init + user['lastname'][0].upper()
    
    nb_init = 0
    for u in var.USERS:
        if id in u['id']:
            nb_init = max(nb_init, int(u['id'][3:]))
    nb_init += 1
    id += str(nb_init).zfill(2)
    return id


def createUser(new_user):
    folder = new_user['firstname'] + " " + new_user['lastname']
    user_path = os.path.normpath(os.path.join(var.PROJ_PATH, folder))
    
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    id = newUserID(new_user)
    user = {
        "lastname": new_user['astlname'],
        "firstname": new_user['firstname'],
        "mail": new_user['mail'],
        "phone": new_user['phone'],
        "id": id
    }
    with open(user_path+"\\infos.json", "w", encoding='utf-8') as f:
        json.dump(user, f, indent=4)
        f.close()
    user['folder'] = user["firstname"] + " " + user['lastname']
    var.USERS.append(user)
    
    return user

def create_devis(proj):

    # Load the workbook
    workbook = openpyxl.load_workbook(os.path.join(var.DOC_PATH, "DEVIS_TEMPLATE.xlsx"))

    worksheet = workbook.active

    proj_name = "B2"
    clientid = "I6"
    projid = "I5"
    
    worksheet[proj_name] = proj['name']
    worksheet[clientid] = proj['user_id']
    worksheet[projid] = str(proj['id']).zfill(5)
    
    devis_name = f"DEVIS_{str(proj['id']).zfill(5)}_{proj['user_id']}.xlsx"
    workbook.save(os.path.join(proj["folder"], devis_name))
        

def create_project(data):
    project = {
        'time_start': data['start'],
        'time_end': data['end'],
        'status': 'Devis',
        'id': db.getLatestId(),
    }
    
    if data['new_user'] is not None:
        user = createUser(data['new_user'])
    else:
        user = db.getUserFromID(data["user"])
    
    #Creating project folder
    project_path = os.path.normpath(os.path.join(var.PROJ_PATH, user['folder'], data['name']))
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    # Creating Cha Assets folders
    os.mkdir(project_path + '/ProjectFiles')
    os.makedirs(project_path + '/Exports/ExportsFinaux')
    os.mkdir(project_path + '/Assets')


    # Writing project data to project.json
    with open(f'{project_path}\\infos.json', 'w', encoding='utf-8') as file:
        json.dump(project, file, indent=4)
        file.close()
        
    with open(f'{project_path}\\todos.txt', 'w') as f:
        f.close()

    # Added additional datas for the software not worth storing to disk
    project['user'] = user["firstname"] + ' ' + user["lastname"]
    project['user_id'] = user["id"]
    project['name'] = data['name']
    project['folder'] = project_path

    create_devis(project)
    var.PROJS.append(project)
    
def openFiles(id):
    proj = db.getProject(id)
    path = os.path.join(var.PROJ_PATH, proj['user'], proj['name']).replace('/', '\\')
    subprocess.Popen('explorer /n,"' + path +'"')
    
def updateTodos(data, proj_id):
    proj = db.getProject(proj_id)
    new_proj = proj
    new_proj['todos'] = data
    var.PROJS[var.PROJS.index(proj)] = new_proj
    
    with open(f"{proj['folder']}\\todos.txt", "w", encoding="utf-8") as f:
        txt = ""
        for todo in data:
            txt += todo["text"]
            if todo["checked"]:
                txt += "<checked>"
            txt += "\n"
        f.write(txt)
        f.close()
            

def getStatus():
    stats = []
    for stat_file in os.listdir("static/logos"):
        stat = {}
        print(stat_file)
        stat["id"] = int(stat_file.split("Logo_Status_")[1].split("_")[1].split(".")[0])
        stat["name"] = stat_file.split("Logo_Status_")[1].split("_")[0]
        stat["file"] = stat_file
        stats.append(stat)
    
    var.STATUS = sorted(stats, key=lambda x: x["id"])
    
def updateProject(proj):
    this_proj = {
        "id": proj["id"],
        "time_start": proj["time_start"],
        "time_end": proj["time_end"],
        "status": proj["status"],
        "paid": proj["paid"]
    }
    user_folder = os.path.join(var.PROJ_PATH, db.getUserFromProj(proj)["folder"])
    old_path = proj['folder']
    new_path = os.path.join(user_folder, proj['name'])
    file_path = os.path.join(old_path, "infos.json")
    
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(this_proj, f, indent=4)
        f.close()
    
    os.rename(old_path, new_path)
    
def updateUser(user):
    this_user = {
        "lastname": user["lastname"],
        "firstname": user["firstname"],
        "phone": user["phone"],
        "mail": user["mail"],
        "address": user["address"],
        "id": user["id"]
    }
    
    user_folder = os.path.join(var.PROJ_PATH, user["folder"])
    new_path = os.path.join(var.PROJ_PATH, f'{user["firstname"]} {user["lastname"]}')
    file_path = os.path.join(user_folder, "infos.json")
    
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(this_user, f, indent=4)
        f.close()
    
    os.rename(user_folder, new_path)