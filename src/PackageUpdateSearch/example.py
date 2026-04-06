#Upload to github this src into prof's src.
#Upload

import requests
import json

#Testing of python package functions. 
class example:
    @staticmethod
    def capstone():
        print("Hello World\n")
        print("This is the start of my Senior Capstone project !\n")

    #Follow link: https://releasetrain.io/docs/ for references.

    @staticmethod
    def get_request(URL):
        response = requests.get(url=URL)
        print(response)
    #FIXME:ADD .help() function AND `help` command for CLI

#======MAIN CAPSTONE FUNCTION; ANY UPDATES TODAY ==============================
#==============================================================================
#NOTE: Does not include an 'ask' function to speak to agent about any updates. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< (reference in app.py))

#FIX: Change URL to the actual URL of the API endpoint. (no parameters for endpoint)
#FIX: Add error handling for non-200 response code.
    @staticmethod
    def package_update(
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

            return reddit_posts

        return 'Currently unable to search updates <Response code not 200:> ' + str(response.status_code)
    #Make something similar to "python --help" as a CLI help such as '-v' for version.. 
    #===HELP FUNCTION for user===============================================================
    #ALSO: Acts as documentation for the package_update() function.
    @staticmethod
    def help():
        help_message=(
        """Fetch and format Reddit posts from the ReleaseTrain by-subreddit endpoint.

        Parameters:
            q (str): comma-separated subreddit names to query, e.g. 'programming,technology'.
            minScore (int): minimum post score to include.
            minComments (int): minimum number of comments to include.
            limit (int): maximum number of posts returned by the API.
            page (int): API page number for pagination.
            fields (str): comma-separated fields to return from the API.
            ascending (bool): sort order for score values; True returns ascending order.

        Returns:
            str: formatted string containing the selected Reddit posts, or an error message if the request fails.

        Example:
            example.package_update(
                q='programming,technology',
                minScore=50,
                minComments=10,
                limit=25,
                page=2,
                fields='url,score,tag,title,subreddit,author_description',
                ascending=False,
            )
        """
        )
        print(help_message)



        

