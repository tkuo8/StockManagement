import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import StockRegister from "./pages/StockRegister";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div>
      {/* <StockManagementApp /> */}
      <Router>
        <div>
          <h3>株管理アプリ</h3>
          <Routes>
            <Route path="/stockRegister" element={<StockRegister />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
