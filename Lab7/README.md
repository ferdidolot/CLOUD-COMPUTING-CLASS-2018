## Using the Elastic Stack to study scraped data from a web page ##

Github repository for the scrapy-lab: https://github.com/ferdidolot/scrapy-lab

## Task 7.1: Extract selected information from a newspaper webpage ##

**Q71: Add the above code to your scrapy-lab repository.
Add the nytimes.json, containing the output of your execution, to the Lab7 folder of your answers repository.**

We have added a new parser for the articles URLs to extract more data for the articles, using the following code.
To achieve this, the new function `def parse_article(self, response)` is needed and this function is invoked using `yield response.follow(next_page, callback=self.parse_article)`.


``` python
    # -*- coding: utf-8 -*-
    import scrapy
    import unidecode
    import re

    cleanString = lambda x: '' if x is None else unidecode.unidecode(re.sub(r'\s+',' ',x))

    class NytimesSpider(scrapy.Spider):
        name = 'nytimes'
        allowed_domains = ['www.nytimes.com']
        start_urls = ['http://www.nytimes.com/']

        def parse(self, response):
            for article in response.css("section.top-news article.story"):
                article_url = article.css('.story-heading>a::attr(href)').extract_first()
                yield {
                    'appears_ulr': response.url,
                    'title': cleanString(article.css('.story-heading>a::text').extract_first()),
                    'article_url': article_url,
                    'author': cleanString(article.css('p.byline::text').extract_first()),
                    'summary': cleanString(article.css('p.summary::text').extract_first())+cleanString(' '.join(article.css('ul *::text').extract())),
                }
                next_page = article_url
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse_article)

        def parse_article(self, response):
            yield {
                'appears_ulr': response.url,
                'title': cleanString(response.css('h1.headline::text').extract_first()),
                'author': cleanString(response.css('span.byline-author::text').extract_first()),
                'contents': cleanString(''.join(response.css('div.story-body p.story-body-text::text').extract())),
            }
```

