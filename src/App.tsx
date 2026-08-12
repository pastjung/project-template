import "./styles.css";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export default function App() {
  return (
    <main className="app">
      <section className="panel">
        <p className="eyebrow">React Vite</p>
        <h1>Application Template</h1>
        <p>API base URL: {apiBaseUrl}</p>
      </section>
    </main>
  );
}
