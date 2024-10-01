import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css"; // Optional CSS file

const container = document.getElementById("root");
const root = createRoot(container!);
root.render(<App />);
