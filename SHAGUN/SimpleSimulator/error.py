import sys
#possible errors
"""
a.Use of wrong name for instruction
there shud be one space between all the words.
instruction= 1. label:instruction(there shud be no space between label and colon)
             2. instruction(shud belong to one of the 6 types)
             3. variable definitn(variables shud be "var" format and variable_name shud be valid(alphanum and _))
a1.use of wrong name of registers in a line of instruction
a3. Use of space between a label 
b. Use of undefined variables
c. Use of undefined labels
variables must be defined at the beginning of the code
d. Illegal use of FLAGS register
e. Illegal Immediate values (less than 0 or more than 255)
f. Misuse of labels as variables or vice-versa
g. Variables not declared at the beginning
h. Missing hlt instruction
i. hlt not being used as the last instruction
j. Wrong syntax used
k.the no of instructions shud be <=256
"""
# 1st pass, add this code to assembler_main.py

file_object = open("errors.txt","w")
mem_addr=[]
i=0                 #line counter

valid_instructions=["add","sub","mul","xor","or","and","mov","rs","ls","div","not","cmp","ld","st","jmp","jlt","jgt","je","hlt"]
valid_register_names=["R0","R1","R2","R3","R4","R5","R6","FLAGS"]  
valid_label_names=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","_","1","2","3","4","5","6","7","8","9","0",":"]

type_A={"add":"00000","sub": "00001","mul":"00110","xor":"01010","or":"01011","and":"01100"}
type_B={"mov" : "00010","rs":"01000","ls":"01001" }   #typeB contains $Imm value
type_C={"mov": "00011","div":"00111","not":"01101","cmp":"01110"}
type_D={"ld":"00100","st":"00101"}
type_E={"jmp":"01111","jlt":"10000","jgt":"10001","je":"10010"}
error_flag_2=False
label_names=[]
variable_names=[]

def check_type(x): 
    #returns the type of instruction
    if x:
        first=x[0]
        m=""
        for i in x:
            m=m+i

        if first in type_A.keys():
            return "A"
        elif first in type_B.keys() and ("$" in m):
            return "B"
        elif first in type_C.keys():
            return "C"
        elif first in type_D.keys():
            return "D"
        elif first in type_E.keys():
            return "E"
        elif first=="hlt":
            return "F"
        elif ":" in first:
            return "label"
        elif "var" ==first:
            return "variable"
        else:
            return "none"
    else:
        return "none"
#this is error dictionary
errors={ 1 : "[ERROR] : Typos in instruction name or label name in line {}", 2: "[ERROR] : Use of undefined variable in line {}",
 3: "[ERROR] : Use of undefined labels in line {}", 4:"[ERROR] : Illegal use of FLAGS register in line{}",
 5: "[ERROR] : Illegal Immediate values (less than 0 or more than 255) in line {}",
 6: "[ERROR] : Variables not declared at the beginning",7: "[ERROR] : hlt not being used as the last instruction",
 8: "[ERROR] : Missing hlt instruction",9: "[ERROR] : General Syntax Error in instruction in line {}",
 10:"[ERROR] : Variable name is not valid (must be alphabet or number) in line {}",
 11: "[ERROR] : Variable used already initialised in memory {}",12: "[ERROR] : immediate value should be an integer in line {}",
 12: "[ERROR] : Variable name used instead of label name in line {}", 13: "[ERROR] : Label name used instead of variable name in line {}"
       } # add more errors here 



def isvalidlabel(line): #returns False if labelname is invalid
    for char in line:
        if not(char in valid_label_names):
            return False
    if(line.find(":")!=len(line)-1):
        return False
    return True        

def check_instruction(line): #returns true if instruction is invalid
    if line:
     if line[0]=="var":
        return False
     elif line[0] in valid_instructions:
        return False
     elif(isvalidlabel(line[0])):
        return False
     else:
         return True
    else:
        return True

