import click
import json
from ape.cli import NetworkBoundCommand, network_option
from ape import project


@click.command(cls=NetworkBoundCommand)
@click.option("--token", default="721", help="Token type to deploy")
@network_option()
def cli(token, network):
    if "foundry" not in network:
        raise click.ClickException("This script is only for the foundry network")

    if token == "721":
        click.echo("Building 721 contract...")
        deployment_bytecode = (
            project.SoulboundToken.contract_type.deployment_bytecode.bytecode
        )
        abi = json.loads(project.SoulboundToken.contract_type.json())["abi"]

        # NOTE: this adds to the file, not overwrites it
        with open("./webapp/.env.local", "a") as f:
            f.write(f'VITE_CONTRACT_BYTECODE="{deployment_bytecode}"\n')
            f.write(f'VITE_CONTRACT_ABI="{json.dumps(abi)}"\n')

        # NOTE: this adds to the file, not overwrites it
        with open("./.env", "a") as f:
            f.write(f"FLASK_CONTRACT_ABI='{json.dumps(abi)}'\n")
    elif token == "1155":
        click.echo("Building 1155 contract...")
        deployment_bytecode = (
            project.SoulboundToken1155.contract_type.deployment_bytecode.bytecode
        )
        abi = json.loads(project.SoulboundToken1155.contract_type.json())["abi"]

        # NOTE: this adds to the file, not overwrites it
        with open("./webapp/.env.local", "w") as f:
            f.write(f'VITE_1155_CONTRACT_BYTECODE="{deployment_bytecode}"\n')
            f.write(f'VITE_1155_CONTRACT_ABI="{json.dumps(abi)}"\n')

        # NOTE: this adds to the file, not overwrites it
        with open("./.env", "a") as f:
            f.write(f"FLASK_1155_CONTRACT_ABI='{json.dumps(abi)}'\n")
    else:
        raise click.ClickException("Invalid token type")

    click.echo("Contract ABI and bytecode written to env files")
