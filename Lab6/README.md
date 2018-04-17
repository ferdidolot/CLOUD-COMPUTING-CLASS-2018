## GitHub Repository for the Web App ##

## Task 6.1: How to provide your services through a REST API? ##

After creating the new view "chart", we can access http://127.0.0.1:8000/chart to see how many emails we have gathered in our web app.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_1.png)

We can also visualize the chat with different parameters defined by the user and we will have:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_2.png)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_3.png)


**Q61a: Having domain_freq.json written as static content is not the best way to distribute it because different clients
can invoke different parameters simultaneously? Can you use S3 to solve the problem? Write the changes in the code and explain your solution?**


The schema below shows the approach that we have used to efficiently implement this view, in order to deal with simultaneous invocations with different parameters.


![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab6/Lab6_Task6.1_4.jpeg)
