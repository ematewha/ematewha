# -*- coding: utf-8 -*-

from konlpy.tag import Twitter
import pymysql
import instagram
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
twitter = Twitter()

# connection to mysql(local)
conn = pymysql.connect(host='aws-server-name', port=3306, user='root', passwd='password', db='ematewha', charset ='utf8', use_unicode=True)
cur = conn.cursor()

# connection to instagram_api
client_id = 'id'
client_secret = 'd790b3e4268c4b4bb91492af520647fd'
access_token = 'given-token'
client_ip = 'ip'
api = instagram.InstagramAPI(client_id=client_id, client_secret=client_secret, client_ips=client_ip, access_token=access_token)

# bring upso_refine.name from mysql
cur.execute('SELECT upso_id from upso_refined')
upso_id = cur.fetchall()


cur.execute('SELECT name_refined from upso_refined')
upso_refine = cur.fetchall()

# search with upso_refine from instagram
print (len(upso_refine))
for n in range(0, 468):
    search_refine = upso_refine[n][0]
    print search_refine
    i = 1
    num = 0 #게시물 수 세기

    # search keywords from instagram
    while i < 2 :
        counter = 1
        media_ids, next = api.tag_recent_media(tag_name= search_refine, count = 1) #한글로 태그 검색 가능, count는 작으면 작을수록 좋은듯.. 0은 안됨
        if(next):   #개수상관없이 받아오는 법
            temp, max_tag = next.split('max_tag_id=')
            max_tag = str(max_tag)
            info_tuple = ()

            while next and max_tag and counter < 50000 :        #개수 상관없이 받아오기 때문에 counter는 큰 수로. (counter를 작게하면 counter x20 만큼의 게시물만 출력됨)
                more_media, next = api.tag_recent_media(tag_name = search_refine, max_tag_id=max_tag)
                if(next):   #개수상관없이 받아오는 법
                    temp, max_tag = next.split('max_tag_id=')
                max_tag = str(max_tag)

                for media_id in more_media:     # items from instagram media_id: str(media_id.id), str(media_id.get_standard_resolution_url()), str(media_id.caption), str(media_id.comments), str(media_id.tags)

                    # option 1) search by keyword_caption
                    taglist = str(media_id.caption).decode('utf-8')
                    print(media_id.caption)
                    num = num + 1
                    print num

                    # # option 2) search by keyword_hashtag
                    # taglist = str(media_id.tags).decode('utf-8')


                    # extract keywords from konlpy and insert into db ematewha
                    tags = twitter.pos(taglist, norm=True, stem=True)
                    for j in range(len(tags)):
                        if(tags[j][1] == 'Noun' or tags[j][1] == 'Adjective'):
                            print tags[j][0],"/",tags[j][1]
                            sql = 'INSERT IGNORE into keyword_caption values ("%s", "%s")' % (upso_id[n][0], tags[j][0])
                            cur.execute(sql)
                        elif(tags[j][1] == 'Hashtag'):
                            nohash = tags[j][0].replace("#", "")
                            nohash = nohash.replace("\"", "")
                            print nohash,"/",tags[j][1]
                            sql = 'INSERT IGNORE into keyword_caption values ("%s", "%s")' % (upso_id[n][0], nohash)
                            cur.execute(sql)
                counter += 1
            # 게시물 갯수 확인
            print "게시물 수"
            print num
            #conn.commit()
        i = i + 1
    conn.commit()
cur.close()
conn.close()
