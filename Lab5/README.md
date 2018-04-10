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

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab5/Lab5_Task5.1_5.png)

## Task 5.2: Create a new option to retrieve the list of leads ##

## Notes ##

* 5.2 Add read permission to lab_sessions user in iam console