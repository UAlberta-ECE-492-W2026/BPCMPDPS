import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import ThresholdPage from './pages/ThresholdPage';
import NotificationsPage from './pages/NotificationsPage';
import ChartsPage from './pages/ChartsPage';


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/threshold" element={<ThresholdPage />} />
      <Route path="/notifications" element={<NotificationsPage />} />
      <Route path="/charts" element={<ChartsPage />} />
    </Routes>
  );
}