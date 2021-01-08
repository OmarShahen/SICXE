from file_formatter import Formatter
from pass_one import Pass_one
from pass_two import Pass_two
import os

file = open("inSICXE.txt", "r")

formatted_file = Formatter(file)
pass_one_output = Pass_one(formatted_file)
pass_two_output = Pass_two(pass_one_output.get_pass_one_data())


if __name__ == "__main__":
    while(True):
        print("1. Pass One")
        print("2. Pass Two All Data")
        print("3. All Object Codes")
        print("4. HTE Record")
        print("5. Clear Screen")
        opt = int(input("Enter The Option Number: "))
        if opt == 1:
            pass_one_output.print_pass_one()
        elif opt == 2:
            pass_two_output.print_pass_2_data()
        elif opt == 3:
            pass_two_output.print_object_codes()
        elif opt == 4:
            pass_two_output.print_HTE_record()
        elif opt == 5:
            os.system("cls")

        else:
            print("Good Bye")
            exit()
