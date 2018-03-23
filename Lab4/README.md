## GitHub Repository for the Web App ##

https://github.com/ferdidolot/eb-django-express-signup(https://github.com/ferdidolot/eb-django-express-signup)

## DynamoDB Table ##

The following printscreen shows the DynamoDB table that we have created for our application.
The users are registered from both local and the deployed web app.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab4/DynamoDB.png)


## Remarks for the lab ##

* To switch to the virtual environment we have used the following:<br/>
`$ virtualenv --no-site-packages -p python3 ../eb-virt`

* We configured the environmental variables at the "Software Configuration" Box, like shown below:
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab4/EnvironmentalVariables.png)

* We have modified the configuration file at `.elasticbeanstalk/config.yml` like below:
![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab4/ConfigForElasticbeanstalk.png)
