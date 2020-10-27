## Created mkwalter9 10/11/20
import os, sys
import numpy as np
import pandas as pd
from pprint import pprint
from parse_artbnk_html import PageParser
from image_parser import ImageFetcher
import logging
import time

logger = logging.getLogger()

run = str(time.time())

try:
    PAGES_DIR = str(sys.argv[1])
except:
    PAGES_DIR = 'pages'
logger.info(' || Using pages inside directory ' + PAGES_DIR)

IMAGES_DIR = 'images'

###########################

def get_img(row, fetcher):
    row['image_file'] = fetcher.fetch_image(row['img_url'])
    return row
########################## MAIN ###########################


pages = os.listdir(PAGES_DIR)

main_df = pd.DataFrame()

parser = PageParser(PAGES_DIR)
for page in pages:
    feats = parser.scrape_feats(page)
    df=pd.DataFrame(feats)

    imager = ImageFetcher(df.iloc[0]['Artist Name'])

    df = df.apply(get_img, args=(imager,),axis=1)
    print(df.head())
    main_df=main_df.append(df)

print(main_df.describe())
df.to_csv("artist_dataset_{}.csv".format(run), sep="|")
