from rich.console import Console
console = Console()

def banner() -> None:
    " Prints Pinkerton's banner "

    console.print("""[bold yellow]
Pinkerton 1.8
Investigating JavaScript files since 1850
by 000pp
""")