We have also uploaded the `nytimes.json` that was generated after running the above piece of code.
The structure of this file after adding the new parser is:
```
    [
    {"title": "Korea Talks Begin as Kim Jong-un Crosses to South's Side of DMZ",
     "contents": "SEOUL, South Korea -- on Friday became the first North Korean leader to set foot in South Korean-controlled territory, starting a historic summit meeting with the South's president that will test Mr. Kim's willingness to bargain away his nuclear weapons.Mr. Kim's crossing of the line at the heart of the world's most heavily armed border zone, a prospect that seemed unthinkable just a few months ago, was broadcast live in South Korea, where a riveted nation sought to discern the intentions of the North's 34-year-old leader.For South Korea's president, Moon Jae-in, who has placed himself at the center of diplomacy to end the nuclear standoff with the North, the meeting presents a formidable task: finding a middle ground between a to the North and an impulsive ally in the United States.The historic encounter at the Peace House, a conference building on the South Korean side of , could set the tone for an even more critical meeting planned between Mr. Kim and President Trump.On Friday morning, Mr. Kim emerged from a North Korean administrative building inside Panmunjom and walked toward the border line, where Mr. Moon was waiting. The two leaders smiled and shook hands across a concrete slab that marks the border bisecting Panmunjom.Then, Mr. Kim stepped across the border.After the two leaders posed for photos, they crossed briefly into the North's territory at Mr. Kim's suggestion, another highly symbolic moment. They then stepped back into South Korean territory, holding hands, and walked down a red carpet to inspect a South Korean military honor guard and enter the Peace House.\"I came here to put an end to the history of confrontation,\" Mr. Kim was quoted as saying during the meeting, according to Mr. Moon's spokesman, Yoon Young-chan. Mr. Moon suggested they hold more meetings, and Mr. Kim said he would visit South Korea's presidential Blue House \"if the president invites me.\"While Mr. Moon's meeting with Mr. Kim on Friday -- their first face-to-face talk -- is rich with symbolism, Mr. Kim is not expected to capitulate on Mr. Trump's key demand: total and immediate nuclear disarmament.Mr. Moon's other challenge, with Mr. Trump, turns on how best to deal with North Korea and its leader -- who is expected to meet with Mr. Trump in the next few months.The South Korean president favors an \"action for action\" strategy in which the North takes steps to dismantle its nuclear arsenal and is rewarded for each move with economic benefits and security guarantees. South Korean officials said that the entire process could take about two years.Mr. Trump's national security team, by contrast, has insisted that North Korea must scrap its weapons programs before any relief from the sanctions that isolate the nation can be granted. And they say that \"substantial dismantlement\" should be completed much more quickly, perhaps in six months.Mr. Moon sees himself less as a negotiator with Mr. Kim and more as a mediator shuttling between two men who believe that keeping others guessing gives them an edge: a volatile American president with no experience in nuclear negotiations, and a with no experience on a global stage.\"What we can do is to try to help the North and the United States reach an agreement, helping them narrow their differences and seeking and presenting practical ideas both sides can accept,\" Mr. Moon said recently, adding that he may have only one shot to get it right. \"This is an opportunity that will not come again.\". No nation that has openly tested a nuclear device has ever surrendered its arsenal, and North Korea has conducted six underground explosions, each more powerful than the last, and has test-fired .But Mr. Trump and Mr. Kim have both already about what is possible. If they meet in June -- most likely in Singapore, according to American and South Korean officials -- it would be the between the leaders of the two nations, as well as a chance to test the argument that making progress with North Korea in the nuclear standoff requires starting at the top.The meeting between Mr. Kim and Mr. Moon is the third summit meeting between leaders of the two countries, but the first in which denuclearizing the Korean Peninsula tops the agenda.\"I hope we can have open-minded talks on issues of concern and produce good results, not the kind of results we saw in the past that were not implemented and made us start from scratch again,\" Mr. Kim said as the talks began on Friday. For his part, Mr. Moon said he hoped that the two leaders could engage in \"broad-minded\" discussions and produce \"a big gift\" for those yearning for peace on the Korean Peninsula.Mr. Moon hopes to emerge from Friday's summit meeting with a formal but vague denuclearization commitment from Mr. Kim and perhaps a path to negotiating a peace treaty or a plan to reduce military tensions. Some have suggested a pullback of troops from the Demilitarized Zone between the North and South is possible.But Mr. Moon has acknowledged that there is a limit to what the two Koreas can agree on without American involvement. \"Peace on the Korean Peninsula cannot be achieved by agreements between South and North Korea alone,\" he said last month. \"It has to have American endorsement.\"One measure of success will be whether Mr. Moon can persuade Mr. Kim to set a timetable for denuclearization in his talks with Mr. Trump.\"Confirming a willingness to denuclearize is not enough. What matters is an agreement on by when the North will denuclearize,\" said Cheong Seong-chang, a North Korea specialist at the Sejong Institute, a South Korean think tank.Some who have tried and failed to persuade North Korea to abandon its nuclear program worry that Mr. Trump, having threatened the North with nuclear annihilation, has now swung too far to the other side and may be too eager to make a deal. Having derided Mr. Kim previously as \"Little Rocket Man,\" Mr. Trump described the North Korean leader as \"very honorable\" this week.\"I find it impossible to believe that Kim is prepared to give up what his father and his grandfather bequeathed to him,\" said Gary Samore, a veteran of negotiations with North Korea as the top arms control aide in the Clinton and Obama administrations, speaking at the Asan Institute for Policy Studies in Seoul.But he added that Mr. Kim \"may now calculate he has enough of a nuclear arsenal\" -- and so can afford to put more on the table than in the past.One possibility that causes consternation in the region is that Mr. Trump will settle for dismantling North Korea's small fleet of intercontinental ballistic missiles, eliminating its ability to strike the United States -- but leaving South Korea and Japan vulnerable. \"It would be the 'America First' way,\" Mr. Samore said, referring to Mr. Trump's campaign slogan.If skepticism is rampant in Washington, the Moon administration is somewhat more optimistic. To South Korean policymakers, Mr. Kim's recent decisions suggest that he is willing to , which the young leader may see as necessary to preserving his rule for decades. They also argue that Mr. Trump's threats of military action have proved more effective at changing Mr. Kim's calculations than anticipated.South Korean officials say they have spent far more time and energy coordinating with the Trump administration before the Friday summit meeting than with the North Koreans, an effort complicated by the White House shake-up that included the as national security adviser and the .The focus on Washington also reflects concern about General McMaster's successor, , who joined the administration after to destroy North Korea's nuclear arsenal, ridiculing South Korean leaders as \"putty in North Korea's hands,\" and calling North Koreans \"the biggest con men in the world.\"Mr. Moon's national security adviser, Chung Eui-yong, described Mr. Bolton as an \"honest broker\" after their first meeting this month, and he traveled again to Washington this week for further discussions with Mr. Bolton.One mystery is what, if any, progress was made in , the North's capital, this month between Mr. Kim and Mike Pompeo, the former C.I.A. director who was confirmed Thursday as secretary of state. Mr. Trump said Thursday that Mr. Pompeo was not scheduled to see Mr. Kim but had \"a great meeting\" that lasted more than an hour.Though Mr. Moon and Mr. Trump have outlined different approaches to negotiating with North Korea, they agree on the need to avoid the pitfalls that doomed previous rounds of talks.One area of consensus is an attempt to more clearly establish the talks' desired outcome from the outset, giving all parties greater incentive to move forward. Previous negotiations were open-ended, without specific goals that everyone agreed on.South Korea and the United States also want to push the North to accept a timetable that would move quickly from -- which it announced last week -- to the dismantlement of its nuclear program. Some in the Trump administration have argued for completion in six months, but that may be an opening negotiating position given the challenges involved.Mr. Bolton has occasionally cited the example of Libya, which shipped most of its nuclear equipment to an American weapons lab in Tennessee over the course of several weeks in late 2003. But much of that equipment was still in crates; there was little to dismantle.Iran took a bit more than six months to take apart much of its program and ship 97 percent of its nuclear material from the country. But, like Libya, it had not yet built nuclear weapons.North Korea is believed to have 20 to 60 such weapons -- American intelligence agencies cannot agree on the number -- in addition to a vast infrastructure of fuel production and weapons manufacturing facilities, much of it hidden in the mountains or underground. Mr. Samore argued that the North should be asked to hand over an inventory that the United States and its allies could compare with intelligence reports and seek to verify. That process would offer a first sign of whether Mr. Kim is coming clean, but could take years to complete.\"I do not know of any way of unilaterally verifying an agreement whereby North Korea gives up its nuclear arsenal,\" said William J. Perry, a former defense secretary. \"We do not know how many nuclear weapons North Korea has operational or under construction. We do not know where all of their nuclear facilities are located.\"Mr. Moon's aides have argued that it is unrealistic to expect North Korea to simply surrender its arsenal without an \"action for action\" process that offers immediate benefits and builds trust. Early steps by the North could include the dismantlement of missile production facilities and allowing the return of international inspectors to nuclear sites, while the United States could begin normalizing diplomatic relations and easing some sanctions, like those that primarily affect North Korea's population rather than officials, analysts say.Mr. Kim has also endorsed \"phased, synchronized steps\" toward denuclearization.But White House officials have repeatedly rejected the incremental approach, saying past administrations have tried it without success.There have been hints of friction between the Trump administration and Mr. Moon's team over the issue, with local news outlets in South Korea reporting that Mr. Bolton had pressed Seoul \"not to move too far ahead\" in its talks with Mr. Kim. A senior aide to Mr. Moon firmly denied the reports.",
     "author": "DAVID E. SANGER",
     "appears_ulr": "https://www.nytimes.com/2018/04/26/world/asia/korea-kim-moon-summit.html"},
     ...
    ]


```


