import json
import nltk
import re, string

with open('goldenglobes.json', 'r') as f:
 tweets = map(json.loads, f)

tweet_text = [tweet['text'] for tweet in tweets]
#-------------------------------------------------------------------------------
# Constants and Variables
#-------------------------------------------------------------------------------

AWARDS = [u"Best Picture Drama", u"Best Picture Musical or Comedy", u"Best Director",
u"Best Actor Drama", u"Best Actor Musical or Comedy",
u"Best Actress Drama", u"Best Actress Musical or Comedy", u"Best Supporting Actor",
u"Best Supporting Actress", u"Best Screenplay", u"Best Original Score", u"Best Original Song", u"Best Foreign Language Film",
u"Best Animated Feature Film"]
NAME_RE = "([A-Z][a-z]+\s[A-Z][a-z]+)"
WINNER_RE = re.compile("winner.*is " + NAME_RE)
WON_RE = re.compile(NAME_RE + " won")
#WIN_WORDS = ["win", "won", "winner"]

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
    if award in tweet['text']:
        possible_winners = re.findall(WINNER_RE, tweet['text']) + re.findall(WON_RE, tweet['text'])

    #add a check for "winner is (match)" or "winner was (match)", etc.

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

def find_all_winners():
    "Given proper constants returns a dict with awards as keys and winners as values."
    results = dict()
    for award in AWARDS:
        results[award] = find_winner_people(award)

    return results
#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

def main():
    results = find_all_winners()
    print results
    #for award, winner in results:
    #    print award + ": " + winner

if __name__ == '__main__':
    main()
