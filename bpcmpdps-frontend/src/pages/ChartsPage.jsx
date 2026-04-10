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
  const [priceData, setPriceData] = useState([]);

  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch demand forecast and price forecast in parallel
        const [demandRes, priceRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/forecasting/latest/`, {
            headers: { Authorization: `Token ${token}` },
          }),
          fetch(`${API_BASE_URL}/api/pricemodel/latest/`, {
            headers: { Authorization: `Token ${token}` },
          }),
        ]);

        if (!demandRes.ok) throw new Error('Failed to load demand forecast');
        if (!priceRes.ok) throw new Error('Failed to load price forecast');

        const demandData = await demandRes.json();
        const priceRaw = await priceRes.json();

        console.log('Demand forecast count:', demandData.length, demandData);
        console.log('Price forecast count:', priceRaw.length, priceRaw);

        // Use demand data for labels and power values
        const newLabels = demandData.map((entry, i) => {
          if (i === 0) return 'Now';
          const target = new Date(entry.target_time);
          return target.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        });

        const newPower = demandData.map((entry) => entry.predicted_demand_kw);

        // Price predictions cover hours 12-15, so pad the front with nulls
        // to align them at the correct x-axis positions
        const offset = demandData.length - priceRaw.length;
        const newPrice = demandData.map((_, i) => {
          const priceIndex = i - offset;
          if (priceIndex < 0 || priceIndex >= priceRaw.length) return null;
          return priceRaw[priceIndex]?.predicted_Price ?? null;
        });

        setLabels(newLabels);
        setPowerData(newPower);
        setPriceData(newPrice);
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
        label: 'Price ($)',
        data: priceData,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.15)',
        yAxisID: 'yPrice',
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      title: { display: true, text: '12-Hour Forecast', font: { size: 18 } },
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
      yPrice: {
        type: 'linear',
        position: 'right',
        min: 0,
        title: { display: true, text: 'Price ($)' },
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