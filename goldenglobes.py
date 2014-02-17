import nltk
import json
import re

"""

List of Awards:

Best Motion Picture
***Best Performance by an Actress in a Motion Picture***
***Best Performance by an Actor in a Motion Picture***
Best Motion Picture - Comedy or Musical
***Best Performance by an Actress in a Motion Picture - Comedy or Musical***
***Best Performance by an Actor in a Motion Picture - Comedy or Musical***
Best Animated Feature Film
Best Foreign Language Film
***Best Performance by and Actor in a Supporting Role in a Motion Picture***
***Best Performance by and Actress in a Supporting Role in a Motion Picture***
***Best Director***
Best Screenplay
Best Original Score
Best Original Song
***Best Performance by an Actress in a Television Series***
***Best Performance by an Actor in a Television Series***
Best Television Series
***Best Performance by an Actress in a Television Series - Comedy or Musical***
***Best Performance by an Actor in a Television Series - Comedy or Musical***
Best Television Series - Comedy or Musical

"""

with open('goldenglobes.json','r') as f:
  tweets = map(json.loads, f);

def findWinnerPerson(award_name):
  award_words = nltk.word_tokenize(award_name);
  for tweet in tweets:
    tokens = nltk.word_tokenize(tweet.get("text"))
    winner_words = ["wins", "win", "winner", "won"]
    for x in award_words:
      if x in tokens:
        for y in winner_words:
          if y in tokens:
            # Tweet contains winner word and words in award name
            m = re.search('^[A-Z]\'?[- a-zA-Z]( [a-zA-Z])*$',tweet)
            print m.group(0)

findWinnerPerson("Actor Motion Picture")

