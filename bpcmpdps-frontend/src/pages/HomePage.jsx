import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="page">
      <div className="card">
        <h1>Home Page</h1>
        <p>Select a page:</p>

        <div className="nav-links">
          <Link to="/threshold" className="btn">
            Threshold Page
          </Link>

          <Link to="/notifications" className="btn">
            Notification Page
          </Link>

          <Link to="/charts" className="btn">
            Charts Page
          </Link>
        </div>
      </div>
    </div>
  );
}