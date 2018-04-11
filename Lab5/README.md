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

To avoid this error we modified the access to the IAM profile (instead of having access to put one item we change it to a list of allowed action in the Action property), like below:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_4.png)

After this steps when we add a lead we will get a notification on the defined  email:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_5.jpeg)

## Task 5.2: Create a new option to retrieve the list of leads ##

When we access  http://127.0.0.1:8000/search we will have the following screen showing that we can successfully retrieve the list of leads.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.2_1.png)

The following printscreen shows the list displays the list of the leads (We have also add new options to the menu bar).

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.2_2.png)

Q 5.2: **Has everything gone alright? What have you changed?**

Yes, everything has gone alright. We managed to have our web app running and successfully perform
the searching for the leads.

As mentioned in Task 5.1, it is important to emphasise that we have add Read Permission
to `lab_session user` in IAM console.

## Task 5.3: Improve the web app transfer of information (optional) ##

**Create a new dynamoDB table to store domain and count** <br/>
By examining the current app, we know that to get all the domain, the code will try to get all the domain from the list of all users' email addresses by parsing them. We all know that this is inefficient, and the better solution would be to create a separate table just to store the domain and the count associated with it. That way, when we are displaying the search page, list of domain can be taken from that particular table to reduce amount of data being transferred. 
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
