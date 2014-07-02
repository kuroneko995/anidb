from os import path
import os
from anidb import database
from anidb import udp_api
from anidb import ed2k


def get_anime_info(database, udp_conn, aid):
    '''Look up an anime using aid. 
    First in local database, next in anidb
    Automatically update local base if searched anidb
    '''
    info = database.get_info_aid(aid)
    if len(info): # Has entry in local database
        print "Get anime info: Local data found"
        return info
    else: # Local db return blank. Ask anidb
        info = udp_conn.get_anime_info(aid, ('aid' , 'romanji_name', 'episodes', 'year', 'eng_name',
                    'kanji_name'))
        if len(info): # Anime found. Update local
            database.add_anime(int(info['aid']), info['romanji_name'], int(info['episodes']), \
                                int(info['year']), info['eng_name'], info['kanji_name'])
            return info
        else: # No match found
            return {}
        
        
def get_episode_info(database, udp_conn, eid):
    '''Look up episode info using eid
    Add to local db if searched anidb'''  
    local_info = database.get_info_eid(eid)
    if len(local_info):
        print "Get episode info: Local info found"
        return local_info
    else: # Ask anidb
        anidb_info = udp_conn.get_episode_info(eid) 
        if len(anidb_info): # Found the episode
            database.add_episode(eid, anidb_info['epno'], anidb_info['eng_name'], \
                                anidb_info['romanji_name'], anidb_info['kanji_name'])
            return anidb_info
        else: # No episode found 
            return {}
        
def get_file_info(database, udp_conn, size, ed2k):
    '''Look up file using size and ed2k
    First in local database, next in anidb
    Update local db if asked anidb
    '''
    local_info = database.get_info_hash(size, ed2k)
    if len(local_info):
        print "Get file info: Local info found"
        return local_info
    else: # Ask anidb
        anidb_info = udp_conn.get_file_info(size, ed2k)
        if anidb_info: # File found on anidb
            print "Get file info: Anidb info found"
            if not database.in_db('anime', int(anidb_info['aid'])): # Anime not in local
                database.add_anime(int(anidb_info['aid']), anidb_info['romanji_name'], int(anidb_info['anime_total_episodes']), \
                                anidb_info['year'], anidb_info['english_name'], anidb_info['kanji_name'])
            if not database.in_db('episode', int(anidb_info['eid'])): # Episode not in local
                database.add_episode(int(anidb_info['eid']), anidb_info['epno'], anidb_info['ep_name'], \
                                anidb_info['ep_romanji_name'], anidb_info['ep_kanji_name'])
            # Add file info to local database
            # print "Adding to local db"
            database.add_file(int(anidb_info['fid']), int(anidb_info['aid']), int(anidb_info['eid']), int(anidb_info['gid']),\
                                int(anidb_info['size']), anidb_info['ed2k'], anidb_info['md5'], \
                                anidb_info['sha1'], anidb_info['crc32'], anidb_info['dub'], anidb_info['sub'], \
                                anidb_info['src'], anidb_info['audio'], anidb_info['video'], \
                                anidb_info['res'], anidb_info['file_type'], anidb_info['group_short_name'])
           
            return anidb_info
        else:
            return {}
            
def check_file(database, udp_conn, file_path):
    """Check file info to see if in local db. Otherwise search anidb
    First round: test name and size
    Second round: test ed2k and size. Search local
    """
    size = path.getsize(file_path)
    file_name = unicode(path.split(file_path)[1])
    folder = unicode(path.split(file_path)[0])
    info = database.get_info_filename(file_name ,size)
    
    if info: # File in local db found
        print "File record found in local database"
        database.add_job(file_name, int(info['fid']), folder[0] , folder)
        return info
    else: # Nothing found. Hash file and search anidb
        ed2k = get_ed2k(file_path)
        info = get_file_info(database, udp_conn, size, ed2k)
        if info: # found on anidb
            
            database.add_job(file_name, int(info['fid']), folder[0] , folder)
        else:
            print "File information not found"
        return info
    
            
def scan_folder(database, udp_conn, search_path, file_type = ['mkv','avi','mp4']):
    """Depth first search into search_path to look for anime folders and add
    to database. Ignore file not of the specified file type
    """
    directory = []
    directory += [path.join(search_path, branch) for branch in os.listdir(search_path)] 
    
    while directory != []:
        file_path = directory.pop()
        if path.isdir(file_path): #If it is a folder. Add content and move on
            directory = [path.join(file_path, branch) for branch in os.listdir(file_path)] + directory
        elif path.isfile(file_path): # If it is a file, move on
            file_name = unicode(path.split(file_path)[1])
            correct_type = False
            for tail in file_type:
                if tail in file_name:
                    correct_type = True
                break
            if not correct_type:
                continue
            print "Now checking %s" % file_name
            check_file(database, udp_conn, file_path)
        else: # If not file or folder, give up
            pass
           


            
def get_ed2k(file_path):
    ''' Use code taken from http://pydoc.net/Python/pyanidb/0.2.0/pyanidb.hash/
    and modified
    '''
    f = open(file_path, 'rb')
    data = f.read()
    f.close()
   
    newHash = ed2k.Ed2k()
    newHash.update(data)
    return newHash.hexdigest()