from urllib import request
import json
import time
import asyncio
import aiohttp
from PIL import Image
from io import BytesIO

from Views.book_view import Book

def fetch_book_data(search_data):
    results_list = asyncio.run(get_info(search_data))
    books = []
    for result in results_list:
        book = Book(
            id=0,
            title=result["Τίτλος"],
            author=result["Συγγραφέας"],
            publisher=result["Εκδότης"],
            release_year=result["Έτος έκδοσης"],
            description=result["Περιγραφή"],
            image_raw=result["Εξώφυλλο"],
            version=1
        )
        books.append(book)
    return books

async def get_info(search_data):
    results_list_data = api_call(search_data)
    image_calls_start = time.perf_counter()
    urls = []
    for i in range(len(results_list_data)):
        urls.append(results_list_data[i]["Εξώφυλλο"])
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            if url != '':
                tasks.append(asyncio.create_task(get_image_data(session, url)))
                #tasks.append(get_image_data(session, url))
        results = await asyncio.gather(*tasks)
    count = 0
    urls_remaining = []
    for result_list_entry in results_list_data:
        if result_list_entry["Εξώφυλλο"] != '':
            img = Image.open(BytesIO(results[count]))
            print(type(img))
            if img.size != (300, 48):
                result_list_entry["Εξώφυλλο"] = results[count]
                count = count + 1
            else:
                urls_remaining.append(result_list_entry["Εξώφυλλο"])
                count = count + 1
    for i in range(len(urls_remaining)):
        urls_remaining[i] = urls_remaining[i].replace("&zoom=2", "&zoom=1")
    tasks.clear()
    results.clear()
    async with aiohttp.ClientSession() as session:
        for url in urls_remaining:
            tasks.append(asyncio.create_task(get_image_data(session, url)))
            # tasks.append(fetch_data(session, url))
        results = await asyncio.gather(*tasks)
    count = 0
    for result_list_entry in results_list_data:
        if type(result_list_entry["Εξώφυλλο"]) == str and result_list_entry["Εξώφυλλο"] != '':
            print(result_list_entry["Εξώφυλλο"])
            result_list_entry["Εξώφυλλο"] = results[count]
            count = count + 1
    image_calls_end = time.perf_counter()
    print(f"image calls:{image_calls_end - image_calls_start}")
    return results_list_data

def api_call(search_data):
    start = time.perf_counter()
    url = 'https://www.googleapis.com/books/v1/volumes?q='
    max_results = '&maxResults=10'
    fields = '&fields=items(volumeInfo(title,authors,publisher,publishedDate,description,categories,imageLinks))'
    api_key = '&key=AIzaSyBl7lf8Y8Frix__Bh7OoqPZfKSvvgdQfUw'
    full_url = url + search_data.replace(" ", "%20") + max_results + fields + api_key
    response = request.urlopen(full_url)
    if response.code == 200:
        data = response.read()
        book_data = data.decode('Utf-8')
        data_needed = json.loads(book_data)
        results_list = []
        if "items" in data_needed:
            for number in range(len(data_needed["items"])):
                if "title" in data_needed["items"][number]["volumeInfo"]:
                    title = data_needed["items"][number]["volumeInfo"]["title"]
                else:
                    title = ''
                if "imageLinks" in data_needed["items"][number]["volumeInfo"]:
                    thumbnail = data_needed["items"][number]["volumeInfo"]["imageLinks"]["thumbnail"].replace("&edge=curl", "")
                    thumbnail = thumbnail.replace("&zoom=1", "&zoom=2")
                else:
                    thumbnail = ''
                if "authors" in data_needed["items"][number]["volumeInfo"]:
                    author = data_needed["items"][number]["volumeInfo"]["authors"][0]
                else:
                    author = ''
                if "publisher" in data_needed["items"][number]["volumeInfo"]:
                    publisher = data_needed["items"][number]["volumeInfo"]["publisher"]
                else:
                    publisher = ''
                if "publishedDate" in data_needed["items"][number]["volumeInfo"]:
                    published_date = data_needed["items"][number]["volumeInfo"]["publishedDate"]
                else:
                    published_date = ''
                if "description" in data_needed["items"][number]["volumeInfo"]:
                    description = data_needed["items"][number]["volumeInfo"]["description"]
                else:
                    description = ''
                results_dict = {"Τίτλος": title, "Συγγραφέας": author, "Εκδότης": publisher, "Έτος έκδοσης": published_date, "Εξώφυλλο": thumbnail, "Περιγραφή": description}
                results_list.append(results_dict)
            end = time.perf_counter()
            print(end-start)
            return results_list
        else:
            print('not found')
    else:
        print('error')

async def get_image_data(session, url):
    call_s = time.perf_counter()
    async with session.get(url) as response:
        data = await response.read()
        call_e = time.perf_counter()
        print(f"call:{call_e-call_s}")
        return data