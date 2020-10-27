## Created mkwalter9 10/11/20
from bs4 import BeautifulSoup
import re

class PageParser:

    def __init__(self, pages_dir):
    	self.pagedir = pages_dir

    def scrape_feats(self, path_to_html):
        self.path = "{}/{}".format(self.pagedir, path_to_html)
        with open(self.path, 'r') as f: contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        try:
            itemlist_tag = find_tagnum(soup, "ItemList-0-")
            works_set = soup.find("div", {"class": "ItemList-0-{}".format(itemlist_tag)}).children
        except:
            works_tag = find_tagnum(soup, "artistWorks-0-")
            works_set = soup.find("div", {"class": "artistWorks-0-{}".format(works_tag)}).children

        works = []

        for n in works_set:
            root_tag = find_tagnum(n,"root-0-")
            thumb_tag = find_tagnum(n, "thumb-0-")
            try:
                img_url = str(n.find('div', {"class": "root-0-{} thumb-0-{}".format(root_tag, thumb_tag)})).split('("')[1].split('")')[0]
            except IndexError:
                img_url = ''

            title_tag = find_tagnum(n,"title-0-")
            value_tag = find_tagnum(n,"value-0-")
            title = str(n.find('dt', {"class":"title-0-{} ItemList titleSolver".format(title_tag)})).split(">")[1].split("</")[0]
            title_val = str(n.find('dd', {"class":"value-0-{} ItemList titleSolver".format(value_tag)})).split(">")[1].split("</")[0]

            artist = str(n.find('dt', {"class":"title-0-{} ItemList artistSolver".format(title_tag)})).split(">")[1].split("</")[0]
            artist_val = str(n.find('dd', {"class":"value-0-{} ItemList artistSolver".format(value_tag)})).split(">")[1].split("</")[0]

            a = []
            b = []

            content_tag = find_tagnum(n,"content-0-")
            for m in n.find('div', {"class":"content-0-{}".format(content_tag)}).children:
                keys = m.find_all('dt', {"class":"title-0-{} ItemList".format(title_tag)})
                vals = m.find_all('dd', {"class":"value-0-{} ItemList".format(value_tag)})
            for i in keys: a.append(str(i).split(">")[1].split("</")[0])
            for j in vals: b.append(str(j).split(">")[1].split("</")[0])
            attrs = dict(zip(a,b))
            attrs['img_url'] = img_url
            attrs[title] = title_val
            attrs[artist] = artist_val
            works.append(attrs)
        return works

def find_tagnum(item, search_for): #different for each element for each artist/page
    ind=str(item).find(search_for)
    pad=len(search_for)
    matched=re.match(r"[0-9]+",str(item)[ind+pad:])
    return matched[0]
