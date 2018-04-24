from flickrapi import FlickrAPI
import os
import json
import urllib
import base64
from PIL import Image
import requests
from io import BytesIO


import io

#obtain public images from flickr
flickr = FlickrAPI(os.environ['flickr_public'], os.environ['flickr_secret'], format='parsed-json')
extras='url_m'
cats = flickr.photos.search(user_id='johnnydeppforever', per_page='100', extras=extras )
sample_url = cats['photos']['photo'][0]['url_m']
print ('URL: '+sample_url)


response = requests.get(sample_url)
print(response.content)
img = Image.open(BytesIO(response.content))
print (img)
image_content = base64.b64encode(requests.get(sample_url).content)
print(image_content)