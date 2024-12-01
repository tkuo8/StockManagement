import React, { useState } from "react";
import axios from "axios";

function StockRegister() {
  const [formData, setFormData] = useState({
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
        "http://localhost:50000/api/stocks",
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
    <div className="container mt-5">
      <div className="card shadow-sm">
        <div className="card-body">
          <h2 className="card-title text-center text-primary mb-4">
            株情報登録
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="symbol" className="form-label">
                証券コード
              </label>
              <input
                type="text"
                className="form-control"
                name="symbol"
                id="symbol"
                value={formData.symbol}
                onChange={handleChange}
                placeholder="例： 1234"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="purchasePrice" className="form-label">
                取得単価
              </label>
              <input
                type="text"
                className="form-control"
                name="purchasePrice"
                id="purchasePrice"
                value={formData.purchasePrice}
                onChange={handleChange}
                placeholder="例： 1000"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="quantity" className="form-label">
                保有株数
              </label>
              <input
                type="text"
                className="form-control"
                name="quantity"
                id="quantity"
                value={formData.quantity}
                onChange={handleChange}
                placeholder="例： 100"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="targetPrice" className="form-label">
                売却目標価格
              </label>
              <input
                type="text"
                className="form-control"
                name="targetPrice"
                id="targetPrice"
                value={formData.targetPrice}
                onChange={handleChange}
                placeholder="例： 1500"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="cutlossPrice" className="form-label">
                損切り価格
              </label>
              <input
                type="text"
                className="form-control"
                name="cutlossPrice"
                id="cutlossPrice"
                value={formData.cutlossPrice}
                onChange={handleChange}
                placeholder="例： 900"
              />
            </div>
            <button type="submit" className="btn btn-primary w-100">
              登録
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default StockRegister;