def check_line(line): #returns line no of an instruction in the original code
    i=0
    for i in range(len(original_instruction)):
        if line == original_instruction[i]:
            return i+1
        else:
            i+=1
    return -1

def check_typos(instruction_code):
 # gives the type of instruction, input arg is in form of array of strings of each line
    global error_flag_2
    type=check_type(instruction_code)
    m1=type.split()
    if(m1[0]=="label"):
        a= check_typos(instruction_code[1:])
        return a
    error_flag_2 =check_instruction(instruction_code)
    line_no=check_line(instruction_code)
    if(error_flag_2):
        return True
    else:
        return False
    """"
    if(type=="A"):
        if(len(instruction_code)!=4):
            error_flag_1=True
            return(error_flag_1)
        elif(not(instruction_code[1] in valid_register_names) or not(instruction_code[2] in valid_register_names) or not(instruction_code[3] in valid_register_names)):
            error_flag_1=True
            return(error_flag_1)
    elif(type=="B"):
        if(len(instruction_code)!=3):
            error_flag_1=True
            return(error_flag_1)
        elif((instruction_code[1] not in valid_register_names) or str((instruction_code[2] )).find("$")!=0):
            error_flag_1=True
            return(error_flag_1)
    elif(type=="C"):
        if(len(instruction_code)!=3):
            error_flag_1=True
            return(error_flag_1)
        elif(not(instruction_code[1] in valid_register_names) or not(instruction_code[2] in valid_register_names) ):
            error_flag_1=True
            return(error_flag_1)
    elif(type=="D"):
        if(len(instruction_code)!=3):
            error_flag_1=True
            return(error_flag_1)
        elif(not(instruction_code[1] in valid_register_names)):
            error_flag_1=True
            return(error_flag_1)
    elif(type=="E"):
        if(len(instruction_code)!=2):
            error_flag_1=True
            return(error_flag_1)
        elif(not(instruction_code[1] in valid_register_names) ):
            error_flag_1=True
            return(error_flag_1)
    elif(type=="F"):
        if(instruction_code!=["hlt"]):
            error_flag_1=True
            return(error_flag_1)
    else:
        return False
    """

def check_syntax(instruction_code):
    type=check_type(instruction_code)
    global error_flag_2
    m1=type.split()
    if(m1[0]=="label"):
        a= check_syntax(instruction_code[1:])
        return a
    if(type=="A"):
        if(len(instruction_code)!=4):
            error_flag_2=True
            return(error_flag_2)
        elif(not(instruction_code[1] in valid_register_names) or not(instruction_code[2] in valid_register_names) or not(instruction_code[3] in valid_register_names)):
            error_flag_2=True
            print("[ERROR] : Typos in register name")
            return(error_flag_2)
    elif(type=="B"):
        if(len(instruction_code)!=3):
            error_flag_2=True
            return(error_flag_2)
        elif((instruction_code[1] not in valid_register_names) or str((instruction_code[2] )).find("$")!=0):
            error_flag_2=True
            print("[ERROR] : Typos in register name")
            return(error_flag_2)
    elif(type=="C"):
        if(len(instruction_code)!=3):
            error_flag_2=True
            return(error_flag_2)
        elif(not(instruction_code[1] in valid_register_names) or not(instruction_code[2] in valid_register_names) ):
            error_flag_2=True
            print("[ERROR] : Typos in register name")
            return(error_flag_2)
    elif(type=="D"):
        if(len(instruction_code)!=3):
            error_flag_2=True
            return(error_flag_2)
        elif(not(instruction_code[1] in valid_register_names)):
            error_flag_2=True
            print("[ERROR] : Typos in register name")
            return(error_flag_2)
    elif(type=="E"):
        if(len(instruction_code)!=2):
            error_flag_2=True
            return(error_flag_2)
        elif(not(instruction_code[1] in label_names) ):
            error_flag_2=True
            print("[ERROR] : Typos in register name")
            return(error_flag_2)
    elif(type=="F"):
        if(instruction_code!=["hlt"]):
            error_flag_2=True
            return(error_flag_2)
    else:
        return False



