import React, { useState } from "react";

function StockRegister() {
  const [formData, setFormData] = useState({
    userId: "1",
    symbol: "",
    purchasePrice: "",
    quantity: "",
    targetPrice: "",
    cutlossPrice: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8080/api/stocks", {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        console.log("Data submitted successfully!");
        setFormData({
          userId: "1",
          symbol: "",
          purchasePrice: "",
          quantity: "",
          targetPrice: "",
          cutlossPrice: "",
        });
      } else {
        const errorText = await response.text();
        alert(`Validation error ${errorText}`);
        console.log("Failed to submit data.");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="symbol">銘柄コード</label>
        <input
          type="text"
          name="symbol"
          id="symbol"
          value={formData.symbol}
          onChange={handleChange}
        />
        <label htmlFor="purchasePrice">取得価格</label>
        <input
          type="text"
          name="purchasePrice"
          id="purchasePrice"
          value={formData.purchasePrice}
          onChange={handleChange}
        />
        <label htmlFor="quantity">保有株数</label>
        <input
          type="text"
          name="quantity"
          id="quantity"
          value={formData.quantity}
          onChange={handleChange}
        />
        <label htmlFor="targetPrice">売却目標価格</label>
        <input
          type="text"
          name="targetPrice"
          id="targetPrice"
          value={formData.targetPrice}
          onChange={handleChange}
        />
        <label htmlFor="cutlossPrice">損切り価格</label>
        <input
          type="text"
          name="cutlossPrice"
          id="cutlossPrice"
          value={formData.cutlossPrice}
          onChange={handleChange}
        />
        <button type="submit">登録</button>
      </form>
    </div>
  );
}

export default StockRegister;
