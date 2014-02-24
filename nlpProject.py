import json
import nltk
import re, string

with open('goldenglobes.json', 'r') as f:
 tweets = map(json.loads, f)

tweet_text = [tweet['text'] for tweet in tweets]
#-------------------------------------------------------------------------------
# Constants and Variables
#-------------------------------------------------------------------------------

AWARDS = [["Best Picture", "Motion"], 
["Motion", "Musical", "Comedy"], 
["Best Director"],
["Best Actor", "Drama", "Motion", "Picture"], 
["Best Actor", "Musical", "Comedy", "Motion"],
["Best Actress", "Drama", "Motion", "Picture"], 
["Best Actress", "Musical", "Comedy", "Motion"], 
["Best Supporting Actor"],
["Best Supporting Actress"], 
["Best Screenplay"], 
["Best Original Score", "Score"], 
["Best Original Song"], 
["Foreign", "Film"],
["Best Animated"],
# TV AWARDS
["Best" "Drama" "TV"],
["Best" "Comedy", "Series"],
["Best Actor", "Drama", "TV"],
["Best Actress", "Drama", "TV"],
["Best Actor", "Comedy", "TV"],
["Best Actress", "Comedy", "TV"],
["Best Actor", "Miniseries" "Television", "TV"],
["Best Actress", "Miniseries", "Television", "TV"],
["Best Supporting Actor", "Television", "TV"],
["Best Supporting Actress", "Television", "TV"],
["Best Miniseries", "TV Film", "Series"]]

AWARDS_NAMES = ["Best Motion Picture - Drama",
"Best Motion Picure - Musical or Comedy",
"Best Director",
"Best Actor in a Motion Picture - Drama",
"Best Actor in a Motion Picture - Musical or Comedy",
"Best Actress in a Motion Picture - Drama",
"Best Actress in a Motion Picture - Musical or Comedy",
"Best Supporting Actor - Drama, Musical or Comedy",
"Best Supporting Actress - Drama, Musical or Comedy",
"Best Screenplay",
"Best Original Score",
"Best Original Song",
"Best Foreign Film",
"Best Animated Feature Film",
# TV AWARDS
"Best Television Series - Drama",
"Best Television Series - Musical or Comedy",
"Best Actor in a TV Series - Drama",
"Best Actress in a TV Series - Drama",
"Best Actor in a TV Series - Musical or Comedy",
"Best Actress in a TV Series - Musical or Comedy",
"Best Actor in a TV Miniseries or Film",
"Best Actress in a TV Miniseries or Film",
"Best Supporting Actor in a TV Series - Drama, Musical or Comedy",
"Best Supporting Actress in a TV Series - Drama, Musical or Comedy",
"Best Miniseries or TV Film"]

NUMBER_OF_AWARDS = len(AWARDS);
NUMBER_OF_BEST_DRESSED = 8;
NUMBER_OF_PRESENTERS = 8;


BIGRAM_RE = "([A-Z][a-z]+\s[A-Z][-'a-zA-Z]+)"
UNIGRAM_RE = "([A-Z][a-z]+)"
BIGRAM_WINNER_RE = re.compile("winner.*is " + BIGRAM_RE)
BIGRAM_WON_RE = re.compile(BIGRAM_RE + " won")
UNIGRAM_WINNER_RE = re.compile("winner.*is " + UNIGRAM_RE)
UNIGRAM_WON_RE = re.compile(UNIGRAM_RE + " won")

PRESENTED_BY_RE = re.compile("presented.*by " + BIGRAM_RE)

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
                    if upw in unigram_possible_winners:
                        unigram_possible_winners.remove(upw)
        # Weight bigram winners more by adding them thrice
        possible_winners = unigram_possible_winners + bigram_possible_winners + bigram_possible_winners + bigram_possible_winners
    #add a check for "winner is (match)" or "winner was (match)", etc.

    return possible_winners

