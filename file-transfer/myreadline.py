from os import read, write

buff = ""
data = ""

def myreadline():
    global buff
    global data
    
    index = 0
    line = ""
    
    if buff == "":
        buff = read(0, 100) # Buffer set with limit 100 
        data = buff.decode() # makes string interpretable
    
    while index < len(data):
        current_char = data[index]
        if current_char == '\n': # checks for newline char
            return line
        
        line += current_char
        index += 1;
        
        if index == 100:
            buff =  read(0,100)
            data = buff.decode()
            index = 0
    
    return "" # EOF reached
