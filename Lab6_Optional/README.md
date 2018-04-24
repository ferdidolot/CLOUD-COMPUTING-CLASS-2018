## Advanced Analytics as a Service in the Cloud (optional task) ##

## Task 6.3.4: Classify images ##

We have decided to analyze images from Flickr, by using Flickr API.

In the `environment.sh` file we have define the environment variables like below.
We have replaced the `YOURFLICKRPUBLIC` and `YOURFLICKRSECRET` with the API public key and secret for our account, to enable authentication.
Also we have specified the path for our credentials of the Google Cloud Platform.

```
flickr_public='YOURFLICKRPUBLIC'
flickr_secret='YOURFLICKRSECRET'
AWS_REGION='YOURAWSREGION'
GOOGLE_APPLICATION_CREDENTIALS='YOURPATHTOGOOGLEVISIONAPI.json'
```


**Obtain the last 100 images from the profile entered and send the images to Google Cloud Vision**

We have analyzed the 100 Flickr photos from the public profile`johnnydeppforever`. The max number of tags that we will retrieve for each
photo is limited to 5.

```
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
            
```
            

**Store all the tags describing the images and the associated probabilities**

We stored the tags and the associated probabilities for each image in Dynamo DB.

```
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
```
This is how our Dynamo DB table looks like:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6_Optional/Lab6_Task6.3_1.png)

**Create a histogram**

We decided to offer the user the possibility to easily check on a chart the top 15 tags of his/her pictures.
The interesting part is that we are considering only the tags that have a probability greater than 0.7 assigned by Google Cloud Vision.
So the user can see with an accurancy greater than 70% with what tags are his/her pictures mostly related.


To get the tags we have used the following function:
```
def get_tag():
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']
    logger.error('Unknown error')
    return None
```

To generate the plot we use the following function:
```
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
```

The following histogram shows that with an accuracy of 70% the pictures of Johny Deep are mostly related with `outwear`,
`costume`, `poster`, `headgear`, etc.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6_Optional/Lab6_Task6.3_2.png)
**Q63: What problems have you found developing this section? How did you solve them**

We were trying to find a way to process the images on the fly and send them directly to Google Vision API. We used `base64` to encode the content and send it to the API. 

**Q64: How long have you been working on this session ? What have been the main difficulties you have faced and how have you solved them?**

We have worked on this session 4 hours. There were no main difficulties for this Lab and we use to referer to the documentation for issues we faced. 