and we also have the information for each article in the same JSON file:

```
    [
    {"author": "By DAVID E. SANGER and CHOE SANG-HUN ",
     "article_url": "https://www.nytimes.com/2018/04/26/world/asia/korea-kim-moon-summit.html",
     "summary": "President Moon Jae-in of South Korea is meeting North Korea's leader, Kim Jong-un, in the Demilitarized Zone. Mr. Kim is the first North Korean leader to set foot in South Korean-controlled territory.",
     "title": "Korea Talks Begin as Kim Enters South's Side of DMZ",
     "appears_ulr": "https://www.nytimes.com/"},
     ...
     ]
 ```

In order for the content to be consistent it is recommenced to combine the information for an article into a single object    (`{ }`), instead of having separate objects, one that displays summary and another one that displays content. We have implemented this and we will explain it in details for the `imbd.json` file in section 7.2.


## Task 7.2: Obtain a subset of the movie industry to do some research ##

**Q72: Add the code of the new spider your scrapy-lab repository. Add the imdb.json, containing the output of your execution, to the Lab7 folder of your answers repository.**


In this section we have used the online database for movies, IMDb, to study the relationship between actors regarding the movies they have been playing.
We have followed the following logic:
 * We have started scraping our favorite movie `start_urls = ['https://www.imdb.com/title/tt0096463/fullcredits/']`
 * We continued scraping other movies using the pages of each actor.
 * We also scraped actor`s bio pages to collect some personal data about them (birthdate, height)

 We have constructed three functions: `def parse_actor_from_movie(self, response)`, `def parse_next_movie(self, response)` and `def parse_actor_bio(self, response)` and we will explain each of them in details below. After every successful crawl, the `parse` method is called and that is where we invoke the first function `def parse_actor_from_movie(self, response)` by using the following lines of code:

``` python
    def parse(self, response):
    request = scrapy.Request('https://www.imdb.com/title/tt0096463/fullcredits/',
                         callback=self.parse_actor_from_movie)
    yield request
