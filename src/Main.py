import os
import sys

        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'lost the filename\n'
        sys.exit()
    elif len(sys.argv) > 2:
        print 'too much arguments\n'
        sys.exit()
    file1 = open(sys.argv[1], 'rb')
    filename = os.path.split(sys.argv[1])[-1]
    filepath = os.path.split(sys.argv[1])[0]
    file2 = open(filepath + '_' + sys.argv[1], 'wb')
    
    address = 0x0
    pace = 0
    
    lines = list(file1)
    processlines = []
    word = ''
    chnum = ''
    flag = 0
    bracketflag = 0
    substructflag = 0
    numflag = 0
    preflag = 0
    arrayflag = 0
    num = 1
    structname = ''
    address = 0
    space = 0
    linenumber = 0

    for line in lines:
        linenumber += 1
        for i in range(len(line)):
            if flag == 0: #nomal mode
                if 'A' <= line[i] <= 'Z' or 'a' <= line[i] <= 'z':
                    word += line[i]
                elif line[i] == '/':
                    if line[i+1] == '/':
                        preflag = flag
                        flag = 1 #comment mode
                elif line[i] == ' ':
                    if word == 'struct':
                        substructflag = 1
                        structname = line[:-2]
                    word = '' #clear
                elif line[i] == '{':
                    if substructflag == 1:
                        substructflag = 0
                        flag = 2 #struct mode
                        address = input('find a structure named: ' + structname + '\n' + 'please enter an address>')
                        space = 0
                    word = ''
                else:
                    word = ''
                    
                    
            elif flag == 1: #comment mode
                if line[i] == '\n':
                    flag = preflag
                
            elif flag == 2: #struct mode
                if 'A' <= line[i] <= 'Z' or 'a' <= line[i] <= 'z':
                    word += line[i]
                elif line[i] == '/':
                    if line[i+1] == '/':
                        preflag = flag
                        flag = 1 #comment mode
                elif line[i] == ' ':
                    if word == 'char':
                        numflag = 1
                    elif word == 'short':
                        numflag = 2
                    elif word == 'int':
                        numflag = 3
                    word = ''
                elif line[i] == '*':
                    if word == 'char' or word == 'short' or word == 'int':
                        print 'find pointer'
                        numflag = 4
                    elif word == '':
                        if numflag > 0:
                            numflag = 4
                elif line[i] == ';':  #the end of one row
                    address = address + space
                    processlines.append({'linenumber': linenumber, 'addr': address})
                    if numflag == 1:
                        if arrayflag == 1:
                            print 'find char array'
                            space = num
                        else:
                            print 'find char'
                            space = 1
                    elif numflag == 2:
                        if arrayflag == 1:
                            print 'find short array'
                            space = num*2
                        else:
                            print 'find short'
                            space = 2
                    elif numflag == 3:
                        if arrayflag == 1:
                            print 'find int array'
                            space = num*4
                        else:
                            print 'find int'
                            space = 4
                    elif numflag == 4:
                        if arrayflag == 1:
                            print 'find pointer array'
                            space = num*4
                        else:
                            print 'find pointer'
                            space = 4
                    numflag = 0
                    bracketflag = 0
                    word = ''
                    arrayflag = 0
                    num = 1
                    break
                elif line[i] == '[' and bracketflag == 0:
                    bracketflag = 1
                    arrayflag = 1
                    chnum = ''
                elif '0' <= line[i] <= '9' and bracketflag == 1:
                    chnum += line[i]
                elif line[i] == ']' and bracketflag == 1:
                    num = num * int(chnum)
                    bracketflag = 0
                    chnum = ''
                elif line[i] == '}':
                        word = ''
                        flag = 0
                        bracketflag = 0
                        substructflag = 0
                        numflag = 0
                        preflag = 0
                        num = 1
                        chnum = ''
                        structname = ''
                        address = 0
                        arrayflag = 0
    linenumber = 0
    index = 0
    maxindex = len(processlines)
    for line2 in lines:
        linenumber += 1
        if index < maxindex:
            if linenumber == processlines[index]['linenumber']:
                if '/*' in line2:
                    firstindex = line2.find('/*')
                    secondindex = line2.find('*/')
                    templine = line2[:firstindex] + str('/* 0x%05x ' % processlines[index]['addr']) + line2[secondindex:]
                    file2.write(templine)
                else:
                    firstindex = line2.find('\r')
                    templine = line2[:firstindex] + str('/* 0x%05x */' % processlines[index]['addr']) + line2[firstindex:]
                    file2.write(templine)
                index += 1
            else:
                file2.write(line2)
        else:
            file2.write(line2)
    
    file2.close()
    file1.close()                           
                        
            
            
            
             
    
