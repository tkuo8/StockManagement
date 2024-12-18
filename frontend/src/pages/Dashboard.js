import React, { useState, useEffect } from "react";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import axios from "axios";
import {
  Chart as ChartJS,
  LinearScale,
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
  TimeScale,
  Tooltip,
  Legend
);

function Mainboard() {
  const [data, setData] = useState([]);
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

  // グラフコンポーネント
  const CandlestickChart = ({ history }) => {
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
      cell: ({ getValue }) => (
        <div style={{ height: "300px" }}>
          <CandlestickChart history={getValue()} />
        </div>
      ),

      // const data = getValue(); // historyの値を取得
      // const chartData = {
      //   labels: data.map((item) => item.Date),
      //   datasets: [
      //     {
      //       label: "始値",
      //       data: data.map((item) => item.Open),
      //       borderColor: "blue",
      //       backgroundColor: "rgba(0, 0, 255, 0.2)",
      //       tension: 0.4,
      //     },
      //     {
      //       label: "高値",
      //       data: data.map((item) => item.High),
      //       borderColor: "green",
      //       backgroundColor: "rgba(0, 255, 0, 0.2)",
      //       tension: 0.4,
      //     },
      //     {
      //       label: "安値",
      //       data: data.map((item) => item.Low),
      //       borderColor: "red",
      //       backgroundColor: "rgba(255, 0, 0, 0.2)",
      //       tension: 0.4,
      //     },
      //     {
      //       label: "終値",
      //       data: data.map((item) => item.Close),
      //       borderColor: "orange",
      //       backgroundColor: "rgba(255, 165, 0, 0.2)",
      //       tension: 0.4,
      //     },
      //   ],
      // };
      // const options = {
      //   responsive: true,
      //   maintainAspectRatio: false,
      // };

      // return (
      //   <div style={{ height: "300px" }}>
      //     <Line data={chartData} options={options} />
      //   </div>
      // );
    },
  ];

  // useReactTable フックを使用
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(), // 行データの取得
  });

  return (
    <div className="card shadow" style={{ height: "400px" }}>
      <div
        className="card-body"
        style={{ overflowY: "auto", maxHeight: "350px" }}
      >
        <h2 className="card-title text-center text-primary mb-4">
          ダッシュボード
        </h2>
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead className="table-primary">
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th key={header.id} className="text-center">
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
                    <td key={cell.id} className="text-center">
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
