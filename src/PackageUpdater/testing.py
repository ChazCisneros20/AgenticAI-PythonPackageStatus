# from PackageUpdater import example

import requests 
import json
URL = ''
response = requests.get(url=URL)

if response.status_code == 200:
    
    #Turns it into a dict.
    response_data = response.json()
    #Data contains data. Other 2 branches are # of posts/comments.
    response_data = response_data['data']
    response_data = sorted(response_data, key=lambda item: item['score'], reverse=True)
    json_response_data = json.dumps(response_data, indent=4)

    #===RAW DATA=== : Comment/Uncomment to refer to the full raw original data fetched
    # print(json_response_data)

    #===OLD METHOD===
    # for item in response_data:
    #     try:
    #         print("[URL: ]", item['url'])
    #         print("[TAG(S): ]", item["tag"])
    #         print("[TITLE: ]", item['title'])
    #         print("[SUBREDDIT: ]", item['subreddit'])
    #         print("[AUTHOR DESCRIPTION: ]", item['author_description'], "\n")
    #     #If there lies no post description (author_description) --> apply newline '\n'.                
    #     except KeyError: 
    #         print("\n")
    #         continue

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

    print(reddit_posts)

else: 
    print('Currently unable to search updates','<Response code not 200:>', response.status_code)


#The user can answer android, sort, how many results.
#That value. 