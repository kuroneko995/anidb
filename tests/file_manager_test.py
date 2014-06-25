from nose.tools import *
from anidb import file_manager
from anidb import database
from anidb import udp_api


# def test_get_info():
    # mydb = database.Local_DB()
    # a = udp_api.UDP_Conn()
    # a.get_session()
    # # print mydb.get_info_hash(470496917, "6b088d49697c4aa79d0b080ab4eafdba")
    # # print mydb.get_info_fid(1426505)
    # print file_manager.get_anime_info(mydb, a, 10182)
    # print file_manager.get_episode_info(mydb, a, 158750)
    # print file_manager.get_file_info(mydb, a, 470496917, "6b088d49697c4aa79d0b080ab4eafdba")
    
# def test_add_file():
    # mydb = database.Local_DB()
    # a = udp_api.UDP_Conn()
    # a.get_session()
    # print file_manager.check_file(mydb, a, "C:\Users\mnguyen\Downloads\New folder\Hataraku Maou-sama! [1080p, FFF]\[FFF] Hataraku Maou-sama! - C09 (1920x1080 Blu-ray H264 FLAC) [79D7BA58].mkv")
    
def test_scan_folder():
    mydb = database.Local_DB()
    a = udp_api.UDP_Conn()
    a.get_session()
    file_manager.scan_folder(mydb, a, "C:\Users\mnguyen\Downloads\New folder")