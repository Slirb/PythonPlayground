import math

def stretchWord(word):
    middleBuild = ""
    firstBuild = ""
    secondBuild = ""

    if word == "" or  word == " ":
        return word
    length = len(word)

    # Only stretch words of 3 characters or more
    if length < 3:
        return word   
    
    # If odd we need to build the middle segment
    if length % 2 != 0:
        length = int(length / 2)
        middleBuild = (length + 1) * word[length]
    else:
        length = math.trunc(length/2)
    
    firstHalf = word[ :length]
    secondHalf = word[-length:]
    
    # Build the halfs
    for x in range(length):
        # First half
        firstBuild += firstHalf[x] * (x + 1)

        # Second half
        secondBuild += secondHalf[x] * (length - x)
        

    stretchedWord = firstBuild + middleBuild + secondBuild
    return stretchedWord

# print (stretchWord("anna"))
# print (stretchWord("kayak"))
# print (stretchWord(" "))
