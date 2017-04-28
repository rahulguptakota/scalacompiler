import datafile
import register
asmcode = []
datafile.lineno = 0
#soure of instruction is tutorials point
f = open('asmfile','w') 

def blockasmgenerate():
    datafile.blocknuminst = len(datafile.block)
    register.initializeblock()
    for i in range(0,len(datafile.block) - 1):
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        print i ," i am in blockasmgenerate ok ....",datafile.block[i].type
        OperatorMap[datafile.block[i].type](i)
    i = len(datafile.block) - 1
    if i == -1:
        return 
    if datafile.block[i].type in ['jg', 'jge', 'je', 'jle', 'jne', 'jl', 'goto', 'jump', 'call', 'ret']:
        register.save()
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        OperatorMap[datafile.block[i].type](i)
    else:
        datafile.L = None
        datafile.yprime = None
        datafile.zprime = None
        OperatorMap[datafile.block[i].type](i)
        register.save()
    for b in datafile.blockout:
        # print(b)
        f.write(b + '\n')


def asm():
    print("section .data")
    f.write("section .data\nmessage db \"Register = %d\", 10, 0\n")
    f.write("\n formatin: db \"%d\", 0\n")
    # for k,v in datafile.setofString.items() :
    #     print('\n'+k+ ' db '  + "'" + v + "',0xa")
    #     f.write('\n'+k+ ' db '  + "'" + v + "',0xa\n")
    #     f.write("len_" + k + " equ $ - " + k + "\n")
    #     datafile.lineno = datafile.lineno + 2
    datafile.lineno = datafile.lineno + 1
    for data in datafile.globalsection:
        f.write()
        # print("{}:".format(data))
        # f.write("{}:\n".format(data))
        # datafile.lineno = datafile.lineno + 1
        # print("\t.long {}".format(1))
        # f.write("\t.long {}\n".format(1))
        # datafile.lineno = datafile.lineno + 1
    for data in datafile.setofarray.keys():
        # INVENTORY TIMES 8 DW 0
        f.write(data + " TIMES " + str(datafile.setofarray[data]) + " DW  0\n")
        # print("{}:".format(data))
        # f.write("{}:\n".format(data))
        # datafile.lineno = datafile.lineno + 1
        # print("\t.zero {}".format(4*int(datafile.setofarray[data])))
        # f.write("\t.zero {}\n".format(4*int(datafile.setofarray[data])))
        # datafile.lineno = datafile.lineno + 1
    print("\nsection.text\n")
    f.write("\nsection .text\n\t")
    datafile.lineno = datafile.lineno + 3
    # for k,v in datafile.setofString.items() :
    #     print('\n'+k+':  .asciz ' +v)
    #     f.write('\n'+k+':  .asciz ' +v + '\n')
    #     datafile.lineno = datafile.lineno + 2

    # print('\nprintFormat:  .asciz "%d"')
    # f.write('\nprintFormat:  .asciz "%d"\n')
    # datafile.lineno = datafile.lineno + 2
    # print('\nscanFormat:  .asciz "%d"\n')
    # f.write('\nscanFormat:  .asciz "%d"\n\n')
    # datafile.lineno = datafile.lineno + 3
    # print datafile.lineno, "lineno"
    print('global main\n\n')
    f.write('global main\nextern printf\nextern scanf\n\n')
    datafile.lineno = datafile.lineno + 3
    # print datafile.lineno, "lineno"
    print('main:')
    f.write('main:\n')
    datafile.lineno = datafile.lineno + 1
    f.write('call func_1_main\nmov  eax, 1\nint  0x80\n')
    # print datafile.lineno, "lineno"
    blockbreaker = set()
    blockbreaker.add(0)   #starting of first block
    for i in range(0,len(datafile.instruction)):
        if datafile.instruction[i].type == 'label:':
            blockbreaker.add(i)   #any target of a goto statement is a leader
        elif datafile.instruction[i].type in ['jg', 'je', 'jle', 'jge', 'je', 'jne', 'ret', 'goto', 'call' ]:
            blockbreaker.add(i+1) #any statement that follows a goto statement is a leader
    blockbreaker.add(len(datafile.instruction))
    blockbreaker = sorted(blockbreaker)
    for i in range (0,len(blockbreaker)-1):
        datafile.block = []
        if i == 0:
            datafile.block = datafile.instruction[blockbreaker[i]:blockbreaker[i+1]]
            # print datafile.block, "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\asdasda"
        if datafile.instruction[blockbreaker[i]].type == 'label:':
            print("\n{}:".format(datafile.instruction[blockbreaker[i]].out))
            f.write("\n{}:\n".format(datafile.instruction[blockbreaker[i]].out))
            # f.write("lineno" + str(datafile.lineno) + "\n")
            datafile.lineno = datafile.lineno + 2
            datafile.block = datafile.instruction[blockbreaker[i] + 1 : blockbreaker[i+1]]
            if datafile.instruction[blockbreaker[i]].op1[0:4] =='func':
                datafile.currentscope = datafile.instruction[blockbreaker[i]].op1
                print("\t" + "push ebp")
                f.write("push ebp\n")
                datafile.lineno = datafile.lineno + 1
                print("\t" + "mov ebp, esp")
                f.write("mov ebp, esp\n")
                datafile.lineno = datafile.lineno + 1
                print("\t" + "add esp, {}".format(datafile.numberofvariables[datafile.instruction[blockbreaker[i]].op1] - 4))
                f.write("sub esp, {}\n".format(datafile.numberofvariables[datafile.instruction[blockbreaker[i]].op1] - 4))
                datafile.lineno = datafile.lineno + 1
        else:
            datafile.block = datafile.instruction[blockbreaker[i]:blockbreaker[i+1]]
        blockasmgenerate()  
    f.write("int_to_string:\nadd esi,9\nmov byte [esi],0\nmov ebx,10\n.next_digit:\nxor edx,edx\ndiv ebx\nadd dl,'0'\ndec esi\n  mov [esi],dl\ntest eax,eax\njnz .next_digit\nmov eax,esi\nret\n")

