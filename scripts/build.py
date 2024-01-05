import click
import json
from ape.cli import NetworkBoundCommand, network_option
from ape import project


@click.command(cls=NetworkBoundCommand)
@network_option()
def cli(network):
    if "foundry" not in network:
        raise click.ClickException("This script is only for the foundry network")
    
    deployment_bytecode = project.SoulboundToken.contract_type.deployment_bytecode.bytecode
    abi = json.loads(project.SoulboundToken.contract_type.json())["abi"]

    with open("./webapp/.env.local", "w") as f:
        f.write(f'VITE_CONTRACT_BYTECODE="{deployment_bytecode}"\n')
        f.write(f'VITE_CONTRACT_ABI="{json.dumps(abi)}"')

    with open("./.env", "w") as f:
        f.write(f"FLASK_CONTRACT_ABI='{json.dumps(abi)}'")
