import React, { useState, useEffect } from "react";
import { useReactTable, getCoreRowModel } from "@tanstack/react-table";
import axios from "axios";

function Dashboard() {
  const [data, setData] = useState([]);
  const userId = 1;
  useEffect(() => {
    axios
      .get("http://localhost:5100/api/stocks", { params: { userId } })
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching stock data", error);
      });
  }, [userId]);

  // カラム定義
  const columns = [
    {
      accessorKey: "symbol", // データキー
      header: "証券コード", // ヘッダー名
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
      accessorKey: "cutlossPrice",
      header: "損切り価格",
    },
  ];

  // サンプルデータ
  //   const data = [
  //     {
  //       symbol: "1234",
  //       purchasePrice: 300,
  //       quantity: 100,
  //       targetPrice: 400,
  //       cutlossPrice: 200,
  //     },
  //     {
  //       symbol: "5678",
  //       purchasePrice: 500,
  //       quantity: 100,
  //       targetPrice: 600,
  //       cutlossPrice: 400,
  //     },
  //     {
  //       symbol: "9101",
  //       purchasePrice: 1000,
  //       quantity: 100,
  //       targetPrice: 1100,
  //       cutlossPrice: 900,
  //     },
  //   ];

  // useReactTable フックを使用
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(), // 行データの取得
  });

  return (
    <div className="container mt-5">
      <div className="card shadow-">
        <div className="card-body">
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
                          : header.column.columnDef.header}
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
                        {cell.getValue()}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
