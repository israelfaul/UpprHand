import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [fighters, setFighters] = useState([]);
  const [fighterA, setFighterA] = useState("");
  const [fighterB, setFighterB] = useState("");
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/fighters")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load fighters");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Loaded fighters:", data);
        setFighters(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const analyzeMatchup = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/predict?fighter_a=${fighterA}&fighter_b=${fighterB}`
      );

      const data = await response.json();

      setPrediction(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="app">
      <h1>UpprHand</h1>
      <p>Boxing matchup prediction platform</p>

      <div className="controls">
        <select
          value={fighterA}
          onChange={(e) => setFighterA(e.target.value)}
        >
          <option value="">Select Fighter A</option>

          {fighters.map((fighter) => (
            <option
              key={fighter.name}
              value={fighter.name}
            >
              {fighter.name}
            </option>
          ))}
        </select>

        <select
          value={fighterB}
          onChange={(e) => setFighterB(e.target.value)}
        >
          <option value="">Select Fighter B</option>

          {fighters.map((fighter) => (
            <option
              key={fighter.name}
              value={fighter.name}
            >
              {fighter.name}
            </option>
          ))}
        </select>

        <button
          onClick={analyzeMatchup}
          disabled={!fighterA || !fighterB}
        >
          Analyze Matchup
        </button>
      </div>

      {prediction && (
  <div className="results">
    <h2>Prediction</h2>

    {Object.entries(prediction.probabilities).map(([fighter, probability]) => (
      <div className="fighter-result" key={fighter}>
        <div className="result-header">
          <span>{fighter}</span>
          <span>{probability}%</span>
        </div>

        <div className="bar">
          <div
            className="fill"
            style={{
              width: `${probability}%`
            }}
          />
        </div>
      </div>
    ))}

    <div className="advantages">
      <h2>Key Advantages</h2>

      {Object.entries(prediction.advantages).map(([fighter, advantages]) => (
        <div className="advantage-card" key={fighter}>
          <h3>{fighter}</h3>

          {advantages.length > 0 ? (
            <ul>
              {advantages.map(([category, difference]) => (
                <li key={category}>
                  {category.replaceAll("_", " ")} (+{difference})
                </li>
              ))}
            </ul>
          ) : (
            <p>No major category advantages.</p>
          )}
        </div>
      ))}
    </div>
  </div>
)}
    </div>
  );
}

export default App;