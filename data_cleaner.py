import re
import json
import HTMLParser
from pprint import pprint


data = []
with open('/Users/harshalkutkar/Documents/halkutka-project/Output.txt') as f:
    for line in f:
        x = json.loads(line,'utf-8')
        data.append(x)
        print x[0]['sentiment']





'''
limit = 30
# Script for cleaning basic json #
json_data = '/Users/harshalkutkar/Documents/halkutka-project/tweets_toclean.json'
final_array = '['

with open(json_data) as f:

    for line in f:
        line = line.replace("\r", "").replace("\n", ", ")
        content = line
        final_array = final_array + content
        limit = limit + 1
        if limit>50: break


final_array = final_array[:-2] + "]"

text_file = open("/Users/harshalkutkar/Documents/halkutka-project/Output.txt", "w")

text_file.write(final_array)

text_file.close()

'''