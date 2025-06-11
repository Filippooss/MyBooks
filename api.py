import urllib
from urllib import request
from urllib.parse import quote_plus
from urllib import error
import json
#import time
import asyncio
import aiohttp
from aiohttp import ClientError
from PIL import Image
from io import BytesIO

from Views.book_view import Book

def fetch_book_data(search_data, filter_field):
    results_list = asyncio.run(get_info(search_data, filter_field))     #Εκτελεί τήν συνάρτηση/coroutine api_call και η
                                                    #οποία επιστρέφει τη λίστα με τα λεξικά με τις επεξεργασμένες εικόνες
    # Διαφορετικά, δημιουργία του event loop χειροκίνητα ώς εξής:
    # loop = asyncio.get_event_loop()
    # results_list = loop.run_until_complete(api_call(search_data))
    # loop.close()
    if type(results_list) != str:       #Άν δεν επιστράφηκε μήνυμα λάθους
        books = []      #Κάνει τη λίστα λεξικών λίστα αντικειμένων κλάσης Βook
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
        return books        #Επιστρέφει τη λίστα στο ui απο όπου κλήθηκε η fetch_book_data με το πάτημα κάποιου κουμπιού
    else:
        return results_list     #Επιστρέφει το μήνυμα λάθους για να εμφανιστεί στο ui

async def get_info(search_data, filter_field):
    results_list_data = api_call(search_data, filter_field)
    #image_calls_start = time.perf_counter()
    # Άνοιγμα των εικόνων απο το url που είναι αποθηκευμένες στη λίστα με τα λεξικά και αποθήκευση τους σε binary μορφή
    # για να τις περάσουμε στο gui. Θα το κάνουμε ασύγχρονα
    urls = []       #Μεταφέρουμε τις urls από τα λεξικά της λίστας αποτελεσμάτων σε μία δικιά τους λίστα
    if type(results_list_data) != str:
        for i in range(len(results_list_data)):
            urls.append(results_list_data[i]["Εξώφυλλο"])
        tasks = []      #Κάθε ένα task θα είναι το άνοιγμα μιας μεμονωμένης url εξώφυλλου
        try:
            async with aiohttp.ClientSession() as session:
                # Διαφορετικά με urllib3:
                # async with urllib3.AsyncPoolManager() as pm:
                for url in urls:    #για κάθε μία url + αυτών που μπορεί να βάλαμε εμείς ή να είναι από μόνες τους "image not available"
                    tasks.append(asyncio.create_task(get_image_data(session, url)))     #Τυλίγουμε τήν συνάρτηση/coroutine get_image_data
                                                                                        #με την εκάστοτε url σε ένα task και
                                                                                        #τα προσθέτουμε ένα-ένα στη λίστα tasks
                    #tasks.append(get_image_data(session, url))
                    # urllib3:
                    # tasks.append(asyncio.create_task(get_image_data(pm, url))) Ή
                    # tasks.append(get_image_data(pm, url)
                results = await asyncio.gather(*tasks)      #Τα επιμέρους results είναι τύπου 'bytes'
                #Βάζουμε κάθε αποτέλεσμα, δηλ. τις εικόνες σε binary(τύπου 'bytes'), στήν θέση των αντίστοιχων url απο όπου προήλθαν πίσω στα αντίστοιχα λεξικά τους
                count = 0       #Βοηθητικός απαριθμητής για τους δείκτες που αντιστοιχούν στα στοιχεία της λίστας results
                urls_remaining = []
                #Ορισμένα αποτελέσματα είχαν μορφή οριζόντιου παραλληλόγραμμου σαν παύλα με συγκεκριμένο μέγεθος για το πεδίο small
                for result_list_entry in results_list_data:
                    img = Image.open(BytesIO(results[count]))       #Τις ανοίγουμε με pillow και ελέγχουμε τις διαστάσεις τους
                    if img.size != (300, 48):       #Άν είναι κανονικές
                        result_list_entry["Εξώφυλλο"] = results[count]      #Τις προσθέτουμε στην αρχική λίστα στη θέση της αντίστοιχης url
                        count = count + 1
                    else:       #Άν είναι προβληματικές
                        #Τις προσθέτουμε σε μία άλλη λίστα σε προετοιμασία για να τις γυρίσουμε πίσω σε τύπου thumbnail μιας και συνήθως αυτά ήταν κανονικά
                        #Θα υποστούμε τήν μείωση της ευκρίνειας για να έχουμε τουλάχιστον μία εικόνα
                        urls_remaining.append(result_list_entry["Εξώφυλλο"])
                        count = count + 1
                #image_calls_correct_end = time.perf_counter()
                #print(f'correct:{image_calls_start-image_calls_correct_end}')
                for i in range(len(urls_remaining)):        #for url in urls_remaining: url = url.replace('&zoom=2', '&zoom=1') δεν δουλεύει
                    urls_remaining[i] = urls_remaining[i].replace("&zoom=2", "&zoom=1")     #Αλλαγή πίσω σε μέγεθος thumbnail
                #Θα "καθαρίσουμε" τις 2 λίστες που χρησιμοποιήσαμε με σκοπό να τις χρησιμοποιήσουμε εκ νέου
                tasks.clear()
                results.clear()
                #άνοιγμα των υπόλοιπων εξώφυλλων σε μέγεθος thumbnail που ήταν προβληματικά σε μέγεθος small
                try:        #Και η δευτερεύουσα επεξεργασία γίνεται στο ίδιο ClientSession για να επωφεληθούμε του connection pooling.
                    if len(urls_remaining) != 0:
                        for url in urls_remaining:
                            tasks.append(asyncio.create_task(get_image_data(session, url)))
                            # tasks.append(fetch_data(session, url))
                        results = await asyncio.gather(*tasks)
                        count = 0
                        for result_list_entry in results_list_data:     #Τοποθέτηση τους πίσω στην αρχική λίστα. Είναι γεμάτη από εικόνες μεγέθους small
                                                                        #πλήν εκείνων που είχαν πρόβλημα στη θέση των οπίων έχουμε ακόμα τo string της url
                            if type(result_list_entry["Εξώφυλλο"]) == str:
                                result_list_entry["Εξώφυλλο"] = results[count]      #Εκμεταλλευόμαστε το γεγονός ότι τα results τοποθετήθηκαν με την ίδια
                                                                                    #σειρά με την οποία εμφανίζονται και στήν λίστα
                                count = count + 1
                        #image_calls_remaining_end = time.perf_counter()
                        #print(f'remaining:{image_calls_correct_end-image_calls_remaining_end}')
                    #image_calls_end = time.perf_counter()
                    #print(f"image calls:{image_calls_end - image_calls_start}")
                except ClientError:     #Άν παρουσιαστεί λάθος στο δευτερεύων άνοιγμα των εικόνων
                    error_message = "Error during loading of covers"
                    return error_message
        except aiohttp.ClientError:     #Άν παρουσιαστεί λάθος κατά το πρωτεύων άνοιγμα των εικόνων
            error_message = "Error during loading of covers"
            return error_message        #Επιστροφή μηνύματος λάθους και όχι τήν λίστα των αποτελεσμάτων
    return results_list_data        #Άν στην κλήση στη σειρά 42 επιστράφηκε error string προσπερνώνται οι παραπάνω εντολές και επιστρέφεται το string
                                    #αλλιώς επιστροφή της ίδιας λίστας, που αντί για τις url, έχει τις εικόνες σε binary

