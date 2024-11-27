import React, { useState } from "react";
import { useReactTable, getCoreRowModel } from "@tanstack/react-table";

// カラム定義
const columns = [
  {
    accessorKey: "symbol", // データキー
    header: "銘柄コード", // ヘッダー名
  },
  {
    accessorKey: "purchasePrice",
    header: "購入価格",
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
const data = [
  {
    symbol: "1234",
    purchasePrice: 300,
    quantity: 100,
    targetPrice: 400,
    cutlossPrice: 200,
  },
  {
    symbol: "5678",
    purchasePrice: 500,
    quantity: 100,
    targetPrice: 600,
    cutlossPrice: 400,
  },
  {
    symbol: "9101",
    purchasePrice: 1000,
    quantity: 100,
    targetPrice: 1100,
    cutlossPrice: 900,
  },
];

function Dashboard() {
  // useReactTable フックを使用
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(), // 行データの取得
  });

  return (
    <div>
      <h2>Dashboard</h2>
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {header.isPlaceholder ? null : header.column.columnDef.header}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>{cell.getValue()}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
