import cs50

# declare variables
characterOffset = 1
maxHeight = 23
minHeight = 0

def main():
    
    # store the valid value from the input check function prototype
    height = get_valid_int()

    # create a new row equal to the user inputted height
    for i in range (height):
        
        # print space characters on the left side of the pyramid
        for j in range (height - characterOffset - i):
            
            print(" ", end="")
            
        # print hash characters on the left side of the pyramid
        for k in range (i + characterOffset):
            
            print("#", end="")
            
        # print 2 spaces between each side of the pyramid in each row
        print("  ", end="")
        
        # print hash characters on the right side of the pyramid
        for k in range (i + characterOffset):
            
            print("#", end="")
            
        # print a new line after each row
        print()
    
# valid user input check function prototype
def get_valid_int():
    
    while True:
        
        # ask the user for a valid number between 1 - 22
        print("Enter a height: ", end="")
        validHeight = cs50.get_int()

        # checks if an invalid number was entered
        if validHeight <= minHeight or validHeight >= maxHeight:
    
            # reprompt the user and repeat the loop  
            continue
        
        # if a valid number is entered, break the loop    
        break
    
    # return the valid user input to the function prototype 
    return validHeight

# call main function
if __name__ == "__main__":
    main()