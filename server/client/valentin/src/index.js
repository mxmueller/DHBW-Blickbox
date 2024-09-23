import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Dashboard from "./dashboard/dashboard";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Dashboard />
  </React.StrictMode>,
);

reportWebVitals();
