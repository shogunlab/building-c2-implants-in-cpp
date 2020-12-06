import click
import requests
import pprint
import json

# Configuration Settings
listening_post_addr = "http://127.0.0.1:5000"

# Helper functions
def api_get_request(endpoint):
    response_raw = requests.get(listening_post_addr + endpoint).text
    response_json = json.loads(response_raw)
    return response_json

# CLI commands and logic
@click.group()
def cli():
    pass

@click.command(name="list-tasks")
def list_tasks():
    """Lists the tasks that are being served to the implant."""
    api_endpoint = "/tasks"
    print("\nHere's the tasks:\n")
    pprint.pprint(api_get_request(api_endpoint))
    print()

@click.command(name="list-results")
def list_results():
    """List the results returned from the implant."""
    api_endpoint = "/results"
    print("\nHere's the results:\n")
    pprint.pprint(api_get_request(api_endpoint))
    print()

@click.command(name="list-history")
def list_history():
    """List the history of tasks and their associated results."""
    api_endpoint = "/history"
    print("\nHere's the tasks history:\n")
    pprint.pprint(api_get_request(api_endpoint))
    print()

# Add commands to CLI
cli.add_command(list_tasks)
cli.add_command(list_results)
cli.add_command(list_history)

if __name__ == '__main__':
    cli()
