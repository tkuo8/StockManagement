import React, { useState, useEffect } from "react";
import {
  Button,
  Overlay,
  Popover,
  Form,
  Badge,
  Dropdown,
} from "react-bootstrap";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import axios from "axios";
import { Link } from "react-router-dom";
import CandlestickChart from "../components/CandlestickChart";

function Mainboard({
  setPage,
  setTotalPages,
  page,
  totalPages,
  status,
  possession,
  searchSymbol,
}) {
  const [tableData, setTableData] = useState([]);
  const [currentRow, setCurrentRow] = useState(null);
  const [showPopover, setShowPopover] = useState(false);
  const [popoverTarget, setPopoverTarget] = useState(null);

  const [columnVisibility, setColumnVisibility] = useState({
    stockId: false,
    symbol: true,
    companyName: true,
    purchasePrice: true,
    quantity: true,
    profitAndLoss: true,
    alerts: true,
    history: true,
  });

  useEffect(() => {
    axios
      .get(
        `http://localhost:50000/api/stocks?page=${page}&pageSize=10&status=${status}&possession=${possession}&searchSymbol=${searchSymbol}`
      )
      .then((response) => {
        setTableData(response.data.financeData);
        setTotalPages(response.data.totalPages);
      })
      .catch((error) => {
        console.error("Error fetching stock data", error);
      });
  }, [page, totalPages, status, possession, searchSymbol]);

  const handleEdit = (rowData, event) => {
    setCurrentRow(rowData);
    setPopoverTarget(event.target);
    setShowPopover(true);
  };

  const handleSave = async () => {
    try {
      // APIへのPUTリクエスト
      const response = await axios.put(
        `http://localhost:50000/api/stocks/${currentRow.stockId}`,
        {
          purchasePrice: currentRow.purchasePrice,
          quantity: currentRow.quantity,
        }
      );

      if (response.status === 201) {
        const updatedData = response.data;

        // テーブルデータの更新
        setTableData((prevData) =>
          prevData.map((row) =>
            row.stockId === updatedData.stockId ? updatedData : row
          )
        );

        // ポップオーバーを閉じる
        setShowPopover(false);
      } else {
        alert("Failed to update data");
      }
    } catch (error) {
      console.error("Error updating data:", error);
      alert("Error updating data");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCurrentRow((prevRow) => ({
      ...prevRow,
      [name]: value,
    }));
  };

  // カラム定義
  const columns = [
    {
      accessorKey: "stockId",
      header: "ストックID", // データベース上の主キー
    },
    {
      accessorKey: "symbol", // データキー
      header: "証券コード", // ヘッダー名
    },
    {
      accessorKey: "companyName",
      header: "企業名",
      getSize: () => 100,
    },
    {
      accessorKey: "purchasePrice",
      header: "取得単価",
    },
    {
      accessorKey: "quantity",
      header: "保有株数",
    },
    {
      accessorKey: "profitAndLoss",
      header: "損益額",
    },
    {
      accessorKey: "alerts",
      header: "アラート",
      cell: renderAlertsCell,
    },
    {
      accessorKey: "history",
      header: "6ヶ月の推移",
      cell: renderHistoryCell,
    },
  ];

  // useReactTable フックを使用
  const table = useReactTable({
    data: tableData,
    columns,
    getCoreRowModel: getCoreRowModel(), // 行データの取得
    state: {
      columnVisibility,
    },
    onColumnVisibilityChange: setColumnVisibility,
  });

  return (
    <div className="card shadow" style={{ height: "520px" }}>
      <div className="card-body">
        <div className="table-responsive">
          <div
            className="table-wrapper"
            style={{ overflowY: "auto", maxHeight: "480px" }}
          >
            <table className="table align-middle">
              <thead className="table-primary">
                {table.getHeaderGroups().map((headerGroup) => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <th
                        key={header.id}
                        className="text-center"
                        style={{
                          width: header.getSize(),
                          position: "sticky",
                          top: 0,
                          zIndex: 1,
                        }}
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody>
                {table.getRowModel().rows.map((row) => (
                  <tr key={row.id}>
                    {row.getVisibleCells().map((cell) => (
                      <td
                        key={cell.id}
                        className="text-center"
                        onClick={(e) => handleEdit(row.original, e)}
                        style={{ cursor: "pointer" }}
                      >
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Popover for editing */}
            <Overlay
              show={showPopover}
              target={popoverTarget}
              placement="right"
              onHide={() => setShowPopover(false)}
              rootClose
            >
              <Popover id="popover-edit">
                <Popover.Header as="h3">銘柄情報編集</Popover.Header>
                <Popover.Body>
                  {currentRow && (
                    <Form>
                      <Form.Group controlId="formPurchasePrice">
                        <Form.Label>取得単価</Form.Label>
                        <Form.Control
                          type="number"
                          name="purchasePrice"
                          step="0.01"
                          value={currentRow.purchasePrice}
                          onChange={handleChange}
                        />
                      </Form.Group>
                      <Form.Group controlId="formQuantity">
                        <Form.Label>保有株数</Form.Label>
                        <Form.Control
                          type="number"
                          name="quantity"
                          value={currentRow.quantity}
                          onChange={handleChange}
                        />
                      </Form.Group>
                      <Button
                        variant="secondary"
                        className="me-2"
                        onClick={() => setShowPopover(false)}
                      >
                        取消
                      </Button>
                      <Button variant="primary" onClick={handleSave}>
                        登録
                      </Button>
                    </Form>
                  )}
                </Popover.Body>
              </Popover>
            </Overlay>
          </div>
        </div>
      </div>
    </div>
  );
}

function renderAlertsCell({ getValue }) {
  const value = getValue();
  return (
    <div>
      {value.isBuy && (
        <Badge bg="danger" className="me-1">
          買い
        </Badge>
      )}
      {value.isSell && (
        <Badge bg="success" className="me-1">
          売り
        </Badge>
      )}
      {value.isExclusion && (
        <Badge bg="secondary" className="me-1">
          除外
        </Badge>
      )}
    </div>
  );
}

function renderHistoryCell({ getValue, row }) {
  return (
    <div className="p-3" style={{ height: "400px", width: "800px" }}>
      <CandlestickChart history={getValue()} />
    </div>
  );
}

function Dashboard() {
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [status, setStatus] = useState(""); // アラートのフィルター状態
  const [possession, setPossession] = useState(""); // 保有中・未保有フィルター状態
  const [symbol, setSymbol] = useState(""); // 証券コード検索フィールドの値
  const [searchSymbol, setSearchSymbol] = useState(""); // 証券コードで検索する際の値

  const handleUpdateAllStocksData = () => {
    axios
      .get("http://localhost:50000/api/stocks/update_all")
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error fetching stock data", error);
      });
  };

  const handleInputChange = (e) => {
    setSymbol(e.target.value);
  };

  const handleSearch = () => {
    setSearchSymbol(symbol);
  };

  const handleStatusChange = (selectedStatus) => {
    setStatus(selectedStatus);
  };

  const handlePossessionChange = (selectedPossession) => {
    setPossession(selectedPossession);
  };
  return (
    <div className="container mt-5">
      <div className="d-flex align-items-center gap-3 mb-1">
        <Link to="/stockRegister">株価情報を新規登録する</Link>
        {/* 保有中フィルター */}
        <Form.Group className="mb-1">
          <Form.Label>保有中フィルター</Form.Label>
          <Dropdown onSelect={handlePossessionChange}>
            <Dropdown.Toggle variant="primary" id="dropdown-possession">
              {possession === "in"
                ? "保有中"
                : possession === "out"
                ? "未保有"
                : "-"}
            </Dropdown.Toggle>

            <Dropdown.Menu>
              <Dropdown.Item eventKey="">-</Dropdown.Item>
              <Dropdown.Item eventKey="in">保有中</Dropdown.Item>
              <Dropdown.Item eventKey="out">未保有</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Form.Group>

        {/* アラートフィルター */}
        <Form.Group className="mb-1">
          <Form.Label>アラートフィルター</Form.Label>
          <Dropdown onSelect={handleStatusChange}>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
              {status === "buy"
                ? "買い"
                : status === "sell"
                ? "売り"
                : status === "exclusion"
                ? "除外"
                : "-"}
            </Dropdown.Toggle>

            <Dropdown.Menu>
              <Dropdown.Item eventKey="">-</Dropdown.Item>
              <Dropdown.Item eventKey="buy">買い</Dropdown.Item>
              <Dropdown.Item eventKey="sell">売り</Dropdown.Item>
              <Dropdown.Item eventKey="exclusion">除外</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Form.Group>

        <Form.Group className="d-flex align-items-end gap-3 mb-1">
          <div>
            <Form.Label>証券コード検索</Form.Label>
            <Form.Control
              type="text"
              value={symbol}
              onChange={handleInputChange}
              placeholder="証券コードを入力してください"
            />
          </div>
          <Button variant="secondary" onClick={handleSearch}>
            検索
          </Button>
        </Form.Group>

        <Button
          variant="secondary"
          className="mb-1"
          onClick={handleUpdateAllStocksData}
        >
          株価データ全更新（約5分）
        </Button>
      </div>
      <Mainboard
        totalPages={totalPages}
        setTotalPages={setTotalPages}
        page={page}
        setPage={setPage}
        status={status}
        possession={possession}
        searchSymbol={searchSymbol}
      />
      <div className="d-flex justify-content-center align-items-center my-3">
        <Button
          variant="outline-primary"
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </Button>
        <span className="mx-3">
          Page {page} of {totalPages}
        </span>
        <Button
          variant="outline-primary"
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
        >
          Next
        </Button>
      </div>
    </div>
  );
}

export default Dashboard;
