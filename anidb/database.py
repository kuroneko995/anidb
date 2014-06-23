import sqlite3

class Local_DB(object):
    def __init__(self, file_path = 'local_db.db'):
        '''Load database from file or create new local_db.db in
        current directory
        '''
        self.conn = sqlite3.connect(file_path)
        self.c = conn.cursor()
        
        # Create the anime, episode and file table
        c.execute("CREATE TABLE IF NOT EXISTS anime (aid INTEGER PRIMARY KEY, \
                romanji_name TEXT, episodes NUMBER, year NUMBER, eng_name TEXT,\
                kanji_name TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS episode (eid INTEGER PRIMARY KEY,\
                epno TEXT, eng_name TEXT, romanji_name TEXT, kanji_name TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS file (fid INTEGER PRIMARY KEY, \
                aid INTEGER, eid INTEGER, gid INTEGER, size INTEGER,  \
                ed2k TEXT, md5 TEXT, sha1 TEXT, crc32 TEXT, dub TEXT, \
                sub TEXT, src TEXT, audio TEXT, video TEXT, res TEXT, \
                grp TEXT, type TEXT)")   
        c.execute("CREATE TABLE IF NOT EXISTS job (filename TEXT, fid TEXT, path TEXT,\
                    drive TEXT")