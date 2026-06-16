import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getAssets } from "../api";

const STATUS_COLORS = {
  available:   "badge green",
  assigned:    "badge blue",
  maintenance: "badge orange",
  retired:     "badge gray",
};

export default function Assets() {
  const [filter, setFilter] = useState("");
  const { data: assets = [], isLoading } = useQuery({
    queryKey: ["assets", filter],
    queryFn:  () => getAssets(filter || undefined),
  });

  return (
    <div>
      <h2 className="page-title">Assets</h2>

      <div className="filters">
        {["", "available", "assigned", "maintenance", "retired"].map(s => (
          <button
            key={s}
            className={`filter-btn ${filter === s ? "active" : ""}`}
            onClick={() => setFilter(s)}
          >
            {s === "" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Brand</th>
              <th>Model</th>
              <th>Serial</th>
              <th>Status</th>
              <th>Cost</th>
            </tr>
          </thead>
          <tbody>
            {assets.map(a => (
              <tr key={a.id}>
                <td>{a.name}</td>
                <td>{a.asset_type}</td>
                <td>{a.brand}</td>
                <td>{a.model}</td>
                <td><code>{a.serial_number}</code></td>
                <td><span className={STATUS_COLORS[a.status]}>{a.status}</span></td>
                <td>${a.cost?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
