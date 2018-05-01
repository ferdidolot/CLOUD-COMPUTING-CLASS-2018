## Using the Elastic Stack to study scraped data from a web page ##

Github repository for the scrapy-lab: https://github.com/ferdidolot/scrapy-lab

## Task 7.1: Extract selected information from a newspaper webpage ##

**Q71: Add the above code to your scrapy-lab repository.
Add the nytimes.json, containing the output of your execution, to the Lab7 folder of your answers repository.**

We have added a new parser for the articles URLs to extract more data for the articles, using the following code.
To achieve this, the new function `def parse_article(self, response)` is needed and this function is invoked using `yield response.follow(next_page, callback=self.parse_article)`.


``` 
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

In order for the content to be consistent it is recommenced to combine the information for an article into a single object (`{ }`), instead of having separate objects, one that displays summary and another one that displays content. We have implemented this and will explain this in details for the `imbd.json` file in section 7.2.
