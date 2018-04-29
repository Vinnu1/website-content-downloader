import urllib.request
import re
from bs4 import BeautifulSoup
base_url = str(input("Enter homepage(with https/http):"))
base_url_regex = r""+re.escape(base_url)+r""
def get_page(my_url,dict_list):
    print("This url:",my_url)
    #print("Inside func:",dict_list)
    try:
        html = urllib.request.urlopen(my_url)
    except urllib.error.URLError as e:
        print("Error", e.reason)
        return
    html_page = BeautifulSoup(html,"html.parser")
    #page_content = html_page.find('html') #+ "\n"
    all_links = html_page.find_all('a')
    for links in all_links:
        url = links.get('href')
        if(url.find('#') > - 1): #re.match(r'#',url,re.M
            print("A comment found:",url) #REMOVE ID #
            continue
        if(not re.match( r'https:' or 'http:', url, re.M)):
            if(my_url.find(url) > -1):
                print("Current url:",my_url,"Link:",url)
                url = base_url + "/" + url #PROBLEM
            else:
                if(re.match(r'$.com' or r'a-zA-Z',url[len(url)-6:],re.M )): # check last <6 characters to see whether its .com or a folder
                    print("Current url:",my_url ,"Child url:",url)
                    url = my_url +"/"+ url
                else:
                    url = base_url + "/" + url
        else:
            if(not re.match( base_url_regex, url, re.M)):
                continue
        #print (url,"is relative.")
        #print ("Converting into absolute:",my_url + "/" + url)

        if(url in dict_list):
            continue
        else:
            #print("Url:",url)
            dict_list[url] = 1
    return dict_list

count = 0
my_list = {base_url:1}
distinct_list = get_page(base_url,my_list)
for urls in distinct_list:
    count+=1
    this_list = get_page(urls, distinct_list) 
    distinct_list = {**distinct_list, **this_list}
print("Total loops:",count)
print(distinct_list)