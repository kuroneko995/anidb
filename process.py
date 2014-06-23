import sqlite3


conn = sqlite3.connect('local_db.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS anime (aid INTEGER PRIMARY KEY, romanji_name TEXT, \
            episodes NUMBER, year NUMBER, eng_name TEXT, kanji_name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS episode (eid INTEGER PRIMARY KEY, epno TEXT, \
            eng_name TEXT, romanji_name TEXT, kanji_name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS file (fid INTEGER PRIMARY KEY, aid INTEGER, \
            eid INTEGER, gid INTEGER, size INTEGER, ed2k TEXT, md5 TEXT, sha1 TEXT, \
            crc32 TEXT, dub TEXT, sub TEXT, src TEXT, audio TEXT, video TEXT, res TEXT, \
            grp TEXT, type TEXT)")                                

f = open('webAOM.txt')


for line in f:
    if line[0] == 'a' and line != 'a0\n':
        # print 'Anime:',
        # print line.split('|')
        line = line.split('|')
        aid = int(line[0][1:])
        episodes = int(line[1])
        year = int(line[3])
        type = unicode(line[4])
        romanji_name = unicode(line[5])
        kanji_name = unicode(line[6],'utf_8')
        eng_name = unicode(line[7])
        row = (aid, romanji_name, episodes, year, eng_name, kanji_name)
        c.execute("INSERT or IGNORE INTO anime (aid, romanji_name, episodes, year, eng_name, kanji_name) \
        VALUES (?,?,?,?,?,?) ", row)
        
    elif line[0] == 'e':
        # print 'Episode',
        line = line.split('|')
        # print line
        eid = int(line[0][1:])
        epno = unicode(line[1])
        eng_name = unicode(line[2])
        romanji_name = unicode(line[3])
        kanji_name = unicode(line[4],'utf_8')
        row = (eid, epno, eng_name, romanji_name, kanji_name)
        c.execute("INSERT OR IGNORE INTO episode (eid, epno, eng_name, romanji_name, kanji_name) \
                    VALUES (?,?,?,?,?)", row)
        
    elif line[0] == 'f':
        # print 'File',
        line = line.split('|')
        # print line
        fid = int(line[0][1:])
        aid = int(line[1])
        eid = int(line[2])
        gid = int(line[3])
        size = int(line[6])
        ed2k = unicode(line[7])
        md5 = unicode(line[8])
        sha1 = unicode(line[9])
        crc32 = unicode(line[10])
        dub = unicode(line[11])
        sub = unicode(line[12])
        
        src = unicode(line[14])
        audio = unicode(line[15])
        video = unicode(line[16])
        res = unicode(line[17])
        type = unicode(line[18])
        grp = unicode(line[21].rstrip())
        row = (fid, aid, eid, gid, size, ed2k, md5, sha1, crc32, dub, sub, \
                src, audio, video, res, type, grp)
        c.execute("INSERT OR IGNORE INTO file (fid, aid, eid, gid, size, ed2k, md5, sha1, crc32, dub, sub,  \
                src, audio, video, res, type, grp) VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?)", row)
    # else:
        # pass

    # print line.split('|')
    
    # parse = line.split('|')
    # if len(parse) < 2:
        # print str(count) + ": " + line
    
f.close()

c.execute("SELECT * FROM file")
row1 = c.fetchone()
a = row1.keys()
b = row1
for i in range(len(a)):
    print a[i], ":", b[i]
# for row in c:
    # print row



                                
conn.commit()
conn.close