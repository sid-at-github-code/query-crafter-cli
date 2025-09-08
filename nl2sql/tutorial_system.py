
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.tree import Tree
from rich.markdown import Markdown
from rich.align import Align
from rich.rule import Rule
from rich.progress import track
from rich.prompt import Prompt, Confirm

class NL2SQLTutorial:
    """Complete tutorial system for query-crafter-CLI tool"""
    
    def __init__(self, package_name="qcraft"):
        self.console = Console()
        self.package_name = package_name
    
    def show_welcome(self):
        """Display welcome screen with ASCII art and intro"""
        self.console.clear()
        
        # ASCII Art Title
        title_art = """
 ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗      ██████╗██████╗  █████╗ ███████╗████████╗███████╗██████╗       ██████╗██╗     ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝     ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗     ██╔════╝██║     ██║
██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝      ██║     ██████╔╝███████║█████╗     ██║   █████╗  ██████╔╝     ██║     ██║     ██║
██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝       ██║     ██╔══██╗██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗     ██║     ██║     ██║
╚██████╔╝╚██████╔╝███████╗██║  ██║   ██║        ╚██████╗██║  ██║██║  ██║██║        ██║   ███████╗██║  ██║     ╚██████╗███████╗██║
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝         ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝      ╚═════╝╚══════╝╚═╝

"""

        
        self.console.print(Panel(
            Align.center(Text(title_art, style="bold green")),
            title="🚀 Welcome to QUERY-CRAFTER-CLI",
            subtitle="Convert Natural Language to SQL with AI Power",
            border_style="blue",
            padding=(1, 2)
        ))
        

        
        if Confirm.ask("Ready to start the tutorial?", default=True):
            self.console.print("\n" + "="*60 + "\n")
    
    def show_overview(self):
            """Show tool overview and workflow"""
            self.console.print(Rule("🔄 How QCraft Works", style="bold magenta"))
            
            # Create workflow tree
            workflow_tree = Tree("🚀 QCraft Workflow", style="bold blue")
            
            step1 = workflow_tree.add("1️⃣ [bold green]Set Database Schema[/bold green]")
            step1.add("📝 Paste schema directly or extract from file")
            step1.add("🎯 Example: CREATE TABLE users (id INT, name VARCHAR...)")
            
            step2 = workflow_tree.add("2️⃣ [bold yellow]Configure Query Type[/bold yellow]")
            step2.add("🔧 Specify database type (MySQL, PostgreSQL, MongoDB...)")
            step2.add("🎯 Example: PostgreSQL, SQLite, etc.")
            
            step3 = workflow_tree.add("3️⃣ [bold cyan]Convert Natural Language[/bold cyan]")
            step3.add("🗣️ Write your query in plain English")
            step3.add("🤖 AI converts it to proper database query")
            step3.add("📋 Result automatically copied to clipboard")
            
            step4 = workflow_tree.add("4️⃣ [bold red]Refine & Explain[/bold red]")
            step4.add("🔄 Retry with specific improvements")
            step4.add("💡 Get detailed explanations")
            
            self.console.print(Panel(workflow_tree, title="🔄 Workflow Overview", border_style="magenta"))
            
            # Provider comparison table
            provider_table = Table(title="🤖 AI Provider Options", show_header=True, header_style="bold blue")
            provider_table.add_column("Provider", style="cyan", width=12)
            provider_table.add_column("Cost", style="green", width=10)
            provider_table.add_column("Setup", style="yellow", width=15)
            provider_table.add_column("Models", style="magenta", width=20)
            
            provider_table.add_row("Free", "Free", "No setup needed", "Built-in model")
            provider_table.add_row("OpenAI", "Paid", "API key required", "GPT-4, GPT-3.5-turbo")
            provider_table.add_row("Ollama", "Free", "Local installation", "Llama2, Mistral, etc.")
            provider_table.add_row("LMStudio", "Free", "Local installation", "Various local models")
            
            self.console.print(provider_table)
            self.console.print("\n")
        
    def show_quick_start(self):
        """Show quick start guide"""
        self.console.print(Rule("⚡ Quick Start Guide", style="bold green"))
        
        steps = [
            "Set your database schema",
            "Configure query type", 
            "Convert your first query",
            "Enjoy the results!"
        ]
        
        
        quick_commands = Table(show_header=True, header_style="bold blue")
        quick_commands.add_column("Step", style="cyan", width=8)
        quick_commands.add_column("Command", style="green", width=50)
        quick_commands.add_column("Description", style="yellow")
        
        quick_commands.add_row(
            "1", 
            f"{self.package_name} method --paste 'CREATE TABLE...'", 
            "Set database schema"
        )
        quick_commands.add_row(
            "2", 
            f"{self.package_name} query-type 'PostgreSQL'", 
            "Configure database type"
        )
        quick_commands.add_row(
            "3", 
            f"{self.package_name} convert 'get all users' --provider free", 
            "Convert to SQL"
        )
        
        self.console.print(Panel(quick_commands, title="🚀 Essential Commands", border_style="green"))
    
    def show_commands_guide(self):
        """Show detailed command guide"""
        self.console.print(Rule("📖 Detailed Command Reference", style="bold blue"))
        
        # Schema Commands
        schema_panel = self.create_command_panel(
            "📊 Schema Management",
            "method",
            "Sets the database schema to be used for conversion",
            [
                ("--paste", "Provide schema by pasting directly", f"{self.package_name} method --paste 'CREATE TABLE...'"),
                ("--extract", "Extract schema from file", f"{self.package_name} method --extract schema.txt")
            ],
            "border_style='blue'"
        )
        self.console.print(schema_panel)
        
        # Query Type Commands  
        type_panel = self.create_command_panel(
            "🔧 Query Type Configuration",
            "query-type",
            "Sets the type of query to be generated",
            [],
            "border_style='green'",
            examples=[
                f"{self.package_name} query-type 'PostgreSQL'",
                f"{self.package_name} query-type 'MongoDB'"
            ]
        )
        self.console.print(type_panel)
        
        # Convert Commands
        convert_panel = self.create_command_panel(
            "🚀 Natural Language Conversion", 
            "convert",
            "Converts natural language to database queries",
            [
                ("--provider", "AI provider (openai/ollama/lmstudio/free)", ""),
                ("--api-key", "API key for the provider", ""),
                ("--model", "Specific model to use", "")
            ],
            "border_style='cyan'",
            examples=[
                f"{self.package_name} convert 'fetch all orders below $1000' --provider free",
                f"{self.package_name} convert 'find customers created on Jan 31' --provider openai --model gpt-4o-mini"
            ]
        )
        self.console.print(convert_panel)
        
        # Assist Commands
        assist_panel = self.create_command_panel(
            "🛠️ Query Assistance",
            "assist",
            "Retry or explain previous queries",
            [
                ("retry", "Regenerate query with improvements", ""),
                ("explain", "Get detailed explanation of query", "")
            ],
            "border_style='magenta'",
            examples=[
                f"{self.package_name} assist retry 'incorrect fetching' --provider ollama",
                f"{self.package_name} assist explain --provider openai"
            ]
        )
        self.console.print(assist_panel)
        
        # Config Commands
        self.show_config_commands()
    
    def create_command_panel(self, title, command, description, options, style_args="", examples=None):
        """Helper to create formatted command panels"""
        content = f"**Command:** `{command}`\n\n{description}\n\n"
        
        if options:
            content += "**Options:**\n"
            for opt, desc, example in options:
                content += f"- `{opt}`: {desc}\n"
                if example:
                    content += f"  Example: `{example}`\n"
            content += "\n"
        
        if examples:
            content += "**Examples:**\n"
            for example in examples:
                content += f"```\n{example}\n```\n"
        
        return Panel(Markdown(content), title=title, **eval(f"dict({style_args})"))
    
    def show_config_commands(self):
        """Show configuration command details"""
        config_tree = Tree("⚙️ Configuration Management", style="bold yellow")
        
        # Config Set
        set_branch = config_tree.add("[bold green]config set[/bold green] - Set configuration values")
        set_branch.add("🔑 SCHEMA - Database schema")
        set_branch.add("🏷️ TYPE - Database type") 
        set_branch.add("🤖 DEFAULT_PROVIDER - Default AI provider")
        set_branch.add("🎯 DEFAULT_MODEL - Default model")
        set_branch.add("🔐 API_KEY - API key for providers")
        
        # Config Get
        get_branch = config_tree.add("[bold cyan]config get[/bold cyan] - Retrieve configuration values")
        get_branch.add(f"📖 Example: {self.package_name} config get SCHEMA")
        
        # Config List
        list_branch = config_tree.add("[bold magenta]config list[/bold magenta] - List all configurations")
        list_branch.add("📋 Shows all current settings")
        
        # Config Flush
        flush_branch = config_tree.add("[bold red]config flush[/bold red] - Clear all configurations")
        flush_branch.add("🗑️ Removes all saved settings")
        
        self.console.print(Panel(config_tree, title="⚙️ Configuration Commands", border_style="yellow"))
    
    def show_workflow_example(self):
        """Show step-by-step workflow example"""
        self.console.print(Rule("🎯 Complete Workflow Example", style="bold green"))
        
        example_steps = [
            {
                "title": "1️⃣ Setting Up Schema",
                "command": f"{self.package_name} method --paste",
                "example": """CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    order_date DATE
);""",
                "description": "Define your database structure"
            },
            {
                "title": "1️⃣ Setting Up Schema",
                "command": f"{self.package_name} method --extract 'schema.txt' ",
                "example": """place our schema in a file and then extract it form there """,
                "description": "Define your database structure"
            },
            
            {
                "title": "2️⃣ Configure Database Type", 
                "command": f"{self.package_name} query-type PostgreSQL",
                "example": "",
                "description": "Specify the target database system"
            },
            {
                "title": "3️⃣ Convert Natural Language",
                "command": f"{self.package_name} convert",
                "example": "\"Show me all orders above $500 from last month\" --provider free",
                "description": "Transform English to SQL"
            },
            {
                "title": "4️⃣ Refine if Needed",
                "command": f"{self.package_name} assist retry",
                "example": "\"add ORDER BY date\" --provider free",
                "description": "Improve the generated query"
            }
        ]
        
        for step in example_steps:
            step_content = f"**Command:** `{step['command']}`\n\n"
            if step['example']:
                if step['command'] == f"{self.package_name} method --paste":
                    step_content += f"**Schema:**\n```sql\n{step['example']}\n```\n\n"
                else:
                    step_content += f"**Example:**\n```bash\n{step['command']} {step['example']}\n```\n\n"
            step_content += f"*{step['description']}*"
            
            self.console.print(Panel(
                Markdown(step_content),
                title=step['title'],
                border_style="green",
                padding=(1, 2)
            ))
    
    def show_configuration_guide(self):
        """Show configuration management guide"""
        self.console.print(Rule("⚙️ Configuration Management", style="bold yellow"))
        
        config_info = f"""
## Configuration Keys

| Key | Description | Example |
|-----|-------------|---------|
| `SCHEMA` | Database schema definition | `CREATE TABLE users (id INT, name VARCHAR(50)...)` |
| `TYPE` | Target database type | `PostgreSQL`, `MySQL`, `SQLite` |
| `DEFAULT_PROVIDER` | Preferred AI provider | `openai`, `anthropic`, `free` |
| `DEFAULT_MODEL` | Default model to use | `gpt-4o-mini`, `claude-3-haiku` |
| `API_KEY` | API key for providers | `sk-...` (OpenAI), `sk-ant-...` (Anthropic) |

## Useful Commands

```bash
# Set default provider
{self.package_name} config set DEFAULT_PROVIDER openai

# View current schema  
{self.package_name} config get SCHEMA

# List all settings
{self.package_name} config list

# Clear everything
{self.package_name} config flush
```
        """
        
        self.console.print(Panel(Markdown(config_info), title="⚙️ Configuration Guide", border_style="yellow"))
    
    def show_tips_and_tricks(self):
        """Show helpful tips and best practices"""
        self.console.print(Rule("💡 Tips & Best Practices", style="bold magenta"))
        
        tips_columns = [
            Panel(
                Markdown("""
### 🎯 Writing Better Queries

- Be specific about what you want
- Mention table names when possible  
- Include filtering criteria clearly
- Specify sorting requirements

**Good:** "Get customers who ordered in January, sorted by name"

**Bad:** "Get some data"
                """),
                title="Query Writing",
                border_style="green"
            ),
            Panel(
                Markdown("""
### 🚀 Provider Selection

- **Free**: Quick testing, no setup
- **OpenAI**: Best quality, requires API key
- **Ollama**: Local, private, free
- **LMStudio**: Local GUI, easy setup

Start with **free** for testing!
                """),
                title="Provider Choice", 
                border_style="blue"
            )
        ]
        
        self.console.print(Columns(tips_columns, equal=True, expand=True))
        
        # Advanced tips
        advanced_tips = """
### 🔧 Pro Tips

1. **Schema Management**: Keep your schema files organized and version controlled
2. **Query Refinement**: Use the `assist retry` command with specific feedback
3. **Clipboard Integration**: Generated queries are auto-copied - just paste and run!
4. **Error Handling**: If a query fails, use `assist explain` to understand why
5. **Model Selection**: Larger models (GPT-4) give better results for complex queries

### ⚡ Keyboard Shortcuts

- Ctrl+C: Stop current operation
- Up Arrow: Recall previous command (in most terminals)
- Ctrl+V: Paste generated query (auto-copied!)
        """
        
        self.console.print(Panel(Markdown(advanced_tips), title="🎓 Advanced Usage", border_style="magenta"))
    
    def show_conclusion(self):
        """Show conclusion and next steps"""
        self.console.print(Rule("🎉 You're Ready to Go!", style="bold green"))
        
        conclusion_text = f"""
## 🚀 What's Next?

You now have everything you need to start converting natural language to SQL like a pro!

### Quick Reference

```bash
# Essential workflow
{self.package_name} method --paste "YOUR_SCHEMA"
{self.package_name} query-type "DATABASE_TYPE" 
{self.package_name} convert "your natural language query" --provider free
```

### 📚 Additional Resources

- Run `{self.package_name} tutorial commands` for detailed command reference
- Use `{self.package_name} config list` to check your current setup
- Try `{self.package_name} assist explain` to understand generated queries

### 🤝 Need Help?

- Check your schema is properly set if conversions fail
- Try different providers if you get errors
- Use the `assist retry` command to refine results

**Happy Querying! 🎯**
        """
        
        self.console.print(Panel(
            Markdown(conclusion_text),
            title="🎊 Tutorial Complete!",
            border_style="green",
            padding=(1, 2)
        ))
        
        # Final animation
        self.console.print("\n" + "🎉 " * 20)
        self.console.print(Align.center(Text("Thank you for using QCraft!", style="bold blue")))
        self.console.print("🎉 " * 20 + "\n")
    
    def run_complete_tutorial(self):
        """Run the complete interactive tutorial"""
        self.show_welcome()
        self.show_overview()
        self.show_commands_guide()
        self.show_workflow_example()
        self.show_configuration_guide()
        self.show_tips_and_tricks()
        self.show_conclusion()
    
    def run_quick_tutorial(self):
        """Quick start guide - essential commands only"""
        self.show_welcome()
        self.show_quick_start()



# =============================================================================
# USAGE EXAMPLES
# =============================================================================

# Users can now run these commands:
# nl2sql tutorial complete     # Full interactive tutorial
# nl2sql tutorial quick        # Quick start guide  
# nl2sql tutorial commands     # Command reference
# nl2sql tutorial workflow     # Example workflow
# nl2sql tutorial config       # Configuration guide
# nl2sql tutorial tips         # Tips and tricks