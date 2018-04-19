## GitHub Repository for the Web App ##

## Task 6.1: How to provide your services through a REST API? ##
After creating the new view "chart", we can access http://127.0.0.1:8000/chart to see how many emails we have gathered in our web app.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_1.png)

We can also visualize the chat with different parameters defined by the user and we will have:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_2.png)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_3.png)


**Q61a: Having domain_freq.json written as static content is not the best way to distribute it because different clients
can invoke different parameters simultaneously? Can you use S3 to solve the problem? Write the changes in the code and explain your solution?**


We don't think that using S3 will solve the problem of user accessing sumultinous file, so we used the approach below to efficiently implement this view, in order to deal with simultaneous invocations with different parameters.


![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_4.jpeg)

The flow is as follow: client request the chart with parameter, then our web application will send query to dynamoDB database and get the result from it. Instead of storing the data from dynamoDB and load render it to html, we can create a json object and render it to html directly. We have changed the implementation of chart in views.py as follow:
```
def chart(request):
    domain = request.GET.get('domain')
    preview = request.GET.get('preview')
    leads = Leads()
    items = leads.get_leads(domain, preview)
    domain_count = Counter()
    if domain or preview:
        items = leads.get_leads(domain, preview)
        domain_count.update([item['email'].split('@')[1] for item in items])
    else:
        domains = leads.get_domains()
        domain_list = {}
        for item in domains:
            domain_list[item['domain']] = int(item['num'])
        domain_count = Counter(dict(domain_list))

    domain_freq = domain_count.most_common(15)
    if len(domain_freq) == 0:
        return HttpResponse('No items to show', status=200)

    labels, freq = zip(*domain_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    val = bar.to_json()

    return render(request, 'chart.html', {'view': bar.to_json()})
```

And in chart.html file, we also have changed the implementation to adjust with the explained change as follow:
```
<script type="text/javascript">
    function parse(spec) {
        vg.parse.spec(spec, function (chart) {
            chart({el: "#vis"}).update();
        });
    }
    {% autoescape off %}
    var spec = JSON.parse(JSON.stringify({{ view }}));
    parse(spec);
    {% endautoescape %}


</script>
```

**Q61b: Once you have your solution implemented publish the changes to EB and try the new functionality in the cloud. Did you need to change anything, apart from the code, to make the web app work?** <br/>
We have to replace requirement.txt by executing `pip freeze > requirement.txt` and push it into the repository and add environment variable for twitter-geo table. 

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_5.png)

That way, the chart is successfully deployed to EB.
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_8.png)

## Task 6.2: How to provide our service combined with third-party services? ##

We implemented TwitterListener.py as follow. First we have to create table in dynamoDB for twitter-geo. In TwitterListener.py, we specified the AWS_REGION and GEO_TABLE from os environment. First, we have to define environment.sh file to export some additional parameter.
```
...
export GEO_TABLE="twitter-geo"
export consumer_key="OurTwitterConsumerKey"
export consumer_secret="OurTwitterConsumerSecret"
export access_token="OurTwitterAccessToken"
export access_secret="OurTwitterAccessSecret"
```

And we source the environment variables. The reason why we put the authentication in environment variable is because later we want to use it when we are deploying our application to elastic beanstalk for easier purposes. We have changed TwitterListener.py as following:

```
..
AWS_REGION = os.environ['AWS_REGION']
GEO_TABLE = os.environ['GEO_TABLE']
...
def run():
    print("Twitter Listener run!")
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_secret = os.environ['access_secret']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(locations=[-2.5756, 39.0147, 5.5982, 43.957])
```
Content of dynamoDB after running TwitterListener.py can be seen as follow.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_3.png)

And the result of map can also be seen on image below.
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_1.png)

