from flickrapi import FlickrAPI
import os
import base64
import requests
import boto3
import logging
from collections import Counter
import sys
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (14,14)
import matplotlib.pyplot as plt

plt.switch_backend('agg')

import googleapiclient.discovery
import decimal


logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
table = dynamodb.Table('lab6-flickr')

def store_tag(count, img_id, tag, probability):
    response = table.put_item(
        Item={
            'id': str(count),
            'img-id': img_id,
            'tag': tag,
            'probability': round(decimal.Decimal(probability), 2),
        },
        ReturnValues='ALL_OLD',
    )
    return response

def get_tag():
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']
    logger.error('Unknown error')
    return None

def generatePlot(count,plotName):
    print(count.most_common(15))
    sorted_x, sorted_y = zip(*count.most_common(15))
    print(sorted_x, sorted_y)

    plt.bar(range(len(sorted_x)), sorted_y, width=0.75, align='center')
    plt.xticks(range(len(sorted_x)), sorted_x, rotation=60)
    plt.axis('tight')
    plt.show()
    plt.savefig(plotName)
    plt.gcf().clear()



def generate_chart():
    items = get_tag()
    count  = Counter()

    for item in items:
        if item['probability'] > 0.7:
            tag = [item['tag']]
            count.update(tag)
    generatePlot(count, "chart")

    return None

def get_image():
    count = 0
    service = googleapiclient.discovery.build('vision', 'v1')
    flickr = FlickrAPI(os.environ['flickr_public'], os.environ['flickr_secret'], format='parsed-json')

    cats = flickr.photos.search(user_id='johnnydeppforever', per_page='100', extras='url_m')

    for i in cats['photos']['photo']:
        image_content = base64.b64encode(requests.get(i['url_m']).content)
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
            }]
        })

        response = service_request.execute()
        print("Results for image %s:" % i['title'])
        if response['responses'][0] :
            for result in response['responses'][0]['labelAnnotations']:
                count = count + 1
                print("%s - %.3f" % (result['description'], result['score']))
                store_tag(count, i['id'], result['description'], result['score'])

            print("\n")

if sys.argv[1] == "store":
    get_image()
if sys.argv[1] == "chart":
    generate_chart()
