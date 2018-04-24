from flickrapi import FlickrAPI
import os
import base64
import requests
import boto3

import googleapiclient.discovery
import decimal


def main():
    service = googleapiclient.discovery.build('vision', 'v1')
    flickr = FlickrAPI(os.environ['flickr_public'], os.environ['flickr_secret'], format='parsed-json')
    extras = 'url_m'

    cats = flickr.photos.search(user_id='johnnydeppforever', per_page='100', extras=extras)

    count = 0
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

        dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
        table = dynamodb.Table('lab6-flickr')

        response = service_request.execute()
        print("Results for image %s:" % i['title'])
        for result in response['responses'][0]['labelAnnotations']:
            count = count + 1
            print("%s - %.3f" % (result['description'], result['score']))
            response = table.put_item(
                Item={
                    'id' : str(count),
                    'img-id': i['id'],
                    'tag': result['description'],
                    'probability': round(decimal.Decimal(result['score']), 2),
                },
                ReturnValues='ALL_OLD',
            )
        print("\n")


if __name__ == '__main__':
    main()
