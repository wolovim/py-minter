import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import {
  Address,
  createPublicClient,
  createWalletClient,
  custom,
  Hash,
  http,
  stringify,
  TransactionReceipt,
} from "viem";
import { foundry } from "viem/chains";
import "viem/window";
import MintCollection from "./MintCollection";
import DeployCollection from "./DeployCollection";
import HolderList from "./HolderList";

const SERVER_URL = "http://localhost:9898/721";
const CONTRACT_ABI = JSON.parse(import.meta.env.VITE_721_CONTRACT_ABI);
const CONTRACT_DEPLOY_BYTECODE = import.meta.env.VITE_721_CONTRACT_BYTECODE;
const tokenContract = {
  abi: CONTRACT_ABI,
  bytecode: CONTRACT_DEPLOY_BYTECODE,
};

const publicClient = createPublicClient({
  chain: foundry,
  transport: http("http://localhost:8545"),
});
const walletClient = createWalletClient({
  chain: foundry,
  transport: custom(window.ethereum),
});

function TokenCollectionPage({ account, walletClient, publicClient }) {
  const [hash, setHash] = useState<Hash>();
  const [selectedCollection, setSelectedCollection] = useState<Address>();
  const [collections, setCollections] = useState([]);
  const [receipt, setReceipt] = useState<TransactionReceipt>();

  const deployContract = async (name, symbol) => {
    if (!account) return;
    const hash = await walletClient.deployContract({
      ...tokenContract,
      account,
      args: [name, symbol, account],
    });
    setHash(hash);
    await storeDeployment(hash);
  };

  const mintToken = async (contractAddress, userAddress) => {
    if (!account) return;
    const { request } = await publicClient.simulateContract({
      account,
      address: contractAddress,
      abi: CONTRACT_ABI,
      functionName: "safeMint",
      args: [userAddress],
    });
    await walletClient.writeContract(request);
    await fetchCollections();
  };

  const storeDeployment = async (hash) => {
    try {
      const response = await fetch(`${SERVER_URL}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hash }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("POST request successful:", data);
      await fetchCollections();
    } catch (error) {
      console.error("Error making POST request:", error.message);
    }
  };

  const fetchCollections = async () => {
    if (account) {
      const result = await fetch(SERVER_URL)
        .then((res) => res.json());
      console.log("result: ", result.collections);
      setCollections(result.collections);
    } else {
      setCollections([]);
    }
  };

  useEffect(() => {
    (async () => {
      if (account) {
        await fetchCollections();
        if (collections.length > 0) {
          setSelectedCollection(collections[0].contract_address);
        }
      }
    })();
  }, [account]);

  useEffect(() => {
    (async () => {
      if (hash) {
        const receipt = await publicClient.waitForTransactionReceipt({ hash });
        setReceipt(receipt);
      }
    })();
  }, [hash]);

  if (account) {
    return (
      <div className="collection-page">
        {collections && (
          <>
            <h2>My 721 Collections</h2>
            <div>
              {collections.map((collection) => (
                <div
                  className={`collection-card ${
                    selectedCollection === collection.contract_address &&
                    "collection-card-selected"
                  }`}
                  key={collection.id}
                  onClick={() =>
                    setSelectedCollection(collection.contract_address)}
                >
                  <div>
                    {collection.name || "(No name)"}{" "}
                    ({collection.symbol || "No symbol"})
                  </div>
                  <div>{collection.contract_address}</div>
                  <div>Holders: {collection.holders.length}</div>

                  {selectedCollection === collection.contract_address && (
                    <>
                      <HolderList holders={collection.holders} />
                      <MintCollection
                        contractAddress={collection.contract_address}
                        mintToken={mintToken}
                      />
                    </>
                  )}
                </div>
              ))}
            </div>
          </>
        )}

        <DeployCollection deployContract={deployContract} />

        {receipt && (
          <>
            <div>Contract Address: {receipt.contractAddress}</div>
            <div>
              Receipt: <pre>
                <code>{stringify(receipt, null, 2)}</code>
              </pre>
            </div>
          </>
        )}
      </div>
    );
  }
}

export default TokenCollectionPage;
