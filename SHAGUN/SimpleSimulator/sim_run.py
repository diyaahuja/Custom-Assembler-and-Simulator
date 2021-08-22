
Bin_reg = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4": "100", "R5": "101", "R6":"110","FLAGS":"111"}  
valid_label_names=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","_","1","2","3","4","5","6","7","8","9","0",":"]

type_A={"add":"00000","sub": "00001","mul":"00110","xor":"01010","or":"01011","and":"01100"}
type_B={"mov" : "00010","rs":"01000","ls":"01001" }   #typeB contains $Imm value
type_C={"mov": "00011","div":"00111","not":"01101","cmp":"01110"}
type_D={"ld":"00100","st":"00101"}
type_E={"jmp":"01111","jlt":"10000","jgt":"10001","je":"10010"}
error_flag_2=False
label_names=[]
variable_names=[]
mem_add=[None]*256
Registers = {"R0":"0000000000000000", "R1":"0000000000000000", "R2":"0000000000000000", "R3":"0000000000000000",
 "R4": "0000000000000000", "R5": "0000000000000000", "R6":"0000000000000000","FLAGS":"0000000000000000"}



k=1
pc=0 #program counter
mem=["0"*16]*256 #mem to be dumped
def Immediate(n):
    n=int(n)
    Bin=""
    while n:
        Bin=str(n%2)+Bin
        n=n//2
    if len(Bin)>16:
        return Bin[len(Bin)-16:]
    while len(Bin)<16:
        Bin="0"+Bin
    return Bin

def left_shift(bin,imm):
    shift=str("0"*int(imm))
    bin=bin+shift
    bin=bin[int(imm):]
    return bin

def right_shift(bin,imm):
    shift=str("0"*int(imm))
    bin=shift+bin
    bin=bin[0:16]
    return bin

def findregister(register): #finds  register 
    for key, value in Bin_reg.items():
        if value==register:
            return key

def fetch_instruction(type,inst_name,bin_inst,i):
    instruction=""
    if type=="A":
        r1=findregister(bin_inst[7:10])
        r2=findregister(bin_inst[10:13])
        r3=findregister(bin_inst[13:])
        instruction=inst_name + " " + r1+" "+ r2+" "+ r3
        #print(instruction)
    elif type=="B":
        r1=findregister(bin_inst[5:8])
        imm=int(bin_inst[8:],2)
        #print(imm)
        instruction=inst_name+" "+r1+" "+ str(imm)
        #print(instruction)
    elif type=="C":
        r1=findregister(bin_inst[10:13])
        r2=findregister(bin_inst[13:])
        instruction=inst_name+" "+r1+" "+r2
        #print(instruction)
    elif type=="D":
        r1=findregister(bin_inst[5:8])
        mem=int(bin_inst[8:],2)
        mem_add[mem]=["var "+"x"]
        instruction=inst_name+" "+r1+" "+ "variable at mem add " +str(mem)  #X is just dummy variable, go to mem_add using mem 
        #print(instruction)
    elif type=="E":
        mem=int(bin_inst[8:],2) #mem is the memory address of that instruction
        instruction=inst_name+" "+ str(mem)
        #print(instruction)
    mem_add[i]=[instruction]+ [type] #storing all the instructions in mem_add
  


def execute_instruction(instruction,type,pc,mem):
    instruction=instruction.split(" ")

