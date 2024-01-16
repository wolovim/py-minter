import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import "./HolderList.css";

function HolderList({ holders }) {
  return (
    <ul className="holder-list">
      {holders &&
        holders.map((address) => <div className="holder-address" key={address}>{address}</div>)}
    </ul>
  );
}

export default HolderList;
