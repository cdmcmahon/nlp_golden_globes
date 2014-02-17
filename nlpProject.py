import json
import nltk
import re, string

with open('goldenglobes.json', 'r') as f:
 tweets = map(json.loads, f)

#-------------------------------------------------------------------------------
# Constants and Variables
#-------------------------------------------------------------------------------

AWARDS = ["Best Motion Picture – Drama", "Best Motion Picture – Musical or Comedy", "Best Director",
"Best Actor – Motion Picture Drama", "Best Actor – Motion Picture Musical or Comedy",
"Best Actress – Motion Picture Drama", "Best Actress – Motion Picture Musical or Comedy", "Best Supporting Actor – Motion Picture",
"Best Supporting Actress – Motion Picture", "Best Screenplay", "Best Original Score", "Best Original Song", "Best Foreign Language Film",
"Best Animated Feature Film"]
NAME_RE = re.compile("[A-Z][a-z]+\s[A-Z][a-z]+")
WIN_WORDS = ["win", "won", "winner"]

#-------------------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------------------
class Result (object):
    """
        class comment
    """
    R_STRING ="""
----------------------------------
The winner of {award} is {winner}.
The presenter was {presenter}.
Other nominees were: {nominees}.
----------------------------------"""
    def __init__(self, award, winner, presenter, nominees):
        self.award = award
        self.winner = winner
        self.presenter = presenter
        self.nominees = nominees

    def __str__(self):
        return self.R_STRING.format(award=self.award, winner=self.winner, presenter = self.presenter, nominees = self.nominees)


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def tweet_winner_people(tweet, award):
    """Takes a FULL tweet and checks to see if it might be announcing the winner of award. If so returns a list containing all names in the tweet."""
    counts = dict()
    possible_winners = list()
    for win_word in WIN_WORDS:
        if award in tweet['text'] and win_word in tweet['text']:
            possible_winners = re.findall(NAME_RE, tweet['text'])

    return possible_winners

def add_counts (source, target):
    target = {x:source.count(x) for x in source}

def find_winner_people(award):
    results = dict()
    for tweet in tweets:
        for r in tweet_winner_people(tweet, award):
            if r in results:
                results[r] += 1
            else:
                results[r] = 1

    if award in results:
        results.pop(award)

    if results:
        return max(results, key = results.get)
    else:
        return None
#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
