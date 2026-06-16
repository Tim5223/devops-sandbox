import { Routes, Route, NavLink } from "react-router-dom";
import Assets from "./pages/Assets.jsx";
import Employees from "./pages/Employees.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <nav className="sidebar">
        <div className="logo">
          <span>🖥️</span>
          <h1>IT Assets</h1>
        </div>
        <NavLink to="/"           className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>📊 Dashboard</NavLink>
        <NavLink to="/assets"     className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>💻 Assets</NavLink>
        <NavLink to="/employees"  className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>👥 Employees</NavLink>
      </nav>
      <main className="content">
        <Routes>
          <Route path="/"          element={<Dashboard />} />
          <Route path="/assets"    element={<Assets />} />
          <Route path="/employees" element={<Employees />} />
        </Routes>
      </main>
    </div>
  );
}
