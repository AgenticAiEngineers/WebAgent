import { useMemo, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8711";

function App() {
  const [agent, setAgent] = useState("simple");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: "system", text: "Choose an agent and start chatting." }
  ]);

  const title = useMemo(
    () => (agent === "executor" ? "Executor Agent Mode" : "Simple Agent Mode"),
    [agent]
  );

  const sendMessage = async (event) => {
    event.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text, agent })
      });

      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "agent", text: data.response || "No response received." }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "agent", text: `Connection error: ${error.message}` }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="noise-layer" />
      <main className="chat-card">
        <header className="topbar">
          <div>
            <p className="eyebrow">WebAgent</p>
            <h1>{title}</h1>
          </div>
          <label className="agent-picker">
            <span>Agent</span>
            <select value={agent} onChange={(e) => setAgent(e.target.value)}>
              <option value="simple">Simple Agent</option>
              <option value="executor">Executor Agent</option>
            </select>
          </label>
        </header>

        <section className="messages">
          {messages.map((message, index) => (
            <article key={`${message.role}-${index}`} className={`msg ${message.role}`}>
              <p className="role">{message.role}</p>
              <p>{message.text}</p>
            </article>
          ))}
          {loading && (
            <article className="msg agent typing">
              <p className="role">agent</p>
              <p>Thinking...</p>
            </article>
          )}
        </section>

        <form className="composer" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything..."
            autoComplete="off"
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
