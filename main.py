from src.interface.ui import banner
from src.pinkerton.main import perform_checks, perform_local_scan

from argparse import ArgumentParser

if __name__ == "__main__":

    banner()

    parser = ArgumentParser()
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("-u", "--url", help="Target URL to crawl for JavaScript files")
    target.add_argument("-f", "--file", help="Local JavaScript file to scan")
    parser.add_argument("-H", "--HEADER", help="Custom header (name value), can be repeated", nargs=2, default=[], action='append')
    args = parser.parse_args()

    if args.url:
        perform_checks(args)
    else:
        perform_local_scan(args)
