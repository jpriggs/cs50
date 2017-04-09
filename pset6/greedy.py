import cs50

# variable declaration
minValue = 0
centsMultiplier = 100
quarterValue = 25
dimeValue = 10
nickelValue = 5
pennyValue = 1

def main():
    
    # call the coin calculating prototype function and print the result
    coins = calculate_coins()
    print(coins)

# valid user input check function prototype
def get_valid_float():
    
    while True:
        
        # promt the user for a valid positive float greater than zero
        print("O Hai! How much change is owed? ")
        valid_float = cs50.get_float()
        
        # check if the user input is invalid
        if valid_float <= minValue:
            
            # continue the loop until a valid input is entered
            continue
        
        # break the loop once a valid input is entered
        break
    
    # return the input to the function
    return valid_float
    
# coin calculating prototype
def calculate_coins():
    
    # converts the user inputted dollars all to cents
    totalCents = round(get_valid_float() * centsMultiplier)
    coinCount = 0
    
    # loops until the total cents equals zero
    while totalCents > minValue:
        
        # checks how many quarters there are
        if totalCents >= quarterValue:
            
            coinCount = coinCount + (totalCents // quarterValue)
            totalCents = totalCents % quarterValue
        
        # checks how many dimes there are    
        elif totalCents < quarterValue and totalCents >= dimeValue:
            
            coinCount = coinCount + (totalCents // dimeValue)
            totalCents = totalCents % dimeValue
        
        # checks how many nickels there are    
        elif totalCents < dimeValue and totalCents >= nickelValue:
            
            coinCount = coinCount + (totalCents // nickelValue)
            totalCents = totalCents % nickelValue
         
        # checks how many pennies there are   
        else:
            coinCount = coinCount + (totalCents // pennyValue)
            totalCents = totalCents % pennyValue
    
    # returns the total number of coins counted
    return coinCount

# calls the main function
if __name__ == "__main__":
    main()