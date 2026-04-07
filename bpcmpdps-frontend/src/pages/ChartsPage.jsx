import React from 'react';
import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function ChartsPage() {
  const [labels, setLabels] = useState([]);
  const [powerData, setPowerData] = useState([]);
  const [tempData, setTempData] = useState([]);

  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/forecasting/latest/`, {
          method: 'GET',
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        if (!response.ok) throw new Error('Failed to load forecasting data');

        const data = await response.json();

        // Build labels: "Now" for the first point, actual time for the rest
        const newLabels = data.map((entry, i) => {
          if (i === 0) return 'Now';
          const target = new Date(entry.target_time);
          return target.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        });

        const newPower = data.map((entry) => entry.predicted_demand_kw);

        setLabels(newLabels);
        setPowerData(newPower);
        // Temperature not available from backend yet — placeholder
        setTempData(data.map(() => null));
      } catch (err) {
        console.error(err);
      }
    };

    if (token) fetchData();
  }, [token]);

  const data = {
    labels,
    datasets: [
      {
        label: 'Power (kW)',
        data: powerData,
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.15)',
        yAxisID: 'yPower',
        tension: 0.3,
      },
      {
        label: 'Temperature (°C)',
        data: tempData,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.15)',
        yAxisID: 'yTemp',
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      title: { display: true, text: '15-Hour Forecast', font: { size: 18 } },
      legend: { position: 'top' },
    },
    scales: {
      x: {
        title: { display: true, text: 'Time' },
      },
      yPower: {
        type: 'linear',
        position: 'left',
        min: 0,
        title: { display: true, text: 'Power (kW)' },
        grid: { drawOnChartArea: true },
      },
      yTemp: {
        type: 'linear',
        position: 'right',
        title: { display: true, text: 'Temperature (°C)' },
        grid: { drawOnChartArea: false },
      },
    },
  };

  return (
    <div className="page">
      <div className="card chart-card">
        <Line data={data} options={options} />
      </div>
    </div>
  );
}