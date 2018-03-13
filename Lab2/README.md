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

The configuration to access Twitter are saved in the file: default_configuration.ini
In order to access it, you should rename it to "configuration.ini" and update it with the values of your Twitter Authentications.

In our case the information printed from our Twitter account was:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab2/Lab2.2.1_Output.png)


## Task 2.2.1: Accessing Tweets ##

The file `twitter_2.py` that we have uploaded is accessing tweet information using the `JSON format` (we have used `attribute _json`).

To make the output more readible, we have tested the code using the `text format` as following:

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

* We have pre-processed 10 tweets from our twitter account timeline:
    `for status in tweepy.Cursor(api.home_timeline).items(10):`
* To remove the unicode characters we have used:
    `print(word_tokenize(json.dumps(status.text)[1:-1]))`






