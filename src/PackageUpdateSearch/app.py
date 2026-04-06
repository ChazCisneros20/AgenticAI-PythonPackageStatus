import argparse
import os
import sys

from example import example

#CREATES parser OBJECT. 
def create_parser():
    parser = argparse.ArgumentParser(
        description='CLI wrapper for PackageUpdateSearch example utilities.',
        add_help=False
    )
    subparsers = parser.add_subparsers(dest='command', required=False)

    parser_update = subparsers.add_parser(
        'package-update',
        help='Fetch and format ReleaseTrain Reddit posts using package_update().'
    )
    #Ex: --q will create a data member/attribute called "q" that can be accessed with args.q. <<<
    #This is done automatically due to the '--' prefix ^^^^
    parser_update.add_argument('--q', default='programming,technology', help='Comma-separated subreddit names to query.') #FIXED: works for comma-separated string input.
    parser_update.add_argument('--min-score', type=int, default=50, help='Minimum post score to include.')
    parser_update.add_argument('--min-comments', type=int, default=10, help='Minimum number of comments to include.')
    parser_update.add_argument('--limit', type=int, default=25, help='Maximum number of posts to return.')
    parser_update.add_argument('--page', type=int, default=2, help='Page number for pagination.')
    parser_update.add_argument(
        '--fields',
        default='url,score,tag,title,subreddit,author_description',
        help='Comma-separated fields to request from the API.',
    )
    parser_update.add_argument(
        '--ascending',
        action='store_true',
        help='Sort by score in ascending order. Default is descending.',
    )

    parser_get = subparsers.add_parser('get-request', help='Send a generic GET request to the provided URL.')
    parser_get.add_argument('url', help='The full URL to request.')

    subparsers.add_parser('capstone', help='Print the capstone project greeting message.')
    
    subparsers.add_parser('help', help='Show available commands.')
    subparsers.add_parser('exit', help='Exit the CLI.')

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

        #CLI if typed package-update. 
        #If need new attribute, use the `parser_update.add_argument(...)``
        if args.command == 'package-update':
            result = example.package_update(
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

        elif args.command == 'get-request':
            example.get_request(args.url)

        elif args.command == 'capstone':
            example.capstone()

        elif args.command == 'help':
            print_help()

        elif args.command == 'exit':
            print("Goodbye!")
            return False

        return True

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
    print("  exit            - Exit the CLI\n")

#====MAIN CLI APPLICATION LOOP ===================================================
#NOTE: Does not include an 'ask' function to speak to agent about any updates. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< (reference in example.py))
def main():
    #parser object.
    parser = create_parser()
    print("Welcome to the PackageUpdateSearch CLI!")

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