def JE(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("je " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("je " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append("je " + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1
def JNE(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("jne " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("jne " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append("jne " + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1

def JLE(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("jle " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("jle " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append("jle " + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1

def JL(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("jl " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("jl " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append("jl " + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1

def JGE(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("jge " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("jge " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append("jge " + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1

def JG(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("jg " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("jg " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append("jg " + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1

def ADD(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    print y,", ", z, ", ", l ,"these are y and l in add function"
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    # print datafile.L , "Hello"
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    
    datafile.blockout.append("add " + register.mem(datafile.L) + ", "+register.mem(datafile.zprime) )
    # datafile.blockout.append("lineno" + str(datafile.lineno))
    datafile.lineno = datafile.lineno + 1
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def SUB(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    
    datafile.blockout.append("sub " + register.mem(datafile.L)  + ", " + register.mem(datafile.zprime) )
    datafile.lineno = datafile.lineno + 1    
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def AND(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    
    datafile.blockout.append("and " + register.mem(datafile.L)  + ", " + register.mem(datafile.zprime))
    datafile.lineno = datafile.lineno + 1    
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def OR(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    
    datafile.blockout.append("or " +register.mem(datafile.L) + ", " + register.mem(datafile.zprime) )
    datafile.lineno = datafile.lineno + 1    
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def XOR(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    
    datafile.blockout.append("xor " + register.mem(datafile.L) + ", " + register.mem(datafile.zprime) )
    datafile.lineno = datafile.lineno + 1
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def PUSH_ARG(i) :
    var = datafile.block[i].out
    t = False
    
    try:
        int(var)
    except:
        t = True
    if t and datafile.addressdescriptor[var] != None :
        place = datafile.addressdescriptor[var]
    else :
        place = register.emptyregister(i)
        datafile.blockout.append("mov  " +  register.mem(place) +', ' + register.mem(var))
        datafile.registerdescriptor[place] = var
    datafile.blockout.append("push " + place)

def ARG(i):
    pass

def LABEL(i):
    pass

def GET(i):
    
    datafile.blockout.append("mov "+register.mem(datafile.block[i].out)+", eax" )
    # datafile.lineno = datafile.lineno + 1
    pass

#CMP destination, source
#One has to be in register 
def COMPARE(i):
    (y,z) = (datafile.block[i].op1,datafile.block[i].op2)
    # print y,z, "aaaaaaaasdaddddddddddddddddddddddddddddddddddddddddaaaaaaaaaa",i
    try:
        int(z)
        datafile.zprime = z
    except:
        datafile.zprime = register.getz(z)
    
    try:
        int(y)
        datafile.yprime = y
    except:
        if datafile.addressdescriptor[y] != None:
            datafile.L = datafile.addressdescriptor[y]
        elif datafile.zprime in datafile.allvariables:
            reg = register.emptyregister(i)
            datafile.blockout.append("mov " + register.mem(reg) + ", " + register.mem(y) )
            datafile.L = reg
            datafile.registerdescriptor[reg] = y
            datafile.addressdescriptor[y] = reg
        else:
            datafile.L = y

    datafile.blockout.append("push edx")
    datafile.blockout.append("push ecx")
    datafile.blockout.append("mov ecx, " + register.mem(z))
    datafile.blockout.append("mov edx, " + register.mem(y))
    datafile.blockout.append("cmp edx, ecx")
    datafile.blockout.append("pop ecx")
    datafile.blockout.append("pop edx")
    datafile.lineno = datafile.lineno + 1
    register.freereg(y,i)
    register.freereg(z,i)
    
def MUL(i):
    (y, z, l) = (datafile.block[i].op1, datafile.block[i].op2, datafile.block[i].out)
    #check if z is constant or not if not get the momloc or register if it is already in register since op r_i , r_j is similar to op r_i , M
    try :
        int(z)
        datafile.zprime = z
    except :
        register.getz(z)
        pass
    #get the register for L to store the output of the operation 
    register.getreg(l, y, i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("push eax")
    datafile.blockout.append("push ebx")
    datafile.blockout.append("mov eax," + register.mem(datafile.L))
    datafile.blockout.append("mov ebx," + register.mem(datafile.zprime))
    datafile.blockout.append("imul ebx")
    datafile.blockout.append("mov " + register.mem(datafile.zprime) + ",ebx")
    datafile.blockout.append("mov " + register.mem(datafile.L) + ",eax")
    datafile.blockout.append("pop eax")
    datafile.blockout.append("pop ebx")
    datafile.lineno = datafile.lineno + 1
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def ASSIGN(i):
    (y,l) = (datafile.block[i].op2,datafile.block[i].out)
    register.getreg(l,y,i)
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)

def RETURN(i):  
    if datafile.block[i].out != None:
        # print datafile.block[i].out, "haghahahah"
        datafile.blockout.append("mov " +"eax, " + register.mem(datafile.block[i].out))
        datafile.lineno = datafile.lineno + 1
    datafile.blockout.append("mov esp, ebp")
    datafile.lineno = datafile.lineno + 1
    datafile.blockout.append("pop ebp")
    datafile.lineno = datafile.lineno + 1
    datafile.blockout.append("ret")
    datafile.lineno = datafile.lineno + 1
    datafile.currentscope = ""

def DIV(i):
    (l, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
    register.storereg('edx')
    
    datafile.blockout.append("xor edx, edx")
    datafile.lineno = datafile.lineno + 1
    try :
        int(z)
        reg = register.emptyregister(i,['edx', 'eax'])
        datafile.blockout.append('mov ' + reg + ", " + z)
        datafile.lineno = datafile.lineno + 1
        datafile.zprime = reg
    except :
        if datafile.addressdescriptor[z] == 'eax':
            register.storereg(z)
        register.getz(z)
        pass
    register.getreg(l, y, i, 'eax')
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("idiv " + register.mem(datafile.zprime))
    datafile.lineno = datafile.lineno + 1
    register.UpdateAddressDescriptor(l)
    register.freereg(y, i)
    register.freereg(z, i)

def MOD(i):
    (l, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
    register.storereg('edx')
    
    datafile.blockout.append("xor edx, edx")
    datafile.lineno = datafile.lineno + 1
    try :
        int(z)
        datafile.zprime = z
        reg = register.emptyregister(i,['eax', 'edx'])
        datafile.blockout.append('mov ' + reg + ", " + z)
        datafile.lineno = datafile.lineno + 1
        datafile.zprime = reg

    except :
        if datafile.addressdescriptor[z] == 'eax':
            register.storereg(z)
        register.getz(z)
        pass
    register.getreg(l, y, i, 'eax')
    try :
        int(y)
        datafile.yprime = y
    except :
        pass
    register.gety(y)
    datafile.blockout.append("idiv " + register.mem(datafile.zprime))
    datafile.lineno = datafile.lineno + 1
    datafile.L = 'edx'    #since the remainder is store in edx 
    register.update(l)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def ARRAYLOAD(i):
    (l, y, z) = (datafile.block[i].out, datafile.block[i].op1, datafile.block[i].op2)
    #sb $0, array1($3)  index addressing mode is used here
    try:
        int(z)
        datafile.zprime = z
    except:
        register.getz(z)
    
    reg = register.emptyregister(i)
    datafile.blockout.append("mov " + register.mem(reg) + ", " + register.mem(datafile.zprime) )
    datafile.lineno = datafile.lineno + 1
    datafile.L = reg




    datafile.blockout.append("mov " + y + "(, %" + reg +", 4 ), %" + reg )
    datafile.lineno = datafile.lineno + 1
    register.UpdateAddressDescriptor(l)


def GOTO(i):
    
    if datafile.block[i].out == "2":
        temp = 2 + datafile.lineno
        datafile.blockout.append("jmp " + str(temp))
        datafile.lineno = datafile.lineno + 1
    elif datafile.block[i].out == "3":
        temp = 3 + datafile.lineno
        datafile.blockout.append("jmp " + str(temp))
        datafile.lineno = datafile.lineno + 1
    else:
        datafile.blockout.append('jmp ' + datafile.block[i].out)
        datafile.lineno = datafile.lineno + 1
def ARRAY(i):
    pass

def CALL(i):
    
    # datafile.lineno = datafile.lineno + 1
    datafile.blockout.append('call ' + datafile.block[i].out)
    # print datafile.numberofarguments , "number of arguments ......... \n\n"
    # datafile.blockout.append('add esp, {}'.format(datafile.numberofarguments[datafile.block[i].out]-8))

def PRINTSTR(i):
    for reg in datafile.registerlist:
        datafile.blockout.append('push ' + reg)
    inno = datafile.block[i].instnumber #because string is already store 
    datafile.blockout.append('mov edx,'  + 'len_str'+ str(inno))
    datafile.blockout.append('mov ecx,str' + str(inno))
    datafile.blockout.append('mov ebx,1')
    datafile.blockout.append('mov eax,4')
    datafile.blockout.append('int 0x80')
    datafile.blockout.append('pop edx')
    datafile.blockout.append('pop ecx')
    datafile.blockout.append('pop ebx')
    datafile.blockout.append('pop eax')

def PRINT(i):
    l = datafile.block[i].out
    print l , "inside print function in nasm"
    try :
        datafile.addressdescriptor[l]
        # datafile.blockout.append('push eax\npush ebx\npush ecx\npush edx\n')
        datafile.blockout.append('push eax')
        datafile.blockout.append('xor eax, eax')
        datafile.blockout.append('mov ' + 'eax, ' +  datafile.addressdescriptor[l])
        datafile.lineno = datafile.lineno + 3
    except :
        datafile.blockout.append('push eax')
        datafile.blockout.append('xor eax, eax')
        datafile.blockout.append('mov ' + 'eax, ' + register.mem(l))
    datafile.blockout.append('push eax')
    datafile.blockout.append('push message')
    datafile.blockout.append('call printf')
    datafile.blockout.append('add esp, 8')
    # datafile.blockout.append('sub esp, 10')
    # datafile.blockout.append('mov esi, tempbuffer')
    # datafile.blockout.append("add eax, '0'")
    # datafile.blockout.append('push ebx\npush edx')
    # datafile.blockout.append('call int_to_string')
    # datafile.blockout.append('pop edx\npop ebx')
    # datafile.blockout.append('mov edx, 1')
    # datafile.blockout.append('push eax')
    # datafile.blockout.append('mov ecx, esp')
    # datafile.blockout.append('mov ebx, 1')
    # datafile.blockout.append('mov eax,4')
    # datafile.blockout.append('int 0x80')
    # datafile.blockout.append('pop eax')
    datafile.blockout.append('pop eax')
    # datafile.blockout.append('pop edx\npop ecx\npop ebx\npop eax\n')
    datafile.lineno = datafile.lineno + 14
    # register.save()
    # datafile.blockout.append('add esp, 8')
    # datafile.lineno = datafile.lineno + 1

def READ(i): 
    # for reg in datafile.registerlist:
    datafile.blockout.append("push eax")
    l = datafile.block[i].out
    print l, "this is l in read"
    # datafile.blockout.append("mov ecx,ebp")
    try:
        datafile.addressdescriptor[l]
        k = datafile.addressdescriptor[l]
        datafile.blockout.append("mov eax, esp")
    except:
        k = register.mem(l)
        datafile.blockout.append("lea eax," + k)
    
    # print k, "in read function"
    # if k[0] == "[":
        
    #     # datafile.blockout.append("sub ecx,edx")
    # else:
    #     datafile.blockout.append("mov eax, esp")
    datafile.blockout.append("push eax")
    datafile.blockout.append("push formatin")
    # datafile.blockout.append("mov eax,3")
    # datafile.blockout.append("mov ebx,2")
    # datafile.blockout.append("mov edx,4")
    # datafile.blockout.append("int 80h")
    # for reg in datafile.registerlist.reverse():
    #     datafile.blockout.append("pop " + reg)
    datafile.blockout.append("call scanf")
    datafile.blockout.append("add esp, 8")
    if k[0] != "[":
        datafile.blockout.append("mov " + k + ", [esp]")
        # datafile.blockout.append("pop eax")
    # datafile.blockout.append('pop edx')
    # datafile.blockout.append('pop ecx')
    # datafile.blockout.append('pop ebx')
    datafile.blockout.append('pop eax')

OperatorMap = {'jl': JL, 'je': JE, 'jg':JG, 'jle':JLE, 'jge':JGE, 'jne':JNE, 'pusharg':  PUSH_ARG, 'arg' : ARG, 'label:' : LABEL, 'get' : GET, 'cmp': COMPARE, '+' : ADD, '-' : SUB,'|' : OR, '&': AND, '^': XOR, '*' : MUL, '=' : ASSIGN, 'ret' : RETURN, '/' : DIV, '%' : MOD, '<-' : ARRAYLOAD, 'goto' : GOTO, 'ARRAY' : ARRAY , 'call' : CALL, 'printstr': PRINTSTR, 'print' : PRINT, 'read' : READ }