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
const CandlestickChart = ({ history }) => {
  const canvasRef = useRef(null);

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
              x: new Date(item.date),
              o: item.openPrice,
              h: item.highPrice,
              l: item.lowPrice,
              c: item.closePrice,
            })),
            yAxisID: "y1",
            borderColor: "black",
            borderWidth: 1,
            barThickness: 2,
            backgroundColors: {
              up: "#ea5550",
              down: "#00a960",
              unchanged: "#696969",
            },
            borderColors: {
              up: "#ea5550",
              down: "#00a960",
              unchanged: "#696969",
            },
          },
          //   {
          //     label: "StopLossPrice",
          //     data: history.map((item) => ({
          //       x: new Date(item.Date),
          //       y: stopLossPrice,
          //     })),
          //     yAxisID: "y1",
          //     type: "line",
          //     borderColor: "black",
          //     borderWidth: 1,
          //     borderDash: [5, 5],
          //     fill: false,
          //     pointRadius: 0,
          //   },
          {
            label: "5d-MA",
            data: history.map((item) => ({
              x: new Date(item.date),
              y: item.ma5,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#fcc800",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: "20d-MA",
            data: history.map((item) => ({
              x: new Date(item.date),
              y: item.ma20,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#ea618e",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: "60d-MA",
            data: history.map((item) => ({
              x: new Date(item.date),
              y: item.ma60,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#3cb37a",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: "100d-MA",
            data: history.map((item) => ({
              x: new Date(item.date),
              y: item.ma100,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#0068b7",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          //   {
          //     label: "%D",
          //     data: stochastics.map((item) => ({
          //       x: new Date(item.Date),
          //       y: item.D,
          //     })),
          //     type: "line",
          //     yAxisID: "y2",
          //     borderColor: "#82cddd",
          //     borderWidth: 1,
          //     fill: false,
          //     pointRadius: 0,
          //     borderDash: [5, 2],
          //   },
          //   {
          //     label: "Slow%D",
          //     data: stochastics.map((item) => ({
          //       x: new Date(item.Date),
          //       y: item.SlowD,
          //     })),
          //     type: "line",
          //     yAxisID: "y2",
          //     borderColor: "#008db7",
          //     borderWidth: 1,
          //     fill: false,
          //     pointRadius: 0,
          //     borderDash: [5, 2],
          //   },
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
          y1: {
            position: "left",
            title: {
              display: true,
              text: "Stock Price / Moving Average",
            },
          },
          //   y2: {
          //     position: "right",
          //     beginAtZero: true,
          //     max: 100,
          //     title: {
          //       display: true,
          //       text: "Stochastics Percentage",
          //     },
          //   },
        },
      },
    });

    return () => {
      chart.destroy();
    };
  }, [history]);

  return <canvas ref={canvasRef} />;
};

export default CandlestickChart;