def add_counts (source, target):
    target = {x:source.count(x) for x in source}
    return

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


def find_host():
    # This function will find the host of the show.
    results = dict()
    for tweet in tweets:
        possible_winners = list()
        tweet_text = tweet['text']
        host_words = ["host", "hosting", "hosts", "hosted", "hosted by"]
        for w in host_words:
            if w in tweet_text:
                possible_winners = possible_winners + re.findall(BIGRAM_RE, tweet_text)
        for r in possible_winners:
            if r in results:
                results[r] += 1
            else:
                results[r] = 1

    if results:
        return max(results, key = results.get)
    else:
        return None



def find_best_dressed():
    # This function will find the host of the show.
    results = dict()
    for tweet in tweets:
        possible_winners = list()
        tweet_text = tweet['text']
        host_words = ["best dressed", "best dress"]
        for w in host_words:
            if w in tweet_text:
                possible_winners = possible_winners + re.findall(BIGRAM_RE, tweet_text)
        for r in possible_winners:
            if r in results:
                results[r] += 1
            else:
                results[r] = 1
    results.pop("Golden Globes")
    i = 0
    best_dressed = list()
    while results and (i<NUMBER_OF_BEST_DRESSED):
        next = max(results, key = results.get);
        best_dressed.append(next);
        results.pop(next);
        i += 1
    return best_dressed


def find_presenters():
    # This function will find the host of the show.
    results = dict()
    for tweet in tweets:
        possible_winners = list()
        tweet_text = tweet['text']
        host_words = ["presented by", "presenter", "presenting"]
        for w in host_words:
            if w in tweet_text:
                possible_winners = possible_winners + re.findall(BIGRAM_RE, tweet_text)
        for r in possible_winners:
            if r in results:
                results[r] += 1
            else:
                results[r] = 1
    results.pop("Golden Globes")
    i = 0
    presenters = list()
    while results and (i<NUMBER_OF_BEST_DRESSED):
        next = max(results, key = results.get);
        presenters.append(next);
        results.pop(next);
        i += 1
    return presenters



            



#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

def main():
    host = find_host()
    print "\nHOST:\n" + host
    best_dressed = find_best_dressed()
    print "\n" + str(NUMBER_OF_BEST_DRESSED) + " BEST DRESSED:\n"
    for x in range(0,NUMBER_OF_BEST_DRESSED):
        print str(x+1) + ": " + best_dressed[x]

    print "\n" + str(NUMBER_OF_PRESENTERS) + " MOST POPULAR PRESENTERS (ACCORDING TO TWITTER):\n"
    presenters = find_presenters();
    for x in range(0,NUMBER_OF_PRESENTERS):
        print str(x+1) + ": " + presenters[x]

    results = find_all_winners()

    # ONLY PRINT MOVIE AWARDS
    print "\nMOVIE AWARD WINNERS:\n"
    for award, winner in results.iteritems():
        if AWARDS_NAMES.index(award) < 14:
            if winner:
                print award + ": " + winner
            else:
                print "Could not find winner for " + award
    print "\n"

    # ONLY PRINT MOVIE AWARDS
    print "\nTELEVISION AWARD WINNERS:\n"
    for award, winner in results.iteritems():
        if AWARDS_NAMES.index(award) >= 14:
            if winner: 
                print award + ": " + winner
            else:
                print "Could not find winner for " + award
    print "\n"


    # for x in range(0,NUMBER_OF_AWARDS):
    #     if x == 0:
    #         print "MOVIE AWARDS:\n"
    #     if x == 14:
    #         print "\nTELEVISION AWARDS:\n"
    #     a = results(AWARDS_NAMES[x])
    #     if a:
    #         print AWARDS_NAMES[x] + ": " + results(AWARDS_NAMES[x])
    #     else:
    #         print "Could not find winner for " + AWARDS_NAMES[x]



if __name__ == '__main__':
    main()
