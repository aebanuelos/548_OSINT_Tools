import os, sys, re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#soup = BeautifulSoup(html_doc, 'html.parser')
#def savePage(url, pagepath='page'):

def savePage(url, file_save_name):
    def savenRename(soup, pagefolder, session, url, tag, inner):
        if not os.path.exists(pagefolder): # create only once
            os.mkdir(pagefolder)
        for res in soup.findAll(tag):   # images, css, etc..
            if res.has_attr(inner): # check inner tag (file object) MUST exists
                try:
                    filename, ext = os.path.splitext(os.path.basename(res[inner])) # get name and extension
                    filename = re.sub('\W+', '', filename) + ext # clean special chars from name
                    fileurl = urljoin(url, res.get(inner))
                    filepath = os.path.join(pagefolder, filename)
                    # rename html ref so can move html and folder of files anywhere
                    res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                    if not os.path.isfile(filepath): # was not downloaded
                        with open(filepath, 'wb') as file:
                            filebin = session.get(fileurl)
                            file.write(filebin.content)
                except Exception as exc:
                    print(exc, file=sys.stderr)
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    #path, _ = os.path.splitext(pagepath)
    path, _ = os.path.splitext(desktop)
    #pagefolder = path+'_files' # page contents folder

    parent_dir = desktop
    directory = file_save_name+"_files"
    new_path = os.path.join(parent_dir, directory)
    os.mkdir(new_path)

    tags_inner = {'img': 'src', 'link': 'href', 'script': 'src'} # tag&inner tags to grab
    for tag, inner in tags_inner.items(): # saves resource files and rename refs
        savenRename(soup, new_path, session, url, tag, inner)
    with open(path+'.html', 'wb') as file: # saves modified html doc
        file.write(soup.prettify('utf-8'))

# url_name = input("Please Enter a URL to Scrape: ")
# file_save_name = input("Please Enter a folder name: ")
#
# savePage(url_name, file_save_name)