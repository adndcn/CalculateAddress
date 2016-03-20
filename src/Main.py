import re
ctype = ['int', 'unsigned']

address = 0x36004
space = 0

file1 = open("teststruct.h",'rb')
file2 = open('test.h', 'wb')

lines = list(file1)
processlines = []

for line in lines:
    temp = line.translate(None, '\t\n\r') #delete the tab, space and carrige return
    if temp:
        temp = temp.split(' ')
        if temp[0] in ctype:
            width = 4
            num = 1
            #check it is an array
            if '[' in temp[-1]:
                count = temp[-1].count('[')
                patstring = r'.+' + '\[(.+)\]'*count
                pattern = re.compile(patstring)
                result = pattern.match(temp[-1])
                
                for i in range(count):
                    num *= int(result.group(i+1))
            address = address + space
            space = width*num
            #append the address at the end of the line (before \r\n).
            pos = line.index('\r') #find the positon of \r in the string
            line = line[:pos] + '   //0x' + str('%x' % address) + '\r\n'
            file2.write(line)    
        else:
            file2.write(line)
    else:
        file2.write(line)
        
file2.close()
        

# for line in processlines:
#     temp = line.split(' ')
#     if temp[0] in type:
#         if
    
