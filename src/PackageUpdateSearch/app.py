import argparse
import os
import sys
import RT
from agenticRT import SYSTEM_PROMPT, TOOL_REGISTRY, AgentUpdate 
from importlib.metadata import version, PackageNotFoundError #< For getting the python package version number from the hatchling build. (preinstalled with Python 3) 

def get_version():
    try:
        return version("PackageUpdateSearch")
    except PackageNotFoundError:
        return "unknown"

#CREATES parser OBJECT. 
#Notes: If it says .add_paser(..) it creates a new COMMAND to parse. If it says .add_argument(..) it adds a PARAMETER to that command. 
#Notes: If it says .add_parser(..) again, it creates a NEW command to parse, and the previous parameters using .add_argument(..) will not apply to the new command. <<<
def create_parser():
    parser = argparse.ArgumentParser(
        description='CLI wrapper for PackageUpdateSearch RT utilities.'
        #Removed add_help=False to allow automatic help flag generation for each command. <<<
    )
    subparsers = parser.add_subparsers(dest='command', required=False)

    #=====package-update command==========================================================
    parser_update = subparsers.add_parser(
        'package-update',
        help='Fetch and format ReleaseTrain Reddit posts using package_update().',
        description='Fetch Reddit posts from ReleaseTrain API with filtering and sorting options.'
        #--help^
    )
    #Ex: --q will create a data member/attribute called "q" that can be accessed with `args.q`. <<<
    parser_update.add_argument('--q', default='programming,technology', help='Comma-separated subreddit names to query.') #FIXED: works for comma-separated string input.
    parser_update.add_argument('--min-score', type=int, default=50, help='Minimum post score to include.')
    parser_update.add_argument('--min-comments', type=int, default=10, help='Minimum number of comments to include.')
    parser_update.add_argument('--limit', type=int, default=25, help='Maximum number of posts to return.')
    parser_update.add_argument('--page', type=int, default=2, help='Page number for pagination.')
    parser_update.add_argument('--fields', default='url,score,tag,title,subreddit,author_description', help='Comma-separated fields to request from the API.',)
    parser_update.add_argument('--ascending', action='store_true', help='Sort by score in ascending order. Default is descending.',)

    #=====get-request command==========================================================
    parser_get = subparsers.add_parser('get-request', 
                                       help='Send a generic GET request to the provided URL.', 
                                       description='Performs a GET request to a given URL and prints the response.'    
                                        #--help^
    )
    parser_get.add_argument('url', help='The full URL to request.')

    #=====capstone command==========================================================
    subparsers.add_parser('capstone', help='Print the capstone project greeting message.', description='Prints a greeting message for the PackageUpdateSearch capstone project.')
    #=====agent-update command==========================================================
    subparsers.add_parser('agent-update', help='Start an agent conversation about Reddit updates.', 
                          description='Engage in a conversation with an agent about Reddit updates using the AgentUpdate class.\n Allow an agent to summarize Reddit posts based on your question.')
                          #--help^
    #=====help command==========================================================
    subparsers.add_parser('help', help='Show available commands.', 
                          description='Display a list of available commands and their descriptions.')
                          #--help^
    #=====version command (global optional argument, `-v`)==========================================================
    parser.add_argument(
                        '-v', '--version',
                        action='version',
                        version=f'PackageUpdateSearch CLI version {get_version()}')
    #=====exit command==========================================================
    subparsers.add_parser('exit', help='Exit the CLI.', 
                          description='Exit the command-line interface.')
                          #--help^
    return parser

#FOR HANDLING COMMANDS. 
def handle_command(parser, command_line):
    """Parse and execute a single command."""
    try:
        command_parts = command_line.strip().split()
        if not command_parts:
            return True
        
        args = parser.parse_args(command_parts)

        if not args.command:
            print_help()
            return True
        
        #=====package-update command==========================================================
        if args.command == 'package-update':
            result = RT.Update.package_update(
                #These dot accessed data members/attributes come from `parser_update.add_argument('--q' ...` in `create_parser()`.<<<
                q=args.q,
                minScore=args.min_score,
                minComments=args.min_comments,
                limit=args.limit,
                page=args.page,
                fields=args.fields,
                ascending=args.ascending,
            )
            print(result)
        #=====agent-update command==========================================================
        elif args.command == 'agent-update':
            try:
                AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)
                print("Agent conversation ended.")
                print_help()
            except KeyboardInterrupt:
                print("\nExiting agent mode...")
        #=====get-request command==========================================================
        elif args.command == 'get-request':
            RT.get_request(args.url)
        #=====capstone command==========================================================
        elif args.command == 'capstone':
            RT.capstone()
        #FIX: 'help' should actually provide an overview help of the CLI, not just print available commands. <<<
        #=====help command==========================================================
        elif args.command == 'help':
            print_help()
        #=====version command==========================================================
        elif args.command == '-v':
            print("PackageUpdateSearch CLI version 0.0.6")
        #=====exit command==========================================================
        elif args.command == 'exit':
            print("Goodbye!")
            return False
        
        return True
        
        #======END : CLI Branches based on user input command============================


    except SystemExit:
        return True
    except Exception as e:
        print(f"Error: {e}")
        return True



def print_help():
    """Display available commands."""
    print("\nAvailable commands:")
    print("  package-update  - Fetch and format ReleaseTrain Reddit posts")
    print("  get-request     - Send a GET request to a URL")
    print("  capstone        - Print the capstone greeting")
    print("  help            - Show this help message")
    print("  -v              - Show PackageUpdateSearch CLI version information")
    print("  agent-update    - Start an agent conversation about Reddit updates") #FIX: Add this to help menu. <<<
    print("  exit            - Exit the CLI\n")
    print("\n Use '<command> --help'  or '<command> --h' for more details on a specific command.\n")

#====MAIN CLI APPLICATION LOOP ===================================================
#NOTE: Does not include an 'ask' function to speak to agent about any updates. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< (reference in RT.py))
def main():
    #parser object.
    parser = create_parser()
    print("\n===Welcome to the PackageUpdateSearch CLI!===")

    #Shows avaialable commands on start. <<<
    print_help()
    
    #Use of parser object in loop. 
    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            if not handle_command(parser, user_input):
                break

        #If user presses Ctrl+C it will break loop. <<<
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == '__main__':
    main()
