from tkinter import *
from turtle import right

def int2bs(s, n):
        """ Converts an integer string to a 2's complement binary string.

            Args: s = Integer string to convert.to 2s complement binary.
                  n = Length of outputted binary string.

            Example Input: stpd("4", 4)
            Example Output: "0100"

            Example Input: stpd("-3", 16)
            Example Output: "1111111111111101" """

        x = int(s)                              # Convert string to integer, store in x.
        if x >= 0:                              # If not negative, use python's binary converter and strip the "0b"
            ret = str(bin(x))[2:]
            return ("0"*(n-len(ret)) + ret)     # Pad with 0s to length.
        else:
            ret = 2**n - abs(x)                 # If negative, convert to 2s complement integer
            return bin(ret)[2:]

def bintint(a):
    b = int(a[1:],2)-int(a[0])*2**(len(a)-1)
    return b

# Disassembler-----------------------------------------------------------
# Dictionary for the opcodes
opcodes = {
    0: "rtyp",
    # 1:"branch",
    2: "j",
    3: "jal",
    4: "beq",
    5: "bne",
    8: "addi",
    10: "slti",
    12: "andi",
    13: "ori",
    14: "xori",
    15: "lui",
    32: "lb",
    35: "lw",
    40: "sb",
    43: "sw"
}

# if we have a r-type instruction (opcode 0), we need the function codes to decode the functions
fcodes = {
    0: "sll",
    3: "sra",
    4: "sllv",
    6: "srlv",
    7: "srav",
    8: "jr",
    9: "jalr",
    12: "syscall",
    32: "add",
    34: "sub",
    36: "and",
    37: "or",
    38: "xor",
    39: "nor",
    42: "slt"
}

# List of registernumbers and their cleartext names
registers = {
    0: "$zero",
    1: "$at",
    2: "$v0",
    3: "$v1",
    4: "$a0",
    5: "$a1",
    6: "$a2",
    7: "$a3",
    8: "$t0",
    9: "$t1",
    10: "$t2",
    11: "$t3",
    12: "$t4",
    13: "$t5",
    14: "$t6",
    15: "$t7",
    16: "$s0",
    17: "$s1",
    18: "$s2",
    19: "$s3",
    20: "$s4",
    21: "$s5",
    22: "$s6",
    23: "$s7",
    24: "$t8",
    25: "$t9",
    26: "$k0",
    27: "$k1",
    28: "$gp",
    29: "$sp",
    30: "$fp",
    31: "$ra"
}

#------------------------------------------
def disassemble(in_ins): #input instruction
    out_ins = [0]*len(in_ins) #output instruction
    for iteration in range(len(in_ins)):
        x = in_ins[iteration].split('0x')[1]  # instruction
        ins_interger = int(x, 16)
        ins_binary = bin(ins_interger)
        ins_binary = ins_binary.split("0b")[1]
        ins_binary = ins_binary.zfill(32) #instruction in 32 bit binary

        opcode_binary = ins_binary[:6]
        opcode_integer = int(opcode_binary, 2)

        if opcode_integer not in opcodes:
            out_ins[iteration] = "THE OPERATION IS NOT IN OUR DATA CARD"
            return
        elif opcode_integer == 0:  # r type instruction
            funct_binary = ins_binary[26:]
            funct_integer = int(funct_binary, 2)
            if funct_integer not in fcodes:
                out_ins[iteration] =  "THE OPERATION IS NOT IN OUR DATA CARD"
                return

            rs = registers[int(ins_binary[6:11], 2)]
            rt = registers[int(ins_binary[11:16], 2)]
            rd = registers[int(ins_binary[16:21], 2)]

            # special r type instruction
            if(funct_integer == 0 or funct_integer == 2 or funct_integer == 3):  # shift instructions
                shamt = ins_binary[21:26]
                out_ins[iteration] = fcodes[funct_integer] + " " + rd + " " + rt + " " + str(int(shamt, 2))
            elif(funct_integer == 8 or funct_integer == 9):  # jr/jalr
                out_ins[iteration] = fcodes[funct_integer] + " " + rs
            elif(funct_integer == 12 or funct_integer == 13):  # syscall or break
                out_ins[iteration] = fcodes[funct_integer]
            elif(funct_integer == 16 or funct_integer == 17 or funct_integer == 18 or funct_integer == 19):
                out_ins[iteration] = fcodes[funct_integer] + " " + rd
                # mfhi, mthi, mflo, mtlo
            elif(funct_integer == 24 or funct_integer == 26):  # mult and div
                out_ins[iteration] = fcodes[funct_integer] + " " + rs + " " + rt
            else:
                out_ins[iteration] = fcodes[funct_integer] + " " + rd + " " + rs + " " + rt

        # j type instruction
        elif (opcode_integer == 2 or opcode_integer == 3):
            # j/jal j-type instructions
            imm_binary = ins_binary[6:]
            imm_integer = bintint(imm_binary)
            out_ins[iteration] = opcodes[opcode_integer] + " " + str(imm_integer)


        # i type instruction
        else:
            imm_binary = ins_binary[16:]
            imm_integer = bintint(imm_binary)
            rs = registers[int(ins_binary[6:11], 2)]
            rt = registers[int(ins_binary[11:16], 2)]
            imm_hex = hex(imm_integer)
            if (opcode_integer == 32 or opcode_integer == 35 or opcode_integer == 40 or opcode_integer == 43):  # lw lb sb sw
                out_ins[iteration] = opcodes[opcode_integer] + " " + rt + " " + str(imm_integer) + "(" + rs + ")"
            elif opcode_integer == 15: #lui
                out_ins[iteration] = opcodes[opcode_integer] + " " + rt + " "+str(imm_integer)
            else:
                out_ins[iteration] = opcodes[opcode_integer] + " " + rt + " " + rs + " " + str(imm_integer)
    return out_ins
