import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import StockRegister from "./pages/StockRegister";

function App() {
  return (
    <div>
      {/* <StockManagementApp /> */}
      <Router>
        <div>
          <h1>株管理アプリ</h1>
          <Routes>
            <Route path="/stockRegister" element={<StockRegister />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
