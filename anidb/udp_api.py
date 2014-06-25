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
            print "Waiting for %d seconds" % (4 - current_time + self.timer)
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
        
        amask =  '%0*X' % ((len(bitstr) + 3) // 4, int(bitstr, 2)) 
        msg ="ANIME aid=%d&amask=%s&s=%s" % (aid, amask, self.session)
        self.send_msg(msg)
        d = self.s.recvfrom(1024)
        if '230 ANIME' in d[0]: # Anime found reply
            reply = d[0].split('\n')[1] # Ignore first line of reply
            returned_fields = reply.split('|')
            result = {}
            for field in fields_tuple:
                # match the order of the tuples coming in. I don't like this line 
                result[field] = unicode(returned_fields[wanted_fields.index(field)],'utf_8')            
            return result
        else: # No anime found
            return {}
        
    def get_episode_info(self, eid):
        '''Return a dictionary of unicode string with keys being
        (eid, aid, epno, eng_name, romanji_name, kanji_name)
        '''
        map = ['eid','aid','length','rating','votes','epno','eng_name','romanji_name','kanji_name','aired','type']
        # epno special character S(special), C(credits), T(trailer), P(parody), O(other).
        # type 1: regular episode (no prefix), 2: special ("S"), 3: credit ("C"), 4: trailer ("T"), 5: parody ("P"), 6: other ("O")
        wanted_fields = ['eid', 'aid', 'epno', 'eng_name', 'romanji_name', 'kanji_name']
        msg = 'EPISODE eid=%d&s=%s' % (eid, self.session)
        self.send_msg(msg)
        d = self.s.recvfrom(1024)
        print "Message", d[0]
        if '240 EPISODE' in d[0]: # Episode found
            reply = d[0].split('\n')[1]
            print "Reply %s" % reply
            returned_fields = reply.split('|')
            result = {}
            for field in wanted_fields:
                result[field] = unicode(returned_fields[map.index(field)],'utf_8')
            return result
        else: # No episode found
            return {}
            
    def get_file_info(self, size, ed2k, fields_list = ['fid', 'aid', 'eid', 'gid', 'size', 'ed2k', 'md5', 'sha1', \
                    'crc32', 'dub', 'sub', 'src', 'audio', 'video', 'res', 'file_type', 'group_short_name',\
                    'epno', 'ep_name', 'ep_romanji_name', 'ep_kanji_name',\
                    'year', 'anime_total_episodes', 'romanji_name', 'english_name','kanji_name']): 
        
        '''Return info for a file using size and ed2k'''
        fmap = ['unused','aid','eid','gid','mylist_id','list_other_episodes','IsDeprecated','state',
        'size','ed2k','md5','sha1','crc32','unused','unused','reserved',
        'quality','src','audio','audio_bitrate_list','video','video_bitrate','res','file_type',
        'dub','sub','length_in_seconds','description','aired_date','unused','unused','anidb_file_name',
        'mylist_state','mylist_filestate','mylist_viewed','mylist_viewdate','mylist_storage','mylist_source','mylist_other','unused']

        fbitstr = ''
        wanted_fields = []
        for field in fmap:
            if field in fields_list:
                fbitstr += '1'
                wanted_fields.append(field)
            else:
                fbitstr += '0'
        fmask =  '%0*X' % ((len(fbitstr) + 3) // 4, int(fbitstr, 2)) 
        
        
        amap = ['anime_total_episodes','highest_episode_number','year','file_type','related_aid_list','related_aid_type','category_list','reserved',
        'romanji_name','kanji_name','english_name','other_name','short_name_list','synonym_list','retired','retired',
        'epno','ep_name','ep_romanji_name','ep_kanji_name','episode_rating','episode_vote_count','unused','unused',
        'group_name','group_short_name','unused','unused','unused','unused','unused','date_aid_record_updated']

        abitstr = ''
        for field in amap:
            if field in fields_list:
                abitstr += '1'
                wanted_fields.append(field)
            else:
                abitstr += '0'
        amask =  '%0*X' % ((len(abitstr) + 3) // 4, int(abitstr, 2)) 
        
        wanted_fields.insert(0,'fid')
        
        msg = 'FILE size=%d&ed2k=%s&fmask=%s&amask=%s&s=%s' % (size, ed2k, fmask, amask, self.session) 
        print "Message is %s" % msg
        self.send_msg(msg)
        d = self.s.recvfrom(1024)
        print "Message", d[0]
        if '220 FILE' in d[0]: # File found
            reply = d[0].split('\n')[1]
            print "Reply %s" % reply
            returned_fields = reply.split('|')
            result = {}
            for field in fields_list:
                result[field] = unicode(returned_fields[wanted_fields.index(field)],'utf_8')
            return result
        else: # File not found
            return {} 
        


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