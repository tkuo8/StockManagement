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
      <label htmlFor='ticker'>銘柄コード</label>
      <input type='text' id='ticker' />
      <label htmlFor='stockPrices'>取得単価</label>
      <input type='text' id='stockPrices' />
      <label htmlFor='stockNumberHeld'>保有株数</label>
      <input type='text' id='stockNumberHeld' />
      <label htmlFor='goalPrices'>目標利益</label>
      <input type='text' id='goalPrices' />
    </div>
  );
}

function App () {
  return (
    <div>
      <StockManagementApp />
    </div>
  );
}

export default App;
