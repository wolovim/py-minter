import React, { useEffect, useState } from "react";

function DeployCollection({ deployContract }) {
  const [formData, setFormData] = useState({
    uri: "",
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
    await deployContract();
    setFormData({
      uri: "",
    });
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>
          URI:
          <input
            type="text"
            name="uri"
            placeholder="https://..."
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
