import json
import nltk
import re, string

with open('goldenglobes.json', 'r') as f:
 tweets = map(json.loads, f)

tweet_text = [tweet['text'] for tweet in tweets]
#-------------------------------------------------------------------------------
# Constants and Variables
#-------------------------------------------------------------------------------

AWARDS = [[u"Best Motion Picture", u"Best", u"Motion", u"Drama"], 
[u"Motion", u"Musical", u"Comedy"], 
[u"Best Director"],
[u"Best Actor", u"Drama", u"Motion", u"Picture"], 
[u"Best Actor", u"Musical", u"Comedy", u"Motion" u"Picture"],
[u"Best Actress", u"Drama", u"Motion", u"Picture"], 
[u"Best Actress", u"Musical", u"Comedy", u"Motion" u"Picture"], 
[u"Best Supporting Actor"],
[u"Best Supporting Actress"], 
[u"Best Screenplay"], 
[u"Best Original Score", u"Score"], 
[u"Best Original Song"], 
[u"Foreign", u"Film"],
[u"Best Animated"]]

AWARDS_NAMES = [u"Best Motion Picture - Drama",
u"Best Motion Picture - Musical or Comedy",
u"Best Director",
u"Best Actor in a Motion Picture - Drama",
u"Best Actor in a Motion Picture - Musical or Comedy",
u"Best Actress in a Motion Picture - Drama",
u"Best Actress in a Motion Picture - Musical or Comedy",
u"Best Supporting Actor - Drama, Musical or Comedy",
u"Best Supporting Actress - Drama, Musical or Comedy",
u"Best Screenplay",
u"Best Original Score",
u"Best Original Song",
u"Best Foreign Film",
u"Best Animated Feature Film"]

NUMBER_OF_AWARDS = len(AWARDS);


BIGRAM_RE = "([A-Z][a-z]+\s[A-Z][-'a-z]+)"
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
    def __init__(self, award, winner=None, presenter=None, nominees=None):
        self.award = award
        self.winner = winner
        self.presenter = presenter
        self.nominees = nominees

    def __str__(self):
        return self.R_STRING.format(award=self.award, winner=self.winner, presenter = self.presenter, nominees = self.nominees)


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def tweet_winners(tweet, award):
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

def find_winners(award):
    results = dict()
    for tweet in tweets:
        for award_phrase in award:
            for r in tweet_winners(tweet, award_phrase):
                if r in results:
                    results[r] += 1
                else:
                    results[r] = 1

    for award_phrase in award:
        if award_phrase in results:
            results.pop(award_phrase)

    if results:
        return max(results, key = results.get)
    else:
        return None

def find_all_winners():
    "Given proper constants returns a dict with awards as keys and winners as values."
    results = dict()
    # for award in AWARDS:
    #     results[award[0]] = find_winners(award)
    for x in range(0,NUMBER_OF_AWARDS):
        results[AWARDS_NAMES[x]] = find_winners(AWARDS[x]);


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
        else:
            print "Could not find winner for " + award
    print "\n"

if __name__ == '__main__':
    main()
