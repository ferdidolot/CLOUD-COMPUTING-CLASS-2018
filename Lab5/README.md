## GitHub Repository for the Web App ##

https://github.com/ferdidolot/eb-django-express-signup

## Pre-lab ##

Below is shown the new user "lab-sessions" created and five policies attached to this user

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Prelab_NewUser.png)


## Task 5.1: Use Amazon Simple Notification Service in your web app ##

After creating the SNS topic (the stream for notification) and after creating
the subscription that tell the SNS where and how to send the notification,
we have modified our configuration environment by adding the unique identifier
for SNS topic like below:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_1.png)

We have also added a new variable to the deployment environment of Elastic Beanstalk

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_2.png)

When we try to add a new lead to our web app, the first time we got the following error, specifying that the user is not authorized to perform this:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_3.png)

To avoid this error we modified the access of `lab_session user` in IAM console (instead of having access to put one item we change it to a list of allowed action in the Action property), like below:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_4.png)

After this steps when we add a lead we will get a notification on the defined  email:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_5.jpeg)

**Q51: Has everything gone alright?**

Everything has gone alright.

## Task 5.2: Create a new option to retrieve the list of leads ##

When we access  http://127.0.0.1:8000/search we will have the following screen showing that we can successfully retrieve the list of leads.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.2_1.png)

The following printscreen shows the list displays the list of the leads (We have also add new options to the menu bar).

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.2_2.png)

**Q5.2: Has everything gone alright? What have you changed?**
Yes, everything has gone alright. We managed to have our web app running and successfully perform
the searching for the leads.

It is important to emphasise that we have add Read Permission
to `lab_session user` in IAM console.

## Task 5.3: Improve the web app transfer of information (optional) ##

**Create a new dynamoDB table to store domain and count** <br/>
By examining the current app it is clear that to get all the domains, the code will try to get all the domain from the list of all users' email addresses by parsing them.
 We all know that this is inefficient, and a better solution would be to create a separate table just to store the domain and the count associated with it.
 In this way, when we are displaying the search page, list of domain can be taken from that particular table to reduce amount of data being transferred.
DynamoDB table for domain can be seen as below:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.3_1.png)


**Change code to accommodate changes** <br/>
As mentioned on previous point, we are going to change the way search page behaves. Instead of using the list of all users to get the domain to be displayed on the list, we will use the newly created dynamoDB table in order to reduce the web app transfer. 
We have changed the following code:
* In views.py code, we have changed: 
```
def search(request):
    domain = request.GET.get('domain')
    preview = request.GET.get('preview')
    leads = Leads()

    if domain or preview:
        items = leads.get_leads(domain, preview)
        return render(request, 'search.html', {'items': items})
    else:
        domains = leads.get_domains()
        domain_list = {}
        for item in domains:
            domain_list[item['domain']] = int(item['num'])
        domain_count = Counter(dict(domain_list))
        return render(request, 'search.html', {'domains': sorted(domain_count.items())})
 ```
Notice that we have moved the function call ` get_leads()` inside the if clause, which means it will be called only if we send the parameter in domain and preview as a request to the web app. Notice also in the else clause, we add another function `get_domains()` (we will discuss about this soon) and some code to do the parsing and data manipulation to accommodate format accepted by search.html code. 

* In models.py file, we have changed: 
```
from django.db import models
import boto3
import os
import logging

DOMAIN_TABLE = os.environ['DOMAIN_TABLE']
STARTUP_SIGNUP_TABLE = os.environ['STARTUP_SIGNUP_TABLE']
AWS_REGION = os.environ['AWS_REGION']
NEW_SIGNUP_TOPIC = os.environ['NEW_SIGNUP_TOPIC']
...
    def insert_lead(self, name, email, previewAccess):
        try:
            dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
            table = dynamodb.Table(STARTUP_SIGNUP_TABLE)
            table_domain = dynamodb.Table(DOMAIN_TABLE)
            domain = email.split('@')[1]
        except Exception as e:
            logger.error(
                'Error connecting to database table: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
            return 403
        ...
        ...
        status = response['ResponseMetadata']['HTTPStatusCode']
        
        if status == 200:
            table_domain.update_item(Key={'domain': domain},
                                 UpdateExpression="ADD num :val1",
                                 ExpressionAttributeValues={':val1': 1})
            if 'Attributes' in response:
                logger.error('Existing item updated to database.')
                return 409
            logger.error('New item added to database.')
        else:
            logger.error('Unknown error inserting item to database.')

        return status

   ...
   ...

    def get_domains(self):
        try:
            dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
            table = dynamodb.Table('gsg-domain-table')
        except Exception as e:
            logger.error(
                'Error connecting to database table: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
            return None
        response = table.scan(
                ReturnConsumedCapacity='TOTAL',
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return response['Items']
        logger.error('Unknown error retrieving domains from database.')
        return None
```
Notice that we added new environment variable, DOMAIN_TABLE, which also needs to be exported before running the application. We have included this part in `extra-files/environment.sh` file as :
```
export DOMAIN_TABLE="gsg-domain-table"
```
During the call of `insert_lead`, which is when the user registered to the app, we take the domain by splitting the email address of the user, and insert the value into the domain table. We use update expression and expression attributes values to automatically increment the existing value in the table, as well as inserting the initial value if the domain is not yet exist.

