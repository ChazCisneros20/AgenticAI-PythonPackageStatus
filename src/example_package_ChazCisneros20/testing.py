from example_package_ChazCisneros20 import example

#Test of print.
#ADDED: different for now.
example.capstone()


import requests 
import json
URL = ""
response = requests.get(url=URL)

if response.status_code == 200:
    
    #Turns it into a dict.
    response_data = response.json()

    #Data contains data. Other 2 branches are # of posts/comments, 
    response_data = response_data['data']
    json_response_data = json.dumps(response_data, indent=4)

    
    #print(json_response_data)
    
    for item in response_data:
        try:
            print(item['title'])
        except KeyError:

            try:
                print(item['author_description'])
                print(item['url'])
            except KeyError:
                continue

            
        
    

else: 
    print('Response code not 200:', response.status_code)


#The user can answer android, sort, how many results.
#That value. 