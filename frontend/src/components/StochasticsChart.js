import React, { useEffect, useRef } from "react";
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
import "chartjs-adapter-date-fns";

// Chart.js モジュールを登録
ChartJS.register(
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  TimeScale,
  Tooltip,
  Legend
);

// グラフコンポーネント
const StochasticsChart = ({ stochastics }) => {
  const canvasRef = useRef(null);

  // ダミーストキャスデータ
  const d = Array.from({ length: 21 }, () => Math.floor(Math.random() * 100));

  useEffect(() => {
    const ctx = canvasRef.current.getContext("2d");

    // Chart.jsインスタンス作成
    const chart = new ChartJS(ctx, {
      type: "line",
      data: {
        datasets: [
          {
            label: "%D",
            data: stochastics.map((item) => ({
              x: new Date(item.Date),
              y: item.D,
            })),
          },
          {
            label: "Slow%D",
            data: stochastics.map((item) => ({
              x: new Date(item.Date),
              y: item.SlowD,
            })),
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
            beginAtZero: true,
            title: {
              display: true,
              text: "Percentage",
            },
          },
        },
      },
    });

    return () => {
      chart.destroy();
    };
  }, []);

  return <canvas ref={canvasRef} />;
};

export default StochasticsChart;
