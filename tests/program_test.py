from nose.tools import *
from anidb import program

def test_program_launch():
    myp = program.Program()
    myp.start()