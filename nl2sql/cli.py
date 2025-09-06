import click
import time
from rich.console import Console
from rich.text import Text

from .config import get_config,set_config, flush_config, load_config
from .llm import OpenAI , req_call , retry_req_call ,req_explain
import pyperclip

console = Console()


@click.group()
def cli():
    """A command-line tool to convert natural language queries to SQL or any database format in a go.

    This tool can use either a cloud-based service( free and paid ) or a local Ollama instance
    for the conversion. The tool uses a configuration file to store the
    database schema and other settings.
    """
    pass


@cli.command()
@click.option('--paste', help="Provide schema by pasting it directly.")
@click.option('--extract', type=click.Path(exists=True), help="Provide schema by extracting it from a file.")
def method(paste, extract):
    """Sets the database schema to be used for the conversion.

    Example:

      nl2sql method --extract "schema.txt" \n Simply provide schema file in any format

      or

      nl2sql method --paste "CREATE TABLE products (
        product_id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        category VARCHAR(50)
      )" \n Simply paste the schema
    """
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
    """Sets the type of query to be generated (e.g., sqlite, mysql, etc.).
    
    simply write comamnd ->
    
    nl2sql query-type "mongo db" (or) 
    nl2sql query-type "PostgreSQL" """
    if get_config("SCHEMA"):
        set_config("TYPE", query_type)
        console.print(f"[green]Query type set to: {query_type}[/green]")
    else:
        console.print("[yellow]Please provide a schema first using the 'method' command.[/yellow]")


@cli.command()
@click.argument("nl_query")
@click.option('--provider', type=click.Choice(['openai', 'lmstudio', 'ollama','free']), help='The LLM provider to use.')
@click.option('--api-key', help='The API key for the LLM provider.')
@click.option('--model', help='The model to use for conversion.')
def convert(nl_query, provider, model, api_key):
    """Converts a natural language query to SQL.
    exmaple :\n
    nl2sql convert "fetech all the orders below 1000$" --provider free 
    \n
    nl2sql convert "find costomers who created account on 31 jan" --provider "openai" --api-key "<your key>" --model "gpt-4o-mini" """
    if get_config("TYPE"):
        schema = get_config("SCHEMA")
        query_type = get_config("TYPE")

        # Get defaults from config if not provided as arguments
        provider = provider or get_config("DEFAULT_PROVIDER", "openai")
        model = model or get_config("DEFAULT_MODEL", "gpt-3.5-turbo")
        api_key = api_key or get_config("API_KEY", "")
        set_config("REC_Q",nl_query)
        base_url = None
        start_time = time.time()
        if provider == 'free':
            console.print(f"[bold blue]Using free model for conversion.(please make sure you have stable internet connection . . . )[/bold blue]")
            try:
                query, i_tokens, o_tokens = req_call(nl_query, schema, query_type)
                console.print("[bold green]Generated Query:[/bold green]")
                console.print(query)
                pyperclip.copy(query)
                set_config("REC_OUTPUT",query)
                end_time = time.time()
                elapsed_time = end_time - start_time
                console.print(f"[bold cyan]Time taken:[/bold cyan] {elapsed_time:.2f} seconds")
                console.print(f"[bold cyan]Tokens Used:[/bold cyan] Prompt: {i_tokens}, Completion: {o_tokens}, Total: {i_tokens+o_tokens}")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")
        else:
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
                pyperclip.copy(output)
                set_config("REC_OUTPUT",output)
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
@click.argument("action", type=click.Choice(["retry", "explain"]))
@click.argument("reason", required=False) 
@click.option('--provider', type=click.Choice(['openai', 'lmstudio', 'ollama','free']), help='The LLM provider to use.')
@click.option('--api-key', help='The API key for the LLM provider.')
@click.option('--model', help='The model to use for conversion.')
def assist(action,reason, provider, model, api_key):
    """
    use this method if you are not satisfied with your previous output 
    example-
    \n
    nl2sql assist retry "incorrect fetching" --provider ollama --model gemma3
    \n
    nl2sql assist explain --provider openai --model gpt-4o-mini 
    """
    if get_config("REC_OUTPUT"):
        rec_q=get_config("REC_Q")
        rec_o=get_config("REC_OUTPUT")
           
        schema = get_config("SCHEMA")
        query_type = get_config("TYPE")

        # Get defaults from config if not provided as arguments
        provider = provider or get_config("DEFAULT_PROVIDER", "openai")
        model = model or get_config("DEFAULT_MODEL", "gpt-3.5-turbo")
        api_key = api_key or get_config("API_KEY", "")
        base_url = None
        start_time = time.time()
        if  action == "retry":
            if provider == 'free':
                try:
                    console.print(f"[bold blue]Using free model for conversion.(please make sure you have stable internet connection . . . )[/bold blue]")
                    query, i_tokens, o_tokens = retry_req_call(rec_q, rec_o , schema, query_type , reason)
                    console.print("[bold green]Generated Query:[/bold green]")
                    console.print(query)
                    pyperclip.copy(query)
                    set_config("REC_OUTPUT",query)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    console.print(f"[bold cyan]Time taken:[/bold cyan] {elapsed_time:.2f} seconds")
                    console.print(f"[bold cyan]Tokens Used:[/bold cyan] Prompt: {i_tokens}, Completion: {o_tokens}, Total: {i_tokens+o_tokens}")
                except Exception as e:
                    console.print(f"[bold red]Error:[/bold red] {e}")
            else:
                if provider == 'lmstudio':
                    base_url = "http://localhost:1234/v1"
                elif provider == 'ollama':
                    base_url = "http://localhost:11434/v1"

                llm = OpenAI(api_key=api_key, base_url=base_url, model=model)
                console.print(f"[bold blue]Using {provider} with model {model} for conversion.[/bold blue]")

                start_time = time.time()
                try:
                    output, usage = llm.retrying(schema, query_type,rec_q,rec_o,reason)
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    # Display the query without rich.Panel or rich.Syntax
                    console.print("[bold green]Generated Query:[/bold green]")
                    console.print(output)
                    pyperclip.copy(output)
                    set_config("REC_OUTPUT",output)
                    console.print(f"[bold cyan]Time taken:[/bold cyan] {elapsed_time:.2f} seconds")
                    if usage:
                        prompt_tokens = usage.get('prompt_tokens', 'N/A')
                        completion_tokens = usage.get('completion_tokens', 'N/A')
                        total_tokens = usage.get('total_tokens', 'N/A')
                        console.print(f"[bold cyan]Tokens Used:[/bold cyan] Prompt: {prompt_tokens}, Completion: {completion_tokens}, Total: {total_tokens}")

                except Exception as e:
                    console.print(f"[bold red]An error occurred:[/bold red] {e}")
        elif action =="explain":
            if provider=="free":
                try:
                    console.print(f"[bold blue](please make sure you have stable internet connection . . . )[/bold blue]")
                    query, i_tokens, o_tokens = req_explain(rec_q, rec_o , schema, query_type)
                    console.print("[bold green]Explanation forGenerated Query:[/bold green]")
                    console.print(query)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    console.print(f"[bold cyan]Time taken:[/bold cyan] {elapsed_time:.2f} seconds")
                    console.print(f"[bold cyan]Tokens Used:[/bold cyan] Prompt: {i_tokens}, Completion: {o_tokens}, Total: {i_tokens+o_tokens}")
                except Exception as e:
                    console.print(f"[bold red]Error:[/bold red] {e}")
            else:
                if provider == 'lmstudio':
                    base_url = "http://localhost:1234/v1"
                elif provider == 'ollama':
                    base_url = "http://localhost:11434/v1"

                llm = OpenAI(api_key=api_key, base_url=base_url, model=model)
                console.print(f"[bold blue]Using {provider} with model {model} for reasoning.[/bold blue]")

                start_time = time.time()
                try:
                    output, usage = llm.explaining(schema, query_type,rec_q,rec_o)
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    # Display the query without rich.Panel or rich.Syntax
                    console.print("[bold green]Reasoning :[/bold green]")
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
    \n
    ALL TYPES OF CONFIG TO SET ARE:
    1) SCHEMA 
    2) TYPE 
    3) DEFAULT_PROVIDER 
    4) DEFAULT_MODEL
    5) API_KEY
    \n
    SIMPLE EXAMPLE -> nl2sql config set TYPE "mongo db"
    
    """
    set_config(key.upper(), value)
    console.print(f"[green]Configuration key '{key.upper()}' set to '{value}'.[/green]")


@config.command(name="get")
@click.argument("key")
def config_get(key):
    """Get the value of a configuration key.
    Insatant lookup on the specific config.example 
    nl2sql config get SCHEMA 
    
    """
    value = get_config(key.upper())
    if value is not None:
        console.print(f"[cyan]'{key.upper()}': '{value}'[/cyan]")
    else:
        console.print(f"[yellow]Configuration key '{key.upper()}' not found.[/yellow]")


@config.command(name="list")
def config_list():
    """List all configuration settings. \n
    nl2sql config list """
    all_config = load_config()
    if all_config:
        console.print("[bold underline]Current Configuration:[/bold underline]")
        for key, value in all_config.items():
            console.print(f"  [magenta]{key}[/magenta]: {value}")
    else:
        console.print("[yellow]No configuration settings found.[/yellow]")

@config.command(name='flush')
def flushing():
    """Total flush of all config set so far \n
    nl2sql config flush """
    flush_config()
    console.print("[yellow]ALL CONFIGRATIONS DELETED.[/yellow]")

cli.add_command(config)