#------------------------------------------

#Disassembler definition ends--------------------------

#Assembler--------------------------------------------
def shamt(i):    #i is the list                     #defining a function to compute the 5- bit shift amount
    if i[0]=="shft":                                #value in case of instruction being of shift type.
        return("sssss")
    else:
        return("00000")


#f=open("input.txt","r+")                            #old commit where program read file
#f.flush()

REGISTERS = {                                           #defining the dictionary key-value pair which
        '$zero': '0',                                   #encodes every on of the 32 registers available
        '$at': '1',                                     #in MIPS with an integer.
        '$v0': '2',
        '$v1': '3',
        '$a0': '4',
        '$a1': '5',
        '$a2': '6',
        '$a3': '7',
        '$t0': '8',
        '$t1': '9',
        '$t2': '10',
        '$t3': '11',
        '$t4': '12',
        '$t5': '13',
        '$t6': '14',
        '$t7': '15',
        '$s0': '16',
        '$s1': '17',
        '$s2': '18',
        '$s3': '19',
        '$s4': '20',
        '$s5': '21',
        '$s6': '22',
        '$s7': '23',
        '$t8': '24',
        '$t9': '25',
        '$k0': '26',
        '$k1': '27',
        '$gp': '28',
        '$sp': '29',
        '$fp': '30',
        '$ra': '31',
    }



opcode={'j': 2, 'jal': 3, 'beq': 4, 'bne': 5, 'blez': 6,     #defining the opcode correspondence
'bgtz': 7, 'addi': 8, 'slti': 10, 'andi': 12, 'ori': 13,     #for non-R Type instructions
 'xori': 14, 'lui': 15, 'lb': 32, 'lw': 35,
  'sb': 40, 'sw': 43}


func={'sll': 0, 'slr': 2, 'sra': 3, 'sllv': 4, 'srlv': 6, 'srav': 7, 'jr': 8,  #defining the funct bit correspondence
 'jalr': 9, 'syscall': 12, 'break': 13, 'mfhi': 16, 'mtlo': 19, 'mflo': 18,    #for R Type instructions
 'mult': 24, 'div': 26,  'add': 32, 'sub': 34, 'and': 36, 'or': 37,
 'xor': 38, 'nor': 39, 'slt': 42}


r_type=['add', "sllv", "srlv", "srav", "sub","and","or","xor","nor","slt"]    #list of supported R type instructions
i_type=["addi","beq","bne", "slti","ori", "xori","lui"]                       #list of supported I type instructions
j_type=["j", "jal"]                                                           #list of supported J type instructions
s_type=["sw","lw","lb","sb"]                                                  #these instructions are originally I type.
                                                                              #But they take a different form (load-store form).
                                                                              #Hence, we store them in s type

shift_type=["sll","sra"]                                                      #These are I type as well. But we use a different
#pseudo_type=[]                                                               #style for them.
#f.seek(0)                                              #old commit where program read text file as input
#code=f.readlines()
                                                   #input list from user text box
