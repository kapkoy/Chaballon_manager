import os

PROJ_PATHS = ["X:/Python/Cha/ClientManager/_files/PROJECTS/clients", "F:/Chaballon/clients", "\\\\CHACHA\clients"]
PROJ_PATH = ""
DOC_PATHS = ["X:/Python/Cha/ClientManager/_files/PROJECTS/documents", "F:/Chaballon/-- Documents"]
DOC_PATH = ""

for path in PROJ_PATHS:
    if os.path.exists(path):
        PROJ_PATH = path
        break
print(PROJ_PATH)    
for path in DOC_PATHS:
    if os.path.exists(path):
        DOC_PATH = path
        break

PROJS = []
USERS = []
STATUS = []
BG_PATH = "static/bg"