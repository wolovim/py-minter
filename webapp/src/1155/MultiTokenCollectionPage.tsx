import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import DeployCollection from "./DeployCollection";
import MintCollection from "./MintCollection";
import HolderList from "./HolderList";
import { Hash, stringify, TransactionReceipt } from "viem";

const CONTRACT_ABI = JSON.parse(import.meta.env.VITE_1155_CONTRACT_ABI);
const CONTRACT_DEPLOY_BYTECODE = import.meta.env.VITE_1155_CONTRACT_BYTECODE;
const tokenContract = {
  abi: CONTRACT_ABI,
  bytecode: CONTRACT_DEPLOY_BYTECODE,
};
const SERVER_URL = "http://localhost:9898/1155";

function MultiTokenCollectionPage({ account, walletClient, publicClient }) {
  const [collections, setCollections] = useState([]);
  const [hash, setHash] = useState<Hash>();
  const [receipt, setReceipt] = useState<TransactionReceipt>();
  const [selectedCollection, setSelectedCollection] = useState<Address>();

  const fetchCollections = async () => {
    if (account) {
      const result = await fetch(SERVER_URL)
        .then((res) => res.json());
      console.log("result 1155: ", result.collections);
      setCollections(result.collections);
    } else {
      setCollections([]);
    }
  };

  const deployContract = async (uri) => {
    if (!account) return;
    const hash = await walletClient.deployContract({
      ...tokenContract,
      account,
      args: [account, uri],
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
      functionName: "mint",
      args: [userAddress, 1, 1, ""],
    });
    const hash = await walletClient.writeContract(request);
    await storeMint(hash, userAddress, contractAddress);
    await fetchCollections();
  };

  const storeMint = async (hash, account, contractAddress) => {
    try {
      const response = await fetch(`${SERVER_URL}/mint`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          account,
          contractAddress,
          tokenId: 1,
          hash,
        }),
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

  return (
    <div className="collection-page">
      {collections && (
        <>
          <h2>My 1155 Collections</h2>
          <div>
            {collections.map((collection) => (
              <div
                className={`collection-card ${
                  selectedCollection === collection.contract_address &&
                  "collection-card-selected"
                }`}
                key={collection.contract_address}
                onClick={() =>
                  setSelectedCollection(collection.contract_address)}
              >
                {selectedCollection === collection.contract_address && (
                  <img
                    src={collection.metadata.image}
                    className="collection-image"
                  />
                )}
                <div>{collection.contract_address}</div>
                <div>URI: {collection.uri}</div>
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

export default MultiTokenCollectionPage;