```

**1. The function `def parse_actor_from_movie(self, response)`**

 This function will parse the required information for the movie: `movie_name, movie_id, movie_year` and the required information for the actors that have played in this movie: `actor_id`, `actor_name` and `role_name`.
After carefully examining the HTML page of IMDb, we have used the following CSS syntax to select the above-mentioned HTML elements:

* **Movie details:**
To select `movie_year` in the appropriate format among the other functions it is also necessary to use `strip()` function to remove ` \t \r \n ` from the beginning and the end of the string.

``` python
    movie_name = response.css('h3[itemprop="name"] a::text').extract_first()
    movie_id = response.css('h3[itemprop="name"] a::attr(href)').extract_first().split("/")[2]
    movie_year = re.sub('\s+', ' ', (response.css('h3[itemprop="name"] span[class="nobr"]::text').extract_first()).strip(' \t \r \n').replace('\n', ' ') ).strip()
    movie_year = movie_year.replace("(", "").replace(")","").split('\u2013')[0]

```
* **Actor details:**
Each movie will have a list of actors, therefore to select the details for all the actors we use a loop. To select the `role_name` in the appropriate format we again use `strip()` function.

``` python
    for actor in response.css('table.cast_list td[itemprop="actor"] span[class="itemprop"]::text ').extract():
            actor_name_list.append(actor)

        for link in response.css('table.cast_list td[itemprop="actor"] a::attr(href)').extract():
            actor_id_list.append(link)

        count = 0
        for character in response.css('td[class="character"]::text').extract():
            if character.strip() :
                temp = re.sub( '\s+', ' ', character.strip(' \t \r \n').replace('\n', ' ') ).strip()

```

* We created a dictionary to put all the details for the movies and their actors.

``` python
    item = dict()

    item['movie_name'] = movie_name
    item['movie_id'] = movie_id
    item['movie_year'] = movie_year
    item['actor_id'] = actor_id_list[count].split("/")[2]
    item['actor_name'] = actor_name_list[count]
    item['role_name'] = temp

```
* For each actor we invoke the two other functions to parse actor`s bio and movies where each actor has played.

``` python
    request = scrapy.Request('https://www.imdb.com/name/' + item['actor_id'] + '/bio',
                             callback=self.parse_actor_bio)
    request.meta['item'] = item
    yield request
    request2 = scrapy.Request('https://www.imdb.com/name/' + item['actor_id'] + '/', callback=self.parse_next_movie)
    yield request2
```

**2. The function `def parse_next_movie(self, response)`**

This function will parse the movies starting from the actor pages.

 * After analyzing the HTML structure of the pages we detected that they use different `id` for actor and actress. Therefore we have covered both cases by using the following piece of code:

