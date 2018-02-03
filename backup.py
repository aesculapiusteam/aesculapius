# Makes a backup of DB_FILE in ./backups/ being "." the folder in which this script resides

from os import listdir, remove, makedirs
from os.path import isfile, join, exists, dirname, abspath
from datetime import datetime
from shutil import copyfile

MAX_BACKUP_FILES = 20
DB_FILE = "db.sqlite3"
DB_PATH = dirname(abspath(__file__))
BACKUP_PATH = join(DB_PATH, "backups/")
BACKUP_NAME_FORMAT = "backup_%Y%m%d_%H%M%S.sqlite3"

if not exists(BACKUP_PATH):
    makedirs(BACKUP_PATH)

backup_src = join(DB_PATH, DB_FILE)
backup_dst = join(BACKUP_PATH, datetime.now().strftime(BACKUP_NAME_FORMAT))
previous_backups = [f for f in listdir(BACKUP_PATH) if isfile(join(BACKUP_PATH, f))]

deleted_backup = "" # Stores the deleted backup filename if any

if len(previous_backups) >= MAX_BACKUP_FILES:
    oldest = reduce(lambda x,y: x if datetime.strptime(x, BACKUP_NAME_FORMAT) < datetime.strptime(y, BACKUP_NAME_FORMAT) else y, previous_backups)
    deleted_backup = join(BACKUP_PATH, oldest)
    remove(deleted_backup)

copyfile(backup_src, backup_dst)

print("[ BACKUP ] backuped: {}, deleted: {}".format(backup_dst, deleted_backup or "None"))
