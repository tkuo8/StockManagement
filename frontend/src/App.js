import './App.css';

function StockManagementApp () {
  return (
    <div>
      <Title />
      <StockInput />
    </div>
  );
}

function Title () {
  return (
    <div>
      <h1>株管理アプリ</h1>
    </div>
  );
}

function StockInput () {
  return (
    <div>
      <label htmlFor='symbol'>銘柄コード</label>
      <input type='text' name='symbol' id='symbol' />
      <label htmlFor='purchasePrice'>取得価格</label>
      <input type='text' name='purchasePrice' id='purchasePrice' />
      <label htmlFor='quantity'>保有株数</label>
      <input type='text' name='quantity' id='quantity' />
      <label htmlFor='targetPrice'>売却目標価格</label>
      <input type='text' name='targetPrice' id='targetPrice' />
      <label htmlFor="cutlossPrice">損切り価格</label>
      <input type="text" name="cutlossPrice" id="cutlossPrice" />
    </div>
  );
}

const handleSubmit = async (e) => {
  e.preventDefault();
  fetch("http://localhost:8080/api/stock-register", {
  "method": "POST",
  "headers": {
    "content-type": "application/json"
  },
  "body": {
    "ticker": "0123",
    "stockPrices": "400",
    "stockNumberHeld": "100",
    "goalPrices": "500"
  }
})
.then(response => {
  console.log(response);
})
.catch(err => {
  console.error(err);
});

  
}

function App () {
  return (
    <div>
      <StockManagementApp />
    </div>
  );
}

export default App;
