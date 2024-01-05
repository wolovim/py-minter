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
  const [receipt, setReceipt] = useState<TransactionReceipt>();

  const connect = async () => {
    const [address] = await walletClient.requestAddresses();
    setAccount(address);
  };

  const deployContract = async () => {
    if (!account) return;
    const hash = await walletClient.deployContract({
      ...tokenContract,
      account,
      args: ["Testing", "TEST", account],
    });
    setHash(hash);
    // make a post request to the server know about the transaction
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
    } catch (error) {
      console.error("Error making POST request:", error.message);
    }
  };

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
        <button onClick={deployContract}>Deploy</button>
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
