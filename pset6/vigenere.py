import cs50
import sys

# global variable declaration
validArguments = 2
alphabet = ord('z') - ord('a')
lowercaseOffset = ord('a')
uppercaseOffset = ord('A')

def main():
    
    # output the enciphered plaintext
    encipheredText = cipher_convert()
    print("ciphertext: ", encipheredText)

# prototype to check correct number of command-line arguments and if the cipherkey is valid
def valid_cipherkey():
    
    # checks if the correct number of command-line arguments are inputted
    if len(sys.argv) != validArguments:
        
        # warn user if they don't enter the correct number of command-line arguments and exit program
        print("Missing command-line argument")
        exit(1)
    
    # local variable declaration
    cipherKey = sys.argv[1]
    
    # iterate through each letter in the cipher key and make sure they are alphabetic characters
    for i in range (len(cipherKey)):
        
        if cipherKey[i].isalpha() == False:
            
            # warn user if they input non-alphabetic characters and exit the program
            print("Please enter alphanumeric characters only!")
            exit(1)
    
    # upon a successful check, return the cipher key back to the function    
    return cipherKey

# prototype to make sure the user inputs some plain text    
def valid_plaintext():
    
    plainText = None
    
    while plainText == None:
        
        # promt the user for some plaintext
        print("plaintext: ", end="")
        plainText = cs50.get_string()
        
    # return the user inputted value of plain text back to the function
    return plainText

# prototype to encipher the plan text characters based on the cipher key    
def cipher_convert():
    
    # local variable declaration
    cipherKey = valid_cipherkey()
    keyLength = len(cipherKey)
    plainText = valid_plaintext()
    convertedString = ""
    cipherIterator = 0
    
    # iterates over each character in plain text
    for i in range (len(plainText)):
        
        # checks if the current character in the plain text is an alphabetical character or not
        if plainText[i].isalpha():
            
            # checks if the current character in the plain text is a lowercase character
            if plainText[i].islower():
                
                # creates the cipher key character wraparound if it doesn't match the plain text input length
                cipherCursor = cipherIterator % keyLength
                
                # converts the current cipher key character to a lowercased integer offset value
                cipherKeyValue = (ord(cipherKey[cipherCursor].lower()) - lowercaseOffset)
                
                # offsets the current plain text character integer value by the cipher key integer value
                newCharValue = ((ord(plainText[i]) + cipherKeyValue - lowercaseOffset) % alphabet) + lowercaseOffset
                
                # converts the current enciphered integer value back to an alphabetical character and stores it in an array
                convertedString += chr(newCharValue)
            
            # in the case the current character in the plain text is an uppercase character    
            else:
                
                # creates the cipher key character wraparound if it doesn't match the plain text input length
                cipherCursor = cipherIterator % keyLength
                
                # converts the current cipher key character to a lowercased integer offset value
                cipherKeyValue = (ord(cipherKey[cipherCursor].lower()) - lowercaseOffset)
                
                # offsets the current plain text character integer value by the cipher key integer value
                newCharValue = ((ord(plainText[i]) + cipherKeyValue - uppercaseOffset) % alphabet) + uppercaseOffset
                
                # converts the current enciphered integer value back to an alphabetical character and stores it in the array
                convertedString += chr(newCharValue)
            
            # moves the current cipher key character forward one position    
            cipherIterator += 1
        
        # in the case that the current character in plain text is not an alphabetical character    
        else:
            
            # make no change to the current character in the plain text and store it in the array
            convertedString += plainText[i]
    
    # return the values in the array back to the function        
    return convertedString

# calls the main function    
if __name__ == "__main__":
    main()