def api_call(query, filter_field):
    #start = time.perf_counter()
    query = quote_plus(query)        #Διαχείριση ειδικών χαρακτήρων και κωδικοποίηση μή ASCII κειμένου για χρήση τους σε url
    url = 'https://www.googleapis.com/books/v1/volumes?q='      #Το πρώτο μέρος της url
    max_results = '&maxResults=15'      #Παράμετρος που περιορίζει τα αποτελέσματα δίνοντας το μέγιστο αριθμό
    fields = '&fields=items(volumeInfo(title,authors,publisher,publishedDate,description,imageLinks))'
    if filter_field == "None":      #Άν το πεδίο φίλτρου είναι None τότε έχουμε γενική αναζήτηση
        url = url + query       #+ query.replace(' ','+') άν στη γραμμή 114 χρησιμοποιούσαμε την απλή quote
    #Για τη δημιουργία της σωστής url εκτός από τα docs ανέτρεξα και στην Advanced Book Search πληκτρολογώντας σε διάφορα entries
    #και βλέποντας πώς σχηματιζόταν η url. 2 τρόπους εκ τον οποίο χρησιμοποίησα τον πιό σύνηθες
    #Δοκίμασα να τα γράφω όλα με τη μορφή '+something:' και δούλεψε και αυτό βέβαια αλλά δεν ήταν ακριβώς όπως έβλεπα να σχηματίζεται η url
    if filter_field == "Title":
        title_keywords_list = query.split()     #Χωρίζουμε το string στα κενά και παίρνουμε τις πιθανές λέξεις μία-μία
        for i, keyword in enumerate(title_keywords_list):       #Κάθε μία με την αντίστοιχη παράμετρο μπροστά
            if i == 0:                                          #και κάθε πρώτη χωρίς το '+'
                url = url + 'intitle:' + keyword
            else:
                url = url + '+intitle:' + keyword
    if filter_field == "Author":
        author_keywords_list = query.split()
        for i, keyword in enumerate(author_keywords_list):
            if i == 0:
                url = url + 'inauthor:' + keyword
            else:
                url = url + '+inauthor:' + keyword
    if filter_field == "Publisher":
        publisher_keywords_list = query.split()
        for i, keyword in enumerate(publisher_keywords_list):
            if i == 0:
                url = url + 'inpublisher:' + keyword
            else:
                url = url + '+inpublisher:' + keyword
    full_url = url  + max_results + fields
    try:
        with request.urlopen(full_url) as response:
            data = response.read()      #Σε 'bytes'
            book_data = data.decode('Utf-8')        #Αποκωδικοποίηση από 'bytes' σε string 'utf-8'
            data_needed = json.loads(book_data)     #σε ένα αντικείμενο της python(λεξικό)
            # Διαφορετικά με urllib3:
            # response = urllib3.request("GET", full_url)
            # if response.status == 200:
            #     data_needed = response.json()
            # ......
            # response.close()
            results_list = []       #Αρχικοποίηση μίας λίστας στην οποία θα εκχωρήσουμε όλα τα αποτελέσματα σε δομή λεξικού. Θα είναι μια λίστα λεξικών
            info_count = 0      #Επειδή ορισμένες φορές για κάποιο αποτέλεσμα υπάρχουν πολύ λίγα από τα πεδία που χρειαζόμαστε
                                #κρατάμε έναν μετρητή με πόσα υπάρχουν και άν υπάρχουν από 4 και πάνω το κρατάμε αλλιώς θεωρείται άχρηστο
            if "items" in data_needed:
                for number in range(len(data_needed["items"])):     #Θα είναι ίσο με τον αριθμό αποτελεσμάτων που
                                                                    # φορτώθηκαν με το &maxresults(απο 0 εως maxresults - 1)
                    # Επειδή δεν υπάρχουν πάντα όλα τα κλειδιά στα αποτελέσματα γίνεται έλεγχος ύπαρξης τους και διαφορετικά μπαίνει ''
                    if "title" in data_needed["items"][number]["volumeInfo"]:       #Άν το κλειδί τίτλου υπάρχει
                        title = data_needed["items"][number]["volumeInfo"]["title"]     #Εκχώρηση της τιμής του στήν αντιστοιχη μεταβλητή
                        info_count = info_count + 1
                    else:
                        title = ''      #Αλλιώς εκχώρηση κενού string
                    if "authors" in data_needed["items"][number]["volumeInfo"]:
                        author = data_needed["items"][number]["volumeInfo"]["authors"][0]
                        info_count = info_count + 1
                    else:
                        author = ''
                    if "publisher" in data_needed["items"][number]["volumeInfo"]:
                        publisher = data_needed["items"][number]["volumeInfo"]["publisher"]
                        info_count = info_count + 1
                    else:
                        publisher = ''
                    if "publishedDate" in data_needed["items"][number]["volumeInfo"]:
                        published_date = data_needed["items"][number]["volumeInfo"]["publishedDate"]
                        info_count = info_count + 1
                    else:
                        published_date = ''
                    if "imageLinks" in data_needed["items"][number]["volumeInfo"]:
                        thumbnail = data_needed["items"][number]["volumeInfo"]["imageLinks"]["thumbnail"].replace(
                            "&edge=curl", "")       #Άφαιρούμε την παράμετρο που κάνει την κάτω δεξιά γωνία των εξώφυλλων να είναι διπλωμένη
                        thumbnail = thumbnail.replace("&zoom=1", "&zoom=2")     #Έύκολος τρόπος να πάρεις από το πεδίο thumbnail το πεδίο small μιάς και αυτά διαφέρουν μόνο στην παράμετρο zoom
                        info_count = info_count + 1
                    else:
                        #Η μόνη διαφορά σε σχέση με τα άλλα είναι πώς αντί για κενό str βάζουμε την εικόνα "image not available"
                        thumbnail = "https://books.google.com/books/content?id=RAEkxQEACAAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api"
                    if "description" in data_needed["items"][number]["volumeInfo"]:
                        description = data_needed["items"][number]["volumeInfo"]["description"]
                        info_count = info_count + 1
                    else:
                        description = ''
                    if info_count >= 4:     #Άν υπάρχουν απο 4 και πάνω αποτελέσματα δημιουργείτε το λεξικό και προστίθεται στο τέλος της λίστας
                        results_dict = {"Τίτλος": title, "Συγγραφέας": author, "Εκδότης": publisher, "Έτος έκδοσης": published_date, "Εξώφυλλο": thumbnail, "Περιγραφή": description}
                        results_list.append(results_dict)
                #end = time.perf_counter()
                #print(end-start)
                return results_list
            else:
                print('not found')
                return []
    except urllib.error.URLError as e:      #Όλες οι πιθανές εξαιρέσεις που μπορεί να προκύψουν από την urllib
        message = str(e.reason)
        return message
    except json.JSONDecodeError as e:       #Εξαιρέσεις για τη χρήση της json.loads
        message = f'Invalid JSON syntax:{str(e)}'
        return message
    except UnicodeDecodeError as e:
        message = str(e)
        return message
    except:         #Γενική εξαίρεση
        return f'An error occurred'

async def get_image_data(session, url):     #urllib3:async def get_image_data(pm, url):
    #call_s = time.perf_counter()
    async with session.get(url) as response:
        data = await response.read()        #Διαβάζουμε τα περιεχόμενα της απάντησης. Επιστρέφει 'bytes'
        #call_e = time.perf_counter()
        #print(f"call:{call_e-call_s}")
        return data