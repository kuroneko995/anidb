from nose.tools import *

from anidb import program


def test_parse_folder_name():
    folder_name = "Nagi no Asukara [TV, Underwater]"
    result = program.parse_folder_name(folder_name)
    assert_equal(result, ["Nagi no Asukara", "TV", "Underwater"])

    folder_name = "Hataraku Maou-sama! [1080p, FFF]"
    result = program.parse_folder_name(folder_name)
    assert_equal(result[0], "Hataraku Maou-sama!")
    
def test_get_eps_number():
    eps_name = "[Underwater] Black Bullet - 10 (720p) [E58AF994].mkv"
    result = program.get_eps_number(eps_name)
    assert_equal(result, 10)
    eps_name = "[FFF] Hataraku Maou-sama! - OP02 [BD][1080p-FLAC][79D7BA58].mkv"
    result = program.get_eps_number(eps_name)
    assert_equal(result, 2)
    
def test_add_folder():
    folder_path = "C:\\Users\\mnguyen\\Downloads\\Hataraku Maou-sama! [1080p, FFF]"
    mydb = program.Anime_database()
    mydb.add_folder(folder_path)
    mySeries = mydb.series_list["Hataraku Maou-sama!"]
    mySeries.print_episode_list()
    assert_equal(mySeries.get_episode(2).filename, "[FFF] Hataraku Maou-sama! - OP02 [BD][1080p-FLAC][79D7BA58].mkv")
    
def test_pickle():
    folder_path = "C:\\Users\\mnguyen\\Downloads\\Hataraku Maou-sama! [1080p, FFF]"
    mydb = program.Anime_database()
    mydb.add_folder(folder_path)
    mySeries = mydb.series_list["Hataraku Maou-sama!"]
    print mySeries.name
    print mySeries.location
    mydb.save()
    loaddb = program.Anime_database()
    loaddb.load()
    print loaddb.series_list["Hataraku Maou-sama!"].episode_list[2].filename
   
   
def test_GUI_intergration():
    program.main()