# Imports for project
import json
from environs import Env
import requests


# Define env where key lives
env = Env()
env.read_env()

# Define Key for search
api_key = env("KEY")

# Object being searched for
searches = []
with open("search_queries.txt", "r") as searchfile:
    searches = searchfile.readlines()
    # Loads the query lines into a list as objs in the list

# Keep track of items that have already been seen and ignore them.


# Doing the search with the queries defined in the txt file.
for query in searches:
    search_term = query.split(",")[0]
    if query.split(",")[1] != None:
        max_price = query.split(",")[1]

        search_url = ("http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=findItemsByKeywords\
&SERVICE-VERSION=1.0.0\
&GLOBAL-ID=EBAY-US\
&SECURITY-APPNAME=" + api_key +
"&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&SortBy=NewestItemsFirst\
&itemFilter(0).name=MaxPrice\
&itemFilter(0).value=" + max_price +\
"&itemFilter(0).paramName=Currency\
&itemFilter(0).paramValue=USD\
&keywords=" + search_term)
    # Remove spaces if they end up in the url
    search_url = search_url.replace(" ", "%20")

    # Search and parse the json
    search_result = requests.get(search_url)
    result_parse = search_result.json()

    for result in (result_parse['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']):
        title = result['title'][0]
        condition = result['condition'][0]['conditionDisplayName'][0]
        price = result['sellingStatus'][0]['currentPrice'][0]['__value__']
        item_id = result['itemId'][0]
        # open the txt file and appeand to the end of it.
        with open("item_log.txt", "a") as item_log:
            item_log.write(item_id + '\n')
        print(title + ' ' + condition + ' ' + price)
