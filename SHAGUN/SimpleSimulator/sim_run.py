

Bin_reg = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4": "100", "R5": "101", "R6":"111","FLAGS":"111"}  
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

Halted=False
i=0
k=1
pc=0 #program counter

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

#add your codes here

    if type=="A":  
        1
    elif type=="B":
        1
    elif type=="C":
        1
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
    #print(instruction,type)
    execute_instruction(instruction,type)