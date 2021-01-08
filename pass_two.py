from pass_one import Pass_one
from file_formatter import Formatter
import os


class Pass_two:
    def __init__(self, obj):
        self.location_counter = obj[0]
        self.labels = obj[1]
        self.instructions = obj[2]
        self.references = obj[3]
        self.symbol_table = obj[4]
        self.program_length = obj[5]
        self.opcodes_info = self.get_opcodes()
        self.object_codes = self.format_classifier()
        self.HTE_record = self.create_HTE_record()

    def zero_filler(self, desired_length, value):
        if "0x" in value:
            value = value[2:]
        zero_count = desired_length - len(value)
        for i in range(zero_count):
            value = "0" + value
        return value

    def print_HTE_record(self):
        print(self.HTE_record["H"])
        print(self.HTE_record["T"])
        for i in self.HTE_record["M"]:
            print(i)
        print(self.HTE_record["E"])

    def print_object_codes(self):
        for row_data in self.object_codes:
            print(row_data["object_code"])

    def print_pass_2_data(self):
        for row_data in self.object_codes:
            if row_data["formate"] == 3 or row_data["formate"] == 4:
                print("===========================")
                print("Instruction: ", row_data["instruction"], "\n", "Reference: ", row_data["reference"], "\n", "OPCODE: ", row_data["opcode"], "\n",
                      "Formate: ", row_data["formate"], "\n", "Binary OPCODE: ", row_data[
                          "binary_opcode"], "\n", "N:", row_data["n"], "\n", "I: ", row_data["i"], "\n"
                      "X: ", row_data["x"], "\n", "B: ", row_data["b"],  "\n", "P: ", row_data[
                          "p"], "\n", "E: ", row_data["e"], "\n", "Displacment/Address: ", row_data["disp_address"], "\n",
                      "Object Code: ", row_data["object_code"])
                print("===========================")

            if row_data["formate"] == 2:
                print("===========================")
                print("Instruction: ", row_data["instruction"], "\n", "Reference", row_data["reference"], "\n", "OPCODE", row_data["opcode"], "\n",
                      "Formate: ", row_data["formate"], "\n", "Register1: ", row_data["Register1"], "\n", "Register2: ", row_data["Register2"], "\n", "Object Code: ", row_data["object_code"])
                print("===========================")

    def create_HTE_record(self):
        HTE_record = {}

        HTE_record["H"] = "H ^ " + self.labels[0] + " ^ " + \
            self.zero_filler(
                6, self.references[0]) + " ^ " + self.zero_filler(6, self.program_length)

        HTE_record["T"] = "T ^ " + \
            self.zero_filler(
                6, self.references[0])
        for row_data in self.object_codes:
            HTE_record["T"] += " ^ " + \
                self.zero_filler(6, row_data["object_code"])
        HTE_record["E"] = "E ^ " + self.zero_filler(6, self.references[0])
        HTE_record["M"] = self.get_modification_record()
        return HTE_record

    def get_modification_record(self):
        modification_record_data = []
        mod_record = "M ^ "
        for i in range(len(self.object_codes)):
            if self.object_codes[i]["formate"] == 4 and "#" not in self.object_codes[i]["reference"]:
                row_data = self.object_codes[i]
                mod_record += self.zero_filler(6, hex(int(row_data["location_counter"],
                                                          16) + 1)) + " ^ 05 ^ " + " + " + self.labels[0]
                modification_record_data.append(mod_record)
                mod_record = "M ^ "
        return modification_record_data

    def search_reference(self, reference, location_counter):
        for i in self.symbol_table:
            for key in i:
                if "#" in reference or "@" in reference:
                    reference = reference[1:]
                if reference == key:
                    return i[key]
        return location_counter

    def format_classifier(self):
        all_object_codes = []
        obj_code_config_table = []
        base = self.search_base()
        for i in range(1, len(self.instructions)-1):
            for j in range(0, len(self.opcodes_info)):
                if "+" in self.instructions[i] and self.instructions[i][1:] == self.opcodes_info[j][0] and self.opcodes_info[j][1] == "3,4":
                    row_data = self.formate_4(
                        self.instructions[i], self.references[i], self.opcodes_info[j][2],
                        self.search_reference(self.references[i], self.location_counter[i]), self.location_counter[i+1], base, self.location_counter[i])
                    all_object_codes.append(row_data)
                    break
                elif self.instructions[i] == "BASE":
                    break
                elif self.instructions[i] == self.opcodes_info[j][0] and self.opcodes_info[j][1] == "3,4":
                    row_data = self.formate_3(
                        self.instructions[i], self.references[i], self.opcodes_info[j][2], self.search_reference(
                            self.references[i], self.location_counter[i]),
                        self.location_counter[i+1], base)
                    all_object_codes.append(row_data)
                    break
                elif self.instructions[i] == self.opcodes_info[j][0] and self.opcodes_info[j][1] == "2":

                    row_data = self.formate_2(self.instructions[i], self.references[i],
                                              self.opcodes_info[j][2], self.location_counter[i])
                    all_object_codes.append(row_data)
                    break
                elif self.instructions[i] == self.opcodes_info[j][0] and self.opcodes_info[j][1] == "1":
                    special_indexs.append(i)
                    break
        return all_object_codes

    def formate_4(self, instruction, reference, opcode, target_address, program_counter, base, location_counter):
        row_data = {
            "location_counter": location_counter,
            "instruction": instruction,
            "reference": reference,
            "opcode": opcode,
            "formate": 4,
            "b": "0",
            "p": "0",
            "e": "1"
        }

        binary_opcode1 = self.opcode_in_4_bits(bin(int(opcode[0], 16))[2:])
        binary_opcode2 = self.opcode_in_2_bits(bin(int(opcode[1], 16))[2:])
        row_data["binary_opcode"] = binary_opcode1 + binary_opcode2
        n_i = self.check_n_and_i(reference)
        row_data["n"] = n_i[0]
        row_data["i"] = n_i[1]
        if ",X" in reference:
            row_data["x"] = "1"
        else:
            row_data["x"] = "0"
        target_address = target_address[2:]
        target_address_difference = 5 - len(target_address)
        for i in range(target_address_difference):
            target_address = "0" + target_address

        all_bits = row_data["binary_opcode"] + row_data["n"] + row_data["i"] + \
            row_data["x"] + row_data["b"] + row_data["p"] + row_data["e"]

        row_data["disp_address"] = target_address
        row_data["object_code"] = self.calculate_object_code(
            all_bits, target_address)
        return row_data

    def formate_3(self, instruction, reference, opcode, target_address, program_counter, base):
        row_data = {
            "instruction": instruction,
            "reference": reference,
            "opcode": opcode,
            "formate": 3,
            "e": "0"
        }
        binary_opcode1 = self.opcode_in_4_bits(bin(int(opcode[0], 16))[2:])
        binary_opcode2 = self.opcode_in_2_bits(bin(int(opcode[1], 16))[2:])
        row_data["binary_opcode"] = binary_opcode1 + binary_opcode2

        n_i = self.check_n_and_i(reference)
        row_data["n"] = n_i[0]
        row_data["i"] = n_i[1]
        if ",X" in reference:
            row_data["x"] = "1"
        else:
            row_data["x"] = "0"

        if row_data["i"] == "1" and row_data["n"] == "0":
            returned_value = self.immediate_value(reference)
            if returned_value != False:
                row_data["b"] = "0"
                row_data["p"] = "0"
                returned_value = returned_value[2:]
                diff = 3 - len(returned_value)
                for i in range(diff):
                    returned_value = "0" + returned_value
                row_data["disp_address"] = returned_value
                all_bits = row_data["binary_opcode"] + row_data["n"] + row_data["i"] + \
                    row_data["x"] + row_data["b"] + \
                    row_data["p"] + row_data["e"]

                row_data["object_code"] = self.calculate_object_code(
                    all_bits, row_data["disp_address"])
                # print(row_data)
                return row_data

        disp = int(target_address, 16) - int(program_counter, 16)
        if disp >= -2048 and disp <= 2047:
            row_data["b"] = "0"
            row_data["p"] = "1"
            disp = hex(disp)
            if "-" in disp:
                disp = disp[1:]
                complement_2s = hex(int("FFFFFFFF", 16) - int(disp, 16))
                row_data["disp_address"] = complement_2s[-3:]
            else:
                disp = disp[2:]
                disp_length = len(disp)
                if disp_length == 1:
                    row_data["disp_address"] = "00" + disp
                elif disp_length == 2:
                    row_data["disp_address"] = "0" + disp
                else:
                    row_data["disp_address"] = disp
        else:
            row_data["b"] = "1"
            row_data["p"] = "0"
            disp = hex(int(target_address, 16) - int(base, 16))
            if "-" in disp:
                disp = disp[1:]
                complement_2s = hex(int("FFFFFFFF", 16) - int(disp, 16))
                row_data["disp_address"] = complement_2s[-3:]
            else:
                disp = disp[2:]
                disp_length = len(disp)
                if disp_length == 1:
                    row_data["disp_address"] = "00" + disp
                elif disp_length == 2:
                    row_data["disp_address"] = "0" + disp
                else:
                    row_data["disp_address"] = disp

        all_bits = row_data["binary_opcode"] + row_data["n"] + row_data["i"] + \
            row_data["x"] + row_data["b"] + row_data["p"] + row_data["e"]

        row_data["object_code"] = self.calculate_object_code(
            all_bits, row_data["disp_address"])
        # print(row_data)
        return row_data

    def search_base(self):
        for i in range(len(self.instructions)):
            if "BASE" == self.instructions[i]:
                return self.search_reference(self.references[i], self.location_counter[i])

    def formate_2(self, instruction, reference, opcode, location_counter):
        row_data = {
            "location_counter": location_counter,
            "instruction": instruction,
            "reference": reference,
            "opcode": opcode,
            "formate": 2,
        }
        registers = {
            "A": "0",
            "X": "1",
            "b": "4",
            "B": "4",
            "s": "5",
            "S": "5",
            "t": "6",
            "T": "6",
            "f": "7",
            "F": "7"
        }
        if "," in reference:
            reference1 = reference.split(",")[0]
            reference2 = reference.split(",")[1]
            row_data["Register1"] = registers[reference1]
            row_data["Register2"] = registers[reference2]
        else:
            row_data["Register1"] = registers[reference]
            row_data["Register2"] = "0"
        row_data["object_code"] = row_data["opcode"] + \
            row_data["Register1"] + row_data["Register2"]

        return row_data

    def opcode_in_4_bits(self, bin_num):
        length = len(bin_num)
        if length == 3:
            return "0" + bin_num
        elif length == 2:
            return "00" + bin_num
        elif length == 1:
            return "000" + bin_num
        else:
            return bin_num

    def opcode_in_2_bits(self, bin_num):
        return self.opcode_in_4_bits(bin_num)[:2]

    def check_n_and_i(self, reference):
        if "#" in reference:
            return "0", "1"
        elif "@" in reference:
            return "1", "0"
        else:
            return "1", "1"

    def calculate_object_code(self, bits, hexa):
        return hex(int(bits[:4], 2))[2:] + hex(int(bits[4:8], 2))[2:] + hex(int(bits[8:len(bits)], 2))[2:] + hexa

    def get_opcodes(self):
        OPTAB = []
        OPTAB.append(["FIX", "1", "C4"])
        OPTAB.append(["FLOAT", "1", "C0"])
        OPTAB.append(["HIO", "1", "F4"])
        OPTAB.append(["NORM", "1", "C8"])
        OPTAB.append(["SIO", "1", "F0"])
        OPTAB.append(["TIO", "1", "F8"])
        OPTAB.append(["ADDR", "2", "90"])
        OPTAB.append(["CLEAR", "2", "B4"])
        OPTAB.append(["COMPR", "2", "A0"])
        OPTAB.append(["DIVR", "2", "9C"])
        OPTAB.append(["MULR", "2", "98"])
        OPTAB.append(["RMO", "2", "AC"])
        OPTAB.append(["SHIFTL", "2", "A4"])
        OPTAB.append(["SHIFTR", "2", "A8"])
        OPTAB.append(["SUBR", "2", "94"])
        OPTAB.append(["SVC", "2", "B0"])
        OPTAB.append(["TIXR", "2", "B8"])
        OPTAB.append(["ADD", "3,4", "18"])
        OPTAB.append(["ADDF", "3,4", "58"])
        OPTAB.append(["AND", "3,4", "40"])
        OPTAB.append(["COMP", "3,4", "28"])
        OPTAB.append(["COMPF", "3,4", "88"])
        OPTAB.append(["DIV", "3,4", "24"])
        OPTAB.append(["DIVF", "3,4", "64"])
        OPTAB.append(["J", "3,4", "3C"])
        OPTAB.append(["JEQ", "3,4", "30"])
        OPTAB.append(["JGT", "3,4", "34"])
        OPTAB.append(["JLT", "3,4", "38"])
        OPTAB.append(["JSUB", "3,4", "48"])
        OPTAB.append(["LDA", "3,4", "00"])
        OPTAB.append(["LDB", "3,4", "68"])
        OPTAB.append(["LDCH", "3,4", "50"])
        OPTAB.append(["LDF", "3,4", "70"])
        OPTAB.append(["LDL", "3,4", "08"])
        OPTAB.append(["LDS", "3,4", "6C"])
        OPTAB.append(["LDT", "3,4", "74"])
        OPTAB.append(["LDX", "3,4", "04"])
        OPTAB.append(["LPS", "3,4", "D0"])
        OPTAB.append(["MUL", "3,4", "20"])
        OPTAB.append(["MULF", "3,4", "60"])
        OPTAB.append(["OR", "3,4", "44"])
        OPTAB.append(["RD", "3,4", "D8"])
        OPTAB.append(["RSUB", "3,4", "4C"])
        OPTAB.append(["SSK", "3,4", "EC"])
        OPTAB.append(["STA", "3,4", "0C"])
        OPTAB.append(["STB", "3,4", "78"])
        OPTAB.append(["STCH", "3,4", "54"])
        OPTAB.append(["STF", "3,4", "80"])
        OPTAB.append(["STI", "3,4", "D4"])
        OPTAB.append(["STL", "3,4", "14"])
        OPTAB.append(["STS", "3,4", "7C"])
        OPTAB.append(["STSW", "3,4", "E8"])
        OPTAB.append(["STT", "3,4", "84"])
        OPTAB.append(["STX", "3,4", "10"])
        OPTAB.append(["SUB", "3,4", "1C"])
        OPTAB.append(["SUBF", "3,4", "5C"])
        OPTAB.append(["TD", "3,4", "E0"])
        OPTAB.append(["TIX", "3,4", "2C"])
        OPTAB.append(["WD", "3,4", "DC"])
        return OPTAB

    def immediate_value(self, reference):
        try:
            return hex(int(reference[1:]))
        except ValueError:
            return False


if __name__ == "__main__":
    file = open("inSICXE.txt", "r")

    formatted_file = Formatter(file)
    pass_one_output = Pass_one(formatted_file)
    pass_two_output = Pass_two(pass_one_output.get_pass_one_data())
