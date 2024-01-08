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

CONTRACT_ABI = json.loads(os.environ.get("FLASK_CONTRACT_ABI"))

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


w3 = Web3(HTTPProvider("http://localhost:8545"))


@app.route("/")
def index():
    collections = Collection.query.all()
    return render_template("collections.html", collections=collections)


@app.route("/collections/<account>")
def collections(account):
    print(f"∆∆∆ {account}")
    # TODO: scope to account
    collections = Collection.query.all()
    serialized_collections = []
    for collection in collections:
        c = collection.__dict__

        # get the holders for each collection
        contract = w3.eth.contract(address=c["contract_address"], abi=CONTRACT_ABI)
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


@app.route("/create_collection", methods=["POST"])
def create_collection():
    try:
        tx_hash = request.get_json()
        receipt = w3.eth.get_transaction_receipt(tx_hash["hash"])
        if receipt is None:
            raise Exception("Invalid transaction hash")
        if receipt["contractAddress"] is None:
            raise Exception("Contract failed to deploy")

        contract = w3.eth.contract(
            address=receipt["contractAddress"],
            abi=CONTRACT_ABI,
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


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="localhost", port=9898)