We also added the new function of `get_domains` to get the list of all domains in the web app and be consumed by search.html page. 

**Add update permission to lab_sessions user in iam console** <br/>
In order to make the changes work, we need to add update policy for lab_sessions user in iam console. 

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.3_2.png)


**Q53: Describe the strategy used to fulfill the requirements of this section. What have you changed in the code and the configuration of the different resources used by the web app? What are the tradeoffs of your solution?**

The strategy that we have used and the modification that we have done to the code  is described above.

**The tradeoffs of our solution are:**
* We would require extra space to store the domain.
* If the user data has very different domain of email (each user has different email domain), then the domain table will also producing the nearly same workload as we will have the the same number of the row. Our current design will perform better on search page when the users have the same email domain so that the content of domain table will be less then the number of user.

**The Tradeoffs in terms of man work are:**
* We have to create a new table for storing domain count 
* We have to create a new functionality to storing the domain count in the new table 
* We need to create additional service to get all the existing domain and count from the new table
* We need to adjust the html page with the newly built services



## Task 5.4: Deliver static content using a Content Delivery Network ##
**Q54: Take a couple of screenshots of you S3 and CloudFront consoles to demonstrate that everything worked all right.**

The screenshots below demonstrate that S3 and CloudFront concoles work fine for our app.

**Custom CSS file** <br/>
After using custom.css, we recognize there are some changes in the web app as follow: <br/>
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.4_1.png)
One different that we recognize is that there are new background which also using the file inside the static directory 
```
#newstartup {
    background: url('startup-bg.png') no-repeat center center fixed;
    ...
}

#jumbohome {
    background: url('CCBDA-Square.png') no-repeat;
  ...
}
```
**Add static files to S3 bucket** <br/>
We then add the static files to Amazon S3 bucket. We make it public so it is readable by public. Here is the capture of our S3 bucket. <br/>
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.4_2.png)

**Add CloudFront** <br/>
By following the step in CloudFront quick start, we have successfully deployed the cloudfront as follows: <br/>
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.4_3.png)
Once the CloudFront was successfully deployed, we will check the content of our webapp. By accessing the network inspection browser, we can now see that the files are served from cloudfront. <br/>
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.4_4.png)

**Q55: How long have you been working on this session (including the optional part)? What have been the main difficulties you have faced and how have you solved them?**
Estimated hours: 6 hours.
For the optional part, we were able to think about the solution directly, although we spent some time to explore on how to implement it in dynamoDB and understand the existing code in general in order to adjust with the changes.
The other parts were quite straightforward.

**Django support for CDN**
We configure our settings.py as follows:
```
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'form',
    'storages'
]
...

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = "eb-django-express-signup-raisa-ferdi"
AWS_S3_CUSTOM_DOMAIN = 'd3ertrvto3v3uu.cloudfront.net'
```

In order to be able to upload the file to s3, we have to set the policy for s3: <br/>
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.4_5.png)

We defaulted all the policy for s3 just for simplicity of this project, however we are aware that in practice, we should only select the required policy. Lastly, We managed to run collect static and get the output as follow:
```
(eb-virt) dolsky@ubuntu:~/PycharmProjects/eb-django-express-signup$ python manage.py collectstatic

You have requested to collect static files at the destination
location as specified in your settings.

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/lt.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/fa.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/it.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ar.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/eu.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ru.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/sk.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/fr.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/mk.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/el.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/hi.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/sr-Cyrl.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ms.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/az.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ko.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ja.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/vi.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ro.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/nb.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/hu.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/hr.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/lv.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/uk.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/pl.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/et.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/en.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/da.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/de.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/es.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/pt-BR.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/bg.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/sr.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/tr.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/id.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/th.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/km.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/is.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/nl.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/gl.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/cs.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/zh-TW.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/pt.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/fi.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/sv.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/select2/i18n/ca.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/xregexp/LICENSE-XREGEXP.txt'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/xregexp/xregexp.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/xregexp/xregexp.min.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/jquery/jquery.min.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/jquery/LICENSE-JQUERY.txt'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/js/vendor/jquery/jquery.js'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/widgets.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/login.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/responsive_rtl.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/base.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/autocomplete.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/changelists.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/fonts.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/responsive.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/forms.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/dashboard.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/rtl.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/vendor/select2/select2.min.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/vendor/select2/LICENSE-SELECT2.md'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/css/vendor/select2/select2.css'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/inline-delete.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-no.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-yes.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-changelink.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-deletelink.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/search.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/tooltag-arrowright.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-alert.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/sorting-icons.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-calendar.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-addlink.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/calendar-icons.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/tooltag-add.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/LICENSE'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/README.txt'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/selector-icons.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-unknown-alt.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-clock.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/icon-unknown.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/gis/move_vertex_off.svg'
Copying '/home/dolsky/PycharmProjects/eb-virt/lib/python3.5/site-packages/django/contrib/admin/static/admin/img/gis/move_vertex_on.svg'

86 static files copied, 35 unmodified.
```

And here is how the S3 bucket looked like: <br/>

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.4_6.png)