def check_wrong_variabe_usage(line):  #returns true if undefined variable is used
     
     type=check_type(line)
     
     if type=="label":
         a=check_wrong_variabe_usage(line[1:])
         return a
     if(type=="D"):
         if line[2] not in variable_names :
             return True
    
     return False


        
def check_wrong_label_usage(line): #returns true if undefined label is used
    type=check_type(line)
    if type=="label":
         a= check_wrong_label_usage(line[1:])
         return a
    if(type=="E"):
         if line[1] not in label_names:
             return True
    return False

def check_wrong_use_of_flags_register(line): #checks if flags are used incorrectly
    type=check_type(line)
    if type=="label":
        a=check_wrong_use_of_flags_register(line[1:])
        return a
    if "FLAGS"in line:
        if(line[1] in valid_register_names) and (line[1]!="FLAGS" and line[2]=="FLAGS"):
            return False 
        else:
            return True
    else:
        return False

    

def check_wrong_immediate_value(line):
    type=check_type(line)
    if type=="label":
        a=check_wrong_use_of_flags_register(line[1:])
        return a
    if type=="B":
        Imm=int(line[2].replace("$",""))
        if(Imm>=256 or Imm<0) :
            return True

    return False  

def check_valid_variable(line): #check if its valid variable
    type=check_type(line)
    if type=="label":
        a=check_valid_variable(line[1:])
        return a
    if type=="variable":
        if len(line)>=2:
            if not(line[1].isalnum()):
                return True
        else:
            return False

    return False

def check_int(a):
    try:
        int(a)
        return True
    except ValueError:
        return False

def check_imm(line):
    type=check_type(line)
    if type=="label":
        a=check_valid_variable(line[1:])
        return a
    if type=="B":
        if not(check_int(line[2].replace("$",""))):
            return True

    return False

def check_label_variable(line):
    type=check_type(line)
    if type=="label":
        a=check_label_variable(line[1:])
        return a
    if(type=="E" and (line[1] in variable_names)):
        return True
    return False

def check_variable_label(line):
    type=check_type(line)
    if type=="label":
        a=check_variable_label(line[1:])
        return a
    if(type=="D" and (line[1] in label_names)):
        return True
    return False

""" this function checks all the possible errors"""
def checkerrors(line):    
                  # this function checks all the errors mentioned in pdf from 1 to 5 
    line_no=check_line(instruction_code) 
    if check_syntax(line):
        print(errors[9].format(line_no))
        file_object.write(errors[9].format(line_no))
        error_flag_2=True
        return error_flag_2 
    if check_typos(line):
        print(errors[1].format(line_no))
        file_object.write(errors[1].format(line_no))
        error_flag_2=True
        return error_flag_2
    if check_label_variable(line):
        print(errors[12].format(line_no))
        file_object.write(errors[12].format(line_no))
        error_flag_2=True
        return error_flag_2
    if check_variable_label(line):
        print(errors[13].format(line_no))
        file_object.write(errors[13].format(line_no))
        error_flag_2=True
        return error_flag_2
    if check_wrong_variabe_usage(line):
        print(errors[2].format(line_no))
        file_object.write(errors[2].format(line_no))
        error_flag_2=True
        return error_flag_2
    if check_wrong_label_usage(line):
        print(errors[3].format(line_no))
        file_object.write(errors[3].format(line_no))
        error_flag_2=True
        return error_flag_2
    if check_wrong_use_of_flags_register(line):
        print(errors[4].format(line_no))
        file_object.write(errors[4].format(line_no))
        error_flag_2=True
        return error_flag_2
    
    if check_imm(line):
        print(errors[12].format(line_no))
        file_object.write(errors[12].format(line_no))
        error_flag_2=True
        return error_flag_2

    if check_wrong_immediate_value(line):
        print(errors[5].format(line_no))
        file_object.write(errors[5].format(line_no))
        error_flag_2=True
        return error_flag_2
    
    if check_valid_variable(line):
        print(errors[10].format(line_no))
        file_object.write(errors[10].format(line_no))
        error_flag_2=True
        return error_flag_2

    #add more remaining errors here


