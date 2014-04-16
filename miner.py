__author__ = 'harshalkutkar'
import os
import twitter
import json
import pprint
from json import JSONEncoder
from alchemyapi import AlchemyAPI

import oauthclient
import functools
import datetime

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

#instantiate the alchemy api
alchemyapi = AlchemyAPI()


#instantiate twitter api
twitapi = twitter.Api(consumer_key='oab3F9Cx5lINWlSadHAL50spo',
                           consumer_secret='DyYPedkhKDgru6H53esW0W2q7e6nGEEYaLA7iTPXLrTOf63hkm',
                           access_token_key='21637668-a2mvcgdOGRE6C5WKA6w6Uim0m4oIfmUxA75oMKkeu',
                           access_token_secret='IvqHYTywacdZc0vA3dOmgV4rVC1KIAoPC3n2gT8kLmto0',
                           cache=None)

#query with geocode
#result = twitapi.GetSearch(term="\"Arvind Kejriwal\" OR \"Narendra Modi\"", geocode=[19.016339, 72.840289, '100km'], count=50)

#MODI_ONLY
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", since_id='456135396947745920',count=200)

#MODI_ONLY_MUMBAI
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[19.016339, 72.840289, '150km'], count=50)


#MODI_ONLY_CHENNAI
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[13.052414, 80.250825, '150km'],count=50)


#MODI_ONLY_GANDHINAGAR
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[23.224820, 72.646377, '150km'],count=50)

#MODI_ONLY_DELHI
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[28.635308, 77.224960, '150km'],count=50)

#MODI_ONLY_BANGALORE
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[12.971599, 77.594563, '150km'],count=50)

#MODI_ONLY_PUNE
result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[18.520430, 73.856744, '150km'],count=50)

#MODI_ONLY_HYDERABAD
#result = twitapi.GetSearch(term="\"Narendra Modi\" OR \"#namo\" ", geocode=[17.385044, 78.486671, '150km'],count=50)

print str(result)

with open('tweets.json', "a") as outfile:
    try:

        for x in result:
            #json_object = MyEncoder().encode(x)
            y = dict()
            y['id'] = x.id
            y['user'] = x.user.name
            y['text'] = x.text
            y['created_at'] = x.created_at_in_seconds
            if x.location:
                y['location'] = x.location
            else:
                if x.user.location:
                    y['location'] = x.user.location
            y['time_zone'] = x.user.time_zone

            try:
                response = alchemyapi.sentiment("text", x.text.encode('utf-8'))
                sentiment = response["docSentiment"]["score"]

                y['sentiment'] = sentiment

            except KeyError:
                continue

            print "text"+x.text
            print "time"+(datetime.datetime.fromtimestamp(int(x.created_at_in_seconds)).strftime('%Y-%m-%d %H:%M:%S'))

            # json.dump(x, outfile, default=lambda o: o.__dict__, indent=4)
            # outfile.write("\n")

            json.dump(y, outfile)
            outfile.write("\n")

    except IOError:
        open('tweets.json', 'w').close()


outfile.close()


