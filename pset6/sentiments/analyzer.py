import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # TODO
        # declare 2 empty lists to store all words in the postive and negative words text seperately 
        self.positiveWords = set()
        self.negativeWords = set()
        self.tweetLimit = 50
        
        # opens the positive-words.txt file
        file = open(positives, "r")
        lines = file.readlines()

        # iterates through each line in the file ignoring lines that begin with a ";" or a space
        for line in lines:
            
            if line[0] == ";" or line[0] == " ":
                
                continue
                
            self.positiveWords.add(line.rstrip("\n"))
        
        # closes the positive-words.txt file    
        file.close()
        
        # opens the negative-words.txt file
        file = open(negatives, "r")
        lines = file.readlines()
        
        # iterates through each line in the file ignoring lines that begin with a ";" or a space
        for line in lines:
            
            if line[0] == ";" or line[0] == " ":
                
                continue
                
            self.negativeWords.add(line.rstrip("\n"))
        
        # closes the negative-words.txt file        
        file.close()
        

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # TODO
        # local variable declaration
        tokens = nltk.word_tokenize(text.lower())
        scoreCounter = 0
        
        # iterates through each word in the tokens list
        for tweetWords in tokens:
            
            # checks if the user inputted word exist in the positive or negative text file or neither
            if tweetWords in self.positiveWords:
                
                scoreCounter += 1
                
            elif tweetWords in self.negativeWords:
                
                scoreCounter -= 1
                
            else:
                
                scoreCounter += 0
                
        return scoreCounter
