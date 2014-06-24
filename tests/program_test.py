from nose.tools import *
from Tkinter import * ### (1)
import ttk
from anidb import program
from anidb import GUI



# def test_parse_folder_name():
    # folder_name = "Nagi no Asukara [TV, Underwater]"
    # result = program.parse_folder_name(folder_name)
    # assert_equal(result, ["Nagi no Asukara", "TV", "Underwater"])

    # folder_name = "Hataraku Maou-sama! [1080p, FFF]"
    # result = program.parse_folder_name(folder_name)
    # assert_equal(result[0], "Hataraku Maou-sama!")
    
# def test_get_eps_number():
    # eps_name = "[Underwater] Black Bullet - 10 (720p) [E58AF994].mkv"
    # result = program.get_eps_number(eps_name)
    # assert_equal(result, 10)
    # eps_name = "[FFF] Hataraku Maou-sama! - OP02 [BD][1080p-FLAC][79D7BA58].mkv"
    # result = program.get_eps_number(eps_name)
    # assert_equal(result, 2)
    
# def test_add_folder():
    # folder_path = "C:\\Users\\mnguyen\\Downloads\\Hataraku Maou-sama! [1080p, FFF]"
    # mydb = program.Anime_database()
    # mydb.add_folder(folder_path)
    # mySeries = mydb.series_list["Hataraku Maou-sama!"]
    # mySeries.print_episode_list()
    # assert_equal(mySeries.get_episode(2).filename, "[FFF] Hataraku Maou-sama! - OP02 [BD][1080p-FLAC][79D7BA58].mkv")
    
# def test_pickle():
    # folder_path = "C:\\Users\\mnguyen\\Downloads\\Hataraku Maou-sama! [1080p, FFF]"
    # mydb = program.Anime_database()
    # mydb.add_folder(folder_path)
    # mySeries = mydb.series_list["Hataraku Maou-sama!"]
    # print mySeries.name
    # print mySeries.location
    # mydb.save()
    # loaddb = program.Anime_database()
    # loaddb.load()
    # print loaddb.series_list["Hataraku Maou-sama!"].episode_list[2].filename
   
   
# def test_GUI_intergration():
    # my_db = program.Anime_database()
    # my_db.scan_folder("E:\\Anime")
    # root = Tk()
    # my_GUI = GUI.GUI_window(root)
    # for Series in my_db.series_list.keys():
        # my_GUI.addSeries(Series, location = my_db.series_list[Series].location)
        # for Episode in my_db.series_list[Series].episode_list.values():
            # my_GUI.addEpisode(Series, location=Episode.filepath, CRC=Episode.crc32, eps_number = Episode.number)
    # root.mainloop()
 
# def test_hash_entry():
    # entry = program.Hash_entry()
    # #print entry.crc32_date
    # print entry.get_date()
    
# def test_hash():
    # newHashdb = program.Hash_database()
    
    # newHashdb.load("crc32")
    # newHashdb.add_new_folder("crc32", "E:\\Anime\\DVD")
    # newHashdb.display("crc32")
    # newHashdb.save("crc32")
    
 