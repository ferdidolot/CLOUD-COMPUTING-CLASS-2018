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

## Terminating the instance ##

**What happens in your EBS console?**<br/>
EBS will remove the instance due to EC2 health check failure.

**Wait a couple of minutes and check again your EC2 console. What has happened?**<br/>
An instance was automatically created in order to replace the instance that has been brought down.

**Why do you think that has happened?**<br/>
EBS detected failover to the instance that has been brought down, then it automatically triggered new instance to replace it.

## Terminating the environment ##

**What has happened in your EBS console?**<br/>
EC2 instance was also brought down. 

**Why do you think that has happened?**<br/>
EC2 instance is linked to EBS in configuration setting, hence when the environment was brought down, it also detect the dedicated instance and terminated it.

**Check both EC2 and EBS consoles**<br/>
EC2 and EBS environment were both terminated.
