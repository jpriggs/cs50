import cs50
import sys

# global variable declaration
validArguments = 2
alphabet = ord('z') - ord('a')
lowercaseOffset = ord('a')
uppercaseOffset = ord('A')

def main():

    # checks if the correct number of command-line arguments are inputted
    if len(sys.argv) != validArguments:
        
        # warn user if they don't enter the correct number of command-line arguments and exit program
        print("Missing command-line argument")
        exit(1)

    # local variable declaration
    cipherKey = sys.argv[1]
    
    if not IsCipherValid(cipherKey):
        # warn user if they input non-alphabetic characters and exit the program
        print("Please enter alphanumeric characters only!")
        exit(1)

    conversionString = GetUserString()
    
    # output the enciphered plaintext
    encipheredText = cipher_convert(cipherKey, conversionString)
    print("ciphertext: ", encipheredText)

# prototype to check if the cipherkey is valid
def IsCipherValid(cipher):
    # iterate through each letter in the cipher key and make sure they are alphabetic characters
    for iterationChar in cipher:
        if not iterationChar.isalpha():
            return False

    return True

# prototype to make sure the user inputs some plain text    
def GetUserString():
    
    plainText = None
    
    while plainText == None:
        
        # promt the user for some plaintext
        print("plaintext: ", end="")
        plainText = cs50.get_string()
        
    # return the user inputted value of plain text back to the function
    return plainText

# prototype to encipher the plan text characters based on the cipher key    
def cipher_convert(cipherKey, plainText):
    # local variable declaration
    keyLength = len(cipherKey)
    convertedString = ""
    cipherIterator = 0
    
    # iterates over each character in plain text
    for currentChar in plainText:
        # checks if the current character in the plain text is an alphabetical character or not
        if currentChar.isalpha():
            
            # checks if the current character in the plain text is a lowercase character
            if currentChar.islower():
                
                # sets the offset to the lowercase value
                offset = lowercaseOffset
                
            # in the case the current character in the plain text is an uppercase character
            else:
                
                # sets the offset to the uppercase value
                offset = uppercaseOffset

            # creates the cipher key character wraparound if it doesn't match the plain text input length
            cipherCursor = cipherIterator % keyLength

            # converts the current cipher key character to a lowercased integer offset value
            cipherKeyValue = (ord(cipherKey[cipherCursor].lower()) - lowercaseOffset)

            # offsets the current plain text character integer value by the cipher key integer value
            newCharValue = ((ord(currentChar) + cipherKeyValue - offset) % alphabet) + offset

            # converts the current enciphered integer value back to an alphabetical character and stores it in the array
            convertedString += chr(newCharValue)

            # moves the current cipher key character forward one position    
            cipherIterator += 1

        # in the case that the current character in plain text is not an alphabetical character    
        else:
            
            # make no change to the current character in the plain text and store it in the array
            convertedString += currentChar
    
    # return the values in the array back to the function        
    return convertedString

# calls the main function    
if __name__ == "__main__":
    main()
