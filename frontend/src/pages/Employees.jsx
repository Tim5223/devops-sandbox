import { useQuery } from "@tanstack/react-query";
import { getEmployees } from "../api";

export default function Employees() {
  const { data: employees = [], isLoading } = useQuery({
    queryKey: ["employees"],
    queryFn:  getEmployees,
  });

  return (
    <div>
      <h2 className="page-title">Employees</h2>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
            </tr>
          </thead>
          <tbody>
            {employees.map(e => (
              <tr key={e.id}>
                <td>{e.first_name} {e.last_name}</td>
                <td>{e.email}</td>
                <td>{e.department?.name ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
