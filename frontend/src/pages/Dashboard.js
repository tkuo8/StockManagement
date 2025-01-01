import React, { useState, useEffect } from "react";
import { Button, Overlay, Popover, Form, Badge } from "react-bootstrap";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import axios from "axios";
import { Link } from "react-router-dom";
import CandlestickChart from "../components/CandlestickChart";

function Mainboard() {
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
      .get("http://localhost:50000/api/stocks")
      .then((response) => {
        setTableData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching stock data", error);
      });
  }, []);

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
    <div className="card shadow" style={{ height: "600px" }}>
      <div className="card-body">
        <div className="table-responsive">
          <div
            className="table-wrapper"
            style={{ overflowY: "auto", maxHeight: "580px" }}
          >
            <table className="table align-middle">
              <thead className="table-primary">
                {table.getHeaderGroups().map((headerGroup) => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <th
                        key={header.id}
                        className="text-center"
                        style={{ position: "sticky", top: 0, zIndex: 1 }}
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
    <div style={{ height: "300px", width: "700px" }}>
      <CandlestickChart
        history={getValue()}
        // shortMa={row.original.shortMa}
        // middleMa={row.original.middleMa}
        // longMa={row.original.longMa}
        // veryLongMa={row.original.veryLongMa}
        // stochastics={row.original.stochastics}
      />
    </div>
  );
}

function Dashboard() {
  return (
    <div className="container mt-5">
      <Link to="/stockRegister">株価情報を新規登録する</Link>
      <Mainboard />
    </div>
  );
}

export default Dashboard;
