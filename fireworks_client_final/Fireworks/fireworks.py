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

def api_post_request(endpoint, payload):
    response_raw = requests.post(listening_post_addr + endpoint, json=payload).text
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

@click.command(name="add-tasks")
@click.option('--tasktype', help='Type of task to submit.')
@click.option('--options', help='Key-value options for task.')
def add_tasks(tasktype, options):
    """Submit tasks to the listening post."""
    api_endpoint = "/tasks"
    print("\nHere are the tasks that were added:\n")

    # Perform options parsing if user provided them to the task
    if options != None:
        task_options_dict = {}
        task_options_pairs = options.split(",")

        # For each key-value pair, add them to a dictionary
        for option in task_options_pairs:
            key_vals = option.split("=")
            key = key_vals[0]
            value = key_vals[1]
            pair = {key:value}
            task_options_dict.update(pair)

        # If more than one option was provided, format and append them into a single string
        if len(task_options_dict) > 1:
            keyval_string = ""
            for key,value in task_options_dict.items():
                keyval_string += f'"{key}":"{value}",'
            request_payload_string = f'[{{"task_type":"{tasktype}",{keyval_string[:-1]}}}]'
            request_payload = json.loads(request_payload_string)
            pprint.pprint(api_post_request(api_endpoint, request_payload))
        # Otherwise, just print the key/value for the single option provided
        else:
            request_payload_string = f'[{{"task_type":"{tasktype}","{key}":"{value}"}}]'
            request_payload = json.loads(request_payload_string)
            pprint.pprint(api_post_request(api_endpoint, request_payload))
    # Otherwise, we just submit a payload with the task type specified
    else:
        request_payload_string = f'[{{"task_type":"{tasktype}"}}]'
        request_payload = json.loads(request_payload_string)
        pprint.pprint(api_post_request(api_endpoint, request_payload))
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
cli.add_command(add_tasks)
cli.add_command(list_results)
cli.add_command(list_history)

if __name__ == '__main__':
    cli()
