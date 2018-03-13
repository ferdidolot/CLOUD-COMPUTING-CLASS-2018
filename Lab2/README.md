## Task 2.1.1: Word Count ##

### Output: ###

`[('the', 1343), (',', 1251), ('.', 810), (')', 638), ('(', 637), ('of', 586), ('to', 491), ('a', 468), (':', 454), ('in', 417)]` <br />
`The total number of the words of the book is: 25155`


## Task 2.1.2: Remove punctuation ##

### Output: ###

`[('the', 1444), ('of', 586), ('to', 531), ('in', 506), ('a', 481), ('and', 346), ('is', 289), ('we', 279), ('that', 275), ('this', 268)]`<br />
`The total number of the words of the book after removing punctuation is: 19593`


## Task 2.1.3: Stop Words ##

### Output: ###

`[('tensorflow', 193), ('data', 102), ('tensor', 99), ('code', 90), ('learning', 81), ('function', 74), ('one', 73), ('use', 65), ('example', 64), ('available', 63)]`<br />
`The total number of the words of the book after removing Stop Words is: 11220`

`tensorflow`is the most common word 

The output for Task 2.1 is shown in the following  printscreen:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab2/Lab2.1_Output.png)


## Task 2.2.1: Accessing twitter account information ##

The configuration to access Twitter are saved in the file: `default-configuration.ini`
You should rename it to `configuration.ini` and update it with the values of your Twitter Authentications. <br /><br />
We used this format of configuration to show flexibility and remove redundancy in configuration file, for example, we use `[TwitterAPI]` section to indicate section in configuration file that is related with twitter API. This section is useful because some of the variable can have the same name in multiple context, for example: <br /><br />
O-auth is a common format for authentication, and will use some general terminology such as token, secret key, etc. It is better to define a section related with each application than creating redundant variable name such as: TwitterAccessToken and FacebookAccessToken. <br />

In our case the information printed from our Twitter account was:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab2/Lab2.2.1_Output.png)


## Task 2.2.1: Accessing Tweets ##

The file `twitter_2.py` that we have uploaded is accessing tweet information using the `JSON format` (we have used `attribute _json`).

To make the output more readable, we have tested the code using the `text format` as following:

1. Twitter home timeline:<br />
`for status in tweepy.Cursor(api.home_timeline).items(10):`<br />
    `print(status.text)`
    <br />
2. List of Friends (their name and screen name): <br />
`for friend in tweepy.Cursor(api.friends).items(10):`<br />
   ` print(friend.name,'|' ,friend.screen_name)`
    <br />
3. List of Tweets (tweet text and created date):<br />
`for tweet in tweepy.Cursor(api.user_timeline).items(5):`<br />
   `print(tweet.text,'|', tweet.created_at)`
   
The output for our Twitter account is: 

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab2/Lab2.2.2_Output.png)

## Task 2.2.3: Tweet pre-processing ##

For this task in order to avoid mixing it with Task 2.2.2 we have created a new file `Python_3.py`.  

* We have pre-processed 10 tweets from our twitter account timeline:<br />
    `for status in tweepy.Cursor(api.home_timeline).items(10):`<br />
* Doing tweet processing directly to status.text will cause the output of the list to have the unicode sign literal as shown in example below:<br />
    `[u'Amsterdam', u',', u'Netherlands', u'to', u'Bangkok', u',', u'Thailand', u'for', u'only', u'\u20ac', u'326', u'roundtrip', u'(', u'min', u'2', u'pax', u')', u'with', u'@SingaporeAir', u'.', u'\u2026', u'https://t.co/BqM0VJLuE9']`
* In order to remove the unicode sign 'u', we used json.dumps function, and the output will be:<br /> 
    `"Amsterdam, Netherlands to Bangkok, Thailand for only €326 roundtrip (min 2 pax) with @SingaporeAir.… https://t.co/BqM0VJLuE9"`
* We then use substring [1:-1] to remove the double quote produced in front and end of json dump output. Our sample output of tweet processing is as following: <br />
    `['Amsterdam', ',', 'Netherlands', 'to', 'Bangkok', ',', 'Thailand', 'for', 'only', '\\', 'u20ac326', 'roundtrip', '(', 'min', '2', 'pax', ')', 'with', '@SingaporeAir', '.', '\\', 'u2026', 'https://t.co/BqM0VJLuE9']`
    

The output for our Twitter account is: (we have displayed only 6 tweets on the printscreen below) 

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab2/Lab2.2.3_Output.png)





