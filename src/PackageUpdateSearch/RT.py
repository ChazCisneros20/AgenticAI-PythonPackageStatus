import requests
import json

class Update:
#======MAIN CAPSTONE FUNCTION; ANY UPDATES TODAY ==============================

#NOTE: Does not include an 'ask' function to speak to agent about any updates. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< (reference in app.py))
    @staticmethod
    def package_update(
        q : str ='programming, Python',
        minScore : int =50,
        minComments : int =10,
        limit : int =25,
        page : int =2,
        fields : str ='url,score,tag,title,subreddit,author_description',
        ascending : int = 1,
    ):
        """
        Fetch and format Reddit posts from the ReleaseTrain by-subreddit endpoint.
        
        Args: 
            q (str): comma-separated subreddit names to query, e.g. 'programming,technology'.
            minScore (int): posts with minimum reddit score.
            minComments (int): minimum number of comments on the reddit post.
            limit (int): maximum number of posts returned by the API.
            page (int): API page number for pagination.
            fields (str): comma-separated fields to return from the API.
            ascending (int): sort order for score values; 1 returns ascending order. 0 returns descending order.
        
        Returns:
            Multiple Reddit posts formatted as a string, each post includes:
            [URL: ] 
            [SCORE: ] 
            [TAG(s): ] 
            [TITLE: ] 
            [SUBREEDDIT: ] 

            Some posts may also include:
            [AUTHOR_DESCRIPTION: ]

        Example:
            >>> example.package_update(
                >>> q='programming,technology',
                >>> minScore=50,
                >>> minComments=10,
                >>> limit=25,
                >>> page=2,
                >>> fields='url,score,tag,title,subreddit,author_description',
                >>> ascending=False,
            )
        """

        ascending = int(ascending)
        if ascending not in (0, 1):
            raise ValueError("ascending must be 0 or 1")

        ascending = bool(ascending)
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
    #===HELP FUNCTION for user===============================================================
    #ALSO: Acts as documentation for the package_update() function.
    @staticmethod
    def help():
        """Returns a help message describing the package_update function, its parameters, return value, and an example of how to call it.

        Parameters:
            None

        Returns:
            str: A help message describing the package_update function, its parameters, return value, and an example of how to call it.

        Example:
            >>> example.help()
        """
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
            >>> example.package_update(
                >>> q='programming,technology',
                >>> minScore=50,
                >>> minComments=10,
                >>> limit=25,
                >>> page=2,
                >>> fields='url,score,tag,title,subreddit,author_description',
                >>> ascending=False
            )

        """
        )
        print(help_message)



        

