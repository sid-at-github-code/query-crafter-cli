import click
from config_crud import set_config, get_config, load_config, save_config


@click.command()
@click.option('--paste', help="Paste schema directly")
@click.option('--file', type=click.Path(exists=True), help="Load schema from file")
def schema(paste, file):
    """Schema processing"""
    
    if paste:
        set_config("pasted_schema",paste)
        click.echo(load_config())
    elif file:
        click.echo(f"[FILE MODE] ")
    else:
        raise click.UsageError("Please use --paste or --file")

# --- feature 2: adder ---
@click.command()
@click.option('--x',  help="First number")
@click.option('--y',  help="Second number")
def add(x, y):
    """Simple adder"""
    if x:
        n = 0
        
    elif y:
        n = 1
        click.echo(y)
    else:
        click.echo("Please pass --x or --y")
        return
    
    click.echo(f"n is set to {n}")
        

@click.command()
def show(): 
    click.echo(load_config())

@click.command()
@click.option("--name", required=True,help="blabla" )
@click.option("--age", prompt="enter you age ",help="hdhdhdhd")
def greet(name,age):
    click.echo(f"{name} is of age ={age}")
    
# --- main entry point ---
@click.group()
def cli():
    """Multi-tool CLI 🤖"""
    pass


# attach commands
cli.add_command(schema)
cli.add_command(add)
cli.add_command(greet)
cli.add_command(show)

if __name__ == "__main__":
    cli()
