import React, { useState, useEffect, useRef } from "react";
import { Button, Overlay, Popover, Form } from "react-bootstrap";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import axios from "axios";
import {
  Chart as ChartJS,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  TimeScale,
  Tooltip,
  Legend,
} from "chart.js";
import {
  CandlestickController,
  CandlestickElement,
} from "chartjs-chart-financial";
import "chartjs-adapter-date-fns";

// Chart.js モジュールを登録
ChartJS.register(
  CandlestickController,
  CandlestickElement,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  TimeScale,
  Tooltip,
  Legend
);

function Mainboard() {
  const [data, setData] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [currentRow, setCurrentRow] = useState(null);
  const [showPopover, setShowPopover] = useState(false);
  const [popoverTarget, setPopoverTarget] = useState(null);
  const editButtonRefs = useRef([]);

  const [columnVisibility, setColumnVisibility] = useState({
    stockId: false,
    symbol: true,
    companyName: true,
    purchasePrice: true,
    quantity: true,
    targetPrice: false,
    stopLossPrice: false,
    currentPrice: true,
    reachTargetPrice: false,
    leftStopLossPrice: false,
    profitAndLoss: true,
    history: true,
  });

  useEffect(() => {
    axios
      .get("http://localhost:50000/api/stocks")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching stock data", error);
      });
  }, []);

  useEffect(() => {
    if (data && Array.isArray(data)) {
      setTableData(data);
    }
  }, [data]);

  const handleEdit = (rowData, event) => {
    setCurrentRow(rowData);
    setPopoverTarget(event.target);
    setShowPopover(true);
  };

  useEffect(() => {
    console.log("Updated tableData:", tableData);
  }, [tableData]);

  const handleSave = async () => {
    try {
      // APIへのPUTリクエスト
      const response = await axios.put(
        `http://localhost:50000/api/stocks/${currentRow.stockId}`,
        {
          purchasePrice: currentRow.purchasePrice,
          quantity: currentRow.quantity,
          targetPrice: currentRow.targetPrice,
          stopLossPrice: currentRow.stopLossPrice,
        }
      );

      if (response.status === 201) {
        const updatedData = response.data;

        console.log("before update:", tableData);
        console.log("updated data:", updatedData);

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

  // グラフコンポーネント
  const CandlestickChart = ({ history, targetPrice, stopLossPrice }) => {
    const canvasRef = React.useRef(null);

    useEffect(() => {
      const ctx = canvasRef.current.getContext("2d");

      // Chart.jsインスタンス作成
      const chart = new ChartJS(ctx, {
        type: "candlestick",
        data: {
          datasets: [
            {
              label: "Stock Price",
              data: history.map((item) => ({
                x: new Date(item.Date),
                o: item.Open,
                h: item.High,
                l: item.Low,
                c: item.Close,
              })),
              borderColor: "black",
              borderWidth: 1,
              barThickness: 5,
              color: {
                up: "rgba(200, 0, 0, 1)",
                down: "rgba(0, 200, 0, 1)",
              },
              categoryPercentage: 0.4,
            },
            {
              label: "TargetPrice",
              data: history.map((item) => ({
                x: new Date(item.Date),
                y: targetPrice,
              })),
              type: "line",
              borderColor: "blue",
              borderWidth: 2,
              borderDash: [5, 5],
              fill: false,
              pointRadius: 0,
            },
            {
              label: "StopLossPrice",
              data: history.map((item) => ({
                x: new Date(item.Date),
                y: stopLossPrice,
              })),
              type: "line",
              borderColor: "orange",
              borderWidth: 2,
              borderDash: [5, 5],
              fill: false,
              pointRadius: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: "time",
              time: {
                unit: "day",
              },
            },
            y: {
              title: {
                display: true,
                text: "Price",
              },
            },
          },
        },
      });

      return () => {
        chart.destroy();
      };
    }, [history]);

    return <canvas ref={canvasRef} />;
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
      accessorKey: "targetPrice",
      header: "目標価格",
    },
    {
      accessorKey: "stopLossPrice",
      header: "損切り価格",
    },
    {
      accessorKey: "currentPrice",
      header: "現在価格",
    },
    {
      accessorKey: "reachTargetPrice",
      header: "目標まであと",
    },
    {
      accessorKey: "leftStopLossPrice",
      header: "損切り額まであと",
    },
    {
      accessorKey: "profitAndLoss",
      header: "損益額",
    },
    {
      accessorKey: "history",
      header: "1ヶ月の推移",
      cell: ({ getValue, row }) => (
        <div style={{ height: "300px" }}>
          <CandlestickChart
            history={getValue()}
            targetPrice={row.original.targetPrice}
            stopLossPrice={row.original.stopLossPrice}
          />
        </div>
      ),
    },
  ];

  // useReactTable フックを使用
  const table = useReactTable({
    tableData,
    columns,
    getCoreRowModel: getCoreRowModel(), // 行データの取得
    state: {
      columnVisibility,
    },
    onColumnVisibilityChange: setColumnVisibility,
  });

  return (
    <div className="card shadow" style={{ height: "450px" }}>
      <div className="card-body">
        <div className="table-responsive">
          <div
            className="table-wrapper"
            style={{ overflowY: "auto", maxHeight: "420px" }}
          >
            <table className="table table-striped table-hover align-middle">
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
                      <Form.Group controlId="formTargetPrice">
                        <Form.Label>目標価格</Form.Label>
                        <Form.Control
                          type="number"
                          name="targetPrice"
                          step="0.01"
                          value={currentRow.targetPrice}
                          onChange={handleChange}
                        />
                      </Form.Group>
                      <Form.Group controlId="formStopLossPrice">
                        <Form.Label>損切り価格</Form.Label>
                        <Form.Control
                          type="number"
                          name="stopLossPrice"
                          value={currentRow.stopLossPrice}
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

function Dashboard() {
  return (
    <div className="container mt-5">
      <Mainboard />
    </div>
  );
}

export default Dashboard;
