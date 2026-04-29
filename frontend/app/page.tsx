"use client";

import { useState } from "react";
import { getStrategy, simulate } from "@/lib/api";

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [sim, setSim] = useState<any>(null);

  const [compound, setCompound] = useState("MEDIUM");
  const [tyreAge, setTyreAge] = useState(10);
  const [gapAhead, setGapAhead] = useState(5);
  const [gapBehind, setGapBehind] = useState(20);

  const payload = {
    compound,
    tyre_age: tyreAge,
    circuit: "Bahrain",
    gap_ahead: gapAhead,
    gap_behind: gapBehind,
  };

  const runStrategy = async () => {
    const data = await getStrategy(payload);
    setResult(data);
  };

  const runSimulation = async () => {
    const data = await simulate(payload);
    setSim(data);
  };

  return (
    <main className="min-h-screen bg-black text-white flex">

      {/* LEFT PANEL */}
      <div className="w-1/3 p-6 border-r border-gray-800">
        <h2 className="text-xl font-bold mb-4">Race Inputs</h2>

        <label>Tyre Compound</label>
        <select
          className="w-full p-2 mb-4 bg-zinc-800"
          onChange={(e) => setCompound(e.target.value)}
        >
          <option>SOFT</option>
          <option>MEDIUM</option>
          <option>HARD</option>
        </select>

        <label>Tyre Age: {tyreAge}</label>
        <input
          type="range"
          min="1"
          max="30"
          value={tyreAge}
          onChange={(e) => setTyreAge(Number(e.target.value))}
          className="w-full mb-4"
        />

        <label>Gap Ahead: {gapAhead}s</label>
        <input
          type="range"
          min="0"
          max="20"
          value={gapAhead}
          onChange={(e) => setGapAhead(Number(e.target.value))}
          className="w-full mb-4"
        />

        <label>Gap Behind: {gapBehind}s</label>
        <input
          type="range"
          min="0"
          max="30"
          value={gapBehind}
          onChange={(e) => setGapBehind(Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* RIGHT PANEL */}
      <div className="w-2/3 p-6">

        <h1 className="text-3xl font-bold mb-6">
          🏁 F1 AI Race Engineer
        </h1>

        {/* Buttons */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={runStrategy}
            className="bg-red-600 px-4 py-2 rounded"
          >
            Run Strategy
          </button>

          <button
            onClick={runSimulation}
            className="bg-gray-700 px-4 py-2 rounded"
          >
            Simulate
          </button>
        </div>

        {/* Strategy Result */}
        {result && (
          <div className="bg-zinc-900 p-6 rounded mb-6">
            <h2 className="text-xl font-semibold mb-2">
              Strategy Decision
            </h2>

            <p className="text-lg">
              Action:{" "}
              <span className="text-green-400">
                {result.action}
              </span>
            </p>

            <p>
              Confidence: {Math.round(result.confidence * 100)}%
            </p>

            <p className="text-gray-400 mt-2">
              {result.reasoning}
            </p>
          </div>
        )}

        {/* Simulation Result */}
        {sim && (
          <div className="bg-zinc-900 p-6 rounded">
            <h2 className="text-xl font-semibold mb-2">
              Simulation
            </h2>

            <p>Stay Out Loss: {sim.stay_out_loss}s</p>
            <p>Pit Loss: {sim.pit_loss}s</p>
            <p>
              Undercut:{" "}
              {sim.undercut_possible ? "YES" : "NO"}
            </p>
          </div>
        )}

      </div>
    </main>
  );
}