from nose.tools import *
from anidb import classes



def test_filename():    
    ep1 = classes.Episode(1, "A34F324CD", "[FFF] Black Bullet 01 [A34F324CD].mkv", "D:\Download\[FFF] Black Bullet 01 [A34F324CD].mkv")
    ep1.print_name()
    assert_equal(ep1.filename,"[FFF] Black Bullet 01 [A34F324CD].mkv") 
    
def test_add_episode():
    ep1 = classes.Episode(1, "A34F324CD", "[FFF] Black Bullet 01 [A34F324CD].mkv", "D:\Download\[FFF] Black Bullet 01 [A34F324CD].mkv")
    series1 = classes.Series(episode_number=13)
    series1.add_episode(ep1)
    series1.print_episode_list()
    assert_equal(series1.get_episode(1),ep1)
    series1.get_episode(1).print_name()