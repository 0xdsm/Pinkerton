import re
from pathlib import Path
from urllib.parse import urljoin

from requests import get, exceptions
from urllib3 import disable_warnings
from rich.console import Console
console = Console()

from src.pinkerton.settings import get_user_agent
from src.pinkerton.modules.secret import scan, scan_file

disable_warnings()

def perform_checks(args) -> None:
    " Check if target is accessible "

    url = args.url

    custom_headers = {
        "User-Agent": get_user_agent(),
    }

    for header in args.HEADER:
        name, value = header
        custom_headers[name] = value

    try:
        response = get(url, headers=custom_headers, verify=False)
        status_code: int = response.status_code
        page_content: str = response.text

        if(response.ok):
            console.print(f"[[green]+[/]] Connected sucessfully with [yellow]{url}[/]", highlight=False)
            extract_js(url, page_content, custom_headers)
        else:
            console.print(f"[[red]![/]] {url} returned {status_code} status code", highlight=False)
            return False

    except exceptions.ConnectionError as con_error:
        console.print(f"[[red]![/]] {url} Connection Error: {con_error}", highlight=False)
        return False
    except exceptions.InvalidURL as invalid_error:
        console.print(f"[[red]![/]] Invalid URL {url}: {invalid_error}", highlight=False)
        return False


def extract_js(url, page_content, custom_headers) -> None:
    " Extract JavaScript files links from page source "

    console.print(f"[[yellow]![/]] Extracting JavaScript files from [yellow]{url}[/]", highlight=False)

    js_file_pattern = r'src=["\']?([^"\'>\s]+\.js)(\?.*?)?["\'\s>]'
    js_files = re.findall(js_file_pattern, page_content)
    
    console.print(f"[[green]+[/]] {len(js_files)} file(s) found\n", highlight=False)

    for js_file, _ in js_files:
        if(js_file.startswith("http")):
            console.print(f"[[yellow]![/]] Scanning [yellow]{js_file}[/]", highlight=False)
            scan(js_file, custom_headers)
        else:
            final_url = urljoin(url, js_file)
            console.print(f"[[yellow]![/]] Scanning [yellow]{final_url}[/]", highlight=False)
            scan(final_url, custom_headers)


def perform_local_scan(args) -> None:
    """Scan a local JavaScript file for exposed secrets."""
    path = Path(args.file)

    if not path.is_file():
        console.print(f"[[red]![/]] File not found: [yellow]{path}[/]", highlight=False)
        return

    console.print(f"[[yellow]![/]] Scanning local file [yellow]{path}[/]", highlight=False)
    scan_file(str(path))