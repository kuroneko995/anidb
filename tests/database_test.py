from nose.tools import *
from anidb import database


# def test_load_db():
    # localdb = database.Local_DB('local_db.db')
    # localdb.close()
    
    
# def test_in_db():
    # localdb = database.Local_DB('local_db.db')
    # print localdb.in_db('episode',95149)
    # localdb.close()
    
# def test_get_anime_info():
    # localdb = database.Local_DB('local_db.db')
    # a = localdb.get_info_aid(6025)
    # print a
    # localdb.close()
    
# def test_get_episode_info():
    # localdb = database.Local_DB('local_db.db')
    # a = localdb.get_info_eid(95149)
    # print a
    # localdb.close()
    
# def test_get_file_info():
    # localdb = database.Local_DB('local_db.db')
    # a = localdb.get_info_fid(598911)
    # print a
    # localdb.close()
    
# def test_get_info_compound():
    # localdb = database.Local_DB('local_db.db')
    # a = localdb.get_info_fid(598911)
    # b = localdb.get_info_eid(a["eid"])
    # c = localdb.get_info_aid(b["aid"])
   
    # print c
    
# def test_get_info_hash():
    # localdb = database.Local_DB('local_db.db')
    # a = localdb.get_info_hash(223886309,'fb29e20a8b9469014e6631aaf516ed51')
    # b = localdb.get_info_aid(a["aid"])
    # print b
    
# def test_list_file():
    # localdb = database.Local_DB('local_db.db')
    # a = localdb.list_file()
    # for item in a:
        # print item