``` python
    noisy_movie_titles_actor = response.css('div[id^="actor"]  b a::attr(href)').extract()
    noisy_movie_titles_actress = response.css('div[id^="actress"]  b a::attr(href)').extract()
    next_movies_id = [];
    next_movies_years = []

    if noisy_movie_titles_actor:
        next_movies_id= [i.split("/")[2] for i in noisy_movie_titles_actor]
        next_movies_years = response.css('div[id^="actor"]  span::text').extract()
    elif noisy_movie_titles_actress:
        next_movies_id = [i.split("/")[2] for i in noisy_movie_titles_actress]
        next_movies_years = response.css('div[id^="actress"]  span::text').extract()
```

* We are concentrated only on the movies filmed during the 80`s

``` python
    for i,j in zip(next_movies_id, next_movies_years) :
        j = j.split('\u2013')[0].strip()
        if int(j) < 1980 or int(j) > 1989:
            continue
        request = scrapy.Request('https://www.imdb.com/title/'+ i +'/fullcredits/',
                                 callback=self.parse_actor_from_movie)
        yield request
```

**3. The function `def parse_actor_bio(self, response)`**

This function is used to parse actor bio details: `birthdate` and `height`

``` python
    def parse_actor_bio(self, response):
        birth_date = response.css('td time::attr(datetime)').extract()
        height = response.css('table[id="overviewTable"] td::text' ).extract()
        if height:
            height = height[-1].strip()
        else:
            height = ""
        if not any(char.isdigit() for char in height):
            height = ""
        item = response.meta['item']
        if birth_date:
            item['birth_date'] = birth_date[0]
        else:
            item['birth_date'] = ""
        item['height'] = height

        yield item
```

The full code for this section is displayed below:


``` python
    # -*- coding: utf-8 -*-
    import scrapy
    import re

    class ImdbSpider(scrapy.Spider):
        name = 'imdb'
        allowed_domains = ['www.imdb.com']
        start_urls = ['https://www.imdb.com/title/tt0096463/fullcredits/']

        def parse(self, response):
            request = scrapy.Request('https://www.imdb.com/title/tt0096463/fullcredits/',
                                 callback=self.parse_actor_from_movie)
            yield request


        def parse_actor_from_movie(self, response):
            actor_name_list = []
            actor_id_list = []

            movie_name = response.css('h3[itemprop="name"] a::text').extract_first()
            movie_id = response.css('h3[itemprop="name"] a::attr(href)').extract_first().split("/")[2]
            movie_year = re.sub('\s+', ' ', (response.css('h3[itemprop="name"] span[class="nobr"]::text').extract_first()).strip(' \t \r \n').replace('\n', ' ') ).strip()
            movie_year = movie_year.replace("(", "").replace(")","").split('\u2013')[0]

            for actor in response.css('table.cast_list td[itemprop="actor"] span[class="itemprop"]::text ').extract():
                actor_name_list.append(actor)

            for link in response.css('table.cast_list td[itemprop="actor"] a::attr(href)').extract():
                actor_id_list.append(link)

            count = 0
            #for character in response.xpath('//td[@class="character"]//div//text()').extract():
            for character in response.css('td[class="character"]::text').extract():
                if character.strip() :
                    temp = re.sub( '\s+', ' ', character.strip(' \t \r \n').replace('\n', ' ') ).strip()
                    item = dict()

                    item['movie_name'] = movie_name
                    item['movie_id'] = movie_id
                    item['movie_year'] = movie_year
                    item['actor_id'] = actor_id_list[count].split("/")[2]
                    item['actor_name'] = actor_name_list[count]
                    item['role_name'] = temp

                    request = scrapy.Request('https://www.imdb.com/name/' + item['actor_id'] + '/bio',
                                             callback=self.parse_actor_bio)
                    request.meta['item'] = item
                    yield request
                    request2 = scrapy.Request('https://www.imdb.com/name/' + item['actor_id'] + '/', callback=self.parse_next_movie)
                    yield request2
                    count = count + 1

        def parse_next_movie(self, response):
            noisy_movie_titles_actor = response.css('div[id^="actor"]  b a::attr(href)').extract()
            noisy_movie_titles_actress = response.css('div[id^="actress"]  b a::attr(href)').extract()

            next_movies_id = [];
            next_movies_years = []

            if noisy_movie_titles_actor:
                next_movies_id= [i.split("/")[2] for i in noisy_movie_titles_actor]
                next_movies_years = response.css('div[id^="actor"]  span::text').extract()
            elif noisy_movie_titles_actress:
                next_movies_id = [i.split("/")[2] for i in noisy_movie_titles_actress]
                next_movies_years = response.css('div[id^="actress"]  span::text').extract()

            for i,j in zip(next_movies_id, next_movies_years) :
                j = j.split('\u2013')[0].strip()
                if int(j) < 1980 or int(j) > 1989:
                    continue
                request = scrapy.Request('https://www.imdb.com/title/'+ i +'/fullcredits/',
                                         callback=self.parse_actor_from_movie)
                yield request

        def parse_actor_bio(self, response):
            birth_date = response.css('td time::attr(datetime)').extract()
            height = response.css('table[id="overviewTable"] td::text' ).extract()
            if height:
                height = height[-1].strip()
            else:
                height = ""
            if not any(char.isdigit() for char in height):
                height = ""
            item = response.meta['item']
            if birth_date:
                item['birth_date'] = birth_date[0]
            else:
                item['birth_date'] = ""
            item['height'] = height

            yield item

