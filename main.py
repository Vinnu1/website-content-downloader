import urllib.request
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import os
base_url = str(input("Enter homepage(with https/http):"))
base_url_regex = r""+re.escape(base_url)+r""
if(base_url[-1] == "/"):
    base_name = re.split(r'/',base_url)[-2]
else:
    base_name = re.split(r'/',base_url)[-1]
#creating download directory    
os.makedirs("downloads",exist_ok=True)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    texts = soup.findAll(text=True) #.get_text()   
    visible_texts = filter(tag_visible, texts)  
    return u"\n".join(t.strip() for t in visible_texts)
    #return texts

def get_page(my_url,dict_list):
    print("This url:",my_url)
    try:
        html = urllib.request.urlopen(my_url)
    except urllib.error.URLError as e:
        print("Error", e.reason)
        return
    html_page = BeautifulSoup(html,"html.parser")
    #naming files
    file_name = re.split(r'/',my_url)[-1]
    if(file_name == "" or file_name == base_name):
        file_name = "home.html"
    #downloading files
    file = open("downloads/"+file_name,"w+")
    #html_body = html_page.find('body')
    file.write(str(text_from_html(html_page)))
    file.close()
    all_links = html_page.find_all('a')
    for links in all_links:
        url = links.get('href') # added str
        if(url.find('#')> -1): #re.match(r'#',url,re.M
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

        if(url[-1:] == "/"):
            print("/ at end:",url)
            url = url[:-1]     
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
#print(distinct_list)
print(len(distinct_list))