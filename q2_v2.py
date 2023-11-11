with open('output_pipeline.txt', 'w') as f:
    global if_id_pipeline
    if_id_pipeline={}
    global id_ex_pipeline
    id_ex_pipeline={"control_signals":{},"alu_constrols":{}}
    global ex_mem_pipeline
    ex_mem_pipeline={}
    global mem_wb_pipeline
    mem_wb_pipeline={}
    import sys

    global count_if
    count_if=1
    global count_id
    count_id=0
    global count_ex
    count_ex=0
    global count_mem
    count_mem=0
    global count_wb
    count_wb=0

    global if_flag
    if_flag=1
    global id_flag
    id_flag=1
    global ex_flag
    ex_flag=1
    global mem_flag
    mem_flag=1


    global reg_in_process
    reg_in_process=[]
    global result

    global forwardA
    forwardA="111"
    global pc
    pc=0
    op_dict= {
        "000000": "R_TYPE",
        "011100": "MUL",
        
        "001001":"ADDIU",
        "001000": "ADDI",
        "001101": "ORI",
        "001111": "LUI",
        "100011": "LW",
        "101011": "SW",
        "0011111":"LUI",
        "000101":"BGE",
        "001101":"ORI",
        "000100": "BEQ",
        "000101": "BNE",
        "000010": "J",
        "000011": "JAL",
        
        
    }
    r_type=1
    i_type=11
    j_type=17
    mul_value=2
    decoded_list=[]
    func_dict = {
        "100000":"ADD",
        "100010":"SUB",
        "001100":"syscall",
        "100110":"XOR",
        "011000":"MUL",
        "101010": "SLT",
    }

    global test_flag
    test_flag=1

    # data_memory={
    # # BEGIN: 9f3d8f3d
    # memory = {}
    # for i in range(2**32):
    #     memory[i] = i % 256
    # # END: 9f3d8f3d

    # }

    #control signals
    piped_instr={}
    global RegWrite 
    global MemRead 
    global MemWrite 
    global MemtoReg 
    global ALUSrc 
    global ALUControl
    global RegDst 
    global Branch 
    global Jump  
    global ALUOp  
    global PCSrc 
    global counter
    counter=0 
    memory_dict={
    "0x10010000" : 0x00000009,
    "0x10010004" : 0x0000000f,
    "0x10010008" : 0x00000006,
    "0x1001000c" : 0x00000005,
    "0x10010010" : 0x00000004,
    "0x10010014" : 0x00000003,
    "0x10010018" : 0x00000002,
    "0x1001001c" : 0x00000001,
    }

    class pipe_instructions:
        def __init__(self):
            self.done=[0,0,0,0,0]
            self.instr=None
        
            self.i=0

        

            
    class Processor:
        
        def __init__(self, machine_code):
            self.pipeline=[]
            self.machine_code = machine_code
            self.instructions = self.machine_code.splitlines()
            reg_dict={}
            for i in range(0, 30):
                key = f"{i:0>5b}" 
                reg_dict[key] = 0 
        
            self.registers = reg_dict
            hex_dict={}
            # print(self.registers)
            for i in range(1, 70000):
                key = f"0x{i:0>8x}" 
                hex_dict[key] = 0      
            self.data_memory = memory_dict
            self.clock_cycles = 0
            k=0x400000
            for i in range(15):
                    piped_instr[k]=self.machine_code[i]
                    k+=4
            
        

        def controlsignal(self,instruction_name):
        
            
            global id_ex_pipeline 
        
            if(instruction_name=="ADD"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=1
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=0



            elif(instruction_name=="SUB"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=1
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=0    

        
            elif(instruction_name=="MUL"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=1
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

            elif(instruction_name=="ADDI"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="00"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

            elif(instruction_name=="ADDIU"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="00"
                id_ex_pipeline["control_signals"]["PCSrc"]=0


            elif(instruction_name=="SUBI"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="00"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

            elif(instruction_name=="ORI"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

            elif(instruction_name=="LUI"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=0        

            elif(instruction_name=="LW"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=1
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=1
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="00"
                id_ex_pipeline["control_signals"]["PCSrc"]=0
            
            elif(instruction_name=="SW"):
                id_ex_pipeline["control_signals"]["RegWrite"]=0
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=1
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=1
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="00"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

        

            elif(instruction_name=="BEQ"):
                id_ex_pipeline["control_signals"]["RegWrite"]=0
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=1
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="01"
                id_ex_pipeline["control_signals"]["PCSrc"]=0
            
            elif(instruction_name=="BNE"):
                id_ex_pipeline["control_signals"]["RegWrite"]=0
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=1
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="01"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

            
            elif(instruction_name=="SLT"):
                id_ex_pipeline["control_signals"]["RegWrite"]=1
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=1
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=0
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=0

            elif(instruction_name=="J"):
                id_ex_pipeline["control_signals"]["RegWrite"]=0
                id_ex_pipeline["control_signals"]["MemRead"]=0
                id_ex_pipeline["control_signals"]["MemWrite"]=0
                id_ex_pipeline["control_signals"]["MemtoReg"]=0
                id_ex_pipeline["control_signals"]["ALUSrc"]=0
                id_ex_pipeline["control_signals"]["RegDst"]=0
                id_ex_pipeline["control_signals"]["Branch"]=0
                id_ex_pipeline["control_signals"]["Jump"]=1
                id_ex_pipeline["control_signals"]["ALUOp"]="10"
                id_ex_pipeline["control_signals"]["PCSrc"]=1
            
            


        def Alu_Control(self):
            global id_ex_pipeline
        
            if(id_ex_pipeline["control_signals"]["ALUOp"]=="00"):
                id_ex_pipeline["alu_constrols"]["ALUControl"]="0010"
            
            elif(id_ex_pipeline["control_signals"]["ALUOp"]=="01"):
                id_ex_pipeline["alu_constrols"]["ALUControl"]="0110"
            elif(id_ex_pipeline["control_signals"]["ALUOp"]=="10"):
                if(id_ex_pipeline["decoded_list"][0]=="J"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="1110"   
                elif(id_ex_pipeline["decoded_list"][5]=="100000"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0010"

                elif(id_ex_pipeline["decoded_list"][5]=="100010"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0110"

                elif(id_ex_pipeline["decoded_list"][5]=="100100"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0000"
                elif(id_ex_pipeline["decoded_list"][5]=="100101"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0001"
                elif(id_ex_pipeline["decoded_list"][5]=="000010"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0011"
                elif(id_ex_pipeline["decoded_list"][5]=="101010"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0111"
                elif(id_ex_pipeline["decoded_list"][0]=="ORI"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="0010"  
                elif(id_ex_pipeline["decoded_list"][0]=="LUI"):
                    id_ex_pipeline["alu_constrols"]["ALUControl"]="1111" 
                


            elif(id_ex_pipeline["control_signals"]["ALUOp"]=="11"):
                id_ex_pipeline["alu_constrols"]["ALUControl"]="0000"  
                                        


        def reinitialize(self):
            if self.pipeline and self.pipeline[-1].done[-1]:
                self.pipeline.pop()
        def add_inst(self,inst):
            self.reinitialize()
            if len(self.pipeline)<5:
                self.pipeline=[inst]+self.pipeline

        def pipeline_run(self):
            global pc
            global counter
            # print(piped_instr)
            
            while pc<len(self.instructions) or self.pipeline:

                self.reinitialize()
                instr=pipe_instructions()    
                for i in self.pipeline[::-1]:
                    self.run(i)
                if pc<len(self.instructions):
                    # print(pc)
                    # print(self.instructions)
                    self.add_inst(instr)
                    self.run(self.pipeline[0])

                    print('***********************************************',file=f)
                
                pc+=1
                counter=counter+1
                print(f"C CYCLE IS {counter}",file=f)

        def run(self,instr):
            global if_id_pipeline
            global id_ex_pipeline
            global ex_mem_pipeline
            global mem_wb_pipeline
            global count_if
            global count_id
            global count_ex
            global count_mem
            global count_wb
            global if_flag
            global id_flag
            global ex_flag
            global mem_flag
            global forwardA
            global result
            global counter
            global pc
        
            

        
            if(instr.i==0):
                print(pc,file=f)
                print("",file=f)
                print(f"if for instruction{count_if}",file=f)
            
                instruction = self.instructions[pc]
                
                count_if=count_if+1
                if_id_pipeline["instruction"]=instruction 
            elif(instr.i==1):
                
                decoded_list = self.decode(if_id_pipeline["instruction"])
                id_ex_pipeline["decoded_list"]=decoded_list.copy()
                self.controlsignal(decoded_list[0])
                self.Alu_Control()
                if(counter>3 and mem_wb_pipeline["decoded_list"][0]!="BEQ" and mem_wb_pipeline["decoded_list"][0]!="BNE"):

                    if(mem_wb_pipeline["decoded_list"][-1]==id_ex_pipeline["decoded_list"][-3] and mem_wb_pipeline["control_signals"]["MemRead"]):
                        id_ex_pipeline["decoded_list"][1]=mem_wb_pipeline["memory_data"]
                        # print("for1")
                        print("forwarding",file=f)
                        # print(mem_wb_pipeline["memory_data"])

                

                    elif(mem_wb_pipeline["decoded_list"][-1]==id_ex_pipeline["decoded_list"][-2] and  mem_wb_pipeline["control_signals"]["MemRead"]):
                        id_ex_pipeline["decoded_list"][2]=mem_wb_pipeline["memory_data"]
                        # print("for2")
                        print("forwarding",file=f)
                    

                    elif((mem_wb_pipeline["decoded_list"][-1]==id_ex_pipeline["decoded_list"][-2])):
                        # print("for3")
                        print("forwarding",file=f)
                        id_ex_pipeline["decoded_list"][2]=mem_wb_pipeline["result"]
                        
                    elif((mem_wb_pipeline["decoded_list"][-1]==id_ex_pipeline["decoded_list"][-3])):
                        # print("for4")
                        print("forwarding",file=f)
                        id_ex_pipeline["decoded_list"][1]=mem_wb_pipeline["result"]   
                if(counter>1 and ex_mem_pipeline["decoded_list"][0]!="BEQ" and ex_mem_pipeline["decoded_list"][0]!="BNE"):
                    
                    if(ex_mem_pipeline["decoded_list"][-1]==id_ex_pipeline["decoded_list"][-2]):
                        print("forwarding",file=f)
                        if(id_ex_pipeline["decoded_list"][0]=="BNE" or id_ex_pipeline["decoded_list"][0]=="BEQ"):
                            id_ex_pipeline["decoded_list"][1]=ex_mem_pipeline["result"]
                        else:    
                            id_ex_pipeline["decoded_list"][2]=ex_mem_pipeline["result"]
                        if(id_ex_pipeline["decoded_list"][0]=="ORI"):
                            id_ex_pipeline["decoded_list"][1]=ex_mem_pipeline["result"]
                        if(id_ex_pipeline["decoded_list"][0]=="LW"):
                            id_ex_pipeline["decoded_list"][1]=ex_mem_pipeline["result"] 
                        if(id_ex_pipeline["decoded_list"][0]=="SW"): 
                            id_ex_pipeline["decoded_list"][1]=ex_mem_pipeline["result"]   
                        


                    elif(ex_mem_pipeline["decoded_list"][-1]==id_ex_pipeline["decoded_list"][-3]):
                        print("forwarding",file=f)
                        id_ex_pipeline["decoded_list"][1]=ex_mem_pipeline["result"]                    
                    
            elif(instr.i==2):
                
                if(forwardA=="00"):
                    id_ex_pipeline["decoded_list"][2]=result 
                elif(forwardA=="10"):
                    id_ex_pipeline["decoded_list"][1]=result
                elif(forwardA=="111"):
                    pass 
                result = self.execute(id_ex_pipeline["decoded_list"])
            
                
                ex_mem_pipeline["result"]=result
                # print(f"result for the {count_ex-1} is {result}")
                ex_mem_pipeline["control_signals"]=id_ex_pipeline["control_signals"].copy()
                ex_mem_pipeline["alu_constrols"]=id_ex_pipeline["alu_constrols"].copy()
                ex_mem_pipeline["decoded_list"]=id_ex_pipeline["decoded_list"].copy() 
            elif(instr.i==3):
                
                memory_data = self.memory_access(result)
                
                mem_wb_pipeline["memory_data"]=memory_data
                mem_wb_pipeline["control_signals"]=ex_mem_pipeline["control_signals"].copy()
                mem_wb_pipeline["alu_constrols"]=ex_mem_pipeline["alu_constrols"].copy()
                mem_wb_pipeline["decoded_list"]=ex_mem_pipeline["decoded_list"].copy()
                mem_wb_pipeline["result"]=ex_mem_pipeline["result"]
            elif(instr.i==4):
                # print(self.data_memory)
            
                mem_data=self.write_back(mem_wb_pipeline["memory_data"])
                
                        
                
            instr.done[instr.i]=1
            instr.i+=1
                




        def find_reg_value(self,reg_number):
            return self.registers[reg_number]
        
        def decode(self, instruction):
            
        
            decoded_list.clear()
            # print(instruction)
            binary=bin(int(instruction, 16))[2:].zfill(32)
            opcode=binary[0:6]
            # print(opcode)
            for inst_type,op in enumerate(op_dict):
        
                if (op == opcode):
                    
                    
                    
                    if(inst_type<r_type):
                        if(func_dict[binary[26:32]]=="ADD"):
                            decoded_list.append("ADD")
                            
                            rs=binary[6:11]
                            rt=binary[11:16]
                            rd=binary[16:21]
                            shamt=binary[21:26]
                            funct=binary[26:32]
                            
                            decoded_list.append(self.find_reg_value(rs))
                            decoded_list.append(self.find_reg_value(rt))
                            decoded_list.append(self.find_reg_value(rd))

                            decoded_list.append(shamt)
                            decoded_list.append(funct)
                            decoded_list.append(rs)
                            decoded_list.append(rt)
                            decoded_list.append(rd)


                        elif(func_dict[binary[26:32]]=="SUB"):
                            decoded_list.append("SUB")
                            rs=binary[6:11]
                            rt=binary[11:16]
                            rd=binary[16:21]
                            shamt=binary[21:26]
                            funct=binary[26:32]
                            
                            decoded_list.append(self.find_reg_value(rs))
                            decoded_list.append(self.find_reg_value(rt))
                            decoded_list.append(self.find_reg_value(rd))

                            decoded_list.append(shamt)
                            decoded_list.append(funct)
                            decoded_list.append(rs)
                            decoded_list.append(rt)
                            decoded_list.append(rd)


                        elif(func_dict[binary[26:32]]=="SLT"):
                            decoded_list.append("SLT")
                            rs=binary[6:11]
                            rt=binary[11:16]
                            rd=binary[16:21]
                            shamt=binary[21:26]
                            funct=binary[26:32]
                            
                            decoded_list.append(self.find_reg_value(rs))
                            decoded_list.append(self.find_reg_value(rt))
                            decoded_list.append(self.find_reg_value(rd))

                            decoded_list.append(shamt)
                            decoded_list.append(funct)
                            decoded_list.append(rs)
                            decoded_list.append(rt)
                            decoded_list.append(rd)   
                            # print(self.registers) 

                        


                    elif(inst_type<mul_value):
                        decoded_list.append(op_dict[op])
                        rs=binary[6:11]
                        rt=binary[11:16]
                        rd=binary[16:21]
                        shamt=binary[21:26]
                        funct=binary[26:32]
                        
                        decoded_list.append(self.find_reg_value(rs))
                        decoded_list.append(self.find_reg_value(rt))
                        decoded_list.append(self.find_reg_value(rd))

                        decoded_list.append(shamt)
                        decoded_list.append(funct)
                        decoded_list.append(rs)
                        decoded_list.append(rt)
                        decoded_list.append(rd)
                        
                    elif(inst_type<i_type):
                        decoded_list.append(op_dict[op])
                        rs=binary[6:11]
                        rt=binary[11:16]
                        imm=binary[16:32]


                        decoded_list.append(self.find_reg_value(rs))
                        decoded_list.append(self.find_reg_value(rt))
                        decoded_list.append(imm)
                        decoded_list.append(rs)
                        decoded_list.append(rt)
                    
                    elif(inst_type<j_type):
                        decoded_list.append(op_dict[op])
                        addr=binary[6:32]
                        decoded_list.append(addr)
            print("",file=f)

            print(f"ID FOR INSTRUCTION ({decoded_list})",file=f)
            
            print("",file=f)      
            return decoded_list            

        def execute(self, decoded_list):
            
            global id_ex_pipeline
            global pc
            
            print(f"EX FOR INSTRUCTION ({id_ex_pipeline['decoded_list']})",file=f)  
            print("",file=f)
        
            if(id_ex_pipeline["alu_constrols"]["ALUControl"]=="0010"):
                if(id_ex_pipeline["control_signals"]["ALUSrc"]==0):
                    result=int(id_ex_pipeline["decoded_list"][1])+int(id_ex_pipeline["decoded_list"][2])
                else:
                    result=int(id_ex_pipeline["decoded_list"][1])+int(id_ex_pipeline["decoded_list"][3],2) 

                    
                
            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="0110"):
                
                if(id_ex_pipeline["control_signals"]["ALUSrc"]==0):
                    result=int(id_ex_pipeline["decoded_list"][1])-int(id_ex_pipeline["decoded_list"][2])
                else:
                    result=int(id_ex_pipeline["decoded_list"][2])-int(id_ex_pipeline["decoded_list"][3])

                if(id_ex_pipeline["decoded_list"][0]=="BNE" and id_ex_pipeline["control_signals"]["Branch"]==1 and result!=0):
                    
                    # # self.pipeline.pop(0)
                    # # print(pc)
                    # pc= pc-int(''.join(['1' if bit == '0' else '0' for bit in id_ex_pipeline["decoded_list"][3]]),2)-1
                    # # print(pc)  
                    self.pipeline.pop(0)  # self.pipeline.pop(0)
                    if(int( id_ex_pipeline["decoded_list"][3],2)>300):
                        # print("hello")
                        pc= pc-int(''.join(['1' if bit == '0' else '0' for bit in id_ex_pipeline["decoded_list"][3]]),2)-1-1
                    else:
                        pc= pc+int(id_ex_pipeline["decoded_list"][3],2)
                        # print(id_ex_pipeline["decoded_list"][3])

                if(id_ex_pipeline["decoded_list"][0]=="BEQ" and id_ex_pipeline["control_signals"]["Branch"]==1 and result==0 ):
                    # print(id_ex_pipeline["decoded_list"][3])
                
                    self.pipeline.pop(0)
                    if(int( id_ex_pipeline["decoded_list"][3],2)>300):
                        # print("hello")
                        pc= pc-int(''.join(['1' if bit == '0' else '0' for bit in id_ex_pipeline["decoded_list"][3]]),2)-1-1
                    else:
                        pc= pc+int(id_ex_pipeline["decoded_list"][3],2)
                        # print(id_ex_pipeline["decoded_list"][3])

                            
                    # print(pc)

                
                    


            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="0000"):
            
                
                result=id_ex_pipeline["decoded_list"][1] & id_ex_pipeline["decoded_list"][2]

            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="0001"):
                result=id_ex_pipeline["decoded_list"][1] | id_ex_pipeline["decoded_list"][2]

            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="0011"):
                result=id_ex_pipeline["decoded_list"][1] * id_ex_pipeline["decoded_list"][2]   

            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="0111"):
                if(id_ex_pipeline["decoded_list"][1]<id_ex_pipeline["decoded_list"][2]):
                    result=1
                else:
                    result=0 
            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="1110"):
                # print(pc)
                # print(int("0000"+id_ex_pipeline["decoded_list"][1]+"00",2))
                    
                    
                ans=((pc-1)*4+4194304-int("0000"+id_ex_pipeline["decoded_list"][1]+"00",2))//4
                pc=pc-ans-2
                # print(pc)
                return 1
            elif(id_ex_pipeline["alu_constrols"]["ALUControl"]=="1111"):
                result=int(id_ex_pipeline["decoded_list"][3],2)<<16     
            # print(f"EX RESULT FOR {id_ex_pipeline['decoded_list']} is {result}")    
            return result    

        def memory_access(self, data):
            global pc

            print(f"MEM FOR INSTRUCTION ({ex_mem_pipeline['decoded_list']})",file=f)  
            # print(ex_mem_pipeline["control_signals"])    
            
            if  ex_mem_pipeline["control_signals"]["MemRead"]:
            
                # print(f'"MEM  is {self.data_memory[f"0x{data:0>8x}"]} FOR {ex_mem_pipeline["decoded_list"]}"')
                return self.data_memory[f"0x{data:0>8x}"]
                print("done")
            elif ex_mem_pipeline["control_signals"]["MemWrite"]:
                if(f"0x{int(str(data)):0>8x}"=="0x00000000"):
                    sys.exit()
            
                self.data_memory[f"0x{int(str(data)):0>8x}"] = self.registers[ex_mem_pipeline["decoded_list"][-1]]
            
            
            return data

            # assuming the data is an index
        

        def write_back(self, result):
                print('***********************************************',file=f)
                # Write result back to register if RegWrite signal is set
                print(f"WB FOR INSTRUCTION ({mem_wb_pipeline['decoded_list']})",file=f)
                # print(mem_wb_pipeline["result"])

                if mem_wb_pipeline["control_signals"]["RegWrite"]:
                    if(decoded_list[-1]=="10010"):
                        # print("here")
                        pass
                
                    if mem_wb_pipeline["control_signals"]["MemtoReg"]:
                        self.registers[mem_wb_pipeline["decoded_list"][-1]] = mem_wb_pipeline["memory_data"]
                    else:
                        self.registers[mem_wb_pipeline["decoded_list"][-1]] = mem_wb_pipeline["memory_data"]
                        
                # print(f"last value of pc {pc}")     
                # print(self.registers)       

                        


                
    
        
        
        
    print("TYPE 1 FOR FACTORIAL(9)")
    print("TYPE 0 FOR SORTING(9,15,6,5,4,3,2,1)")
    K=int(input())

    if(K==1):
        code="""20080009
    20090001
    200a0001
    71284802
    20010001
    01014022
    150afffc"""
    else:
        code="""3c011001
    34290000
    23180007
    23390000
    21ad0000
    20010001
    02a1a822
    11b80011
    030d6022
    200e0000
    212b0000
    21ad0001
    10000000
    11ccfff9
    8d710000
    216b0004
    8d720000
    21ce0001
    0232082a
    1420fff9
    ad710000
    20010004
    0161c822
    af320000
    1000fff4
    200c0000"""



    if __name__ == '__main__':
     
        machine_code =code
        # 0x34290000,0x23180007,0x23390000,0x21ad0000,0x22b5ffff,0x11b8000f,0x030d6022,0x200e0000,0x212b0000,0x21ad0001,0x0810000c,0x11ccfff9,0x8d710000,0x216b0004,0x8d720000,0x21ce0001,0x0232082a,0x1420fff9,0xad710000,0xad72fffc,0x0810000c,0x200c0000
        processor = Processor(machine_code)
        if(K==0):
            print("Initial Memory-->")
            print()
            print(print(processor.data_memory))
            print()
        processor.pipeline_run()
        # print(processor.registers)
        if(K==1):
            print("Factorial of 9-->")
            print(processor.registers["01001"])
        else:
            print("Final Memory is--> ")
            print()
            print(processor.data_memory)

    # print(processor.registers["01001"])



