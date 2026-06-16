import axios from "axios";

const api = axios.create({
  baseURL: "http://100.73.149.63:8000/api/v1",
});

export const getAssets    = (status) => api.get("/assets/",      { params: status ? { status } : {} }).then(r => r.data);
export const getEmployees = ()       => api.get("/employees/").then(r => r.data);
export const getDepartments = ()     => api.get("/departments/").then(r => r.data);
export const getAssignments = ()     => api.get("/assignments/").then(r => r.data);
export const getMaintenance = ()     => api.get("/maintenance/").then(r => r.data);
export const createAsset  = (data)   => api.post("/assets/", data).then(r => r.data);
export const deleteAsset  = (id)     => api.delete(`/assets/${id}`).then(r => r.data);
