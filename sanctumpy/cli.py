import click

from sanctumpy import SanctumClient

@click.group()
@click.pass_context
def cli(ctx):
    """Sanctum Python Client CLI for interacting with various LST functions."""
    ctx.obj = SanctumClient() 

@cli.command()
@click.pass_context
def help(ctx):
    """Show this message and exit."""
    click.echo(ctx.parent.get_help())

@cli.command()
@click.pass_obj
def infinity_infos(client):
    """Retrieve information about Infinity protocol."""
    click.echo(client.get_infinity_infos())

@cli.command()
@click.argument('token')
@click.pass_obj
def lst_apy(client, token):
    """Get the APY for a specific LST token.

    TOKEN: The name or symbol of the LST token (e.g., JupSOL).
    """
    click.echo(client.get_lst_apy(token))

@cli.command()
@click.argument('token')
@click.pass_obj
def lst_sol_value(client, token):
    """Get the SOL value for a specific LST token.

    TOKEN: The name or symbol of the LST token (e.g., JupSOL).
    """
    click.echo(client.get_lst_sol_value(token))

@cli.command()
@click.argument('token')
@click.pass_obj
def lst_tvl(client, token):
    """Get the Total Value Locked (TVL) for a specific LST token.

    TOKEN: The name or symbol of the LST token (e.g., JupSOL).
    """
    click.echo(client.get_lst_tvl(token))

@cli.command()
@click.argument('token')
@click.pass_obj
def lst_infos(client, token):
    """Retrieve detailed information about a specific LST token.

    TOKEN: The name or symbol of the LST token (e.g., JupSOL).
    """
    click.echo(client.get_lst_infos(token))

@cli.command()
@click.argument('token')
@click.pass_obj
def price(client, token):
    """Get the current price of a token.

    TOKEN: The address of the token (e.g., jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v).
    """
    click.echo(client.get_price(token))

@cli.command()
@click.argument('token')
@click.pass_obj
def metadata(client, token):
    """Retrieve metadata for a specific token.

    TOKEN: The address of the token (e.g., jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v).
    """
    click.echo(client.get_metadata(token))

@cli.command()
@click.argument('token')
@click.argument('quote_token')
@click.argument('amount', type=float)
@click.pass_obj
def quote(client, token, quote_token, amount):
    """Get a quote for exchanging between two tokens.

    TOKEN: The address of the token to sell.
    QUOTE_TOKEN: The address of the token to buy.
    AMOUNT: The amount of the selling token to quote.
    """
    click.echo(client.get_quote(token, quote_token, amount))

if __name__ == '__main__':
    cli()