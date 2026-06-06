import json
from typing import Optional

import click
import requests


API_BASE_URL = "http://localhost:5000/api"


@click.group()
def cli():
    """Automation Platform CLI - Manage automation tasks."""
    pass


@cli.command()
@click.option("--type", "task_type", required=True, type=click.Choice(["backup", "deploy", "cleanup"]))
@click.option("--params", required=True, help="JSON parameters")
@click.option("--priority", default="medium", type=click.Choice(["high", "medium", "low"]))
def submit(task_type: str, params: str, priority: str):
    try:
        parsed_params = json.loads(params)
    except json.JSONDecodeError as exc:
        click.echo(click.style(f"Invalid JSON parameters: {exc}", fg="red"))
        raise SystemExit(1)

    payload = {
        "task_type": task_type,
        "parameters": parsed_params,
        "priority": priority
    }

    try:
        response = requests.post(f"{API_BASE_URL}/tasks", json=payload, timeout=10)
        data = response.json()
    except Exception as exc:
        click.echo(click.style(f"API request failed: {exc}", fg="red"))
        raise SystemExit(1)

    if response.status_code >= 400:
        click.echo(click.style(f"Task rejected: {data}", fg="red"))
        raise SystemExit(1)

    click.echo(click.style("Task submitted successfully", fg="green"))
    click.echo(f"Task ID: {data.get('task_id')}")
    click.echo(f"Status: {data.get('status')}")


@cli.command()
@click.argument("task_id")
def status(task_id: str):
    response = requests.get(f"{API_BASE_URL}/tasks/{task_id}", timeout=10)
    data = response.json()

    if response.status_code >= 400:
        click.echo(click.style(json.dumps(data, indent=2), fg="red"))
        raise SystemExit(1)

    click.echo(json.dumps(data, indent=2))


@cli.command(name="list")
@click.option("--status", "status_filter", help="Filter by status")
@click.option("--type", "type_filter", help="Filter by task type")
def list_tasks(status_filter: Optional[str], type_filter: Optional[str]):
    params = {}
    if status_filter:
        params["status"] = status_filter
    if type_filter:
        params["type"] = type_filter

    response = requests.get(f"{API_BASE_URL}/tasks", params=params, timeout=10)
    data = response.json()

    tasks = data.get("tasks", [])
    click.echo(f"Task Count: {data.get('count', 0)}")

    for task in tasks:
        click.echo(
            f"{task.get('task_id')} | {task.get('task_type')} | "
            f"{task.get('priority')} | {task.get('status')}"
        )


if __name__ == "__main__":
    cli()
