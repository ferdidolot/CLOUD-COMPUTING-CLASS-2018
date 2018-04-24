## Advanced Analytics as a Service in the Cloud (optional task) ##

## Task 6.3.4: Classify images ##

We have decided to analyze images from Flickr, by using Flickr API.

In the `environment.sh` file we have set define the environment variables like below:
We have replaced the `YOURFLICKPUBLIC` and `YOURFLICKRSECRET` with the API public key and secret for our account, to enable authentication.
We have also specified the path for our credentials of the Google Cloud Platform.

``flickr_public='YOURFLICKRPUBLIC'
flickr_secret='YOURFLICKRSECRET'
AWS_REGION='YOURAWSREGION'
GOOGLE_APPLICATION_CREDENTIALS='YOURPATHTOGOOGLEVISIONAPI.json'``


**Obtain the last 100 images from the profile entered and send the images to Google Cloud Vision**

We have analyzed the 100 Flickr photos from the public profile "johnnydeppforever". The max number of tags that we will retrieve for each
photo is limited to 5.

``  def get_image():
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
``


**Store all the tags describing the images and the associated probabilities**

We stored the tags and the associated probabilities for each image in Dynamo DB.


``  dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
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
    ``
This is how our Dynamo DB table look like:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6_Optional/Lab6_Task6.3_1.png)

**Create a histogram**

We decided to offer the user the possibility to easily check on a chart top 15 tags of his/her pictures.
The interesting part is that we are considering only the tags that have a probability greater by 0.7 assigned by Google Cloud Vision.
So the user can see with an accurancy greater than 70% what tags are his pictures mostly related.


To get the tags we have used the following functions:
``
def get_tag():
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']
    logger.error('Unknown error')
    return None
    ``

``
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

    ``
The following histogram shows that with an accuracy of 70% the pictures of Johny Deep are mostly related with `outwear`,
`costume`, `poster`, `headgear`.


![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6_Optional/Lab6_Task6.3_2.png)
**Q63: What problems have you found developing this section? How did you solve them**


**Q64: How long have you been working on this session (including the optional part)? What have been the main difficulties you have faced and how have you solved them? **