def assemble_it (a):
    l=[]
    for i in range(len(a)):
        a[i]=(a[i].strip()).split()
    for i in (a):
        if i[0] in r_type:
            t="000000"+" "+int2bs(REGISTERS[i[2]],5)+" "+int2bs(REGISTERS[i[3]],5)+" "+int2bs(REGISTERS[i[1]],5)+" "+"00000"+" "+int2bs(func[i[0]],6)
            t=t.replace(" ","")
            l.append(hex(int(t,2)))
        elif i[0] in i_type:
            t=int2bs(opcode[i[0]],6)+" "+int2bs(REGISTERS[i[2]],5)+" "+int2bs(REGISTERS[i[1]],5)+" "+int2bs(i[-1],16)
            t=t.replace(" ","")
            l.append(hex(int(t,2)))
        elif i[0] in j_type:
            t=int2bs(opcode[i[0]],6)+" "+ int2bs((i[-1]),26)
            t=t.replace(" ", "")
            l.append(hex(int(t,2)))
        elif i[0] in s_type:
            t=int2bs(opcode[i[0]],6)+" "+int2bs(REGISTERS[i[-1][-4:-1]],5) +" "+int2bs(REGISTERS[i[1]],5)+" "+int2bs(i[-1][0:-5],16)
            t=t.replace(" ", "")
            l.append(hex(int(t,2)))
        elif i[0] in shift_type:
            t="000000"+" "+"00000"+" "+int2bs(REGISTERS[i[2]],5)+" "+int2bs(REGISTERS[i[1]],5)+" "+int2bs(i[3],5)+" "+int2bs(func[i[0]],6)
            t=t.replace(" ", "")
            l.append(hex(int(t,2)))
        elif i[0]=="jr":
            t="000000"+" "+int2bs(REGISTERS[i[1]],5)+" "+"000000000000000"	+"001000"
            t=t.replace(" ", "")
            l.append(hex(int(t,2)))
        elif i[0]=="syscall":
            t="00000000000000000000000000001100"
            t=t.replace(" ", "")
            l.append(hex(int(t,2)))

    return l





#assembler ends-------------------------------------------------

#GUI ------------------------------------------
def assembler_click():
    new_window = Tk()
    new_window.title("ASSEMBLER")
    new_window.geometry("800x700+350+50")
    Label(new_window,pady=20,font='arial 15 bold',text="Assembler").pack()
    def conversion_assembler_click():
        INPUT = assembler_input.get("1.0", "end-1c")
        a = INPUT.split("\n")
        OUTPUT = assemble_it(a)
        for i in range(len(OUTPUT)):
            OUTPUT[i] = OUTPUT[i]+"\n"
            Output_ase.insert(END, OUTPUT[i])

    assembler_input = Text(new_window, height=100, width=50)
    Output_ase = Text(new_window, height=100, width=50)
    display_asem = Button(new_window, text="Convert", width=20,pady=5,font='arial 15 bold',
                     command=conversion_assembler_click)
    display_asem.pack(side=TOP)
    assembler_input.pack(side=LEFT,anchor='w')
    Output_ase.pack(side = RIGHT,anchor='e')


# Disassembler switch--------------------------------
def disassembler_click():
    new_window = Tk()
    new_window.title("DISASSEMBLER")
    new_window.geometry("800x700+350+50")
    Label(new_window, pady=20,font='arial 15 bold',text="Disassembler").pack()
    def conversion_disassembler_click():
        INPUT = Disassembler_input.get("1.0", "end-1c")
        a = INPUT.split("\n")
        OUTPUT = disassemble(a)
        for i in range(len(OUTPUT)):
            OUTPUT[i] = OUTPUT[i]+"\n"
            Output_dis.insert(END, OUTPUT[i])

    Disassembler_input = Text(new_window, height=100, width=50)
    Output_dis = Text(new_window,height=100, width=50)
    display = Button(new_window, text="Convert", pady=5,width=20, font='arial 15 bold',
                     command=conversion_disassembler_click)
    display.pack(side=TOP)
    Disassembler_input.pack(side=LEFT,anchor='w')
    Output_dis.pack(side = RIGHT,anchor='e')
main_window = Tk()
main_window.title("Mips Assembler and Disassembler")
main_window.geometry("800x700+350+50")
Button(main_window, pady=5,text="Assembler",font='arial 15 bold',width=20,command = assembler_click).place(relx=.5, rely=0.33, anchor=CENTER)
Button(main_window, pady=5,text="Disassembler",font='arial 15 bold',width=20,command = disassembler_click).place(relx=.5, rely=0.66, anchor=CENTER)

main_window.mainloop()
# -----------------------------------------------------------


# reading the text file-------------------------------------
# input_file = open("input_instructions.txt","r")
# ins_r1 = input_file.readlines()
# for i in range(len(ins_r1)):
#     ins_r1[i] =ins_r1[i].rstrip("\n")
#     # print(i)
# # print(disassemble(ins_r1))
# result = disassemble(ins_r1)
# output_file= open("output_instruction.txt","w")
# for i in range(len(result)):
#     output_file.write(result[i]+"\n")
# printing in the text file---------------------------------

# print(disassemble(ins_r1))
