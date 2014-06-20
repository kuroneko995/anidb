import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 1444))
except socket.error:
    print 'Failed to create socket'
    sys.exit()
    
host = 'api.anidb.net'
port = 9000

"""
fmask 
01110000    11111000    11101011    11000000    0000000
aid         size        quality     dub lang    mylist stuff
eid         ed2k        source      sub lang
gid         md5         audio codec
            sha1        video codec
            crc32       video res
                        file type

amask
11110000    11000000    11110000    11000000
total ep    romaji name epno        group name
highest ep  kanji name  epname      group short name
year                    ep romaji
type                    ep kanji

amask



"""
fmaskB = '01110000111110001110101111000000'
fmask = '%0*X' % ((len(fmaskB) + 3) // 4, int(fmaskB, 2))

amaskB ='11110000110000001111000011000000'
amask = hstr = '%0*X' % ((len(amaskB) + 3) // 4, int(amaskB, 2)) 

msg1 = 'AUTH user=ndminh92&pass=darkraven&protover=3&client=anidbfilemanager&clientver=0&nat=1'
msg2 = 'PING nat=1'
msg3 = 'FILE fid=977491&fmask='+fmask+'&amask='+amask+'&s=pqhno'

msg = msg2

print msg
try:
    s.sendto(msg, (host,port))
    
    d = s.recvfrom(1024)
    reply = d[0]
    addr = d[1]
    
    print 'Server reply: ' + reply
    
    
except socket.error, msg:
    print 'Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
    
    
    
    
"""
Mapping for request


        # each line is one byte
        # only chnage this if the api changes
map = ['aid','unused','year','type','related_aid_list','related_aid_type','category_list','category_weight_list',
 'romaji_name','kanji_name','english_name','other_name','short_name_list','synonym_list','retired','retired',
 'episodes','highest_episode_number','special_ep_count','air_date','end_date','url','picname','category_id_list',
 'rating','vote_count','temp_rating','temp_vote_count','average_review_rating','review_count','award_list','is_18_restricted',
 'anime_planet_id','ANN_id','allcinema_id','AnimeNfo_id','unused','unused','unused','date_record_updated',
 'character_id_list','creator_id_list','main_creator_id_list','main_creator_name_list','unused','unused','unused','unused',
 'specials_count','credits_count','other_count','trailer_count','parody_count','unused','unused','unused']
      
episode
['eid','aid','length','rating','votes','epno','eng','romaji','kanji','aired','type']
epno special character S(special), C(credits), T(trailer), P(parody), O(other).
type 1: regular episode (no prefix), 2: special ("S"), 3: credit ("C"), 4: trailer ("T"), 5: parody ("P"), 6: other ("O")
      
    def getFileMapF(self):
        # each line is one byte
        # only chnage this if the api changes
map = ['unused','aid','eid','gid','mylist_id','list_other_episodes','IsDeprecated','state',
'size','ed2k','md5','sha1','crc32','unused','unused','reserved',
'quality','source','audio_codec_list','audio_bitrate_list','video_codec','video_bitrate','video_resolution','file_type_extension',
'dub_language','sub_language','length_in_seconds','description','aired_date','unused','unused','anidb_file_name',
'mylist_state','mylist_filestate','mylist_viewed','mylist_viewdate','mylist_storage','mylist_source','mylist_other','unused']
      
    
def getFileMapA(self):
# each line is one byte
# only chnage this if the api changes
map = ['anime_total_episodes','highest_episode_number','year','type','related_aid_list','related_aid_type','category_list','reserved',
'romaji_name','kanji_name','english_name','other_name','short_name_list','synonym_list','retired','retired',
'epno','ep_name','ep_romaji_name','ep_kanji_name','episode_rating','episode_vote_count','unused','unused',
'group_name','group_short_name','unused','unused','unused','unused','unused','date_aid_record_updated']
        
   


"""