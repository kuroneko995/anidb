from nose.tools import *
from anidb import udp_api

def test_socket():
    a = udp_api.UDP_Conn()
    assert_equal(a.port, 9000)
    a.close()
    
    
# def test_ping():
    # a = udp_api.UDP_Conn()
    # assert_equal(a.port, 9000)
    # print a.ping()
    # # print a.auth()
    
# def test_auth():
    # a = udp_api.UDP_Conn()
    # print a.get_session()
    
    
# def test_get_anime_info():
    # a = udp_api.UDP_Conn()
    # print a.get_session()
    # print a.get_anime_info(6025, ('aid', 'romanji_name', 'episodes', 'year', 'eng_name', 'kanji_name'))