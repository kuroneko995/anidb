import sqlite3
from datetime import datetime
import time

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
                    aid INTEGER, epno TEXT, eng_name TEXT, romanji_name TEXT, \
                    kanji_name TEXT)")
            self.c.execute("CREATE TABLE IF NOT EXISTS file (fid INTEGER PRIMARY KEY, \
                    aid INTEGER, eid INTEGER, gid INTEGER, size INTEGER,  \
                    ed2k TEXT, md5 TEXT, sha1 TEXT, crc32 TEXT, dub TEXT, \
                    sub TEXT, src TEXT, audio TEXT, video TEXT, res TEXT, \
                    grp TEXT, file_type TEXT)")   
            self.c.execute("CREATE TABLE IF NOT EXISTS job (filename TEXT, fid INTEGER, folder TEXT,\
                        drive_name TEXT, last_checked DATETIME)")
        else:
            pass
            
        self.conn.commit()  
      
    def close(self):
        '''Close the database and stop writing. Need to reopen if used again'''
        self.conn.close()
       
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
                src, audio, video, res, file_type, grp):
        '''Add an entry to the file table. All string must be in unicode'''
        
        for entry in [ed2k, md5, sha1, crc32, dub, sub, src, audio, video, res, file_type, grp]:
            if type(entry) != unicode:
                raise Exception('episode table: Unicode values expected')
                return
        
        row = (fid, aid, eid, gid, size, ed2k, md5, sha1, crc32, dub, sub, \
                src, audio, video, res, file_type, grp)
        self.c.execute("INSERT OR IGNORE INTO file (fid, aid, eid, gid, size, ed2k, md5, sha1, crc32, dub, sub,  \
                src, audio, video, res, file_type, grp) VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?)", row)
        
        self.conn.commit()
    
    def add_job(self, filename, fid, drive_name, folder):
        '''Add an entry to the job table. All string must be in unicode'''
        for entry in [filename, drive_name, folder]:
            if type(entry) != unicode:
                raise Exception('job table: Unicode values expected')
                return
            
        ctime = datetime.utcnow()
        ctime = ctime.replace(microsecond = 0)
        ctime = ctime.isoformat().replace('T', ' ')
        
        row = (filename, fid, drive_name, folder, ctime)
        self.c.execute("INSERT OR IGNORE INTO job (filename, fid, drive_name, folder, last_checked) \
                    VALUES (?,?,?,?,?)", row)
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
            
    def get_info_filename(self, filename, size=0, crc32=""):
        '''Query for fid based on filename
        If file name is not unicode will return blank
        Recommend checking crc32 and size'''
        if type(filename) != unicode:
            raise Exception('Filename must be unicode')
            return {}
        else:
            if not (size and crc32): # Search using filename only
                result = {}
                data = (filename,)
                self.c.execute('SELECT * FROM job WHERE filename = ?', data)
                row = self.c.fetchone()
                if row != None:
                    keys = row.keys()
                    for i in range(len(keys)):
                        result[keys[i]] = row[i] 
                # If no result will be empty
                return result 
               
                    
            elif (size and crc32): #size and crc32 given
                data = (data, size, unicode(crc32))
                result = {}
                self.c.execute('SELECT * FROM job, file WHERE job.filename = ?, \
                                job.fid = file.fid, file.size = ?, file.crc32 = ?', data)
                row = self.c.fetchone()
                if row != None:
                    keys = row.keys()
                    for i in range(len(keys)):
                        result[keys[i]] = row[i] 
                # If no result will be empty
                return result 
                
            else:
                pass
                
                
    def list_file(self, drive = None):
        if not drive: # Get everything from database
            self.c.execute('SELECT anime.romanji_name, anime.episodes, episode.epno, episode.eng_name, file.fid FROM anime, episode, file WHERE ( \
                            file.eid = episode.eid AND file.aid = anime.aid)')
            mykeys = ['anime_name', 'anime_episodes', 'epno', 'ep_name', 'fid']
            dict_list = []
            for row in self.c:
                entry = {}
                for i in range(len(mykeys)):
                    entry[mykeys[i]] = row[i]
                dict_list.append(entry)
            return dict_list
        else : # select based on storage location
            pass 
        
    def delete_job(self, file_name):
        file_name = unicode(file_name)
        data = (file_name,)
        self.c.execute('DELETE * FROM job WHERE filename = ?',data)
        self.conn.commit()
    
    def update_job(self, file_name):
        file_name = unicode(file_name)
        
        ctime = datetime.utcnow()
        ctime = ctime.replace(microsecond = 0)
        ctime = ctime.isoformat().replace('T', ' ')

        data = ( ctime,file_name)
        self.c.execute("UPDATE job SET last_checked = datetime(?) \
                        WHERE filename = ?", data)
        self.conn.commit()
        
    def list_job(self, drive = None):
        if not drive: # Get everything from database
            self.c.execute('SELECT anime.romanji_name, anime.episodes, episode.epno, episode.eng_name, file.fid,\
                            job.filename, job.folder, job.last_checked, file.size\
                            FROM anime, episode, file, job WHERE (file.eid = episode.eid AND file.aid = anime.aid \
                            AND job.fid = file.fid)')
            mykeys = ['anime_name', 'anime_episodes', 'epno', 'ep_name', 'fid', 'file_name', 'folder', 'last_checked', 'size']
            dict_list = {}
            for row in self.c:
                entry = {}
                for i in range(len(mykeys)):
                    entry[mykeys[i]] = row[i]
                # Return local time
                timestr = entry['last_checked']
                d = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
                d = datetime_from_utc_to_local(d)
                entry['last_checked'] = str(d)
                
                dict_list[entry['file_name']] = entry
            return dict_list
        else : # select based on storage location TO BE ADDED
            pass 
            
def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset