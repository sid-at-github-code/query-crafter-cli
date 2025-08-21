import click
from config_crud import save_config, load_config, set_config,get_config,flush_config
from localcall import llm_call
from cloudcall import nl_to_sql

# --- schma sharing 
@click.command()
@click.option('--paste',   help="provide schema by simply  -> nl2sql method --paste 'schema form code' ")
@click.option('--extract',  help="provide schema by simply -> ml2sql method --extract 'fileName.sql' ")
def method(paste, extract):
    """share schmea by providing direct paste or file name for extraction """
    if paste:
        flush_config()
        click.echo(f"Method choosen PASTE , schema ->  {paste}")
        set_config("SCHEMA",paste)
        
    elif extract:
        flush_config()
        click.echo(f"Method choosen EXTRACT , from file ->  {extract}")
        with open(extract,"r") as f:
            data=f.read()
        click.echo(data)
        set_config("SCHEMA",data)
        
    else:
        click.echo("Please choose method to share schema or try > nl2sql method --help")
        
    
# query type sharing  
@click.command(name="query-type")   
@click.argument("query_type")     
def query_type(query_type):       
    """Select query type"""
    if get_config("SCHEMA"):
        set_config("TYPE",query_type)
        click.echo(f"You selected the query type: {query_type}")
    else:
        click.echo("PLEASE PROVIDE SCHEMA FIRST -> use method --extract or --paste ")

# NL question and LLM call 
@click.command(name="convert")
@click.argument("nl")
def convert_handler(nl):
    if get_config("TYPE"):
        set_config("PROMPT",nl)
        nl_q=get_config("PROMPT")
        schema=get_config("SCHEMA")
        etype=get_config("TYPE")
        output1=nl_to_sql(nl_q,schema,etype)
        click.echo(f"Your query is here ->\n {output1}")
    else:
        click.echo("PLEASE PROVIDE QUERY ENGINE TYPE , use command -> nl2sql query-type 'SQL' or any other ")

# apppend to temp and LLM call , again
@click.command(name="retry")
@click.argument("reason", required=False) 
def retry_handler(reason):
    if reason:
        click.echo(f"error correction statemant -> {reason} \n > retrying . . .")
    else:
        click.echo("no reason specified \n > retrying . . . ")
    
#----to test the cli  
@click.command()
@click.option("--name", required=True,help="blabla" )
def greet(name):
    click.echo(get_config("SCHEMA"))

# --- main entry point ---
@click.group()
def cli():
    """Multi-tool CLI 🤖"""
    pass


# attach commands
cli.add_command(method)
cli.add_command(greet)
cli.add_command(query_type)
cli.add_command(convert_handler)
cli.add_command(retry_handler)


if __name__ == "__main__":
    cli()
