from file_formatter import Formatter


class Pass_one:

    def __init__(self, formatted_file):
        self.labels = formatted_file.get_labels()
        self.instructions = formatted_file.get_instructions()
        self.references = formatted_file.get_references()
        self.location_counter = []
        self.calculate_location_counter()
        self.program_length = self.get_program_length()
        self.referenced_labels = self.labels_references()
        self.constants = self.get_constants_reference()
        self.symbol_table = self.create_symbol_table()

    def get_location_counters(self):
        return self.location_counter

    def get_constants_reference(self):
        row_record = {}
        for i in range(len(self.instructions)):
            if self.instructions[i] == "*":
                row_record["reference"] = self.references[i]
                row_record["location_counter"] = self.location_counter[i]
        return row_record

    def labels_references(self):
        labels_referenced = []
        label_reference = {}
        labels_recorded = []
        special_instructions = ['RESW', 'RESB', 'WORD', 'BYTE']
        for i in range(len(self.references)-1):
            for j in range(len(self.labels)-1):
                if self.references[i] == self.labels[j] and self.instructions[j] not in special_instructions and self.labels[j] != "#" and self.labels[j] not in labels_recorded:

                    # print(self.location_counter[j], " ",
                    # self.labels[j], " ", self.instructions[j], " ", self.references[i])
                    labels_recorded.append(self.labels[j])
                    label_reference["label"] = self.labels[j]
                    # print(self.location_counter[i],
                    # " and ", self.location_counter[j])
                    label_reference["location_counter"] = self.location_counter[j]
                    labels_referenced.append(label_reference)
                    label_reference = {}
        return labels_referenced

    def calculate_location_counter(self):
        special_instructions = ['RESW', 'RESB', 'WORD', 'BYTE']
        opcode_formate_two = ["ADDR", "CLEAR", "COMPR", "DIVR",
                              "MULR", "RMO", "SHIFTL", "SHIFTR", "SUBR", "SVC", "TIXR"]
        for i in range(len(self.instructions)):
            if i == 0 or i == 1:
                self.location_counter.append(hex(int(self.references[0], 16)))
                continue

            elif self.instructions[i-1] in opcode_formate_two:
                num = int(self.location_counter[i-1], 16)
                res = num + 2
                self.location_counter.append(hex(res))

            elif self.instructions[i-1] == 'BASE' or self.instructions[i-1] == 'LTORG':
                self.location_counter.append(self.location_counter[i-1])

            elif '+' in self.instructions[i-1]:
                num = int(self.location_counter[i-1], 16)
                res = num + 4
                self.location_counter.append(hex(res))

            elif self.instructions[i-1] == "*":
                chars = self.references[i-1][3:len(self.references[i-1])-1]
                prev_location_counter = int(self.location_counter[i-1], 16)
                self.location_counter.append(
                    hex(prev_location_counter + len(chars)))

            elif self.instructions[i-1] in special_instructions:
                if self.instructions[i-1] == "BYTE":
                    if self.references[i-1][0] == 'C':
                        chars = self.references[i -
                                                1][2:len(self.references[i-1])-1]
                        prev_loc_count = int(self.location_counter[i-1], 16)
                        self.location_counter.append(
                            hex(prev_loc_count + len(chars)))
                    else:
                        chars = self.references[i -
                                                1][2:len(self.references[i-1])-1]
                        prev_loc_count = int(self.location_counter[i-1], 16)
                        prev_loc_count = int(self.location_counter[i-1], 16)
                        self.location_counter.append(
                            hex(prev_loc_count + int(len(chars)/2)))

                elif self.instructions[i-1] == "RESW":
                    ref_value = int(self.references[i-1]) * 3
                    prev_loc_count = int(self.location_counter[i-1], 16)
                    self.location_counter.append(
                        hex(ref_value + prev_loc_count))
                elif self.instructions[i-1] == "RESB":
                    prev_loc_count = int(self.location_counter[i-1], 16)
                    self.location_counter.append(
                        hex(prev_loc_count + int(self.references[i-1])))

            else:
                self.location_counter.append(
                    hex(int(self.location_counter[i-1], 16)+3))

    def create_symbol_table(self):
        symbol_table = []
        symbol_record = {}
        special_instructions = ['RESW', 'RESB', 'WORD', 'BYTE']
        for i in range(len(self.instructions)):
            if self.instructions[i] in special_instructions:
                symbol_record[self.labels[i]] = self.location_counter[i]
                symbol_table.append(symbol_record)
                symbol_record = {}

        for i in range(len(self.referenced_labels)):
            symbol_record[self.referenced_labels[i]["label"]
                          ] = self.referenced_labels[i]["location_counter"]
            symbol_table.append(symbol_record)
            symbol_record = {}
        symbol_record[self.constants["reference"]
                      ] = self.constants["location_counter"]
        symbol_table.append(symbol_record)

        return symbol_table

    def print_symbol_table(self):
        print("\nSymbol Table")
        print("============")
        for row in self.symbol_table:
            for key in row:
                print(key, " : ", row[key])

    def get_program_length(self):
        return hex(int(self.location_counter[len(self.location_counter)-1], 16) - int(self.location_counter[0], 16))

    def print_pass_one(self):
        print("\nPass One")
        print("=========")
        for i in range(len(self.instructions)):
            print(self.location_counter[i], " ", self.labels[i],
                  " ", self.instructions[i], " ", self.references[i])

        print("\nprogram Length")
        print("===============")
        print("Program Length: ", self.get_program_length())
        self.print_symbol_table()

    def get_pass_one_data(self):
        return self.location_counter, self.labels, self.instructions, self.references, self.symbol_table, self.get_program_length()


if __name__ == "__main__":
    file = open("inSICXE.txt", "r")

    formatted_file = Formatter(file)
    pass_one_output = Pass_one(formatted_file)