#add your codes here

    if type=="A": 
        a=int(Registers[instruction[2]],2)
        b=int(Registers[instruction[3]],2)

        if instruction[0]=="add":
            c=a+b
            if c>65535:
                Registers[instruction[1]]=Immediate(c)
                Registers["FLAGS"]=Registers["FLAGS"][0:12]+"1"+Registers["FLAGS"][13:]
            else:
                Registers[instruction[1]]=Immediate(c)
            #print(Registers)
                
        elif instruction[0]=="sub":
            c=a-b
            if c>=0:
                Registers[instruction[1]]=Immediate(c)
            else:
                Registers[instruction[1]]="00000000"
                Registers["FLAGS"]=Registers["FLAGS"][0:12]+"1"+Registers["FLAGS"][13:]
            #print(Registers)
        elif instruction[0]=="mul":
            c=a*b
            if c>65535:
                Registers[instruction[1]]=Immediate(c)
                Registers["FLAGS"]=Registers["FLAGS"][0:12]+"1"+Registers["FLAGS"][13:]
            else:
                Registers[instruction[1]]=Immediate(c)
            #print(Registers)
        elif instruction[0]=="xor":
            Registers[instruction[1]]=Immediate(a^b)
            reset_flag()
        elif instruction[0]=="or":
            Registers[instruction[1]]=Immediate(a|b)
            reset_flag()
        elif instruction[0]=="and":
            Registers[instruction[1]]=Immediate(a&b)
            reset_flag()

    elif type=="B":
        if instruction[0]=="mov":
            Registers[instruction[1]]=Immediate(instruction[2])
            #print(Registers)
        elif instruction[0]=="ls":
            Registers[instruction[1]]=left_shift(Registers[instruction[1]],instruction[2])
            #print(Registers)
        elif instruction[0]=="rs":
            Registers[instruction[1]]=right_shift(Registers[instruction[1]],instruction[2])
            #print(Registers)
        reset_flag()

    elif type=="C":
        a=int(Registers[instruction[1]],2)
        b=int(Registers[instruction[2]],2)
        if instruction[0]=="div":
            c = a/b
            d = a%b
            Registers["R0"] = format(c, '08b')
            Registers["R1"] = format(d, '08b')
            reset_flag()
        elif instruction[0]=="not":
            c = ~b
            c = format(c, '08b')
            Registers[instruction[1]] = c
            reset_flag()
        elif instruction[0]=="cmp":
            
            if a==b:
                Registers["FLAGS"] = Registers["FLAGS"][0:15] + "1"
            elif a>b:
                Registers["FLAGS"] = Registers["FLAGS"][0:14] + "1" + Registers["FLAGS"][15]
            else:
                Registers["FLAGS"] = Registers["FLAGS"][0:13] + "1" + Registers["FLAGS"][14:]
            

        elif instruction[0]=="mov":
            Registers[instruction[1]] = Registers[instruction[2]]
            reset_flag()

    elif type=="D":
        if instruction[0] == "ld":
            Registers[instruction[1]] = Registers[instruction[2]]
        elif instruction[0] == "st":
            mem[int(Registers[instruction[2]],2)] = Registers[instruction[1]]
        reset_flag()

    elif type=="E":
        if instruction[0]=="jgt":
            if Registers["FLAGS"][-2]=="1":
                
                pc= int(instruction[1])
                reset_flag()
                return pc
            reset_flag()

        elif instruction[0]=="jlt":
            if Registers["FLAGS"][-3]=="1":
                pc=int(instruction[1])
                reset_flag()
                return pc
            reset_flag()

        elif instruction[0]=="jmp":
            pc=int(instruction[1])
            reset_flag()
            return pc
            
        elif instruction[0]=="je":
            if Registers["FLAGS"][-1]=="1":
                pc=int(instruction[1])
                reset_flag()
                return pc
            
            reset_flag()

        else:
            1

    return (pc+1) 
    

i=0
Halted=False
k=1

"""driver prt of function """
while(not Halted):
    bin_inst=input()
    mem[i]=(bin_inst)
    if(bin_inst=="1001100000000000"):
        mem_add[i]=["hlt"]
        Halted=True
        break
    opcode=bin_inst[:5]
    inst_name=""
    for key, value in type_A.items():
        if value==opcode:
            type="A"
            inst_name=key
            
    for key, value in type_B.items():
        if value==opcode:
            type="B"
            inst_name=key
            
    for key, value in type_C.items():
        if value==opcode:
            type="C"
            inst_name=key
            
    for key, value in type_D.items():
        if value==opcode:
            type="D"
            inst_name=key
            
    for key, value in type_E.items():
        if value==opcode:
            type="E"
            inst_name=key
    fetch_instruction(type,inst_name,bin_inst,i)
    i+=1
def reset_flag():
    Registers["FLAGS"]="0"*16
pc=0
Halted=False
while (not Halted) : #fetching each instruction from the memory
    
    type=""
    instruction=""
    if mem_add[pc]==["hlt"]:
        Halted=True
    instruction=mem_add[pc][0]
    if len(mem_add[pc])>1:
        type=mem_add[pc][1]

    i=execute_instruction(instruction,type,pc,mem) 
    #execute each instruction 
    
    print((format(pc, '08b')),end=" ")
    print(Registers["R0"],Registers["R1"],Registers["R2"],Registers["R3"],Registers["R4"],Registers["R5"],Registers["R6"],end=" ")
    print(Registers["FLAGS"])
    #register dump

    pc=i # updated program counter
    k+=1  #k is just printing line no
    
for i in mem:
    print(i) 
    k+=1 
