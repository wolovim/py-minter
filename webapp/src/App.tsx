import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import {
  Address,
  createPublicClient,
  createWalletClient,
  custom,
  http,
} from "viem";
import { foundry } from "viem/chains";
import "viem/window";
import MultiTokenCollectionPage from "./1155/MultiTokenCollectionPage";
import TokenCollectionPage from "./721/TokenCollectionPage";
import "./App.css";

const publicClient = createPublicClient({
  chain: foundry,
  transport: http("http://localhost:8545"),
});
const walletClient = createWalletClient({
  chain: foundry,
  transport: custom(window.ethereum),
});

function App() {
  const [account, setAccount] = useState<Address>();

  const connect = async () => {
    const [address] = await walletClient.requestAddresses();
    setAccount(address);
  };


  if (account) {
    return (
      <>
        <h3>Connected: {account}</h3>

        <TokenCollectionPage
          account={account}
          walletClient={walletClient}
          publicClient={publicClient}
        />
        <MultiTokenCollectionPage
          account={account}
          walletClient={walletClient}
          publicClient={publicClient}
        />
      </>
    );
  }
  return <button onClick={connect}>Connect Wallet</button>;
}

export default App;
