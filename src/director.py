from src.random_interface import RandomInterface

class Director:

    def __init__(self):

        self.randomInterface = RandomInterface()

        

    def run(self):

        min = input("Enter the minimum number: ")
        max = input("Enter the maximum number: ")

        control = ""

        print("Press enter to get a new number. Press q then enter to quit.")
        while control != "q":

            print("New random: " + str(self.randomInterface.rand_int(min, max)))
            control = input("")

        