""" driver part of the code"""
original_instruction=[]
lines=[]
"""
with open("sample_read_instruction.txt","r") as f:
    lines=f.readlines()
    """
Data_original=[Line for Line in lines]
Data = [Line for Line in lines if Line.strip() ] 

if(len(Data))>256:
    print("[ERROR] : The assembler can write less than or equal to 256 lines.")
    file_object.write("[ERROR] : The assembler can write less than or equal to 256 lines.")

for x in Data_original:
    x=x.split()
    original_instruction.append(x)
#original_instruction stores the original input text

Data_updated=[]
mem_add_var=[]
label_add={}
for x in Data: 
    instruction_code=x.split()
    Data_updated.append(instruction_code)
    
    if(check_type(instruction_code)=="variable"):
        if len(instruction_code)>=2 :
            if instruction_code[1] in variable_names:
                print("[ERROR] : Ambiguity in line "+str(check_line(instruction_code))+", you have declared variable "+instruction_code[1]+" already")
                error_flag_2=True
                #sys.exit()
                break

            variable_names.append(instruction_code[1])
            mem_add_var.append(instruction_code)
        else:
            print("[ERROR] :  Wrong variable declaration syntax used ")
            error_flag_2=True
            sys.exit()

    if(check_type(instruction_code)!="variable"):
        mem_addr.append(instruction_code)
        if(check_type(instruction_code)=="label"):
            if(instruction_code[0].replace(":","")in label_names):
                if instruction_code[0].replace(":","") not in mem_addr[mem_addr.index(instruction_code)-1]:
                 print("[ERROR] : Ambiguity in line "+ str(check_line(instruction_code))+", you have used "+instruction_code[0].replace(":","")+ " already")
                 error_flag_2=True
                 #sys.exit()
                 break
                #checks if label is declared twice
                
            label_names.append(instruction_code[0].replace(":",""))
            label_add[instruction_code[0].replace(":","")]=mem_addr.index(instruction_code)
non_var_len = len(mem_addr) 
mem_addr=mem_addr+mem_add_var
""""
#check whether variable is initialised twice
temp=[]
for variable in variable_names:
    if variable in temp:
        print(errors[11].format( "by the name "+ variable))
        file_object.write(errors[11].format( "by the name "+ variable))
    temp.append(variable)
    """

#checks whether variable is initialised a the right location
check=True
for instruction in Data_updated:
    type=check_type(instruction)
    if type!="variable":
        check=False
    if(type=="variable" and check==False):
        error_flag_2=True
        print(errors[6])
        file_object.write(errors[6])
        sys.exit()
        

#checks if hlt instruction is misplaced
def check_type1(line):
    type=check_type(line)
    if type=="label":
        return check_type1(line[1:])
    else:
        return type



#Data_updated stores the updated instructions after removing all empty lines and white spaces  

for instruction_code in Data_updated:
    
    if checkerrors(instruction_code):
        error_flag_2=True
        sys.exit()
        

found=False
for instruction in range(len(Data_updated)):
    type=check_type1(Data_updated[instruction])
    if type=="F":
        found=True
        if(instruction!=len(Data_updated)-1):
            error_flag_2=True
            print(errors[7])
            file_object.write(errors[7])
            sys.exit()
            
            
#checks whether hlt instruction is missing
if found==False:
    error_flag_2=True
    print(errors[8])
    file_object.write(errors[8])
    sys.exit()
    #sys.exit()
   # print("line no "+ str(check_line(instruction_code))+" is verified")
    #this print statement is just to see if my part works, you can delete it 
 #end of error program

