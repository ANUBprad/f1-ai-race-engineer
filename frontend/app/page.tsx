"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function Home() {
  const router = useRouter();
  const nextSectionRef = useRef<HTMLDivElement>(null);

  // Auto-scroll after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      nextSectionRef.current?.scrollIntoView({
        behavior: "smooth",
      });
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <main className="bg-[#050505] text-white overflow-x-hidden">

      {/* HERO SECTION */}
      <section className="h-screen flex flex-col justify-center items-center text-center relative">

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-6xl font-bold mb-6 tracking-wide"
        >
          🏁 F1 AI Race Engineer
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-gray-400 text-lg"
        >
          Precision • Strategy • Telemetry Intelligence
        </motion.p>

        {/* Scanning text */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          className="mt-10 text-sm text-gray-500"
        >
          Initializing race systems...
        </motion.div>

        {/* Scroll indicator (optional but included) */}
        <div className="absolute bottom-10 text-gray-500 animate-bounce">
          ↓
        </div>

      </section>

      {/* MAIN SECTION */}
      <section
        ref={nextSectionRef}
        className="min-h-screen flex flex-col items-center justify-center px-6"
      >

        <motion.h2
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-4xl font-bold mb-10"
        >
          Enter the Control System
        </motion.h2>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="flex flex-col sm:flex-row gap-6"
        >

          <button
            onClick={() => router.push("/dashboard")}
            className="bg-red-600 px-8 py-4 text-lg tracking-wide hover:bg-red-500 transition"
          >
            Dashboard
          </button>

          <button
            onClick={() => router.push("/strategy")}
            className="border border-gray-600 px-8 py-4 text-lg hover:border-red-500 transition"
          >
            Strategy Lab
          </button>

          <button
            onClick={() => router.push("/chat")}
            className="bg-zinc-800 px-8 py-4 text-lg hover:bg-zinc-700 transition"
          >
            AI Engineer
          </button>

        </motion.div>

      </section>

    </main>
  );
}