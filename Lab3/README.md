## Task 3.1: Real-time tweets API of Twitter ##

The dataset that we have generated `ArtificialIntelligenceTweets.json` contains 2316 tweets, matching the filter criteria 'ArtificialIntelligence'.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.1_Output1.png)

The tweets are saved in JSON format. For illustration purposes, the last tweet of this file is displayed below, by using `tail -n 1 ArtificialIntelligenceTweets.json`

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.1_Output2.png)


## Task 3.2: Analyzing tweets - Counting terms ##

During this task we have created the program  `TwitterAnalyzer.py` to analyzed the tweets for `ArtificialIntelligenceTweets.json` file. The  `.json` file is read only once as following:
 ```
    for line in f:
    tweet = json.loads(line)

        # Create a list with all the tokens
        terms_all = [term for term in preprocess(tweet['text']) if term not in stop]
        count_all.update(terms_all)

        # Create a list with hashtags
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#') and len(term) > 1]
        count_hashtag.update(terms_hash)

        #Create a list of terms only skipping hashtags and mentions
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]
        count_only.update(terms_only)
 ```


  The following printscreen shows:

* Top ten most frequent tokens (as we can see 8 from the top ten tokens are hashtags)
* Top ten most frequent hashtags
* Top ten most frequent terms, skipping mentions and hashtags.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.2_Output2.png)

**Some remarks related with this task are:**

* By default the first two tokens listed as the most frequent token were two Unicode characters, as shown below. We have removed these noisy Unicodes from our result as they were not relevant with the given topic. <br/>
```
noisy_unicodes = [u'\U0001f525' , u'\u2026']
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT'] + noisy_unicodes
```



![alt text](https://github.com/raisauku/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/Lab3.2_Output1.png)


* Also empty hashtag `(# )` was listed as one of the most frequent hashtag. We have removed it using: <br/>
` terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#') and len(term) > 1]`. <br/>
  This can also be solved by adding in the above line of code: `and term not in stop`

## Task 3.3: Case study ##

The plot for the Case Study is showed below. From the analysis we can conclude that when it comes to `Artificial Intelligence` people mostly talk about `#BigData` `#BlockChain`, `#IoT`. <br/>
Other useful hashtags are:<br/>
`#InternetOfThings, #IndustrialIoT, #Ai, #DataScience, #Technology, #IndustrialInternetIfThings, #Industry40, #Microsoft, #Cloud, #IIoT, #Business`

To produce the plot, it is necessary to switch py plot backend rendering by including the following line of code:<br/>
`plt.switch_backend('agg')`  <br/>
\**Agg: raster graphics – high quality images using the Anti-Grain Geometry engine (ref: https://matplotlib.org/faq/usage_faq.html)*.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/CaseStudy.png)

## Task 3.4: Student Proposal - Cryptocurrency ##

We have decided to analyze what do people talk about when it comes to one of the most currently hottest topics `cryptocurrency`.

* The file `StudentProposal_TwitterStream.py` is constructed to listen for the stream and collect the tweets in the `.JSON` file.
In order to **simultaneously listen for streams with different filtering criteria** we have modified the line of code where we define our filter criteria, like below: <br/>
`twitter_stream.filter(track=[sys.argv[1]])` <br/>
and produce `.JSON` file associated with the twitter topics: <br/>
`with open(sys.argv[1] + '.json', 'a') as f:` <br/>

* The file `StudentProposal.py` is used to analyze the tweets. We have used the same logic as above, by using arguments to define the topic of `.JSON` file
that will be analyzed: <br/>
`fname = sys.argv[1] + '.json` <br/>

* As our first results also included different `Unicode characters`, which did not help in the analysis of our case, we decided to remove those characters by using:
```
    unicodes = [];
    for i in range(0,65533):
         unicodes.append(chr(i))
    
    stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT'] + unicodes
```

* The function `def generatePlot(count,plotName):` is constructed to generate the following plots:

    * Top 15 most frequent hashtags
    * Top 15 most frequent mentions
    * Top 15 most frequent tokens

**By analyzing the plots we reached into the following conclusions:**

**Hashtags Plot**

People interested into `cryptocurrency`, mostly talk about: <br/>
 `#bitcoin` - Blockchain currency<br/>
 `#blockchain`<br/>
 `#ico` - Initial Coin Offering <br/>
 `#crypto` <br/>
 `#airdrop` - the procedure of distributing tokens by awarding them to existing holders of a particular blockchain currency, such as Bitcoin or Ethereum
 `#ethereum`- another Blockchain currency

Other useful hashtags are: `#btc, #satoshi, #earn_money, #cryptocurrencies, #token, #tokensale, #eth, #ether`

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/StudentProposal_Hashtags.png)

**Mentions Plot**

There are also interesting results from analyzing the top mentions when it comes to `cryptocurrency`.
The top-three are:<br/>
`@gymrewards` - a gym that rewards the members with digital coins for exercising <br/>
`@europencryptob` - Private Banking & Wealth Management on cryptocurrencies <br />
`@cryptoleeps` - Crypto Never Sleeps,  a cryptocurrency trader <br />
`@swapynetwork` - a decentralized platform that aims to provide Universal Access to Credit using blockchain technology <br/>


Other useful mentions are: `@coinsairdrops, @randolphmlny, @justionsuntron, @listia, @coinseedap`

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/StudentProposal_Mentions.png)


**Tokens Plot**

In the tokens plot, despite the hashtags and mentions that we have defined above, we can see that people relate `cryptocurrency` even with `trump` and `US`.
Other useful tokens are `new` `join` `free`, all of them describing the nature of the `cryptocurrency` trend.

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab3/StudentProposal_Tokens.png)
