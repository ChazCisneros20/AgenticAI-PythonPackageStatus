from ollama import chat
from ollama import OllamaError
import requests
import json

class AgentUpdate:
    @staticmethod
    def package_update_agent(
        q='programming, Python',
        minScore=50,
        minComments=10,
        limit=25,
        page=2,
        fields='url,score,tag,title,subreddit,author_description',
        ascending=True,
    ):

        if type(ascending) is not bool:
            raise TypeError("Function package_update() parameter `ascending` only takes boolean value")

        if type(q) is not str:
            raise TypeError("Function package_update() parameter `q` must be a string")

        if type(fields) is not str:
            raise TypeError("Function package_update() parameter `fields` must be a comma-separated string")

        base_url = 'https://releasetrain.io/api/reddit/by-subreddit'
        #Adds paramters to the URL for the GET request.
        params = {
            'q': q,
            'minScore': minScore,
            'minComments': minComments,
            'limit': limit,
            'page': page,
            'fields': fields,
        }

        response = requests.get(url=base_url, params=params)

        if response.status_code == 200:
            response_data = response.json()
            response_data = response_data.get('data', [])
            response_data = sorted(response_data, key=lambda item: item.get('score', 0), reverse=not ascending)

            reddit_posts = ''
            for item in response_data:
                try:
                    reddit_posts += (
                        '[URL: ] ' + str(item.get('url', '')) + '\n' +
                        '[SCORE: ] ' + str(item.get('score', '')) + '\n' +
                        '[TAG(s): ] ' + str(item.get('tag', '')) + '\n' +
                        '[TITLE: ] ' + str(item.get('title', '')) + '\n' +
                        '[SUBREEDDIT: ] ' + str(item.get('subreddit', '')) + '\n'
                    )
                    reddit_posts += '[AUTHOR_DESCRIPTION: ] ' + str(item.get('author_description', '')) + '\n\n'
                except Exception:
                    reddit_posts += '\n'
                    continue

            #pass `reddt_posts` string to agent to speak to user about updates. 
            messages = [
                {
                    'role' : 'system',
                    'content' : ('''
                    You are a helpful package update assistant that provides users with the latest updates from Reddit based on their specified criteria. 
                    You will receive a list of Reddit posts formatted as follows: [URL: ] [SCORE: ] [TAG(s): ] [TITLE: ] [SUBREEDDIT: ] [AUTHOR_DESCRIPTION: ]. 
                    Your task is to summarize the key information from these posts and present it to the user in a clear and concise manner. 
                    Focus on highlighting the most relevant updates, trends, or insights that may be of interest to the user based on the provided data.
                    ''')
                },
                {
                    'role' : 'user',
                    'content' : reddit_posts
                }
            ]
            agent_response = chat(model='gemma3:latest', messages=messages)
            print(agent_response['message']['content'])

        return 'Currently unable to search updates <Response code not 200:> ' + str(response.status_code)    

#Fix: Instanciate the agent and let it dynamically handle functions as "tools"
if __name__ == "__main__":
    print("")