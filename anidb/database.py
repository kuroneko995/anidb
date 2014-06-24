import sqlite3

class Local_DB(object):


    def __init__(self, file_path = 'local_db.db', new = False):
        '''Load database from file or create new local_db.db in
        current directory
        '''
        self.conn = sqlite3.connect(file_path)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        
        
        if new:
            # Create the anime, episode and file table
            self.c.execute("CREATE TABLE IF NOT EXISTS anime (aid INTEGER PRIMARY KEY, \
                    romanji_name TEXT, episodes NUMBER, year NUMBER, eng_name TEXT,\
                    kanji_name TEXT)")
            self.c.execute("CREATE TABLE IF NOT EXISTS episode (eid INTEGER PRIMARY KEY,\
                    epno TEXT, eng_name TEXT, romanji_name TEXT, kanji_name TEXT)")
            self.c.execute("CREATE TABLE IF NOT EXISTS file (fid INTEGER PRIMARY KEY, \
                    aid INTEGER, eid INTEGER, gid INTEGER, size INTEGER,  \
                    ed2k TEXT, md5 TEXT, sha1 TEXT, crc32 TEXT, dub TEXT, \
                    sub TEXT, src TEXT, audio TEXT, video TEXT, res TEXT, \
                    grp TEXT, type TEXT)")   
            self.c.execute("CREATE TABLE IF NOT EXISTS job (filename TEXT, fid INTEGER, folder TEXT,\
                        drive_name TEXT")
        else:
            pass
            
        self.conn.commit()  
      
    def close(self):
        '''Close the database and stop writing. Need to reopen if used again'''
        self.conn.close
       
    def add_anime(self, aid, romanji_name, episodes, year, eng_name, kanji_name):
        '''Add an entry to the anime table. All string must be in unicode'''
        for name in [romanji_name, eng_name, kanji_name]:
            if type(name) != unicode:
                raise Exception('anime table: Unicode name expected')
                return
        
        row = (aid, romanji_name, episodes, year, eng_name, kanji_name)
        self.c.execute("INSERT or IGNORE INTO anime (aid, romanji_name, episodes, year, eng_name, kanji_name) \
        VALUES (?,?,?,?,?,?) ", row)
        self.conn.commit()
            
    def add_episode(self, eid, epno, eng_name, romanji_name, kanji_name):
        '''Add an entry to the episode table. All string must be in unicode'''
        for entry in [epno, eng_name, romanji_name, kanji_name]:
            if type(entry) != unicode:
                raise Exception('episode table: Unicode values expected')
                return
        
        row = (eid, epno, eng_name, romanji_name, kanji_name)
        self.c.execute("INSERT OR IGNORE INTO episode (eid, epno, eng_name, romanji_name, kanji_name) \
                    VALUES (?,?,?,?,?)", row)
        self.conn.commit()
            
    def add_file(self, fid, aid, eid, gid, size, ed2k, md5, sha1, crc32, dub, sub, \
                src, audio, video, res, type, grp):
        '''Add an entry to the file table. All string must be in unicode'''
        for entry in [ed2k, md5, sha1, crc32, dub, sub, src, audio, video, res, type, grp]:
            if type(entry) != unicode:
                raise Exception('episode table: Unicode values expected')
                return
        
        row = (fid, aid, eid, gid, size, ed2k.upper(), md5.upper(), sha1.upper(), crc32.upper(), dub, sub, \
                src, audio, video, res, type, grp)
        c.execute("INSERT OR IGNORE INTO file (fid, aid, eid, gid, size, ed2k, md5, sha1, crc32, dub, sub,  \
                src, audio, video, res, type, grp) VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?)", row)
        self.conn.commit()
    
    def add_job(self, filename, fid, drive_name, folder):
        '''Add an entry to the job table. All string must be in unicode'''
        for entry in [filename, drive_name, folder]:
            if type(entry) != unicode:
                raise Exception('job table: Unicode values expected')
                return
            
        row = (filename, fid, drive, path)
        self.c.execute("INSERT OR IGNORE INTO job (filename, fid, drive_name, folder) \
                    VALUES (?,?,?,?)", row)
        self.conn.commit()
    
    
    def in_db(self, table_name, id):
        '''Check if an entry (anime, episode, file) is in the tables'''
        if table_name not in ['anime','episode','file']:
            raise Exception('Database: Invalid table name. Must be anime, episode or file')
            return False
        else:
            data = (id,)
            if table_name == 'anime':
                self.c.execute('SELECT * FROM anime WHERE aid = ?', data)
            elif table_name == 'episode':
                self.c.execute('SELECT * FROM episode WHERE eid = ?', data)
            elif table_name == 'file':
                self.c.execute('SELECT * FROM file WHERE fid = ?', data)
            else: # This should not happen
                print "in_db: Something has gone wrong"
            
            if self.c.fetchone() == None:
                return False
            else:
                return True
            
    def get_info_aid(self, aid):
        '''Query for anime info based on aid
        Return a dictionary with keys being the column name
        Return blank if aid not found
        '''
        result = {}
        if not self.in_db('anime', aid):
            return result 
        else:
            data = (aid,)
           
            self.c.execute('SELECT * FROM anime WHERE aid = ?', data)
            row = self.c.fetchone()
            keys = row.keys()
            for i in range(len(keys)):
                result[keys[i]] = row[i] 
            return result
                    
    def get_info_eid(self, eid):
        '''Query for anime info based on aid
        Return a dictionary with keys being the column name
        Return blank if aid not found
        '''
        result = {}
        if not self.in_db('episode', eid):
            return result 
        else:
            data = (eid,)
           
            self.c.execute('SELECT * FROM episode WHERE eid = ?', data)
            row = self.c.fetchone()
            keys = row.keys()
            for i in range(len(keys)):
                result[keys[i]] = row[i] 
            return result 
                   
    def get_info_fid(self, fid):
        '''Query for file info based on fid
        Return a dictionary with keys being the column name
        Return blank if aid not found
        '''
        result = {}
        if not self.in_db('file', fid):
            return result 
        else:
            data = (fid,)
           
            self.c.execute('SELECT * FROM file WHERE fid = ?', data)
            row = self.c.fetchone()
            keys = row.keys()
            for i in range(len(keys)):
                result[keys[i]] = row[i] 
            return result 
            
    def get_info_hash(self, size, ed2k):
        '''Query for file info based on fid
        Return a dictionary with keys being the column name
        Return blank if aid not found
        ed2k must be of type unicode
        '''
        result = {}
        data = (size,unicode(ed2k))
        self.c.execute('SELECT * FROM file WHERE (size = ? AND ed2k = ?)', data)
        row = self.c.fetchone()
        if row == None:
            return result
        else:
            keys = row.keys()
            for i in range(len(keys)):
                result[keys[i]] = row[i] 
            return result 