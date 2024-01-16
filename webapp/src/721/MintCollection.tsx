import React, { useEffect, useState } from "react";

function MintCollection({ mintToken, contractAddress }) {
  const [formData, setFormData] = useState({
    address: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await mintToken(contractAddress, formData.address);
    setFormData({
      address: "",
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="address"
        placeholder="Address"
        onChange={handleInputChange}
      />
      <button type="submit">Mint</button>
    </form>
  );
}

export default MintCollection;
