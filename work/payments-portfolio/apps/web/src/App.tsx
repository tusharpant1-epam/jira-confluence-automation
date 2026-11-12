import { useEffect, useState } from "react";

type ApiHealth = "checking" | "available" | "unavailable";

export default function App() {
  const [apiHealth, setApiHealth] = useState<ApiHealth>("checking");

  async function checkApi() {
    setApiHealth("checking");
    try {
      const response = await fetch("/api/health");
      if (!response.ok) {
        throw new Error(`API health check returned ${response.status}`);
      }
      setApiHealth("available");
    } catch (error) {
      console.error("Could not reach the local API", error);
      setApiHealth("unavailable");
    }
  }

  useEffect(() => {
    void checkApi();
  }, []);

  const healthLabel = {
    checking: "Checking",
    available: "Available",
    unavailable: "Unavailable",
  }[apiHealth];

  return (
    <main className="page">
      <section className="panel" aria-labelledby="page-title">
        <p className="eyebrow">Local prototype</p>
        <h1 id="page-title">Jira Sprint Dashboard</h1>
        <p className="intro">
          The local application shell is running. Jira integration and sprint
          data are not configured yet.
        </p>
        <div className="service" role="status" aria-live="polite">
          <span
            className={`indicator indicator--${apiHealth}`}
            aria-hidden="true"
          />
          <span>Backend API</span>
          <strong>{healthLabel}</strong>
        </div>
        {apiHealth === "unavailable" && (
          <button className="retry" onClick={() => void checkApi()}>
            Retry connection
          </button>
        )}
      </section>
    </main>
  );
}
