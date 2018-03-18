## Task 3.1: Real-time tweets API of Twitter ##

The dataset that we have generated contains 2316 tweets in JSON format, matching the filter criteria 'ArtificialIntelligence'.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.1_Output1.png)

The last tweet of this file is displayed below: (JSON format)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.1_Output2.png)


## Task 3.2: Analyzing tweets - Counting terms ##

The following screenshot shows the list of:

* Top ten most frequent tokens
* Top ten most frequent hashtags (by default the empty hashtag (# ) was listed as one of the most frequent hashtag. We have removed it using: ` terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#') and len(term) > 1]`. This can also be solved by adding:`and term not in stop`)
* Top ten most frequent terms, skipping mentions and hashtags.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.2_Output2.png)

## Task 3.3: Case study ##

The plot for the Case Study is:


![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/CaseStudy.png)

From this plot we can see that the most useful hashtags are: #ArtificialInteligence, #BigData, #BlockChain, #IoT, #InternetOfThings, #IndustrialIoT, #Ai, #DataScience, #Technology, #IndustrialInternetIfThings, #Industry40, #Microsoft, #Cloud, #IIoT, #Business.
