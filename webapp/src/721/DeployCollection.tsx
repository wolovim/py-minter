import React, { useEffect, useState } from "react";

function DeployCollection({ deployContract }) {
  const [formData, setFormData] = useState({
    name: "",
    symbol: "",
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
    await deployContract(formData.name, formData.symbol);
    setFormData({
      name: "",
      symbol: "",
    });
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            name="name"
            placeholder="Welpers Delight"
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
            placeholder="WELP"
            value={formData.symbol}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <button type="submit">Deploy</button>
      </form>
    </>
  );
}

export default DeployCollection;