**Q62a: Now we are showing all the collected tweets on the map. Can you think of a way of restricting the tweets plotted using some constraints? For instance, the user could invoke http://127.0.0.1:8000/map?from=2018-02-01-05-20&to=2018-02-03-00-00. Implement that functionality or any other functionality that you think it could be interesting for the users** <br/>
We have to extract the request when user call url /map and pass it to `get_tweet()` function.
```
def map(request):
    start_date = request.GET.get("from", False)
    end_date = request.GET.get("to", False)
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    tweets = Tweets()
    for tweet in tweets.get_tweets(start_date, end_date):
    ...
    return render(request, 'map.html',{'filename' : filename})
```

Inside `get_tweets()` function, we then filter the record in dynamoDB by using expression attribute values and filter expression operation if the parameter does exist.

```
def get_tweets(self, start_date, end_date):
      expression_attribute_values = {}
      FilterExpression = []

      if start_date:
          expression_attribute_values[':start'] = start_date
          FilterExpression.append('created_at >= :start')
      if end_date:
          expression_attribute_values[':end'] = end_date
          FilterExpression.append('created_at <= :end')
      if expression_attribute_values and FilterExpression:
          response = self.table().scan(
              FilterExpression=' and '.join(FilterExpression),
              ExpressionAttributeValues=expression_attribute_values,
          )
      else:
          response = self.table().scan(
              ReturnConsumedCapacity='TOTAL',
          )
```
By doing this, we are able to filter tweet on some period of time.

**Q62b: Make the necessary changes to have geo_data.json distributed using S3, or the method you used for the above section. Publish your changes to EB and explain what changes have you made to have this new function working** <br/>
First we have to specify our settings.py file in order to provide information about our S3 bucket.

```
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = "eb-django-express-signup-raisa-ferdi"
AWS_S3_CUSTOM_DOMAIN = 's3.eu-central-1.amazonaws.com/eb-django-express-signup-raisa-ferdi/static'
```
In order to accommodate multiple json file for each search result, we formatted the name of the json file that is going to be written in S3 by adding the user's request, in this case, `start_date` and `end_date`. But before uploading the file, we first check whether the search is already performed before, which then will reflect the existence of the file in S3 bucket. If this happen, we will not write a new json file, and instead just use the available file. Changes are written as follow: 
```
# with open(os.path.join(BASE_DIR, 'static', filename), 'w') as fout:
#     fout.write(json.dumps(geo_data, indent=4))
data = BytesIO(str.encode(json.dumps(geo_data, indent=4)))
s3 = boto3.resource('s3')
bucket = s3.Bucket('eb-django-express-signup-raisa-ferdi')
try:
    s3.Object('eb-django-express-signup-raisa-ferdi', 'static/'+filename).load()
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        bucket.upload_fileobj(data, 'static/' + filename, ExtraArgs={'ACL': 'public-read'})
```
Additionally, we also need to change CORS rule in S3 bucket configuration as follow:
```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```
Here is the content of our S3 bucket after several function call. 
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_2.png)

**Q62c: How would you run TwitterListener.py in the cloud instead of locally? Try to implement your solution and explain what problems have you found and what solutions have you implemented.** <br/>
We use environment variable for twitter authentication parameter in order to be able to set it up in Elastic Beanstalk. Our idea is to run a thread for TwitterListener.py inside django application. This can we achieved by defining a function inside TwitterListener to be run as thread. 
```
def run():
    print("Twitter Listener run!")
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_secret = os.environ['access_secret']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(locations=[-2.5756, 39.0147, 5.5982, 43.957])
```
We would also need to set environment variables in EB.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_6.png)

Ultimately, we defined the thread in wsgi file and run TwitterListener as a thread.  
```
import os
import threading
from form import TwitterListener
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eb-django-express-signup.settings")
application = get_wsgi_application()

thread = threading.Thread(target=TwitterListener.run,name='TwitterDaemon')
thread.daemon
thread.start()
```
By examining the log on EB below, we know that our TwitterListener application was successfully running on EB server. 

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_7.png)

And here is the snapshot of our web app running on EB server with parameter start date and end date. 

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.2_4.png)
