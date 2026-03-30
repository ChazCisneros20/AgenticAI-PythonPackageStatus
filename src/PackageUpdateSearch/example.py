import requests
import json

class example:
    @staticmethod
    def add_one(number):
        return number + 1

    @staticmethod
    def capstone():
        print("Hello World\n")
        print("This is the start of my Senior Capstone project !\n")

    @staticmethod
    def get_request(URL):
        response = requests.get(url=URL)
        print(response)
    #FIXME:ADD .help() function AND `help` command for CLI

    #===MAIN CAPSTONE FUNCTION; ANY UPDATES TODAY ==============================
    #FIX: Ask prof if he wants it to return String or print(). 
    #FIX: Ask if we are getting info for one specific package. Then I can model it accordingly. Is it dynamic for packages we choose?
    #FIX: Ask if we the API has any parameters such as getting data from specific server, searching by keyword etc.
    #So that I can implement a searchby= parameter that will be specific keywords OR if the API allows free searching. 
    #searchby='r/apple' AND title='package'
    @staticmethod
    def package_update(URL='', ascending=True):

        #===ERROR HANDLING: `ascending` passed non-boolean value.
        try:
            if type(ascending) != bool:
                raise TypeError
        except TypeError:
        #FIX:Ask professor if this is ok. Do we return string typically, do we want the user's backend to have a full error?
            return TypeError("Function package_update() parameter `ascending` only takes boolean value")
        

        response = requests.get(url=URL)
        
        if response.status_code == 200:

            #Turns it into a dict.
            response_data = response.json()
            #Data contains data. Other 2 branches are # of posts/comments.
            response_data = response_data['data']
            #`ascending` comes from the original function parameter. Default set to True (ASC order).
            response_data = sorted(response_data, key=lambda item: item['score'], reverse=ascending)
            json_response_data = json.dumps(response_data, indent=4)

            reddit_posts = '' 

            #ADD: Send string variable to Ollama agent. 
            #DOCUMENTATION: If there are no author descriptions, the loop logic should continue/loop over to next item.
            #===CLEAN DATA===
            for item in response_data:
                try:
                    reddit_posts += ("[URL: ] " + str(item['url']) + '\n' +
                                     "[SCORE: ]" + str(item['score']) + '\n' +
                                     "[TAG(s): ] " + str(item['tag']) + '\n' +
                                     "[TITLE: ] " + str(item['title']) + '\n' +
                                     "[SUBREEDDIT: ] " + str(item['subreddit']) + '\n')
                    reddit_posts += "[AUTHOR_DESCRIPTION: ]" + str(item['author_description']) + '\n' + '\n'
                #If there lies no post description (author_description) --> apply newline '\n'.                
                except KeyError: 
                    reddit_posts += '\n'
                    continue
                
            return reddit_posts
        else: 
            return 'Currently unable to search updates <Response code not 200:>' + str(response.status_code)
    
    #===HELP FUNCTION for user===
    @staticmethod
    def help():
        help = """
TEST
"""
        return help




        

