"use client";

import { useState, useEffect } from "react";
import { getStrategy, simulate } from "@/lib/api";

export default function Dashboard() {

  // INPUT STATE
  const [compound, setCompound] = useState("MEDIUM");
  const [tyreAge, setTyreAge] = useState(10);
  const [gapAhead, setGapAhead] = useState(5);
  const [gapBehind, setGapBehind] = useState(20);
  const [circuit, setCircuit] = useState("Bahrain");

  // OUTPUT STATE
  const [result, setResult] = useState<any>(null);
  const [sim, setSim] = useState<any>(null);

  const payload = {
    compound,
    tyre_age: tyreAge,
    circuit,
    gap_ahead: gapAhead,
    gap_behind: gapBehind,
  };

  // AUTO RUN (pro feel, no button spam)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getStrategy(payload);
        const simRes = await simulate(payload);
        setResult(res);
        setSim(simRes);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, [compound, tyreAge, gapAhead, gapBehind, circuit]);

  return (
    <main className="min-h-screen bg-[#050505] text-white flex">

      {/* LEFT PANEL */}
      <div className="w-1/4 p-6 border-r border-zinc-800">
        <h2 className="text-lg tracking-widest text-red-500 mb-6">
          RACE INPUTS
        </h2>

        <div className="space-y-6 text-sm">

          <div>
            <label className="text-gray-400">Circuit</label>
            <select
              className="w-full bg-zinc-900 p-2 mt-1"
              onChange={(e) => setCircuit(e.target.value)}
            >
              <option>Bahrain</option>
              <option>Monza</option>
              <option>Silverstone</option>
            </select>
          </div>

          <div>
            <label className="text-gray-400">Tyre</label>
            <select
              className="w-full bg-zinc-900 p-2 mt-1"
              onChange={(e) => setCompound(e.target.value)}
            >
              <option>SOFT</option>
              <option>MEDIUM</option>
              <option>HARD</option>
            </select>
          </div>

          <div>
            <label className="text-gray-400">Tyre Age: {tyreAge}</label>
            <input
              type="range"
              min="1"
              max="30"
              value={tyreAge}
              onChange={(e) => setTyreAge(Number(e.target.value))}
              className="w-full"
            />
          </div>

          <div>
            <label className="text-gray-400">Gap Ahead: {gapAhead}s</label>
            <input
              type="range"
              min="0"
              max="20"
              value={gapAhead}
              onChange={(e) => setGapAhead(Number(e.target.value))}
              className="w-full"
            />
          </div>

          <div>
            <label className="text-gray-400">Gap Behind: {gapBehind}s</label>
            <input
              type="range"
              min="0"
              max="30"
              value={gapBehind}
              onChange={(e) => setGapBehind(Number(e.target.value))}
              className="w-full"
            />
          </div>

        </div>
      </div>

      {/* CENTER PANEL */}
      <div className="w-2/4 p-6">

        <h1 className="text-2xl font-bold mb-6 tracking-wide">
          STRATEGY CONTROL
        </h1>

        {/* STRATEGY CARD */}
        {result && (
          <div className="bg-zinc-900 p-6 mb-6 border border-zinc-800">

            <h2 className="text-sm text-gray-400 mb-2">
              DECISION
            </h2>

            <p className={`text-2xl font-bold ${
              result.action.includes("PIT")
                ? "text-red-500"
                : "text-green-400"
            }`}>
              {result.action}
            </p>

            <div className="mt-4">
              <div className="text-sm text-gray-400">
                Confidence
              </div>

              <div className="w-full bg-zinc-800 h-2 mt-1">
                <div
                  className="bg-green-400 h-2"
                  style={{
                    width: `${result.confidence * 100}%`,
                  }}
                />
              </div>
            </div>

            <p className="text-gray-500 text-sm mt-4">
              {result.reasoning}
            </p>

          </div>
        )}

        {/* SIMULATION */}
        {sim && (
          <div className="bg-zinc-900 p-6 border border-zinc-800">

            <h2 className="text-sm text-gray-400 mb-4">
              SIMULATION
            </h2>

            <div className="grid grid-cols-3 gap-4 text-center">

              <div>
                <p className="text-xs text-gray-400">Stay</p>
                <p className="text-lg">{sim.stay_out_loss}s</p>
              </div>

              <div>
                <p className="text-xs text-gray-400">Pit</p>
                <p className="text-lg">{sim.pit_loss}s</p>
              </div>

              <div>
                <p className="text-xs text-gray-400">Undercut</p>
                <p className="text-lg">
                  {sim.undercut_possible ? "YES" : "NO"}
                </p>
              </div>

            </div>

          </div>
        )}

      </div>

      {/* RIGHT PANEL (AI COMING NEXT) */}
      <div className="w-1/4 p-6 border-l border-zinc-800">
        <h2 className="text-lg text-blue-400 mb-4">
          AI ENGINEER
        </h2>

        <p className="text-gray-500 text-sm">
          Chat integration coming next step.
        </p>
      </div>

    </main>
  );
}