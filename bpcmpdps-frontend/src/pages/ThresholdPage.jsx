import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';

export default function ThresholdPage() {
  const [cost, setCost] = useState('');
  const [energy, setEnergy] = useState('');
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentEnergy, setCurrentEnergy] = useState(null);
  const [currentPrice, setCurrentPrice] = useState(null);

  const token = localStorage.getItem('token');

  // Fetch past thresholds on page load
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/alerts/thresholds/`, {
          method: 'GET',
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        if (!response.ok) throw new Error('Failed to load thresholds');

        const data = await response.json();
        // Backend returns a single object — wrap in array so .map() works
        setHistory(Array.isArray(data) ? data : [data]);
        const latest = Array.isArray(data) ? data[0] : data;
        latest && setCurrentPrice(latest.price_threshold);
        latest && setCurrentEnergy(latest.demand_kw_threshold);
      } catch (err) {
        console.error(err);
      }
    };

    fetchHistory();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const costNum = parseFloat(cost);
    const energyNum = parseFloat(energy);

    if (isNaN(costNum) || isNaN(energyNum)) {
      setError('Please enter valid numbers for both fields.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/alerts/thresholds/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
          price_threshold: costNum,
          demand_kw_threshold: energyNum,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to save threshold');
      }

      // Add the new entry (returned by the backend) to the top of the list
      setHistory((prev) => [data, ...prev]);
      setCost('');
      setEnergy('');
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card threshold-card">
        <h1>Set Thresholds</h1>
        <p className="threshold-subtitle">
          Enter your cost and energy limits below.
        </p>

        <form className="form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="cost">Cost Threshold ($)</label>
            <input
              id="cost"
              type="number"
              step="0.01"
              min="0"
              placeholder="e.g. 150.00"
              value={cost}
              onChange={(e) => setCost(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="energy">Energy Threshold (kW)</label>
            <input
              id="energy"
              type="number"
              step="0.01"
              min="0"
              placeholder="e.g. 50.00"
              value={energy}
              onChange={(e) => setEnergy(e.target.value)}
            />
          </div>

          {error && <p className="error-text">{error}</p>}

          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Saving...' : 'Save Threshold'}
          </button>
        </form>
      </div>
      
      <div className="card threshold-card current-thresholds">
        <h2>Current Thresholds</h2>
        <p className="current-subtitle">
          Your latest cost and energy thresholds are shown below.
        </p>
        <div className="current-values">
          <p>
            <strong>Cost Threshold:</strong> {currentPrice !== null ? `$${currentPrice.toFixed(2)}` : 'N/A'}
          </p>
          <p>
            <strong>Energy Threshold:</strong> {currentEnergy !== null ? `${currentEnergy.toFixed(2)} kW` : 'N/A'}
          </p>
        </div>
      </div>

      {/* History table */}
      <div className="card threshold-card threshold-history">
        <h2>Past Thresholds</h2>

        {history.length === 0 ? (
          <p className="empty-text">No thresholds saved yet.</p>
        ) : (
          <div className="table-wrapper">
            <table className="threshold-table">
              <thead>
                <tr>
                  <th>Date / Time</th>
                  <th>Price Threshold ($)</th>
                  <th>Energy Threshold (kW)</th>
                </tr>
              </thead>
              <tbody>
                {history.map((entry) => (
                  <tr key={entry.id}>
                    <td>{new Date(entry.created_at).toLocaleString()}</td>
                    <td>{Number(entry.price_threshold).toFixed(2)}</td>
                    <td>{Number(entry.demand_kw_threshold).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}