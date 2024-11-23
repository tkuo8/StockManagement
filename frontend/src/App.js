import "./App.css";

function StockManagementApp() {
  return (
    <div>
      <Title />
      <StockInput />
    </div>
  );
}

function Title() {
  return (
    <div>
      <h1>株管理アプリ</h1>
    </div>
  );
}

function StockInput() {
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="symbol">銘柄コード</label>
        <input type="text" name="symbol" id="symbol" />
        <label htmlFor="purchasePrice">取得価格</label>
        <input type="text" name="purchasePrice" id="purchasePrice" />
        <label htmlFor="quantity">保有株数</label>
        <input type="text" name="quantity" id="quantity" />
        <label htmlFor="targetPrice">売却目標価格</label>
        <input type="text" name="targetPrice" id="targetPrice" />
        <label htmlFor="cutlossPrice">損切り価格</label>
        <input type="text" name="cutlossPrice" id="cutlossPrice" />
        <button type="submit">登録</button>
      </form>
    </div>
  );
}

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch("http://localhost:8080/api/stock-register", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        symbol: "0123",
        purchasePrice: "400",
        quantity: "100",
        targetPrice: "500",
        cutlossPrice: "350",
      }),
    });
    if (response.ok) {
      console.log("Data submitted successfully!");
    } else {
      console.log("Failed to submit data.");
    }
  } catch (error) {
    console.error(error);
  }
};

function App() {
  return (
    <div>
      <StockManagementApp />
    </div>
  );
}

export default App;
