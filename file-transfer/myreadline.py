from os import read, write

buff = ""


def myreadline():
    global buff
    index = 0
    line = ""
    if buff == "":
        buff = read(0, 100).decode() #set with limit 100

    while index < len(buff):
        current_char = buff[index]
        
        if current_char == '\n' and index + 1 == len(buff): # checks for newline char
            buff = ""
            return line
        
        line += current_char
        index += 1;
        
        if index == 100:
            buff = read(0,100).decode()
            index = 0
        
    return "" # EOF reached
