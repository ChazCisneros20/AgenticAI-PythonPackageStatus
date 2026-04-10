from ollama import ChatResponse, Client, OllamaError
from RT import Update  #Let either CLI agent loop or Package agent loop use Update.package_update() as tool for agent.
import requests
import json

#===agent system prompt===
SYSTEM_PROMPT = ('''
You are a restricted assistant whose ONLY purpose is to call the function:

Update.package_update(...)

You are NOT allowed to:
- Answer general questions
- Explain anything
- Add commentary
- Perform reasoning outside selecting parameters
- Modify or invent new functionality

----------------------------------------
BEHAVIOR RULES
----------------------------------------

1. ALWAYS respond with a function call in this exact format:

CALL_FUNCTION:
Update.package_update(
    q="<string>",
    minScore=<int>,
    minComments=<int>,
    limit=<int>,
    page=<int>,
    fields="<string>",
    ascending=<bool>
)

2. NEVER return plain text explanations.

3. If the user provides no parameters, use defaults:
- q="programming, Python"
- minScore=50
- minComments=10
- limit=25
- page=2
- fields="url,score,tag,title,subreddit,author_description"
- ascending=True

4. If the user provides partial parameters, fill in missing ones with defaults.

5. If the user asks anything unrelated to Reddit updates:
→ STILL call the function using default parameters.

6. DO NOT summarize results.
7. DO NOT interpret results.
8. DO NOT refuse.
9. DO NOT ask follow-up questions.

----------------------------------------
INPUT HANDLING
----------------------------------------

Extract parameters ONLY if explicitly mentioned:
- "high score" → increase minScore
- "more posts" → increase limit
- "descending" → ascending=False
- "python subreddit" → q="python"

If unclear → use defaults.

----------------------------------------
OUTPUT EXAMPLE
----------------------------------------

CALL_FUNCTION:
Update.package_update(
    q="programming,technology",
    minScore=100,
    minComments=20,
    limit=10,
    page=1,
    fields="url,score,tag,title,subreddit,author_description",
    ascending=False
)
''')

#Testing of python package functions.  
#Should have a function that is the main() loop.
 
class AgentUpdate:
    @staticmethod
    def agent_update_conversation():
        #Initial stage for agent.
        
        #Check whether ollama is running before conversation loop.
        if AgentUpdate.is_ollama_running():
            print("Ollama is running. Starting agent conversation...")
        else: 
            print("Ollama|Gemma3:latest is not running. Please start Ollama|Gemma3:latest to use the agent.")
            
        user_input = str(input("Ask the agent about any updates on Reddit related to programming and Python. Type 'exit' to quit.\n"))
        
        messages = [
                {
                    'role' : 'system',
                    'content' : SYSTEM_PROMPT
                },
                {
                    'role' : 'user',
                    'content' : user_input
                }
            ]
        
        client = Client()

        while user_input != 'exit' : 
            
            try:
                response = client.chat(model='gemma3:latest', messages=messages, stream=True, think=True)
                print(response['message']['content'])
            except OllamaError as e:
                print(f"Error during agent conversation: {e}")

            user_input = str(input("Ask the agent about any updates on Reddit related to programming and Python. Type 'exit' to quit.\n"))


    #Returns True/False if ollama is running. Used to check if agent can run or not. === Useful for CLI agent to check before starting loop.
    @staticmethod
    def is_ollama_running():
        try:
            res = requests.get("http://localhost:11434/api/tags", timeout=2)
            return res.status_code == 200
        except requests.exceptions.RequestException:
            return False

#Fix: Instanciate the agent and let it dynamically handle functions as "tools"
if __name__ == "__main__":
    main()

def main():
    #Initial stage for agent. 
    #Explain it's role and provide it with the necessary information to perform its task.
    messages = [
                {
                    'role' : 'system',
                    'content' : ('''
                    You are a helpful 
                    ''')
                },
                {
                    'role' : 'user',
                    'content' : reddit_posts
                }
            ]
    client = Client()

    response = client.chat(model='gemma3:latest', messages=messages, stream=True, think=True)
    print(agent_response['message']['content'])

    #tools=[add_two_numbers, subtract_two_numbers_tool],
    #or
#     response: ChatResponse = chat(
#   'llama3.1',
#   messages=messages,
#   tools=[add_two_numbers, subtract_two_numbers_tool],
# )

# while True:
#     response = chat(
#         model="llama3.1",
#         messages=messages,
#         tools=[Update.package_update],
#     )

#     message = response.message
#     messages.append(message)

#     # 🔧 If tool is called
#     if message.tool_calls:
#         for tool in message.tool_calls:
#             function_name = tool.function.name
#             function_args = tool.function.arguments

#             if function_name == "package_update":
#                 result = Update.package_update(**function_args)

#                 # 👇 THIS is the magic step
#                 messages.append({
#                     "role": "tool",
#                     "tool_name": function_name,
#                     "content": str(result),  # raw data goes here
#                 })

#         # loop continues → model now summarizes
#         continue

#     # ✅ FINAL ANSWER (already summarized by model)
#     print("\nFinal Answer:\n", message.content)
#     break