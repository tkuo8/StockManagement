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
const CandlestickChart = ({
  history,
  stopLossPrice,
  shortMa,
  longMa,
  hundredMa,
  stochastics,
}) => {
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
              x: new Date(item.Date),
              o: item.Open,
              h: item.High,
              l: item.Low,
              c: item.Close,
            })),
            yAxisID: "y1",
            borderColor: "black",
            borderWidth: 1,
            barThickness: 3,
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
          {
            label: "StopLossPrice",
            data: history.map((item) => ({
              x: new Date(item.Date),
              y: stopLossPrice,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "black",
            borderWidth: 1,
            borderDash: [5, 5],
            fill: false,
            pointRadius: 0,
          },
          {
            label: "5d-MA",
            data: shortMa.map((item) => ({
              x: new Date(item.Date),
              y: item.MA,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#fcc800",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: "15d-MA",
            data: longMa.map((item) => ({
              x: new Date(item.Date),
              y: item.MA,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#e73562",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: "100d-MA",
            data: hundredMa.map((item) => ({
              x: new Date(item.Date),
              y: item.MA,
            })),
            yAxisID: "y1",
            type: "line",
            borderColor: "#ea553a",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: "%D",
            data: stochastics.map((item) => ({
              x: new Date(item.Date),
              y: item.D,
            })),
            type: "line",
            yAxisID: "y2",
            borderColor: "#82cddd",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
            borderDash: [5, 2],
          },
          {
            label: "Slow%D",
            data: stochastics.map((item) => ({
              x: new Date(item.Date),
              y: item.SlowD,
            })),
            type: "line",
            yAxisID: "y2",
            borderColor: "#008db7",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
            borderDash: [5, 2],
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
          y1: {
            position: "left",
            title: {
              display: true,
              text: "Stock Price / Moving Average",
            },
          },
          y2: {
            position: "right",
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: "Stochastics Percentage",
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
