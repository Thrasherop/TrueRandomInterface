import requests
import json
from datetime import datetime

import colorama
from colorama import Fore, Back, Style

from keys.api_key import api_key
from configs import config

from errors.errors import *

class RandomInterface:


    def __init__(self) -> None:


        if config.do_entropy_analysis:


            # Validates the randomness of random.org
            if not self.validate_randomness():
                raise EntropyError("Randomness is invalid! Verify the sample size is large enough")

        else:

            print(f"\n\n{Fore.RED} WARNING: ENTROPY CHECK IS NOT ACTIVATED{Style.RESET_ALL}\n\n")




    def rand_int(self, min, max) -> int:


        # Sets up the parameters for the request
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": api_key,
                "n": 1,
                "min": min,
                "max": max,
                "replacement": True
            },
            'id':1
        }


        # Sets up and sends the request
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url='https://api.random.org/json-rpc/2/invoke',
            data=data,
            headers=headers
            )
        

        # Gets the dictionary from the response
        response_dict = json.loads(response.text)

        # Verifies that there wasn't an error
        if 'error' in response_dict:
            raise APICallFailed("Fetch failed: " + response.text)

       # Gets the random number from the response
        number_list = response_dict['result']['random']['data']

        return number_list[0]

        

    def validate_randomness(self) -> bool:

        """
        Validates the randomness of random.org
        """
        

        # Sets up the parameters for the request
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": api_key,
                "n": config.validation_sample_size,
                "min": 1,
                "max": 6,
                "replacement": True
            },
            'id':1
        }


        # Sets up and sends the request
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url='https://api.random.org/json-rpc/2/invoke',
            data=data,
            headers=headers
            )


        # Gets the dictionary from the response
        response_dict = json.loads(response.text)


        # Verifies that there wasn't an error
        if 'error' in response_dict:
            raise APICallFailed("My request failed: " + response.text)


        # Gets the random numbers from the response
        number_list = response_dict['result']['random']['data']


        # Create a dictionary of the numbers and their frequency
        number_dict = {}
        for number in number_list:
            if number in number_dict:
                number_dict[number] += 1
            else:
                number_dict[number] = 1


        # Calculate the probability of each number
        probability_dict = {}
        for number in number_dict:
            probability_dict[number] = number_dict[number] / len(number_list)


        # Save the list to a file named the current time
        filename = 'random_outputs/validations/last_validation.txt'
        filename = filename.replace(' ', '')
        with open(filename, 'w+') as f:

            # Writes the probability and number of frequencies to the file head
            f.write('\nNumber Frequencies' + str(number_dict))
            f.write('\nProbabilities' + str(probability_dict))

            # Writes the random numbers to the file
            for number in number_list:
                f.write(str(number) + '\n')

            


        # Calculate the chi-squared value
        chi_squared = 0
        for number in number_dict:
            chi_squared += ((probability_dict[number] - (1/6)) ** 2) / (1/6)




        # If the chi-squared value is less than 0.05, the randomness is valid
        if chi_squared < 0.05:
            return True
        else:
            return False

