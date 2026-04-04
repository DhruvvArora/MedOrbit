import Navbar from "./components/layout/Navbar";
import Hero from "./components/sections/Hero";
import "./index.css";
import "./styles/theme.css";

function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main>
        <Hero />
      </main>
    </div>
  );
}

export default App;