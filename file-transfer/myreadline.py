from os import read, write


def myreadline():
    index = 0
    line = ""
    buff = read(0, 100) # Buffer set with limit 100 
    string = buff.decode() # makes string interpretable
    
    while index < len(string):
        current_char = string[index]
        if current_char == '\n': # checks for newline char
            return line
        
        line += current_char
        index += 1;
        
        if index == 100:
            buff =  read(0,100)
            string = buff.decode()
            index = 0

    return "" # EOF reached
