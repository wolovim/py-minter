# can/should deploy script insert data into sqlite db?
#   maybe just leave that to an endpoint accessed via the UI

import os
import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

load_dotenv()

CONTRACT_721_ABI = json.loads(os.environ.get("FLASK_721_CONTRACT_ABI"))
CONTRACT_1155_ABI = json.loads(os.environ.get("FLASK_1155_CONTRACT_ABI"))

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Migrate(app, db)


class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    contract_address = db.Column(db.Integer)
    name = db.Column(db.Text)
    symbol = db.Column(db.Text)

    def __init__(self, contract):
        self.contract_address = contract["address"]
        self.name = contract["name"]
        self.symbol = contract["symbol"]


class MultiTokenCollection(db.Model):
    __tablename__ = "multitokencollections"
    id = db.Column(db.Integer, primary_key=True)
    contract_address = db.Column(db.Integer)
    uri = db.Column(db.Text)
    holders = db.relationship("MultiTokenHolder", backref="multitokencollection")

    def __init__(self, contract):
        self.contract_address = contract["address"]
        self.uri = contract["uri"]


class MultiTokenHolder(db.Model):
    __tablename__ = "multitokenholders"
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("multitokencollections.id"))
    account = db.Column(db.Text)
    token_id = db.Column(db.Integer)
    hash = db.Column(db.Text)

    def __init__(self, holder):
        self.account = holder["account"]
        self.token_id = holder["token_id"]
        self.collection_id = holder["collection_id"]
        self.hash = holder["hash"]


w3 = Web3(HTTPProvider("http://localhost:8545"))


@app.route("/")
def index():
    return jsonify({"message": "gm"})


###############
### ERC-721 ###
###############


@app.route("/721")
def collections():
    collections = Collection.query.all()
    serialized_collections = []
    for collection in collections:
        c = collection.__dict__

        # get the holders for each collection
        contract = w3.eth.contract(address=c["contract_address"], abi=CONTRACT_721_ABI)
        total_supply = contract.functions.getNextTokenId().call()
        holders = []
        for token_id in range(1, total_supply):
            owner = contract.functions.ownerOf(token_id).call()
            print(f"Token ID {token_id}: {owner}")
            holders.append(owner)

        data = {
            "id": c["id"],
            "contract_address": c["contract_address"],
            "name": c["name"],
            "symbol": c["symbol"],
            "holders": holders,
        }
        serialized_collections.append(data)
    return jsonify({"collections": serialized_collections})


@app.route("/721/deploy", methods=["POST"])
def deploy_collection():
    try:
        tx_hash = request.get_json()
        receipt = w3.eth.get_transaction_receipt(tx_hash["hash"])
        if receipt is None:
            raise Exception("Invalid transaction hash")
        if receipt["contractAddress"] is None:
            raise Exception("Contract failed to deploy")

        contract = w3.eth.contract(
            address=receipt["contractAddress"],
            abi=CONTRACT_721_ABI,
        )

        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()

        new_collection = {
            "address": receipt["contractAddress"],
            "name": name,
            "symbol": symbol,
        }

        db.session.add(Collection(new_collection))
        db.session.commit()

        return jsonify({"message": "Record created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


################
### ERC-1155 ###
################


@app.route("/1155/<contract_address>/<token_id>.json")
def collection_token_metadata(contract_address, token_id):
    return jsonify(
        {
            "name": f"Soulbound Token #{token_id}",
            "description": f"A soulbound token from a collection at address: {contract_address}",
            "image": "https://cdn-icons-png.flaticon.com/512/7036/7036357.png",
        }
    )


@app.route("/1155")
def multitoken_collections():
    collections = MultiTokenCollection.query.all()
    serialized_collections = []
    for collection in collections:
        c = collection.__dict__

        # no great way to get erc-1155 holders, so pull from db
        serialized_holders = []
        for holder in collection.holders:
            h = holder.__dict__
            serialized_holders.append(h["account"])

        data = {
            "id": c["id"],
            "contract_address": c["contract_address"],
            "uri": c["uri"],
            "holders": serialized_holders,
            "metadata": collection_token_metadata(c["contract_address"], 1).json,
        }
        serialized_collections.append(data)
    return jsonify({"collections": serialized_collections})


@app.route("/1155/deploy", methods=["POST"])
def deploy_multitoken_collection():
    try:
        tx_hash = request.get_json()
        receipt = w3.eth.get_transaction_receipt(tx_hash["hash"])
        if receipt is None:
            raise Exception("Invalid transaction hash")
        if receipt["contractAddress"] is None:
            raise Exception("Contract failed to deploy")

        contract = w3.eth.contract(
            address=receipt["contractAddress"],
            abi=CONTRACT_1155_ABI,
        )

        uri = contract.functions.uri(1).call()

        new_collection = {
            "address": receipt["contractAddress"],
            "uri": uri,
        }

        db.session.add(MultiTokenCollection(new_collection))
        db.session.commit()

        return jsonify({"message": "Record created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/1155/mint", methods=["POST"])
def mint_multitoken():
    try:
        data = request.get_json()
        print(data)

        # todo: verify that user does own the token

        collection = MultiTokenCollection.query.filter_by(
            contract_address=data["contractAddress"]
        ).first()

        new_holder = {
            "account": data["account"],
            "token_id": data["tokenId"],
            "collection_id": collection.id,
            "hash": data["hash"],
        }
        db.session.add(MultiTokenHolder(new_holder))
        db.session.commit()
        return jsonify({"message": "Record created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="localhost", port=9898)
