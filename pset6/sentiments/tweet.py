class Tweet():
    
    def __init__(self, text, positivityValue):
        
        # save the tweet's text
        self.text = text
        # save the tweet's positivity value
        self.positivityValue = positivityValue
        
    def GetColor(self):
        
        returnColor = ""
        if self.positivityValue > 0.0:
            returnColor = "green"
        elif self.positivityValue < 0.0:
            returnColor = "red"
        else:
            returnColor = "orange"
        return returnColor