```

## Task 7.3: Study the obtained data using the Elastic Stack ##

In this section we have used Elastic Stack and Kibana to analyze the data obtained for movies and actors.

After setting up the Elastic Stack cloud trial we included the following lines of code in our 'imdb.py' file, to enable inserting records at 'imdb' index which we will recover from Kibana.


``` python
    ELASTIC_API_URL_HOST = os.environ['ELASTIC_API_URL_HOST']
    ELASTIC_API_URL_PORT = os.environ['ELASTIC_API_URL_PORT']
    ELASTIC_API_USERNAME = os.environ['ELASTIC_API_USERNAME']
    ELASTIC_API_PASSWORD = os.environ['ELASTIC_API_PASSWORD']

    es=Elasticsearch(host=ELASTIC_API_URL_HOST,
                     scheme='https',
                     port=ELASTIC_API_URL_PORT,
                     http_auth=(ELASTIC_API_USERNAME,ELASTIC_API_PASSWORD))
```

``` python
    es.index(index='imdb',
         doc_type='movies',
         id=uuid.uuid4(),
         body={
             "movie_id": item['movie_id'],
             "movie_name": item['movie_name'],
             "movie_year": item['movie_year'],
             "actor_name": item['actor_name'],
             "actor_id": item['actor_id'],
             "role_name": item['role_name'],
             "height": item['height'],
             "birth_date": item['birth_date']
         })
```

We have configured the environment variables for using Elastic Stack in our PyCharm, like below:

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_1.png)


**Q73: Take a screenshot of the Kibana Dashboard showing the above plots without filters. Set a couple of filters, take screetshots. Add all the screenshots to the Lab7 folder of your answers repository**

The following printscreen shows the data that we have in Kibana. We let it run for collecting 12794 records

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_2.png)

**A tag cloud showing who are the most popular actors for the period. A new record is inserted every time that an actor participates in a movie, therefore, you can count how many records exist for each actor.**

This tag cloud shows the most popular actors (100) of movies filmed during the 80`s (without filters)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_3.png)

This tag cloud shows the most popular actor of 80s movies that were born during the 40s. (filtered)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_4.png)


**A bar diagram showing how many actors employ each movie. Take the 50 movies with more actors for the period.**

This bar diagram shows the 50 movies with more actors for the period and how many actors are employed for each movie (without filters)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_5.png)

This bar diagram shows the 50 movies with more actors  for year 1985 and how many actors are employed for each movie (filtered - year 1985)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_6.png)

**A bard diagram showing the filming activity for each year (plot the total count of records per year).**

This bar diagram shows the number of movies for each year (without filters)

![alt text](https://github.com/ferdidolot/CLOUD-COMPUTING-CLASS-2018/blob/master/Lab7/Lab7_Task7.3_7.png)
## What is your question? ##

**Q74: Explain what you have done in the README.md file of the Lab7 folder of your answers repository, add the new plot. Push the code changes to your scrapy-lab repository**

**Q75: How long have you been working on this session? What have been the main difficulties you have faced and how have you solved them?**


