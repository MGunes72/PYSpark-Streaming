import socket
import sys
import requests
import requests_oauthlib
import json
from time import ctime
# Replace the values below with yours
ACCESS_TOKEN = '1648005505-qoNCWx93o3Z7vC9kpSQV9hhYLFWu3Z8IxbP1QHi'
ACCESS_SECRET = '1lpUvUKdukfSEHwjwWShrnGsWf2IzONpkrw3dOGtLcfkr'
CONSUMER_KEY = 'xfurMJHmNtsdkSDP8ieRTi0Nd'
CONSUMER_SECRET = 'sDxbP8q4J16DgxrKfQEEUfOXXh15y2cB8ym1xTtLd71H2dWkeQ'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            print("-------------------------------------------")
            full_tweet = json.loads(line)
            print(full_tweet)
            text=full_tweet['text']
            print(text)
            place=full_tweet['place']['name']
            print(place)
            print ("------------------------------------------")
            tcp_connection.send((place+"\n").encode('utf-8'))
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)


def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    #Türkçe tweetleri almak için language=tr
    query_data = [('language', 'tr'), ('locations', '-130,-20,100,50'),('track','#')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


TCP_IP = "localhost"
TCP_PORT = 60127
conn = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp,conn)