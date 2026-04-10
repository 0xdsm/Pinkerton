from src.interface.ui import banner
from src.pinkerton.main import perform_checks, perform_local_scan, perform_js_scan

from argparse import ArgumentParser

if __name__ == "__main__":

    banner()

    parser = ArgumentParser()
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("-u", "--url", help="Crawl a URL and scan all JavaScript files found")
    target.add_argument("-f", "--file", help="Scan a local JavaScript file")
    target.add_argument("-j", "--js-url", dest="js_url", help="Scan a single remote JavaScript file directly")
    parser.add_argument("-H", "--HEADER", help="Custom header (name value), can be repeated", nargs=2, default=[], action='append')
    args = parser.parse_args()

    if args.url:
        perform_checks(args)
    elif args.file:
        perform_local_scan(args)
    else:
        perform_js_scan(args)
