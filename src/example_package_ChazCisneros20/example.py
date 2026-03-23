import requests
import json
#Ask professor how to build in requests into the python pip package. 

class example:
    @staticmethod
    def add_one(number):
        return number + 1

    @staticmethod
    def capstone():
        print("Hello World\n")
        print("This is the start of my Senior Capstone project !\n")

    @staticmethod
    def get_request(url):
        response = requests.get(url=url)
        print(response)



        

