import React, { useEffect, useRef } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
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
  CategoryScale,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  TimeScale,
  Tooltip,
  Legend
);

// グラフコンポーネント
const CandlestickChart = ({ history, stopLossPrice }) => {
  const canvasRef = useRef(null);

  // ダミー移動平均線データ
  const ma = Array.from({ length: 21 }, () =>
    Math.floor(Math.random() * (2751 - 2600) + 2600)
  );

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
          {
            label: "moving average",
            data: history.map((item, index) => ({
              x: new Date(item.Date),
              y: ma[index],
            })),
            type: "line",
            borderColor: "yellow",
            borderWidth: 2,
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
  }, [history, stopLossPrice]);

  return <canvas ref={canvasRef} />;
};

export default CandlestickChart;
