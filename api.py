from urllib import request
import json


def get_info(search_data):
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
            return results_list
        else:
            print('not found')
    else:
        print('error')