

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

Halted=False
i=0
k=1
pc=0 #program counter

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
    global k
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
  


def execute_instruction(instruction,type):
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
        elif instruction[0]=="or":
            Registers[instruction[1]]=Immediate(a|b)
        elif instruction[0]=="and":
            Registers[instruction[1]]=Immediate(a&b)

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

    elif type=="C":
        a=int(Registers[instruction[1]],2)
        b=int(Registers[instruction[2]],2)
        if instruction[0]=="div":
            c = a/b
            d = a%b
            Registers["R0"] = format(c, '08b')
            Registers["R1"] = format(d, '08b')

        elif instruction[0]=="not":
            c = ~b
            c = format(c, '08b')
            Registers[instruction[1]] = c
        elif instruction[0]=="cmp":
            1
            if a==b:
                1
        elif instruction[0]=="mov":
            Registers[instruction[1]] = Registers[instruction[2]]

    elif type=="D":
        1
    elif type=="E":
        1
    else:
        1
    



"""driver prt of function """
while(i!=256):
    bin_inst=input()
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

for i in mem_add:
    type=""
    instruction=""
    if i:
        instruction=i[0]
        if len(i)>1:
            type=i[1]
    """
    if instruction!="":
        print(instruction,type)
        """
    execute_instruction(instruction,type)