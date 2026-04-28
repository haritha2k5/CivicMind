// frontend/src/App.jsx
import { useState } from "react";
import PolicyPulse from "./components/PolicyPulse";
import GrievanceGPT from "./components/GrievanceGPT";
import SchemeMatch from "./components/SchemeMatch";
import "./App.css";

const TABS = [
  { id: "policy",    label: "PolicyPulse",    component: <PolicyPulse /> },
  { id: "grievance", label: "GrievanceGPT",   component: <GrievanceGPT /> },
  { id: "scheme",    label: "SchemeMatch AI",  component: <SchemeMatch /> },
];

export default function App() {
  const [active, setActive] = useState("policy");
  const current = TABS.find((t) => t.id === active);

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <span className="brand-name">CivicMind</span>
          <span className="brand-sub">RAG-Powered Civic Intelligence Platform</span>
        </div>
        <nav className="tab-nav">
          {TABS.map((t) => (
            <button
              key={t.id}
              className={`tab-btn ${active === t.id ? "active" : ""}`}
              onClick={() => setActive(t.id)}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </header>
      <main className="app-main">{current.component}</main>
      <footer className="app-footer">
        PSG College of Technology · MSc Theoretical Computer Science · AI Course Project 2025–26
      </footer>
    </div>
  );
}
