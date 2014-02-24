import json
import nltk
import re, string

with open('goldenglobes.json', 'r') as f:
 tweets = map(json.loads, f)

tweet_text = [tweet['text'] for tweet in tweets]
#-------------------------------------------------------------------------------
# Constants and Variables
#-------------------------------------------------------------------------------

AWARDS = [u"Best Motion", u"Best Musical Comedy", u"Best Director",
u"Best Actor Drama", u"Best Actor Musical or Comedy",
u"Best Actress Drama", u"Best Actress Musical or Comedy", u"Best Supporting Actor",
u"Best Supporting Actress", u"Best Screenplay", u"Best Original Score", u"Best Original Song", u"Foreign Film",
u"Best Animated Feature Film"]


BIGRAM_RE = "([A-Z][a-z]+\s[A-Z][a-z]+)"
UNIGRAM_RE = "([A-Z][a-z]+)"
BIGRAM_WINNER_RE = re.compile("winner.*is " + BIGRAM_RE)
BIGRAM_WON_RE = re.compile(BIGRAM_RE + " won")
UNIGRAM_WINNER_RE = re.compile("winner.*is " + UNIGRAM_RE)
UNIGRAM_WON_RE = re.compile(UNIGRAM_RE + " won")

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
    # tweet_words = nltk.word_tokenize(tweet['text']);
    # if any(word in award.split() for word in tweet_words):
    if award in tweet['text']:
        # Get unigram and bigram possible winners
        unigram_possible_winners = re.findall(UNIGRAM_WINNER_RE, tweet['text']) + re.findall(UNIGRAM_WON_RE, tweet['text']);
        bigram_possible_winners = re.findall(BIGRAM_WINNER_RE, tweet['text']) + re.findall(BIGRAM_WON_RE, tweet['text']);
        # Remove unigrams contained in bigrams
        for upw in unigram_possible_winners:
            for bpw in bigram_possible_winners:
                if upw in bpw:
                    unigram_possible_winners.remove(upw)
        # Weight bigram winners more by adding them twice
        possible_winners = unigram_possible_winners + bigram_possible_winners
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
    print "\nAWARD WINNERS:\n"
    for award, winner in results.iteritems():
        if winner:
            print award + ": " + winner

if __name__ == '__main__':
    main()
