# -*- coding: euc-kr -*-
from instagram.client import InstagramAPI
from random import randint
import sys
import time
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('euc-kr')

client_id = '364c02ec6bca4643af88d2c506298a63'
client_secret = 'd790b3e4268c4b4bb91492af520647fd'
access_token = '1974102187.364c02e.2b5308bec24b4056aba5368627a6c3d0'
client_ip = '192.168.76.69'

api = InstagramAPI(client_id=client_id, client_secret=client_secret, client_ips=client_ip, access_token=access_token)
all_media_ids = []

media_ids, next = api.tag_recent_media(tag_name='이화당'.decode('euc-kr'), count = 1) #한글로 태그 검색 가능, count는 작으면 작을수록 좋은듯.. 0은 안됨.
temp, max_tag = next.split('max_tag_id=')
max_tag = str(max_tag)
info_tuple = ()
counter = 1
while next and counter < 1000 : #개수 상관없이 받아오기 때문에 counter는 큰 수로. (counter를 작게하면 counter x20 만큼의 게시물만 출력됨)

    more_media, next = api.tag_recent_media(tag_name='이화당'.decode('euc-kr'), max_tag_id=max_tag)
    if(next):   #개수상관없이 받아오는 법
        temp, max_tag = next.split('max_tag_id=')
    max_tag = str(max_tag)


    for media_id in more_media:
        info_tuple=(str(media_id.id), str(media_id.get_standard_resolution_url()), str(media_id.caption), str(media_id.comments)) #뭐뭐 출력할지
        #info_tuple = (str(media_id.get_standard_resolution_url()), str(media_id.tags))
        # #print unicode(str(all_media_ids), 'utf-8').encode('euc-kr')
        all_media_ids.append(info_tuple)

    counter += 1
    print counter

print "Length of All Media IDS:", len(all_media_ids)
print"print info \n"
i=0
while i<len(all_media_ids):
    print unicode(str(all_media_ids[i][2]), 'utf-8').encode('euc-kr', 'ignore') #comments 한글로 출력하기 [i][2]
    i += 1


# ex2_XXX.py  참고 (url 및 다른 정보 받아오기)
#			if ("point" in dir(media_id.location)) and ("latitude" in dir(media_id.location.point)) and ("longitude" in dir(media_id.location.point)):
#				position_tuple=(str(media_id.id),str(media_id.location.point.latitude),str(media_id.location.point.longitude),str(media_id.get_standard_resolution_url()))
#				media_with_location.append(position_tuple)
