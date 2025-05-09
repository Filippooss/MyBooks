from urllib import request
import json
import time
import asyncio
import aiohttp

def fetch_book_data(search_data):
    results_list = asyncio.run(api_call(search_data))
    return results_list

async def api_call(search_data):
    results_list_data = get_info(search_data)
    image_calls_start = time.perf_counter()
    urls = []
    for i in range(len(results_list_data)):
        urls.append(results_list_data[i]["Εξώφυλλο"])
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            if url != '':
                tasks.append(get_image_data(session, url))
                # tasks.append(asyncio.create_task(self.get_image_data(session, url)))
        results = await asyncio.gather(*tasks)
    count = 0
    for num in range(len(results_list_data)):
        if results_list_data[num]["Εξώφυλλο"] != '':
            results_list_data[num]["Εξώφυλλο"] = results[count]
            count = count + 1
    image_calls_end = time.perf_counter()
    print(f"image calls:{image_calls_end - image_calls_start}")
    return results_list_data

def get_info(search_data):
    start = time.perf_counter()
    url = 'https://www.googleapis.com/books/v1/volumes?q='
    max_results = '&maxResults=10'
    fields = '&fields=items(volumeInfo(title,authors,publisher,publishedDate,description,categories,imageLinks))'
    full_url = url + search_data.replace(" ", "%20") + max_results + fields
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
                    thumbnail = data_needed["items"][number]["volumeInfo"]["imageLinks"]["thumbnail"]
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