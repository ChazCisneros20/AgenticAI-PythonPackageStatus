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
    #FIXME:ADD .help() functio AND `help` command for CLI

    #===MAIN CAPSTONE FUNCTION; ANY UPDATES TODAY ==============================
    @staticmethod
    def package_update(URL):
        response = requests.get(url=URL)

        if response.status_code == 200:

            #Turns it into a dict.
            response_data = response.json()
            #Data contains data. Other 2 branches are # of posts/comments.
            response_data = response_data['data']
            response_data = sorted(response_data, key=lambda item: item['score'], reverse=True)
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



        

