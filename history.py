import time, datetime, os, zipfile, sqlite3


TIMESTAMP = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M')
DOWNLOAD_ROOT = 'downloaded/'
DOWNLOAD_FOLDER = 'downloaded/' + TIMESTAMP + '/'
HISTORY_DB = None


def ensure_db():
    global HISTORY_DB
    HISTORY_DB = sqlite3.connect(DOWNLOAD_ROOT + 'history.db')
    cur = HISTORY_DB.cursor()
    result = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='downloads';").fetchall()
    if not result:
        cur.execute('create table downloads(file_id text, folder text, file_name text, modified_date text, download_location text)')
    cur.close()

def close_db():
    if HISTORY_DB:
        HISTORY_DB.close()

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def set_destination(dest='downloaded/'):
    global DOWNLOAD_FOLDER
    global DOWNLOAD_ROOT
    DOWNLOAD_ROOT = dest
    DOWNLOAD_FOLDER = dest + TIMESTAMP + '/'
    ensure_dir(DOWNLOAD_FOLDER)

def is_file_modified( file_id, modified_date ):
    ensure_db()
    cur = HISTORY_DB.cursor()
    result = cur.execute("SELECT max(modified_date) FROM downloads WHERE file_id='" + file_id + "';").fetchall()
    cur.close()
    return not result or result[0][0] < modified_date

def save_file(file_id, folder, file_name, modified_date ,content):
    zipname = DOWNLOAD_FOLDER + file_id + '.zip'
    outzipfile = zipfile.ZipFile(open(zipname,'w'), mode="w")
    outzipfile.writestr(file_name, content)
    outzipfile.close()
    ensure_db()
    cur = HISTORY_DB.cursor()
    cur.execute( "INSERT INTO downloads VALUES ('%s', '%s', '%s', '%s', '%s');" \
                 % (file_id, folder, file_name, modified_date, zipname) )
    cur.close()
    HISTORY_DB.commit()
    return True
