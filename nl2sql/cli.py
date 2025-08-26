import click
import time
from rich.console import Console
# Removed Panel and Syntax imports
from rich.text import Text

from .config import get_config, set_config, flush_config, load_config
from .llm import OpenAI

console = Console()


@click.group()
def cli():
    """A command-line tool to convert natural language queries to SQL.

    This tool can use either a cloud-based service or a local Ollama instance
    for the conversion. The tool uses a configuration file to store the
    database schema and other settings.
    """
    pass


@cli.command()
@click.option('--paste', help="Provide schema by pasting it directly.")
@click.option('--extract', type=click.Path(exists=True), help="Provide schema by extracting it from a file.")
def method(paste, extract):
    """Sets the database schema to be used for the conversion."""
    if paste:
        flush_config()
        console.print("[green]Schema provided via paste.[/green]")
        set_config("SCHEMA", paste)
    elif extract:
        flush_config()
        with open(extract, "r") as f:
            data = f.read()
        console.print(f"[green]Schema extracted from {extract}.[/green]")
        set_config("SCHEMA", data)
    else:
        console.print("[yellow]Please provide a schema using --paste or --extract.[/yellow]")


@cli.command(name="query-type")
@click.argument("query_type")
def query_type(query_type):
    """Sets the type of query to be generated (e.g., sqlite, mysql, etc.)."""
    if get_config("SCHEMA"):
        set_config("TYPE", query_type)
        console.print(f"[green]Query type set to: {query_type}[/green]")
    else:
        console.print("[yellow]Please provide a schema first using the 'method' command.[/yellow]")


@cli.command()
@click.argument("nl_query")
@click.option('--provider', type=click.Choice(['openai', 'lmstudio', 'ollama']), help='The LLM provider to use.')
@click.option('--api-key', help='The API key for the LLM provider.')
@click.option('--model', help='The model to use for conversion.')
def convert(nl_query, provider, model, api_key):
    """Converts a natural language query to SQL."""
    if get_config("TYPE"):
        schema = get_config("SCHEMA")
        query_type = get_config("TYPE")

        # Get defaults from config if not provided as arguments
        provider = provider or get_config("DEFAULT_PROVIDER", "openai")
        model = model or get_config("DEFAULT_MODEL", "gpt-3.5-turbo")
        api_key = api_key or get_config("API_KEY", "")

        base_url = None
        if provider == 'lmstudio':
            base_url = "http://localhost:1234/v1"
        elif provider == 'ollama':
            base_url = "http://localhost:11434/v1"

        llm = OpenAI(api_key=api_key, base_url=base_url, model=model)
        console.print(f"[bold blue]Using {provider} with model {model} for conversion.[/bold blue]")

        start_time = time.time()
        try:
            output, usage = llm.nl_to_query(nl_query, schema, query_type)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Display the query without rich.Panel or rich.Syntax
            console.print("[bold green]Generated Query:[/bold green]")
            console.print(output)

            console.print(f"[bold cyan]Time taken:[/bold cyan] {elapsed_time:.2f} seconds")
            if usage:
                prompt_tokens = usage.get('prompt_tokens', 'N/A')
                completion_tokens = usage.get('completion_tokens', 'N/A')
                total_tokens = usage.get('total_tokens', 'N/A')
                console.print(f"[bold cyan]Tokens Used:[/bold cyan] Prompt: {prompt_tokens}, Completion: {completion_tokens}, Total: {total_tokens}")

        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")
    else:
        console.print("[yellow]Please set the query type first using the 'query-type' command.[/yellow]")


@cli.command()
@click.argument("reason", required=False)
def retry(reason):
    if reason:
        console.print(f"[blue]Retrying with correction:[/blue] {reason}")
    else:
        console.print("[blue]Retrying...[/blue]")
    console.print("[yellow]Retry functionality is not fully implemented yet.[/yellow]")


@cli.group()
def config():
    pass


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a configuration key-value pair.

    KEY: The configuration key (e.g., DEFAULT_PROVIDER, DEFAULT_MODEL, API_KEY).
    VALUE: The value to set for the key.
    """
    set_config(key.upper(), value)
    console.print(f"[green]Configuration key '{key.upper()}' set to '{value}'.[/green]")


@config.command(name="get")
@click.argument("key")
def config_get(key):
    """Get the value of a configuration key.

    KEY: The configuration key to retrieve.
    """
    value = get_config(key.upper())
    if value is not None:
        console.print(f"[cyan]'{key.upper()}': '{value}'[/cyan]")
    else:
        console.print(f"[yellow]Configuration key '{key.upper()}' not found.[/yellow]")


@config.command(name="list")
def config_list():
    """List all configuration settings."""
    all_config = load_config()
    if all_config:
        console.print("[bold underline]Current Configuration:[/bold underline]")
        for key, value in all_config.items():
            console.print(f"  [magenta]{key}[/magenta]: {value}")
    else:
        console.print("[yellow]No configuration settings found.[/yellow]")


cli.add_command(config)
