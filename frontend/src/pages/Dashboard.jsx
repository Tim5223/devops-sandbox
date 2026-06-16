import { useQuery } from "@tanstack/react-query";
import { getAssets, getEmployees, getDepartments, getMaintenance } from "../api";

export default function Dashboard() {
  const { data: assets      = [] } = useQuery({ queryKey: ["assets"],      queryFn: () => getAssets() });
  const { data: employees   = [] } = useQuery({ queryKey: ["employees"],   queryFn: getEmployees });
  const { data: departments = [] } = useQuery({ queryKey: ["departments"], queryFn: getDepartments });
  const { data: maintenance = [] } = useQuery({ queryKey: ["maintenance"], queryFn: getMaintenance });

  const available   = assets.filter(a => a.status === "available").length;
  const assigned    = assets.filter(a => a.status === "assigned").length;
  const inMaintenance = assets.filter(a => a.status === "maintenance").length;

  return (
    <div>
      <h2 className="page-title">Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card blue">
          <div className="stat-number">{assets.length}</div>
          <div className="stat-label">Total Assets</div>
        </div>
        <div className="stat-card green">
          <div className="stat-number">{available}</div>
          <div className="stat-label">Available</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-number">{assigned}</div>
          <div className="stat-label">Assigned</div>
        </div>
        <div className="stat-card red">
          <div className="stat-number">{inMaintenance}</div>
          <div className="stat-label">In Maintenance</div>
        </div>
        <div className="stat-card purple">
          <div className="stat-number">{employees.length}</div>
          <div className="stat-label">Employees</div>
        </div>
        <div className="stat-card gray">
          <div className="stat-number">{departments.length}</div>
          <div className="stat-label">Departments</div>
        </div>
      </div>

      <h3 className="section-title">Recent Maintenance</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Asset</th>
            <th>Type</th>
            <th>Cost</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {maintenance.slice(0, 5).map(m => (
            <tr key={m.id}>
              <td>{m.asset?.name}</td>
              <td><span className="badge">{m.maintenance_type}</span></td>
              <td>${m.cost?.toFixed(2)}</td>
              <td>{new Date(m.performed_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
