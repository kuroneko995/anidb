import socket
import sys
import ConfigParser
import time

class UDP_Conn(object):

    
    def __init__(self, config_file = 'config.txt'):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(config_file,'r'))
        # Get anidb host info
        self.host = config.get('anidb', 'host')
        self.port = int(config.get('anidb', 'port'))
        self.addr = (self.host, self.port)
        print self.host
        
        # Get login info
        username = config.get('login', 'username')
        password = config.get('login', 'password')
        self.auth = "AUTH user=%s&pass=%s&protover=3&client=anidbfilemanager&clientver=0&nat=1&enc=utf-8" % (username, password)
        
        self.session = ""
        self.timer = int(time.time())
        
        # Config socket
        my_port = int(config.get('socket', 'port'))
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind(('', my_port))
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
    
    
    def close(self):
        '''Close socket, end connection. Object is effectively useless'''
        self.s.close()

    
    def update_timer(self):
        self.timer = int(time.time())
        
    def send_msg(self, msg):
        current_time = int(time.time())
        if current_time - self.timer < 4:
            print "Waiting for" + str(4 - current_time + self.timer) + "seconds"
            time.sleep(4 - current_time + self.timer)
        else:
            pass
            
        self.s.sendto(msg, (self.host, self.port))
        self.timer = int(time.time())
        
    
    def ping(self):
        msg = 'PING nat=1'
        
        # self.s.sendto(msg,(self.host,self.port))
        self.send_msg(msg)
        d = self.s.recvfrom(1024)
        reply = d[0]
        return reply # Message part    
    
    
    def get_session(self):
        msg = self.auth
        self.send_msg(msg)
        d = self.s.recvfrom(1024)
        reply = d[0]
        print reply
        self.session = reply.split()[1]
        return self.session
        
    def get_anime_info(self, aid, fields_tuple):
        '''Return a tuple of unicode strings with value equals to the corresponding fields
        in fields_tuple
        '''
        map = ['aid','unused','year','type','related_aid_list','related_aid_type','category_list','category_weight_list',
        'romanji_name','kanji_name','eng_name','other_name','short_name_list','synonym_list','retired','retired',
        'episodes','highest_episode_number','special_ep_count','air_date','end_date','url','picname','category_id_list',
        'rating','vote_count','temp_rating','temp_vote_count','average_review_rating','review_count','award_list','is_18_restricted',
        'anime_planet_id','ANN_id','allcinema_id','AnimeNfo_id','unused','unused','unused','date_record_updated',
        'character_id_list','creator_id_list','main_creator_id_list','main_creator_name_list','unused','unused','unused','unused',
        'specials_count','credits_count','other_count','trailer_count','parody_count','unused','unused','unused']
        bitstr = ''
        wanted_fields = []
        for field in map:
            if field in fields_tuple:
                bitstr += '1'
                wanted_fields.append(field)
            else:
                bitstr += '0'
        print wanted_fields
        
        amask =  '%0*X' % ((len(bitstr) + 3) // 4, int(bitstr, 2)) 
        msg ="ANIME aid=%d&amask=%s&s=%s" % (aid, amask, self.session)
        self.send_msg(msg)
        d = self.s.recvfrom(1024)
        print d
        reply = d[0].split('\n')[1] # Ignore first line of reply
        print reply
        returned_fields = reply.split('|')
        print returned_fields
        result = []
        for field in fields_tuple:
            # match the order of the tuples coming in. I don't like this line 
            result.append(unicode(returned_fields[wanted_fields.index(field)],'utf_8'))
            
        
        return result
        
        
# fmaskB = '01110000111110001110101111000000'
# fmask = '%0*X' % ((len(fmaskB) + 3) // 4, int(fmaskB, 2))

# amaskB ='11110000110000001111000011000000'
# amask =  '%0*X' % ((len(amaskB) + 3) // 4, int(amaskB, 2)) 

# msg1 = 'AUTH user=ndminh92&pass=darkraven&protover=3&client=anidbfilemanager&clientver=0&nat=1'
# msg2 = 'PING nat=1'
# msg3 = 'FILE fid=977491&fmask='+fmask+'&amask='+amask+'&s=pqhno'

# msg = msg2

# print msg
# try:
    # s.sendto(msg, (host,port))
    
    # d = s.recvfrom(1024)
    # reply = d[0]
    # addr = d[1]
    
    # print 'Server reply: ' + reply
    
    
# except socket.error, msg:
    # print 'Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    # sys.exit()
    
    
    
    
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