## Task 3.1: Real-time tweets API of Twitter ##

The dataset that we have generated contains 2316 tweets in JSON format, matching the filter criteria 'ArtificialIntelligence'.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.1_Output1.png)

The last tweet of this file is displayed below: (JSON format)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.1_Output2.png)


## Task 3.2: Analyzing tweets - Counting terms ##

During this task we have analyzed the tweets for `ArtificialIntelligenceTweets.json` file and the following printscreen shows:

* Top ten most frequent tokens
* Top ten most frequent hashtags
* Top ten most frequent terms, skipping mentions and hashtags.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.2_Output2.png)

Some remarks related with this task are:

* By default the first two tokens listed as the most frequent token were two Unicode characters, as shown below. We have removed these noisy Unicodes from our result as they were not relevant with the given topic.
`noisy_unicodes = [u'\U0001f525' , u'\u2026']`
`stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT'] + noisy_unicodes`

![alt text](https://github.com/ferdidowlot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.2_Output1.png)


*Also the empty hashtag (# ) was listed as one of the most frequent hashtag. We have removed it using: ` terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#') and len(term) > 1]`. This can also be solved by adding:`and term not in stop`)

## Task 3.3: Case study ##

The plot for the Case Study is:


![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/CaseStudy.png)

From this plot we can see that the most useful hashtags are: #ArtificialInteligence, #BigData, #BlockChain, #IoT, #InternetOfThings, #IndustrialIoT, #Ai, #DataScience, #Technology, #IndustrialInternetIfThings, #Industry40, #Microsoft, #Cloud, #IIoT, #Business.
