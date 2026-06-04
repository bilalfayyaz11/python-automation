#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import click
import requests
from tabulate import tabulate

API_BASE_URL = "http://127.0.0.1:5000/api"
TOKEN_FILE = "~/.user_cli_token"


class APIClient:
    """Client for interacting with the User API."""

    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.session = requests.Session()

        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}"
            })

    def health_check(self):
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            click.echo("Error: Cannot connect to API server", err=True)
            sys.exit(1)
        except requests.exceptions.RequestException as error:
            click.echo(f"Error: {error}", err=True)
            sys.exit(1)

    def get_users(self):
        try:
            response = self.session.get(f"{self.base_url}/users", timeout=5)

            if response.status_code == 401:
                click.echo("Error: Authentication failed. Check your token.", err=True)
                sys.exit(1)

            response.raise_for_status()
            return response.json().get("users", [])

        except requests.exceptions.ConnectionError:
            click.echo("Error: Cannot connect to API server", err=True)
            sys.exit(1)
        except requests.exceptions.RequestException as error:
            click.echo(f"Error: {error}", err=True)
            sys.exit(1)

    def get_user_by_id(self, user_id):
        try:
            response = self.session.get(f"{self.base_url}/users/{user_id}", timeout=5)

            if response.status_code == 401:
                click.echo("Error: Authentication failed. Check your token.", err=True)
                sys.exit(1)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            click.echo("Error: Cannot connect to API server", err=True)
            sys.exit(1)
        except requests.exceptions.RequestException as error:
            click.echo(f"Error: {error}", err=True)
            sys.exit(1)


def token_path():
    return Path(TOKEN_FILE).expanduser()


def save_token(token):
    path = token_path()
    path.write_text(token.strip())
    os.chmod(path, 0o600)


def load_token():
    path = token_path()
    if not path.exists():
        return None
    return path.read_text().strip()


def delete_token():
    path = token_path()
    if path.exists():
        path.unlink()


def resolve_token(token):
    active_token = token or load_token()

    if not active_token:
        click.echo("Error: No token provided. Run login first or pass --token.", err=True)
        sys.exit(1)

    return active_token


@click.group()
def cli():
    """User Management CLI - interact with a token-protected REST API."""
    pass


@cli.command()
def health():
    """Check API server health."""
    client = APIClient(API_BASE_URL)
    result = client.health_check()
    click.echo(f"Status: {result.get('status')}")
    click.echo(f"Service: {result.get('service')}")


@cli.command("list-users")
@click.option("--token", default=None, help="API token; uses saved token if omitted.")
def list_users(token):
    """List all users."""
    active_token = resolve_token(token)
    client = APIClient(API_BASE_URL, active_token)
    users = client.get_users()

    if not users:
        click.echo("No users found.")
        return

    table = [[user["id"], user["name"], user["role"]] for user in users]
    click.echo(tabulate(table, headers=["ID", "Name", "Role"], tablefmt="github"))


@cli.command("get-user")
@click.argument("user_id", type=int)
@click.option("--token", default=None, help="API token; uses saved token if omitted.")
def get_user(user_id, token):
    """Get user details by ID."""
    active_token = resolve_token(token)
    client = APIClient(API_BASE_URL, active_token)
    user = client.get_user_by_id(user_id)

    if user is None:
        click.echo(f"User with ID {user_id} was not found.")
        return

    table = [[user["id"], user["name"], user["role"]]]
    click.echo(tabulate(table, headers=["ID", "Name", "Role"], tablefmt="github"))


@cli.command()
@click.argument("token")
def login(token):
    """Save authentication token after validating it."""
    client = APIClient(API_BASE_URL, token)
    client.get_users()
    save_token(token)
    click.echo("Authentication token saved successfully.")


@cli.command()
def logout():
    """Remove saved authentication token."""
    delete_token()
    click.echo("Authentication token removed.")


@cli.command()
def whoami():
    """Display current authentication status."""
    token = load_token()

    if not token:
        click.echo("Not authenticated.")
        return

    client = APIClient(API_BASE_URL, token)
    client.get_users()
    click.echo("Authenticated with saved token.")


if __name__ == "__main__":
    cli()
