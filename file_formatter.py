
class Formatter:

    def __init__(self, file):
        self.labels = []
        self.instructions = []
        self.references = []
        for line in file:
            line_length = len(line.split(" "))
            line_splitted = line.split(" ")
            if line_length == 1:
                self.instructions.append(line_splitted[0])
                self.labels.append("#")
                self.references.append("#")
            elif line_length == 2:
                self.instructions.append(line_splitted[0])
                self.references.append(line_splitted[1])
                self.labels.append("#")
            elif line_length == 3:
                self.labels.append(line_splitted[0])
                self.instructions.append(line_splitted[1])
                self.references.append(line_splitted[2])

        # Remove undesired spaces
        clean_instructions = []
        for i in self.instructions:
            if "\n" in i:
                clean_instructions.append(i.split("\n")[0])
            else:
                clean_instructions.append(i)
        # Index 0 is with empty value so, I removed it
        self.instructions = clean_instructions[1:]
        # The last index in labels is empty value so, i sliced it
        self.labels = self.labels[1:len(self.labels)-1]
        self.labels.append("#")
        # remove new lines from references
        self.references = self.remove_new_lines(self.references)
        # Index 0 is with empty value so, I removed it
        self.references = self.references[1:]

    def remove_new_lines(self, column):
        for ref in range(len(column)):
            column[ref] = column[ref].split("\n")[0]
        return column

    def get_labels(self):
        return self.labels

    def get_instructions(self):
        return self.instructions

    def get_references(self):
        return self.references

    def get_labels_length(self):
        return len(self.labels)

    def get_instructions_length(self):
        return len(self.instructions)

    def get_references_length(self):
        return len(self.references)

    def print_formatted_file(self):
        for i in range(self.get_instructions_length()):
            print(self.labels[i], " ", self.instructions[i],
                  " ", self.references[i])
