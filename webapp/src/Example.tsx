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

const abi = import.meta.env.VITE_CONTRACT_ABI;
const bytecode = import.meta.env.VITE_CONTRACT_BYTECODE;
const tokenContract = {
  abi: JSON.parse(abi),
  bytecode,
};

const publicClient = createPublicClient({
  chain: foundry,
  transport: http("http://localhost:8545"),
});
const walletClient = createWalletClient({
  chain: foundry,
  transport: custom(window.ethereum),
});

function Example() {
  const [account, setAccount] = useState<Address>();
  const [hash, setHash] = useState<Hash>();
  const [collections, setCollections] = useState([]);
  const [receipt, setReceipt] = useState<TransactionReceipt>();
  const [formData, setFormData] = useState({
    name: "",
    symbol: "",
  });

  const connect = async () => {
    const [address] = await walletClient.requestAddresses();
    setAccount(address);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const deployContract = async (e) => {
    e.preventDefault();
    if (!account) return;
    const hash = await walletClient.deployContract({
      ...tokenContract,
      account,
      args: [formData.name, formData.symbol, account],
    });
    setHash(hash);
    setFormData({
      name: "",
      symbol: "",
    });
    await handlePostRequest(hash);
  };

  const handlePostRequest = async (hash) => {
    try {
      const server_url = "http://localhost:9898/create_collection";
      const x = await publicClient.getTransactionReceipt({ hash });
      console.log("x", x);

      const response = await fetch(server_url, {
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
      const result = await fetch(`http://localhost:9898/collections/${account}`)
        .then((res) => res.json());
      setCollections(result.collections);
    } else {
      setCollections([]);
    }
  };

  useEffect(() => {
    (async () => {
      if (account) {
        await fetchCollections();
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
      <>
        <div>Connected: {account}</div>

        {collections && (
          <>
            <div>My Collections</div>
            <div>
              {collections.map((collection) => (
                <div key={collection.id}>
                  <div>ID: {collection.id}</div>
                  <div>Name: {collection.name}</div>
                  <div>Symbol: {collection.symbol}</div>
                  <div>Address: {collection.contract_address}</div>
                </div>
              ))}
            </div>
          </>
        )}

        <form onSubmit={deployContract}>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
            />
          </label>
          <br />
          <label>
            Symbol:
            <input
              type="text"
              name="symbol"
              value={formData.symbol}
              onChange={handleInputChange}
            />
          </label>
          <br />
          <button type="submit">Deploy</button>
        </form>
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
      </>
    );
  }
  return <button onClick={connect}>Connect Wallet</button>;
}

export default Example;
