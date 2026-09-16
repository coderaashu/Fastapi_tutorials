"""
import requests
from bs4 import BeautifulSoup

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

soup = BeautifulSoup(requests.text,"html.parse")
print(soup.title.text)

"""
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time    #for cache

app = FastAPI()

#cache storage
cache_data = []
last_fetch = 0

@app.get("/news")
def get_news(page: int = 1,limit:int = 6):
    global cache_data,last_fetch

    start =time.time()
    if time.time() - last_fetch >60:
        print("fetching fresh data")
        url ="https://news.ycombinator.com/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")

        cache_data = [item.text for item in soup.find_all("span",class_="titleline")]
        last_fetch = time.time()
    else:
        print("using cache data")
    end =time.time()

    time_taken = round(end-start,4)

    print("time taken:",time_taken)

    return{
        "time_taken":time_taken,
        "data":cache_data[:5]
    }
"""  
    #simple wb_crawling
    title = []
                                   
    for item in soup.find_all("span",class_="titleline"):    #a 
        title.append(item.text)
    #pagination logic
    start = (page -1)* limit
    end =start + limit
    return{
        # "page":page,
        # "limit":limit,
        # "total": len(title),
        #"data":title[start:end]
        "data":title[:5]
    }
    """