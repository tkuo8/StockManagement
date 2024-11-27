import React, { useState } from "react";
import axios from "axios";

function StockRegister() {
  const userId = 1;
  const [formData, setFormData] = useState({
    userId: userId,
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
      const response = await axios.post(
        "http://localhost:8080/api/stocks",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // 成功時の処理
      console.log("Data submitted successfully!");
      setFormData({
        userId: userId,
        symbol: "",
        purchasePrice: "",
        quantity: "",
        targetPrice: "",
        cutlossPrice: "",
      });
    } catch (error) {
      // サーバーエラーの場合
      if (error.response) {
        const errorText = error.response.data || error.response.statusText;
        alert(`Validation error ${errorText}`);
        console.log("Failed to submit data.");
      } else {
        // ネットワークエラーや他のエラーの場合
        console.error("Error occurred", error.message);
      }
    }
  };

  return (
    <div>
      <h2>株情報登録</h2>
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
