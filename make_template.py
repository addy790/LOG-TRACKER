# -*- coding: utf-8 -*-
"""
Script to build the single-file index.html for GATE Tracker Pro.
"""

import json

def build_index_html():
    html_template = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GATE Tracker Pro - AI-Powered Preparation OS</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          },
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              200: '#c7d2fe',
              300: '#a5b4fc',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              800: '#3730a3',
              900: '#312e81',
              950: '#1e1b4b'
            },
            slate: {
              100: 'var(--text)',
              200: 'var(--text)',
              300: 'var(--muted)',
              400: 'var(--muted)',
              500: 'var(--muted)',
              600: 'var(--muted)',
              700: 'var(--border)',
              750: 'var(--bg)',
              800: 'var(--input-bg)',
              850: 'var(--bg)',
              900: 'var(--bg)',
              950: 'var(--bg)'
            }
          }
        }
      }
    }
  </script>

  <!-- Dexie.js (IndexedDB) -->
  <script src="https://unpkg.com/dexie@latest/dist/dexie.js"></script>

  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <!-- Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

  <style>
    /* === THEME VARIABLES === */
    :root {
      --bg: #f8fafc;
      --text: #1e293b;
      --muted: #64748b;
      --border: rgba(0, 0, 0, 0.08);
      --border-subtle: rgba(0, 0, 0, 0.04);
      --card-bg: rgba(255, 255, 255, 0.75);
      --card-bg-gradient: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(241, 245, 249, 0.8) 100%);
      --input-bg: #ffffff;
      --input-text: #0f172a;
      --hover: rgba(0, 0, 0, 0.04);
      --nav-bg: rgba(255, 255, 255, 0.85);
      --header-bg: rgba(255, 255, 255, 0.75);
      --title-color: #0f172a;
    }
    
    html.dark {
      --bg: #070c18;
      --text: #f8fafc;
      --muted: #94a3b8;
      --border: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.05);
      --card-bg: rgba(30, 41, 59, 0.6);
      --card-bg-gradient: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
      --input-bg: rgba(15, 23, 42, 0.75);
      --input-text: #f8fafc;
      --hover: rgba(255, 255, 255, 0.05);
      --nav-bg: rgba(15, 23, 42, 0.85);
      --header-bg: rgba(15, 23, 42, 0.75);
      --title-color: #ffffff;
    }

    body {
      background: var(--bg);
      color: var(--text);
      transition: background 0.3s, color 0.3s;
    }

    /* Glassmorphic elements mapped to CSS Variables */
    .glass-nav {
      background: var(--nav-bg) !important;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-right: 1px solid var(--border) !important;
    }
    .glass-header {
      background: var(--header-bg) !important;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border) !important;
    }
    .glass-panel {
      background: var(--card-bg) !important;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--border) !important;
    }
    .glass-panel-subtle {
      background: var(--card-bg) !important;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle) !important;
    }
    .glass-card {
      background: var(--card-bg-gradient) !important;
      backdrop-filter: blur(12px);
      border: 1px solid var(--border) !important;
      transition: all 0.2s ease-in-out;
    }
    .glass-card:hover {
      border-color: rgba(99, 102, 241, 0.35) !important;
      transform: translateY(-1px);
    }
    .glass-input {
      background: var(--input-bg) !important;
      border: 1px solid var(--border) !important;
      color: var(--input-text) !important;
      transition: all 0.2s ease;
    }
    .glass-input:focus {
      border-color: #6366f1 !important;
      background: var(--input-bg) !important;
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
      outline: none;
    }

    /* Override hardcoded text-white/text-slate-100 in Light Mode */
    html:not(.dark) .text-white,
    html:not(.dark) h1,
    html:not(.dark) h2,
    html:not(.dark) h3,
    html:not(.dark) h4,
    html:not(.dark) h5,
    html:not(.dark) h6 {
      color: var(--text) !important;
    }
    html:not(.dark) .hover\:text-white:hover {
      color: var(--text) !important;
    }
    html:not(.dark) .group-hover\:text-white:group-hover {
      color: var(--text) !important;
    }
    html:not(.dark) [class*="border-white/"] {
      border-color: var(--border) !important;
    }
    html:not(.dark) [class*="bg-slate-900/"] {
      background-color: var(--input-bg) !important;
    }
    html:not(.dark) [class*="bg-slate-800/"] {
      background-color: var(--hover) !important;
    }
    html:not(.dark) .glass-nav button.active {
      background-color: var(--hover) !important;
      color: var(--text) !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: var(--muted);
      opacity: 0.3;
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(148, 163, 184, 0.7);
    }

    /* Gradients and Glows */
    .text-gradient-brand {
      background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .text-gradient-amber {
      background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .text-gradient-emerald {
      background: linear-gradient(135deg, #34d399 0%, #059669 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .text-gradient-rose {
      background: linear-gradient(135deg, #fb7185 0%, #e11d48 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .glow-brand {
      box-shadow: 0 0 25px -4px rgba(99, 102, 241, 0.4);
    }
    .glow-emerald {
      box-shadow: 0 0 25px -4px rgba(16, 185, 129, 0.35);
    }
    .glow-rose {
      box-shadow: 0 0 25px -4px rgba(244, 63, 94, 0.35);
    }

    /* Modal Backdrop */
    .modal-backdrop {
      background: rgba(3, 7, 18, 0.85);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }

    /* Animations */
    @keyframes pulse-subtle {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.65; }
    }
    .animate-pulse-subtle {
      animation: pulse-subtle 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .animate-fadeIn {
      animation: fadeIn 0.25s ease-out forwards;
    }

    /* === DE-CRAMPING & SPACING === */
    #main-viewport {
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem !important;
    }
    .glass-panel, .glass-card {
      padding: 1.5rem !important;
      margin-bottom: 1.5rem;
    }
    .grid {
      gap: 1.5rem !important;
    }
    #app-sidebar {
      min-width: 260px;
    }
    #app-sidebar > div:first-child {
      padding: 1.75rem 1.5rem !important;
    }
    #app-sidebar .nav-btn {
      padding: 0.75rem 1.25rem !important;
      margin-bottom: 0.35rem;
    }
    td, th {
      padding: 0.75rem 1rem !important;
    }
    #today-schedule li {
      padding: 1rem 1.25rem !important;
      margin-bottom: 0.75rem;
    }
    button, .btn, .btn-outline {
      margin-right: 0.5rem;
      margin-bottom: 0.5rem;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen h-screen overflow-hidden antialiased select-none flex">

  <!-- Toast Notification Container -->
  <div id="toast-container" class="fixed top-5 right-5 z-[9999] flex flex-col gap-3 max-w-sm pointer-events-none"></div>

  <!-- Onboarding Screen (Wizard Overlay) -->
  <div id="onboarding-overlay" class="fixed inset-0 z-50 bg-slate-950 flex items-center justify-center p-4 sm:p-6 overflow-y-auto hidden">
    <div class="glass-panel w-full max-w-2xl rounded-2xl p-6 sm:p-10 shadow-2xl border border-white/10 relative overflow-hidden my-auto">
      
      <!-- Background Ambient Glow -->
      <div class="absolute -top-24 -right-24 w-72 h-72 bg-brand-600/20 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-24 -left-24 w-72 h-72 bg-violet-600/20 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header & Progress -->
      <div class="relative z-10 mb-8">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-violet-500 flex items-center justify-center text-white shadow-lg glow-brand">
              <i data-lucide="zap" class="w-5 h-5"></i>
            </div>
            <div>
              <h1 class="text-xl font-bold text-white tracking-tight">GATE Tracker <span class="text-gradient-brand">PRO</span></h1>
              <p class="text-xs text-slate-400">Personalized AI Preparation OS</p>
            </div>
          </div>
          <div class="text-xs font-mono text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-full border border-white/5">
            Step <span id="onboard-step-num" class="text-brand-400 font-bold">1</span> of 6
          </div>
        </div>

        <!-- Step Progress Bar -->
        <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
          <div id="onboard-progress-bar" class="h-full bg-gradient-to-r from-brand-500 to-violet-500 transition-all duration-300 w-1/6"></div>
        </div>
      </div>

      <!-- Step 1: Welcome & Gemini API Key -->
      <div id="onboard-step-1" class="onboard-step space-y-6 relative z-10">
        <div>
          <h2 class="text-2xl font-bold text-white mb-2">Welcome, Future Ranker! 🎯</h2>
          <p class="text-slate-300 text-sm leading-relaxed">
            Configure your AI Super-Engine. GATE Tracker Pro uses Gemini 1.5 Flash to generate custom GATE-standard mock quizzes, evaluate step-by-step solutions, and auto-diagnose concept gaps.
          </p>
        </div>

        <div class="space-y-4 bg-slate-900/60 p-5 rounded-xl border border-white/5">
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Google Gemini API Key (Client-Side Only)
          </label>
          <div class="relative">
            <input type="password" id="ob-apikey" placeholder="AIzaSy..." class="w-full glass-input rounded-lg px-4 py-3 text-sm pr-28 font-mono">
            <button type="button" onclick="testGeminiConnection('ob')" id="ob-btn-test-key" class="absolute right-2 top-2 px-3 py-1.5 bg-brand-600 hover:bg-brand-500 text-white rounded-md text-xs font-medium transition flex items-center gap-1.5 shadow">
              <i data-lucide="activity" class="w-3.5 h-3.5"></i>
              <span>Test Key</span>
            </button>
          </div>
          <div id="ob-key-status" class="text-xs text-slate-400 flex items-center gap-2 hidden"></div>
          <p class="text-[11px] text-slate-400">
            🔒 Your API key is stored safely in your local IndexedDB. Never sent to any server. Free tier API keys can be generated at <a href="https://aistudio.google.com/app/apikey" target="_blank" class="text-brand-400 hover:underline">Google AI Studio</a>.
          </p>
        </div>

        <div class="flex items-center justify-between pt-4">
          <button onclick="skipApiKeyOnboarding()" class="text-xs text-slate-400 hover:text-slate-200 transition underline underline-offset-4">
            Skip for now (Run Offline Mode)
          </button>
          <button onclick="goOnboardingStep(2)" class="px-6 py-2.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-semibold rounded-xl text-sm transition shadow-lg glow-brand flex items-center gap-2">
            <span>Continue</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Step 2: Aspirant Profile -->
      <div id="onboard-step-2" class="onboard-step space-y-6 relative z-10 hidden">
        <div>
          <h2 class="text-2xl font-bold text-white mb-2">Aspirant Profile 👤</h2>
          <p class="text-slate-300 text-sm">Tell us about your target goals and academic background.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Full Name</label>
            <input type="text" id="ob-name" placeholder="Aditya Sharma" value="Aditya Sharma" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Current Status</label>
            <select id="ob-status" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
              <option value="Full-time Aspirant">Full-time Aspirant (Dropper)</option>
              <option value="Final Year Student" selected>Final Year College Student</option>
              <option value="3rd Year Student">3rd Year College Student</option>
              <option value="Working Professional">Working Professional</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Target AIR Goal</label>
            <input type="text" id="ob-air" placeholder="Top 50 / AIR < 100" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm" value="AIR < 50">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Target Marks (out of 100)</label>
            <input type="number" id="ob-target-marks" min="40" max="100" placeholder="80" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm" value="82">
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Dream Institute</label>
            <select id="ob-institute" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
              <option value="IISc Bangalore (CSA / CDS)" selected>IISc Bangalore (CSA / CDS)</option>
              <option value="IIT Bombay (CSE)">IIT Bombay (CSE)</option>
              <option value="IIT Delhi (CSE)">IIT Delhi (CSE)</option>
              <option value="IIT Madras (CSE)">IIT Madras (CSE)</option>
              <option value="IIT Kanpur (CSE)">IIT Kanpur (CSE)</option>
              <option value="IIT Kharagpur (CSE)">IIT Kharagpur (CSE)</option>
              <option value="IIT Roorkee (CSE)">IIT Roorkee (CSE)</option>
              <option value="Top PSU (ONGC / IOCL / BARC / ISRO)">Top PSU (ONGC / BARC / ISRO)</option>
              <option value="NIT Trichy / Surathkal / Warangal">Top NITs (Trichy / Surathkal / Warangal)</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-between pt-4">
          <button onclick="goOnboardingStep(1)" class="px-5 py-2.5 glass-panel hover:bg-slate-800 text-slate-300 rounded-xl text-sm font-medium transition flex items-center gap-2">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            <span>Back</span>
          </button>
          <button onclick="goOnboardingStep(3)" class="px-6 py-2.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-semibold rounded-xl text-sm transition shadow-lg glow-brand flex items-center gap-2">
            <span>Continue</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Step 3: Exam Config -->
      <div id="onboard-step-3" class="onboard-step space-y-6 relative z-10 hidden">
        <div>
          <h2 class="text-2xl font-bold text-white mb-2">Exam Configuration 📅</h2>
          <p class="text-slate-300 text-sm">Select your stream and customize your target timeline.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">GATE Stream</label>
            <select id="ob-stream" onchange="handleStreamChange(this.value)" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
              <option value="CS" selected>Computer Science & IT (CS)</option>
              <option value="DA">Data Science & AI (DA)</option>
              <option value="EC">Electronics & Comm. (EC)</option>
              <option value="EE">Electrical Engg. (EE)</option>
              <option value="ME">Mechanical Engg. (ME)</option>
              <option value="CE">Civil Engg. (CE)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Target GATE Exam Date</label>
            <input type="date" id="ob-exam-date" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Daily Study Hours Target</label>
            <select id="ob-daily-hours" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
              <option value="4">4 Hours / Day (Moderate / Working)</option>
              <option value="6">6 Hours / Day (Standard)</option>
              <option value="8" selected>8 Hours / Day (Gaokao High-Yield)</option>
              <option value="10">10 Hours / Day (War Mode)</option>
              <option value="12">12 Hours / Day (Final Crunch)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Current Prep Level</label>
            <select id="ob-level" class="w-full glass-input rounded-lg px-4 py-2.5 text-sm">
              <option value="Beginner">Beginner (Starting from scratch)</option>
              <option value="Intermediate" selected>Intermediate (Covered basic subjects)</option>
              <option value="Advanced">Advanced (Revision & Test Series stage)</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-between pt-4">
          <button onclick="goOnboardingStep(2)" class="px-5 py-2.5 glass-panel hover:bg-slate-800 text-slate-300 rounded-xl text-sm font-medium transition flex items-center gap-2">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            <span>Back</span>
          </button>
          <button onclick="goOnboardingStep(4)" class="px-6 py-2.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-semibold rounded-xl text-sm transition shadow-lg glow-brand flex items-center gap-2">
            <span>Continue</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Step 4: Timetable Choice -->
      <div id="onboard-step-4" class="onboard-step space-y-6 relative z-10 hidden">
        <div>
          <h2 class="text-2xl font-bold text-white mb-2">Timetable Strategy ⚡</h2>
          <p class="text-slate-300 text-sm">Select how your preparation blocks should be scheduled.</p>
        </div>

        <div class="grid grid-cols-1 gap-3.5">
          <!-- Option A: Gaokao 180-Day -->
          <label class="cursor-pointer">
            <input type="radio" name="ob-strategy" value="gaokao" checked class="peer sr-only">
            <div class="p-4 rounded-xl border border-white/10 bg-slate-900/60 peer-checked:border-brand-500 peer-checked:bg-brand-950/30 peer-checked:ring-1 peer-checked:ring-brand-500 transition space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-semibold text-white text-sm flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  Option A: AI-Recommended 180-Day Gaokao Protocol
                </span>
                <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-brand-500/20 text-brand-300 rounded border border-brand-500/30">Recommended</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                Dynamic 3-Phase split: Phase 1 (Foundation & Theory), Phase 2 (PYQ & Error Eradication), Phase 3 (Full Mocks & Speed drills). Organizes daily 3 structured blocks (Morning Concept, Afternoon PYQ, Night Spaced Repetition).
              </p>
            </div>
          </label>

          <!-- Option B: Custom Builder -->
          <label class="cursor-pointer">
            <input type="radio" name="ob-strategy" value="custom" class="peer sr-only">
            <div class="p-4 rounded-xl border border-white/10 bg-slate-900/60 peer-checked:border-brand-500 peer-checked:bg-brand-950/30 peer-checked:ring-1 peer-checked:ring-brand-500 transition space-y-1.5">
              <span class="font-semibold text-white text-sm">Option B: Custom Weekly Time-Block Builder</span>
              <p class="text-xs text-slate-300 leading-relaxed">
                Build your own recurring weekly pattern with custom time blocks for College, Office, and Deep Study slots.
              </p>
            </div>
          </label>

          <!-- Option C: JSON Backup Import -->
          <label class="cursor-pointer">
            <input type="radio" name="ob-strategy" value="import" class="peer sr-only">
            <div class="p-4 rounded-xl border border-white/10 bg-slate-900/60 peer-checked:border-brand-500 peer-checked:bg-brand-950/30 peer-checked:ring-1 peer-checked:ring-brand-500 transition space-y-1.5">
              <span class="font-semibold text-white text-sm">Option C: Restore from JSON Backup</span>
              <p class="text-xs text-slate-300 leading-relaxed">
                Import an existing GATE Tracker Pro JSON backup file and restore full state instantly.
              </p>
            </div>
          </label>
        </div>

        <div class="flex items-center justify-between pt-4">
          <button onclick="goOnboardingStep(3)" class="px-5 py-2.5 glass-panel hover:bg-slate-800 text-slate-300 rounded-xl text-sm font-medium transition flex items-center gap-2">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            <span>Back</span>
          </button>
          <button onclick="goOnboardingStep(5)" class="px-6 py-2.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-semibold rounded-xl text-sm transition shadow-lg glow-brand flex items-center gap-2">
            <span>Continue</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Step 5: Syllabus Selection & Weightage Preview -->
      <div id="onboard-step-5" class="onboard-step space-y-6 relative z-10 hidden">
        <div>
          <h2 class="text-2xl font-bold text-white mb-2">Syllabus Matrix & Weightage 📚</h2>
          <p class="text-slate-300 text-sm">Review the official high-yield subject breakdown for your stream.</p>
        </div>

        <div id="ob-syllabus-preview" class="max-h-60 overflow-y-auto space-y-2 pr-1">
          <!-- Populated by JS -->
        </div>

        <div class="flex items-center justify-between pt-4">
          <button onclick="goOnboardingStep(4)" class="px-5 py-2.5 glass-panel hover:bg-slate-800 text-slate-300 rounded-xl text-sm font-medium transition flex items-center gap-2">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            <span>Back</span>
          </button>
          <button onclick="finishOnboarding()" class="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold rounded-xl text-sm transition shadow-lg glow-emerald flex items-center gap-2">
            <span>Complete Setup</span>
            <i data-lucide="check-circle-2" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Step 6: Celebration & Launch -->
      <div id="onboard-step-6" class="onboard-step space-y-6 relative z-10 hidden text-center py-4">
        <div class="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-tr from-brand-500 to-violet-500 flex items-center justify-center text-white shadow-2xl glow-brand animate-bounce">
          <i data-lucide="trophy" class="w-10 h-10"></i>
        </div>

        <div class="space-y-2">
          <h2 class="text-3xl font-extrabold text-white tracking-tight">You're All Set for AIR 1! 🚀</h2>
          <p class="text-slate-300 text-sm max-w-md mx-auto">
            Your 180-Day Gaokao preparation roadmap, Spaced Repetition Error Engine, and AI Question Center are calibrated.
          </p>
        </div>

        <div class="glass-panel p-4 rounded-xl max-w-md mx-auto grid grid-cols-3 gap-2 text-center text-xs">
          <div>
            <div class="text-slate-400">Target</div>
            <div id="ob-sum-target" class="font-bold text-white text-sm">AIR < 50</div>
          </div>
          <div>
            <div class="text-slate-400">Days Left</div>
            <div id="ob-sum-days" class="font-bold text-brand-400 text-sm">--</div>
          </div>
          <div>
            <div class="text-slate-400">Daily Target</div>
            <div id="ob-sum-hours" class="font-bold text-emerald-400 text-sm">8h / day</div>
          </div>
        </div>

        <div class="pt-2">
          <button onclick="launchAppFromOnboarding()" class="px-8 py-3.5 bg-gradient-to-r from-brand-600 via-violet-600 to-brand-500 hover:opacity-95 text-white font-bold rounded-xl text-base transition shadow-xl glow-brand inline-flex items-center gap-2">
            <span>Enter Preparation War Room</span>
            <i data-lucide="arrow-right" class="w-5 h-5"></i>
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- Main Application Layout -->
  <div id="main-layout" class="flex w-full h-full overflow-hidden relative">

    <!-- Sidebar Navigation -->
    <aside id="app-sidebar" class="w-64 glass-nav flex flex-col justify-between h-full shrink-0 z-30 transition-all duration-300">
      
      <!-- Top Brand -->
      <div class="p-5 border-b border-white/5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-violet-500 flex items-center justify-center text-white shadow-md glow-brand">
              <i data-lucide="shield-check" class="w-5 h-5"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
                GATE Tracker <span class="text-[10px] bg-brand-500/20 text-brand-300 px-1.5 py-0.5 rounded font-mono font-bold">PRO</span>
              </h2>
              <p id="sb-user-sub" class="text-[11px] text-slate-400 truncate max-w-[120px]">Aditya • CS</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Links -->
      <div class="flex-1 overflow-y-auto py-3 px-3 space-y-1">
        <button onclick="navigateTab('dashboard')" id="nav-dashboard" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group active">
          <div class="flex items-center gap-3">
            <i data-lucide="layout-dashboard" class="w-4 h-4 text-slate-400 group-hover:text-brand-400 transition"></i>
            <span>War Room</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">D</span>
        </button>

        <button onclick="navigateTab('timetable')" id="nav-timetable" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="calendar" class="w-4 h-4 text-slate-400 group-hover:text-brand-400 transition"></i>
            <span>Schedule & Timetable</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">T</span>
        </button>

        <button onclick="navigateTab('syllabus')" id="nav-syllabus" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="book-open" class="w-4 h-4 text-slate-400 group-hover:text-brand-400 transition"></i>
            <span>Syllabus Matrix</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">S</span>
        </button>

        <button onclick="navigateTab('pyq')" id="nav-pyq" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="layers" class="w-4 h-4 text-slate-400 group-hover:text-brand-400 transition"></i>
            <span>PYQ Tracker</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">P</span>
        </button>

        <button onclick="navigateTab('error')" id="nav-error" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="alert-triangle" class="w-4 h-4 text-slate-400 group-hover:text-rose-400 transition"></i>
            <span>Error Log (SRS)</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span id="sb-error-badge" class="text-[10px] font-bold bg-rose-500/20 text-rose-300 px-1.5 py-0.2 rounded-full hidden">0</span>
            <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">E</span>
          </div>
        </button>

        <button onclick="navigateTab('mocks')" id="nav-mocks" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="target" class="w-4 h-4 text-slate-400 group-hover:text-amber-400 transition"></i>
            <span>Mock Test Center</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">M</span>
        </button>

        <button onclick="navigateTab('ai-test')" id="nav-ai-test" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="bot" class="w-4 h-4 text-slate-400 group-hover:text-violet-400 transition"></i>
            <span>AI Test Center</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">A</span>
        </button>

        <button onclick="navigateTab('analytics')" id="nav-analytics" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-400 group-hover:text-emerald-400 transition"></i>
            <span>Analytics & Radar</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">N</span>
        </button>

        <div class="pt-4 pb-1">
          <div class="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-500">System</div>
        </div>

        <button onclick="navigateTab('settings')" id="nav-settings" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="settings" class="w-4 h-4 text-slate-400 group-hover:text-slate-200 transition"></i>
            <span>Settings & Backup</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">O</span>
        </button>

        <button onclick="navigateTab('help')" id="nav-help" class="nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition group">
          <div class="flex items-center gap-3">
            <i data-lucide="help-circle" class="w-4 h-4 text-slate-400 group-hover:text-slate-200 transition"></i>
            <span>Gaokao Guide & Hotkeys</span>
          </div>
          <span class="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">?</span>
        </button>
      </div>

      <!-- Mini Pomodoro Widget in Sidebar Footer -->
      <div class="p-3 border-t border-white/5 bg-slate-900/40">
        <div class="glass-panel p-3 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5">
              <i data-lucide="timer" class="w-3.5 h-3.5 text-brand-400"></i>
              Focus Pomodoro
            </span>
            <span id="sb-pomo-status" class="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">25:00</span>
          </div>
          <div class="flex items-center gap-1.5">
            <button onclick="togglePomoTimer()" id="sb-btn-pomo-toggle" class="flex-1 py-1 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold transition">
              Start
            </button>
            <button onclick="resetPomoTimer()" class="p-1 glass-panel hover:bg-slate-800 text-slate-400 hover:text-slate-200 rounded-lg text-xs transition" title="Reset">
              <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col h-full overflow-hidden bg-slate-950">
      
      <!-- Top Navigation Header -->
      <header class="glass-header px-6 py-3.5 flex items-center justify-between shrink-0 z-20">
        <div class="flex items-center gap-4">
          <button onclick="toggleSidebar()" class="lg:hidden text-slate-400 hover:text-white p-1 rounded-lg">
            <i data-lucide="menu" class="w-5 h-5"></i>
          </button>
          <div>
            <h2 id="top-view-title" class="text-sm font-bold text-white flex items-center gap-2">
              Preparation War Room
            </h2>
            <p id="top-view-sub" class="text-[11px] text-slate-400">Live Mission Control & Milestone Radar</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <!-- Countdown Timer Pill -->
          <div class="glass-panel px-3.5 py-1.5 rounded-full flex items-center gap-2 border border-brand-500/20 text-xs font-semibold text-slate-200 shadow-sm">
            <span class="w-2 h-2 rounded-full bg-brand-400 animate-ping"></span>
            <i data-lucide="clock" class="w-3.5 h-3.5 text-brand-400"></i>
            <span id="top-countdown" class="font-mono text-brand-300">-- Days Left</span>
          </div>

          <!-- Study Streak Pill -->
          <div class="glass-panel px-3 py-1.5 rounded-full flex items-center gap-1.5 text-xs font-semibold text-amber-300 border border-amber-500/20">
            <i data-lucide="flame" class="w-3.5 h-3.5 text-amber-400"></i>
            <span id="top-streak" class="font-mono">1-Day Streak</span>
          </div>

          <!-- Timetable Weekly Edit Pill -->
          <div id="top-edit-warning-pill" class="glass-panel px-3 py-1.5 rounded-full flex items-center gap-1.5 text-xs font-semibold text-slate-300 border border-white/10 hidden">
            <i data-lucide="git-commit" class="w-3.5 h-3.5 text-slate-400"></i>
            <span id="top-edit-count" class="font-mono text-[11px]">0/3 Changes this week</span>
          </div>

          <!-- Quick Action Button -->
          <div class="relative">
            <button onclick="toggleQuickMenu()" class="px-3.5 py-1.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-semibold rounded-xl text-xs transition shadow-md glow-brand flex items-center gap-1.5">
              <i data-lucide="plus" class="w-3.5 h-3.5"></i>
              <span>Quick Log</span>
            </button>

            <!-- Quick Action Dropdown -->
            <div id="quick-log-dropdown" class="absolute right-0 mt-2 w-48 glass-panel rounded-xl shadow-2xl border border-white/10 p-1.5 space-y-1 z-50 hidden">
              <button onclick="openModal('modal-add-pyq'); toggleQuickMenu()" class="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-800/80 rounded-lg transition">
                <i data-lucide="layers" class="w-3.5 h-3.5 text-brand-400"></i>
                <span>Log PYQ Problem</span>
              </button>
              <button onclick="openModal('modal-add-error'); toggleQuickMenu()" class="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-800/80 rounded-lg transition">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-rose-400"></i>
                <span>Log Mistake / Error</span>
              </button>
              <button onclick="openModal('modal-add-mock'); toggleQuickMenu()" class="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-800/80 rounded-lg transition">
                <i data-lucide="target" class="w-3.5 h-3.5 text-amber-400"></i>
                <span>Log Mock Test</span>
              </button>
              <button onclick="navigateTab('ai-test'); toggleQuickMenu()" class="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-800/80 rounded-lg transition">
                <i data-lucide="bot" class="w-3.5 h-3.5 text-violet-400"></i>
                <span>Generate AI Test</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Scrollable Main Viewport -->
      <main id="main-viewport" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        
        <!-- VIEW: DASHBOARD / WAR ROOM -->
        <section id="view-dashboard" class="app-view space-y-6 animate-fadeIn">
          
          <!-- Dynamic Milestone & Phase Banner -->
          <div id="dash-milestone-banner" class="glass-panel p-4 sm:p-5 rounded-2xl border border-brand-500/30 bg-gradient-to-r from-brand-950/40 via-slate-900/60 to-violet-950/40 relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="space-y-1 relative z-10">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 bg-brand-500/20 text-brand-300 text-[11px] font-bold rounded-full border border-brand-500/30 uppercase tracking-wider">
                  Phase 1: Foundation & Core Concepts
                </span>
                <span class="text-xs text-slate-400" id="dash-milestone-days-left">-- days remaining in phase</span>
              </div>
              <h3 class="text-base sm:text-lg font-bold text-white">Daily Target: 100% Subject Coverage + Error Eradication</h3>
              <p class="text-xs text-slate-300 max-w-2xl leading-relaxed">
                Consistency Protocol: Complete today's 3 scheduled blocks. Never go to sleep with unreviewed SRS error flashcards.
              </p>
            </div>

            <div class="flex items-center gap-2 shrink-0 relative z-10">
              <button onclick="navigateTab('ai-test')" class="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand flex items-center gap-1.5">
                <i data-lucide="zap" class="w-3.5 h-3.5"></i>
                <span>Daily AI Drill</span>
              </button>
              <button onclick="openModal('modal-add-pyq')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-200 text-xs font-semibold rounded-xl transition flex items-center gap-1.5">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                <span>Log PYQs</span>
              </button>
            </div>
          </div>

          <!-- KPI Metric Cards Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3.5">
            
            <!-- Card 1: Syllabus Coverage -->
            <div class="glass-card p-4 rounded-2xl space-y-2">
              <div class="flex items-center justify-between text-slate-400">
                <span class="text-[11px] font-semibold">Syllabus</span>
                <i data-lucide="book-open" class="w-4 h-4 text-brand-400"></i>
              </div>
              <div class="flex items-baseline justify-between">
                <span id="dash-stat-syllabus" class="text-xl sm:text-2xl font-extrabold text-white">0%</span>
                <span id="dash-stat-topics-count" class="text-[10px] text-slate-400 font-mono">0/0</span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div id="dash-stat-syllabus-bar" class="h-full bg-brand-500 transition-all duration-300 w-0"></div>
              </div>
            </div>

            <!-- Card 2: PYQs Solved -->
            <div class="glass-card p-4 rounded-2xl space-y-2">
              <div class="flex items-center justify-between text-slate-400">
                <span class="text-[11px] font-semibold">PYQs Logged</span>
                <i data-lucide="layers" class="w-4 h-4 text-emerald-400"></i>
              </div>
              <div class="flex items-baseline justify-between">
                <span id="dash-stat-pyq" class="text-xl sm:text-2xl font-extrabold text-white">0</span>
                <span id="dash-stat-pyq-acc" class="text-[10px] text-emerald-400 font-mono">--% Acc</span>
              </div>
              <div class="text-[10px] text-slate-400 truncate">GATE 2000-2024</div>
            </div>

            <!-- Card 3: Mocks Attempted -->
            <div class="glass-card p-4 rounded-2xl space-y-2">
              <div class="flex items-center justify-between text-slate-400">
                <span class="text-[11px] font-semibold">Mocks Taken</span>
                <i data-lucide="target" class="w-4 h-4 text-amber-400"></i>
              </div>
              <div class="flex items-baseline justify-between">
                <span id="dash-stat-mock" class="text-xl sm:text-2xl font-extrabold text-white">0</span>
                <span id="dash-stat-mock-avg" class="text-[10px] text-amber-400 font-mono">Avg: --</span>
              </div>
              <div class="text-[10px] text-slate-400 truncate">Pred. AIR: <span id="dash-stat-pred-air" class="text-white font-bold">--</span></div>
            </div>

            <!-- Card 4: SRS Errors Due Today -->
            <div class="glass-card p-4 rounded-2xl space-y-2 cursor-pointer hover:border-rose-500/40" onclick="startDailyReviewSession()">
              <div class="flex items-center justify-between text-slate-400">
                <span class="text-[11px] font-semibold">Errors Due (SRS)</span>
                <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400"></i>
              </div>
              <div class="flex items-baseline justify-between">
                <span id="dash-stat-errors-due" class="text-xl sm:text-2xl font-extrabold text-rose-400">0</span>
                <span class="text-[10px] text-rose-300 font-bold uppercase tracking-wider">Review</span>
              </div>
              <div class="text-[10px] text-slate-400">Total in log: <span id="dash-stat-errors-total">0</span></div>
            </div>

            <!-- Card 5: Today's Study Hours -->
            <div class="glass-card p-4 rounded-2xl space-y-2">
              <div class="flex items-center justify-between text-slate-400">
                <span class="text-[11px] font-semibold">Today's Focus</span>
                <i data-lucide="clock-3" class="w-4 h-4 text-cyan-400"></i>
              </div>
              <div class="flex items-baseline justify-between">
                <span id="dash-stat-today-hours" class="text-xl sm:text-2xl font-extrabold text-white">0.0h</span>
                <span id="dash-stat-target-hours" class="text-[10px] text-slate-400 font-mono">/ 8.0h</span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div id="dash-stat-today-hours-bar" class="h-full bg-cyan-400 transition-all duration-300 w-0"></div>
              </div>
            </div>

            <!-- Card 6: AI Quizzes Done -->
            <div class="glass-card p-4 rounded-2xl space-y-2">
              <div class="flex items-center justify-between text-slate-400">
                <span class="text-[11px] font-semibold">AI Quizzes</span>
                <i data-lucide="bot" class="w-4 h-4 text-violet-400"></i>
              </div>
              <div class="flex items-baseline justify-between">
                <span id="dash-stat-ai-quizzes" class="text-xl sm:text-2xl font-extrabold text-white">0</span>
                <span class="text-[10px] text-violet-300 font-mono">Flash 1.5</span>
              </div>
              <div class="text-[10px] text-slate-400">Auto-graded & logged</div>
            </div>

          </div>

          <!-- Main Interactive Dashboard Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Left 2 Cols: Today's Timeblocks & Weekly Mini-Timeline -->
            <div class="lg:col-span-2 space-y-6">
              
              <!-- Today's Timeblocks Widget -->
              <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-brand-500/20 text-brand-400 flex items-center justify-center">
                      <i data-lucide="check-square" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <h4 class="text-sm font-bold text-white">Today's Gaokao Time Blocks</h4>
                      <p class="text-[11px] text-slate-400" id="dash-today-date-str">Loading date...</p>
                    </div>
                  </div>

                  <div class="flex items-center gap-2">
                    <button onclick="openModal('modal-add-task')" class="px-2.5 py-1 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-medium rounded-lg transition flex items-center gap-1">
                      <i data-lucide="plus" class="w-3 h-3"></i>
                      <span>Add Block</span>
                    </button>
                    <button onclick="autoFillGaokaoToday()" class="px-2.5 py-1 bg-brand-600/30 hover:bg-brand-600 text-brand-300 hover:text-white text-xs font-medium rounded-lg transition">
                      Auto-Schedule
                    </button>
                  </div>
                </div>

                <!-- Timeblock list with interactive cycle status -->
                <div id="dash-today-blocks-list" class="space-y-2.5">
                  <!-- Injected via JS -->
                </div>
              </div>

              <!-- Performance Trend Chart -->
              <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center">
                      <i data-lucide="trending-up" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <h4 class="text-sm font-bold text-white">Mock Score & Rank Progression</h4>
                      <p class="text-[11px] text-slate-400">Score vs Target Marks Curve</p>
                    </div>
                  </div>
                  <button onclick="navigateTab('mocks')" class="text-xs text-brand-400 hover:underline">View All Mocks &rarr;</button>
                </div>
                <div class="h-56 relative">
                  <canvas id="chart-dash-mock-progress"></canvas>
                </div>
              </div>

            </div>

            <!-- Right Col: Interactive Pomodoro Engine & SRS Due Alert -->
            <div class="space-y-6">
              
              <!-- Pomodoro Engine -->
              <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-4 text-center">
                <div class="flex items-center justify-between text-left">
                  <div class="flex items-center gap-2">
                    <i data-lucide="flame" class="w-4 h-4 text-brand-400"></i>
                    <span class="text-xs font-bold text-white uppercase tracking-wider">Deep Work Engine</span>
                  </div>
                  <div class="flex items-center gap-1">
                    <button onclick="setPomoMode(25)" id="pomo-mode-25" class="px-2 py-0.5 text-[10px] font-mono rounded bg-brand-600 text-white font-bold">25m</button>
                    <button onclick="setPomoMode(50)" id="pomo-mode-50" class="px-2 py-0.5 text-[10px] font-mono rounded bg-slate-800 text-slate-400">50m</button>
                  </div>
                </div>

                <!-- Big Timer Display -->
                <div class="py-2">
                  <div id="pomo-big-clock" class="text-4xl sm:text-5xl font-mono font-extrabold text-white tracking-wider">25:00</div>
                  <p id="pomo-subject-label" class="text-xs text-brand-300 mt-1 font-medium">Focus: Linear Algebra & PYQs</p>
                </div>

                <!-- Controls -->
                <div class="flex items-center justify-center gap-3">
                  <button onclick="togglePomoTimer()" id="dash-btn-pomo-main" class="px-6 py-2.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-bold rounded-xl text-sm transition shadow-lg glow-brand flex items-center gap-2">
                    <i data-lucide="play" class="w-4 h-4"></i>
                    <span id="pomo-main-btn-text">Start Focus</span>
                  </button>
                  <button onclick="resetPomoTimer()" class="p-2.5 glass-panel hover:bg-slate-800 text-slate-400 hover:text-slate-200 rounded-xl transition" title="Reset">
                    <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
                  </button>
                </div>

                <div class="pt-2 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
                  <span>Sessions Completed: <strong id="pomo-session-count" class="text-white">0</strong></span>
                  <button onclick="openModal('modal-manual-time')" class="text-brand-400 hover:underline">+ Log Study Time</button>
                </div>
              </div>

              <!-- Spaced Repetition Due Alert Card -->
              <div class="glass-panel p-5 rounded-2xl border border-rose-500/20 bg-rose-950/20 space-y-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
                    <h4 class="text-xs font-bold text-rose-300 uppercase tracking-wider">SRS Errors Due Today</h4>
                  </div>
                  <span id="dash-srs-due-badge" class="px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded text-xs font-bold font-mono">0 Due</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Review mistakes right when your memory curve decays to transform weak spots into automatic reflexes.
                </p>
                <button onclick="startDailyReviewSession()" class="w-full py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-semibold rounded-xl text-xs transition shadow-md glow-rose flex items-center justify-center gap-1.5">
                  <i data-lucide="repeat" class="w-3.5 h-3.5"></i>
                  <span>Launch Flashcard Review Mode</span>
                </button>
              </div>

              <!-- AI Advisor Quick Widget -->
              <div class="glass-panel p-5 rounded-2xl border border-violet-500/20 bg-violet-950/20 space-y-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <i data-lucide="sparkles" class="w-4 h-4 text-violet-400"></i>
                    <h4 class="text-xs font-bold text-violet-300 uppercase tracking-wider">AI Strategy Advisor</h4>
                  </div>
                  <button onclick="runAiStrategyAudit()" class="text-[11px] text-violet-300 hover:text-white underline">Refresh</button>
                </div>
                <p id="dash-ai-advisor-text" class="text-xs text-slate-300 leading-relaxed italic">
                  "Prioritize Discrete Mathematics & Data Structures this week. Solving 25 PYQs per day will push your score past 70+ marks."
                </p>
              </div>

            </div>

          </div>

        </section>

        <!-- VIEW: SCHEDULE & TIMETABLE -->
        <section id="view-timetable" class="app-view space-y-6 hidden animate-fadeIn">
          
          <!-- Timetable Top Bar & Warning Banner -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl border border-white/10">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <span>180-Day Gaokao Protocol Schedule</span>
                <span class="text-xs font-mono px-2 py-0.5 bg-brand-500/20 text-brand-300 rounded">Interactive Blocks</span>
              </h3>
              <p class="text-xs text-slate-400">Structured Phase Milestones & Daily Deep-Work Slots</p>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="openModal('modal-add-task')" class="px-3.5 py-2 glass-panel hover:bg-slate-800 text-slate-200 text-xs font-semibold rounded-xl transition flex items-center gap-1.5">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                <span>Add Custom Task</span>
              </button>
              <button onclick="requestRegenerateTimetable()" class="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand flex items-center gap-1.5">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
                <span>Regenerate Roadmap</span>
              </button>
            </div>
          </div>

          <!-- Weekly Change Warning Alert if >=3 changes -->
          <div id="timetable-change-alert-banner" class="glass-panel p-4 rounded-xl border border-amber-500/40 bg-amber-950/20 flex items-start gap-3 hidden">
            <i data-lucide="alert-triangle" class="w-5 h-5 text-amber-400 shrink-0 mt-0.5"></i>
            <div class="space-y-1">
              <h5 class="text-xs font-bold text-amber-300">Timetable Frequency Warning</h5>
              <p class="text-xs text-slate-300 leading-relaxed">
                You have modified your timetable <span id="tt-warning-change-count" class="font-bold text-white">3</span> times in the last 7 days. Consistency and adherence to the schedule is the #1 predictor of top 100 rank!
              </p>
            </div>
          </div>

          <!-- Phase Navigation Tabs -->
          <div class="flex items-center gap-2 border-b border-white/10 pb-3">
            <button onclick="filterTimetablePhase('all')" class="tt-phase-btn px-4 py-1.5 rounded-xl text-xs font-semibold bg-brand-600 text-white" id="tt-p-all">All Days</button>
            <button onclick="filterTimetablePhase('phase1')" class="tt-phase-btn px-4 py-1.5 rounded-xl text-xs font-semibold glass-panel text-slate-300 hover:bg-slate-800" id="tt-p-1">Phase 1: Foundation (Day 1-90)</button>
            <button onclick="filterTimetablePhase('phase2')" class="tt-phase-btn px-4 py-1.5 rounded-xl text-xs font-semibold glass-panel text-slate-300 hover:bg-slate-800" id="tt-p-2">Phase 2: PYQs & Errors (Day 91-150)</button>
            <button onclick="filterTimetablePhase('phase3')" class="tt-phase-btn px-4 py-1.5 rounded-xl text-xs font-semibold glass-panel text-slate-300 hover:bg-slate-800" id="tt-p-3">Phase 3: Speed Mocks (Day 151-180)</button>
          </div>

          <!-- Timetable Days Cards Grid -->
          <div id="timetable-days-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Injected via JS -->
          </div>

        </section>

        <!-- VIEW: SYLLABUS MATRIX -->
        <section id="view-syllabus" class="app-view space-y-6 hidden animate-fadeIn">
          
          <!-- Top Header -->
          <div class="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <span>GATE Syllabus Matrix & Weightage Tracker</span>
                <span id="syl-stream-badge" class="text-xs font-mono px-2 py-0.5 bg-brand-500/20 text-brand-300 rounded">CS / IT</span>
              </h3>
              <p class="text-xs text-slate-400">Track 3x Revision Loops, Formulas & Subtopic Mastery</p>
            </div>

            <div class="flex items-center gap-2">
              <input type="text" id="syl-search-input" onkeyup="filterSyllabusSearch(this.value)" placeholder="Search subtopic or subject..." class="glass-input px-3 py-1.5 rounded-xl text-xs w-48 sm:w-64">
              <button onclick="openModal('modal-add-subject')" class="px-3.5 py-2 glass-panel hover:bg-slate-800 text-slate-200 text-xs font-semibold rounded-xl transition flex items-center gap-1.5">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                <span>Add Subject</span>
              </button>
            </div>
          </div>

          <!-- Overall Syllabus Summary Progress -->
          <div class="glass-panel p-4 rounded-xl border border-white/10 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-semibold text-slate-300">Overall Syllabus Completion</span>
              <span id="syl-overall-percent" class="font-mono font-bold text-brand-400">0% (0 / 0 subtopics)</span>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div id="syl-overall-bar" class="h-full bg-gradient-to-r from-brand-500 via-violet-500 to-emerald-400 transition-all duration-300 w-0"></div>
            </div>
          </div>

          <!-- Subject Cards Grid -->
          <div id="syllabus-subjects-list" class="space-y-4">
            <!-- Populated via JS -->
          </div>

        </section>

        <!-- VIEW: PYQ TRACKER -->
        <section id="view-pyq" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <span>GATE Previous Year Question (PYQ) Tracker</span>
              </h3>
              <p class="text-xs text-slate-400">Log single problems or use Fast Bulk Text Parser</p>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="openModal('modal-bulk-pyq')" class="px-3.5 py-2 glass-panel hover:bg-slate-800 text-brand-300 text-xs font-semibold rounded-xl transition flex items-center gap-1.5 border border-brand-500/30">
                <i data-lucide="file-text" class="w-3.5 h-3.5"></i>
                <span>Bulk Text Parser</span>
              </button>
              <button onclick="openModal('modal-add-pyq')" class="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand flex items-center gap-1.5">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                <span>+ Log PYQ</span>
              </button>
            </div>
          </div>

          <!-- Filter & Search Bar -->
          <div class="glass-panel p-4 rounded-xl border border-white/10 grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Filter Subject</label>
              <select id="pyq-filter-subject" onchange="renderPYQTable()" class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
                <option value="all">All Subjects</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Status</label>
              <select id="pyq-filter-status" onchange="renderPYQTable()" class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
                <option value="all">All Statuses</option>
                <option value="Correct">Correct (First Try)</option>
                <option value="Hint">Solved with Hints</option>
                <option value="Wrong">Wrong Mistake</option>
                <option value="Skipped">Skipped / Doubt</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Question Type</label>
              <select id="pyq-filter-type" onchange="renderPYQTable()" class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
                <option value="all">All Types (MCQ, MSQ, NAT)</option>
                <option value="MCQ 1M">MCQ 1 Mark</option>
                <option value="MCQ 2M">MCQ 2 Marks</option>
                <option value="MSQ">MSQ (Multi-Select)</option>
                <option value="NAT">NAT (Numerical)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Search Topic / Note</label>
              <input type="text" id="pyq-search-query" onkeyup="renderPYQTable()" placeholder="e.g. Dijkstra, LR(1)..." class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
            </div>
          </div>

          <!-- PYQ Table -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="bg-slate-900/80 border-b border-white/10 text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                    <th class="py-3 px-4">Date</th>
                    <th class="py-3 px-4">Subject</th>
                    <th class="py-3 px-4">Topic</th>
                    <th class="py-3 px-4">Year & Q#</th>
                    <th class="py-3 px-4">Type</th>
                    <th class="py-3 px-4">Status</th>
                    <th class="py-3 px-4">Mistake / Note</th>
                    <th class="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="pyq-table-body" class="divide-y divide-white/5 text-slate-300">
                  <!-- Populated via JS -->
                </tbody>
              </table>
            </div>
            <div id="pyq-table-empty" class="p-10 text-center text-slate-500 text-xs hidden">
              No PYQ entries matching filters. Click "+ Log PYQ" to add one!
            </div>
          </div>

        </section>

        <!-- VIEW: ERROR LOG & SPACED REPETITION (SRS) -->
        <section id="view-error" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <span>Spaced Repetition Error Notebook (Leitner 5-Box)</span>
                <span class="text-xs font-mono px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded">No Repeated Mistakes</span>
              </h3>
              <p class="text-xs text-slate-400">Review schedule: Box 1 (1d) &rarr; Box 2 (3d) &rarr; Box 3 (7d) &rarr; Box 4 (14d) &rarr; Box 5 (30d Mastered)</p>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="startDailyReviewSession()" class="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-xl transition shadow glow-rose flex items-center gap-1.5">
                <i data-lucide="play-circle" class="w-3.5 h-3.5"></i>
                <span>Review Due (<span id="btn-srs-due-count">0</span>)</span>
              </button>
              <button onclick="openModal('modal-add-error')" class="px-3.5 py-2 glass-panel hover:bg-slate-800 text-slate-200 text-xs font-semibold rounded-xl transition flex items-center gap-1.5">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                <span>+ Log Mistake</span>
              </button>
            </div>
          </div>

          <!-- 5-Box Leitner Stage Indicators -->
          <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
            <div class="glass-card p-3.5 rounded-xl text-center space-y-1 border-rose-500/30">
              <div class="text-[10px] font-bold uppercase tracking-wider text-rose-400">Box 1 (Daily)</div>
              <div id="srs-count-box-1" class="text-xl font-extrabold text-white">0</div>
              <div class="text-[10px] text-slate-400">Next: 1 Day</div>
            </div>
            <div class="glass-card p-3.5 rounded-xl text-center space-y-1 border-amber-500/30">
              <div class="text-[10px] font-bold uppercase tracking-wider text-amber-400">Box 2 (3 Days)</div>
              <div id="srs-count-box-2" class="text-xl font-extrabold text-white">0</div>
              <div class="text-[10px] text-slate-400">Next: 3 Days</div>
            </div>
            <div class="glass-card p-3.5 rounded-xl text-center space-y-1 border-blue-500/30">
              <div class="text-[10px] font-bold uppercase tracking-wider text-blue-400">Box 3 (Weekly)</div>
              <div id="srs-count-box-3" class="text-xl font-extrabold text-white">0</div>
              <div class="text-[10px] text-slate-400">Next: 7 Days</div>
            </div>
            <div class="glass-card p-3.5 rounded-xl text-center space-y-1 border-violet-500/30">
              <div class="text-[10px] font-bold uppercase tracking-wider text-violet-400">Box 4 (Bi-Weekly)</div>
              <div id="srs-count-box-4" class="text-xl font-extrabold text-white">0</div>
              <div class="text-[10px] text-slate-400">Next: 14 Days</div>
            </div>
            <div class="glass-card p-3.5 rounded-xl text-center space-y-1 border-emerald-500/30">
              <div class="text-[10px] font-bold uppercase tracking-wider text-emerald-400">Box 5 (Mastered)</div>
              <div id="srs-count-box-5" class="text-xl font-extrabold text-white">0</div>
              <div class="text-[10px] text-slate-400">Next: 30 Days</div>
            </div>
          </div>

          <!-- Error Filter -->
          <div class="glass-panel p-4 rounded-xl border border-white/10 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Mistake Category</label>
              <select id="err-filter-category" onchange="renderErrorTable()" class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
                <option value="all">All Categories</option>
                <option value="Concept Gap">Concept Gap (Understood theory wrong)</option>
                <option value="Calculation Error">Calculation / Arithmetic Slip</option>
                <option value="Silly Mistake">Silly Mistake / Overlooked detail</option>
                <option value="Misread Question">Misread Question (e.g. NOT true)</option>
                <option value="Time Pressure">Time Pressure / Rushed</option>
                <option value="Formula Forgotten">Formula Forgotten / Formula mixup</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Review Stage</label>
              <select id="err-filter-box" onchange="renderErrorTable()" class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
                <option value="all">All Stages</option>
                <option value="due">Due for Review Today</option>
                <option value="1">Box 1 (New / Weak)</option>
                <option value="2">Box 2</option>
                <option value="3">Box 3</option>
                <option value="4">Box 4</option>
                <option value="5">Box 5 (Mastered)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Search Mistake</label>
              <input type="text" id="err-search-query" onkeyup="renderErrorTable()" placeholder="e.g. Cache write-through, Eigenvalue..." class="w-full glass-input rounded-lg px-3 py-1.5 text-xs">
            </div>
          </div>

          <!-- Error Table -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="bg-slate-900/80 border-b border-white/10 text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                    <th class="py-3 px-4">Subject & Topic</th>
                    <th class="py-3 px-4">Mistake Reason</th>
                    <th class="py-3 px-4">Problem / Concept Snippet</th>
                    <th class="py-3 px-4">Correct Approach</th>
                    <th class="py-3 px-4">SRS Stage</th>
                    <th class="py-3 px-4">Next Review</th>
                    <th class="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="error-table-body" class="divide-y divide-white/5 text-slate-300">
                  <!-- Populated via JS -->
                </tbody>
              </table>
            </div>
            <div id="error-table-empty" class="p-10 text-center text-slate-500 text-xs hidden">
              No errors recorded yet. When you get a PYQ or Mock question wrong, log it here to cement it!
            </div>
          </div>

        </section>

        <!-- VIEW: MOCK TEST CENTER -->
        <section id="view-mocks" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <span>Full-Length & Subject Mock Test Center</span>
              </h3>
              <p class="text-xs text-slate-400">Log Test Series, Sectional Accuracy, and Dynamic AIR Predictor</p>
            </div>

            <button onclick="openModal('modal-add-mock')" class="px-4 py-2 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand flex items-center gap-1.5">
              <i data-lucide="plus" class="w-3.5 h-3.5"></i>
              <span>+ Log Mock Test</span>
            </button>
          </div>

          <!-- Mock Stats Overview -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="glass-card p-4 rounded-xl space-y-1">
              <span class="text-[11px] font-semibold text-slate-400">Total Mocks</span>
              <div id="mock-kpi-total" class="text-2xl font-extrabold text-white">0</div>
            </div>
            <div class="glass-card p-4 rounded-xl space-y-1">
              <span class="text-[11px] font-semibold text-slate-400">Highest Score</span>
              <div id="mock-kpi-highest" class="text-2xl font-extrabold text-emerald-400">--</div>
            </div>
            <div class="glass-card p-4 rounded-xl space-y-1">
              <span class="text-[11px] font-semibold text-slate-400">Average Marks</span>
              <div id="mock-kpi-average" class="text-2xl font-extrabold text-amber-400">--</div>
            </div>
            <div class="glass-card p-4 rounded-xl space-y-1">
              <span class="text-[11px] font-semibold text-slate-400">Target AIR Range</span>
              <div id="mock-kpi-air-range" class="text-2xl font-extrabold text-brand-300">--</div>
            </div>
          </div>

          <!-- Mock History Table -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="bg-slate-900/80 border-b border-white/10 text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                    <th class="py-3 px-4">Date</th>
                    <th class="py-3 px-4">Test Series / Mock Name</th>
                    <th class="py-3 px-4">Marks Obtained</th>
                    <th class="py-3 px-4">Negative Marks</th>
                    <th class="py-3 px-4">Accuracy</th>
                    <th class="py-3 px-4">Predicted AIR</th>
                    <th class="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="mock-table-body" class="divide-y divide-white/5 text-slate-300">
                  <!-- Populated via JS -->
                </tbody>
              </table>
            </div>
            <div id="mock-table-empty" class="p-10 text-center text-slate-500 text-xs hidden">
              No mock tests logged yet. Log your first mock test above to see performance graphs!
            </div>
          </div>

        </section>

        <!-- VIEW: AI TEST CENTER & RETEST ENGINE -->
        <section id="view-ai-test" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-violet-500/20 bg-gradient-to-r from-violet-950/30 to-slate-900/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <i data-lucide="bot" class="w-5 h-5 text-violet-400"></i>
                <span>Gemini AI Test Generator & Auto-Grader</span>
              </h3>
              <p class="text-xs text-slate-400">Generate authentic MCQ, MSQ & NAT questions tailored to your syllabus or error list</p>
            </div>

            <div id="ai-status-indicator" class="flex items-center gap-2 text-xs font-medium text-slate-300">
              <span class="w-2 h-2 rounded-full bg-violet-400 animate-pulse"></span>
              <span id="ai-status-label">Gemini 1.5 Flash Ready</span>
            </div>
          </div>

          <!-- AI Test Generator Configuration Panel -->
          <div id="ai-generator-panel" class="glass-panel p-6 rounded-2xl border border-white/10 space-y-5">
            <h4 class="text-sm font-bold text-white flex items-center gap-2">
              <i data-lucide="sliders" class="w-4 h-4 text-brand-400"></i>
              <span>Configure AI Quiz</span>
            </h4>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-semibold text-slate-300 mb-1.5">Subject</label>
                <select id="ai-gen-subject" onchange="updateAiTopicOptions(this.value)" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  <!-- Populated by JS -->
                </select>
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-300 mb-1.5">Specific Focus Topic</label>
                <select id="ai-gen-topic" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  <option value="All Topics">Entire Subject / Mixed</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-300 mb-1.5">Difficulty Level</label>
                <select id="ai-gen-difficulty" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  <option value="Standard GATE Level">Standard GATE Level (Conceptual & Analytical)</option>
                  <option value="Tricky High-Yield">Tricky High-Yield (Trap options & Edge Cases)</option>
                  <option value="Formula & Calculation Heavy">Formula & Calculation Heavy (NAT Focused)</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-300 mb-1.5">Number of Questions</label>
                <select id="ai-gen-count" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  <option value="3">3 Questions (Quick Sprint - 6 min)</option>
                  <option value="5" selected>5 Questions (Standard - 10 min)</option>
                  <option value="10">10 Questions (Deep Drill - 20 min)</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-300 mb-1.5">Question Types Allowed</label>
                <select id="ai-gen-types" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  <option value="Mixed (MCQ + MSQ + NAT)">Mixed (MCQ + MSQ + NAT)</option>
                  <option value="MCQ Only">Single-Choice MCQs Only</option>
                  <option value="MSQ Only">Multi-Select MSQs Only</option>
                  <option value="NAT Only">Numerical Answer Type (NAT) Only</option>
                </select>
              </div>

              <div class="flex items-end">
                <button onclick="generateAiQuiz()" id="btn-generate-ai-quiz" class="w-full py-2.5 bg-gradient-to-r from-violet-600 to-brand-600 hover:from-violet-500 hover:to-brand-500 text-white font-bold rounded-xl text-xs transition shadow-lg glow-brand flex items-center justify-center gap-2">
                  <i data-lucide="sparkles" class="w-4 h-4"></i>
                  <span>Generate Test Now</span>
                </button>
              </div>
            </div>

            <div id="ai-gen-loading" class="text-center py-6 space-y-3 hidden">
              <div class="w-8 h-8 mx-auto border-3 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
              <p class="text-xs text-slate-300 animate-pulse">Generating GATE-standard questions with Gemini AI...</p>
            </div>
          </div>

          <!-- Active Test Interactive Engine (Shown during test) -->
          <div id="ai-active-quiz-engine" class="glass-panel p-6 rounded-2xl border border-white/10 space-y-6 hidden">
            
            <!-- Test Header -->
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
              <div>
                <h4 id="quiz-title-display" class="text-base font-bold text-white">AI Drill: Linear Algebra</h4>
                <p id="quiz-sub-display" class="text-xs text-slate-400">Standard GATE Level • Negative marking active</p>
              </div>
              <div class="flex items-center gap-3">
                <div class="glass-panel px-3 py-1 rounded-full text-xs font-mono text-amber-300 flex items-center gap-1.5 border border-amber-500/20">
                  <i data-lucide="clock" class="w-3.5 h-3.5"></i>
                  <span id="quiz-timer-clock">10:00</span>
                </div>
                <button onclick="confirmSubmitQuiz()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl transition shadow glow-emerald">
                  Submit Test
                </button>
              </div>
            </div>

            <!-- Question Palette Bubbles -->
            <div class="flex items-center gap-2 overflow-x-auto pb-2" id="quiz-palette-container">
              <!-- Injected by JS -->
            </div>

            <!-- Current Question Box -->
            <div id="quiz-current-q-card" class="glass-card p-5 rounded-2xl space-y-4">
              <div class="flex items-center justify-between text-xs text-slate-400">
                <span id="quiz-q-num-label" class="font-bold text-brand-400">Question 1 of 5</span>
                <span id="quiz-q-type-label" class="font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300">MCQ (+1, -0.33)</span>
              </div>

              <!-- Question Statement -->
              <div id="quiz-q-statement" class="text-sm font-medium text-white leading-relaxed select-text">
                Loading question...
              </div>

              <!-- Options Container -->
              <div id="quiz-q-options" class="space-y-2.5 pt-2">
                <!-- Injected by JS -->
              </div>
            </div>

            <!-- Navigation Controls -->
            <div class="flex items-center justify-between pt-2">
              <div class="flex items-center gap-2">
                <button onclick="markCurrentQForReview()" class="px-3 py-2 glass-panel hover:bg-slate-800 text-amber-300 text-xs font-medium rounded-xl transition flex items-center gap-1.5">
                  <i data-lucide="bookmark" class="w-3.5 h-3.5"></i>
                  <span>Mark for Review</span>
                </button>
                <button onclick="clearCurrentAnswer()" class="px-3 py-2 glass-panel hover:bg-slate-800 text-slate-400 text-xs font-medium rounded-xl transition">
                  Clear Answer
                </button>
              </div>

              <div class="flex items-center gap-2">
                <button onclick="quizNavPrev()" id="btn-quiz-prev" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
                  &larr; Previous
                </button>
                <button onclick="quizNavNext()" id="btn-quiz-next" class="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow">
                  Next &rarr;
                </button>
              </div>
            </div>

          </div>

          <!-- Post-Test Result & Detailed Solutions View -->
          <div id="ai-quiz-result-view" class="glass-panel p-6 rounded-2xl border border-white/10 space-y-6 hidden">
            
            <div class="text-center py-4 space-y-2">
              <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-tr from-brand-600 to-emerald-500 flex items-center justify-center text-white shadow-xl glow-emerald">
                <i data-lucide="award" class="w-8 h-8"></i>
              </div>
              <h3 class="text-xl font-bold text-white">Test Evaluation Completed</h3>
              <p class="text-xs text-slate-400">Detailed breakdown of answers & step-by-step solutions</p>
            </div>

            <!-- Score Summary Cards -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div class="glass-card p-3.5 rounded-xl space-y-1">
                <div class="text-[10px] text-slate-400">Marks Scored</div>
                <div id="res-marks" class="text-xl font-extrabold text-brand-400">--</div>
              </div>
              <div class="glass-card p-3.5 rounded-xl space-y-1">
                <div class="text-[10px] text-slate-400">Accuracy</div>
                <div id="res-accuracy" class="text-xl font-extrabold text-emerald-400">--%</div>
              </div>
              <div class="glass-card p-3.5 rounded-xl space-y-1">
                <div class="text-[10px] text-slate-400">Correct / Wrong</div>
                <div id="res-counts" class="text-xl font-extrabold text-white">--</div>
              </div>
              <div class="glass-card p-3.5 rounded-xl space-y-1">
                <div class="text-[10px] text-slate-400">Time Spent</div>
                <div id="res-time" class="text-xl font-extrabold text-amber-400">--</div>
              </div>
            </div>

            <!-- Quick Action: Auto-Add All Wrong Questions to Error Log -->
            <div class="flex items-center justify-between p-4 rounded-xl bg-rose-950/30 border border-rose-500/30">
              <div>
                <h5 class="text-xs font-bold text-rose-300">Spaced Repetition Sync</h5>
                <p class="text-[11px] text-slate-300">Push all incorrect questions into your SRS Error Notebook with 1-click.</p>
              </div>
              <button onclick="addAllWrongQuestionsToErrorLog()" id="btn-add-wrong-to-errors" class="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-xl transition shadow glow-rose shrink-0 flex items-center gap-1.5">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i>
                <span>Add Mistakes to SRS</span>
              </button>
            </div>

            <!-- Step-by-Step Question Review Accordions -->
            <div id="res-solutions-list" class="space-y-4">
              <!-- Injected by JS -->
            </div>

            <div class="text-center pt-2">
              <button onclick="closeQuizResultView()" class="px-6 py-2.5 glass-panel hover:bg-slate-800 text-slate-200 text-xs font-semibold rounded-xl transition">
                Return to AI Test Center
              </button>
            </div>

          </div>

        </section>

        <!-- VIEW: ANALYTICS & INSIGHTS -->
        <section id="view-analytics" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <span>Preparation Analytics & Radar Deep-Dive</span>
              </h3>
              <p class="text-xs text-slate-400">Study hours distribution, error causes, and subject mastery radar</p>
            </div>

            <button onclick="runAiStrategyAudit()" class="px-4 py-2 bg-gradient-to-r from-violet-600 to-brand-600 hover:from-violet-500 hover:to-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand flex items-center gap-1.5">
              <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
              <span>Generate AI Strategy Audit</span>
            </button>
          </div>

          <!-- Charts Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Chart 1: Study Hours per Day -->
            <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">Weekly Study Hours (Mon - Sun)</h4>
                <span class="text-[11px] text-brand-400 font-mono" id="chart-weekly-hours-total">0.0 hrs total</span>
              </div>
              <div class="h-64 relative">
                <canvas id="chart-weekly-study-hours"></canvas>
              </div>
            </div>

            <!-- Chart 2: Subject Mastery Radar -->
            <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">Subject-Wise Syllabus Coverage (%)</h4>
                <span class="text-[11px] text-emerald-400 font-mono">Target: 100% All</span>
              </div>
              <div class="h-64 relative">
                <canvas id="chart-subject-radar"></canvas>
              </div>
            </div>

            <!-- Chart 3: Mistake Categorization Donut -->
            <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">Error Root-Cause Distribution</h4>
                <span class="text-[11px] text-rose-400 font-mono">Error Notebook</span>
              </div>
              <div class="h-64 relative flex items-center justify-center">
                <canvas id="chart-mistake-types"></canvas>
              </div>
            </div>

            <!-- Chart 4: PYQ Accuracy by Subject -->
            <div class="glass-panel p-5 rounded-2xl border border-white/10 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">PYQ Accuracy Rate (%)</h4>
                <span class="text-[11px] text-amber-400 font-mono">High-Yield Check</span>
              </div>
              <div class="h-64 relative">
                <canvas id="chart-pyq-accuracy"></canvas>
              </div>
            </div>

          </div>

        </section>

        <!-- VIEW: SETTINGS & DATA MANAGEMENT -->
        <section id="view-settings" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-white/10">
            <h3 class="text-lg font-bold text-white">System Settings & Data Control</h3>
            <p class="text-xs text-slate-400">Manage profile, Gemini API key, JSON export/import and database backups</p>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Left: Profile & API Key -->
            <div class="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
              <h4 class="text-sm font-bold text-white border-b border-white/10 pb-2">Aspirant Profile</h4>
              
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-semibold text-slate-300 mb-1">Aspirant Name</label>
                  <input type="text" id="set-name" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Target AIR Goal</label>
                    <input type="text" id="set-air" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Target Marks (/100)</label>
                    <input type="number" id="set-target-marks" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                  </div>
                </div>

                <div>
                  <label class="block text-xs font-semibold text-slate-300 mb-1">Dream Institute</label>
                  <input type="text" id="set-institute" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                </div>

                <div>
                  <label class="block text-xs font-semibold text-slate-300 mb-1">GATE Target Date</label>
                  <input type="date" id="set-exam-date" class="w-full glass-input rounded-lg px-4 py-2 text-xs">
                </div>

                <div>
                  <label class="block text-xs font-semibold text-slate-300 mb-1">Google Gemini API Key</label>
                  <div class="relative">
                    <input type="password" id="set-apikey" placeholder="AIzaSy..." class="w-full glass-input rounded-lg px-4 py-2 text-xs pr-24 font-mono">
                    <button onclick="testGeminiConnection('set')" class="absolute right-1.5 top-1 px-2.5 py-1 bg-brand-600 hover:bg-brand-500 text-white rounded text-[11px] font-medium transition">
                      Test Key
                    </button>
                  </div>
                  <div id="set-key-status" class="text-[11px] text-slate-400 mt-1"></div>
                </div>

                <button onclick="saveUserProfileSettings()" class="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl text-xs transition shadow glow-brand">
                  Save Profile Settings
                </button>
              </div>
            </div>

            <!-- Right: Data Management & Backup -->
            <div class="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
              <h4 class="text-sm font-bold text-white border-b border-white/10 pb-2">Backup & Storage</h4>

              <div class="space-y-4 text-xs">
                <div class="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-2">
                  <span class="font-semibold text-white">Full JSON Database Backup</span>
                  <p class="text-slate-400 text-[11px]">
                    Export all your notes, PYQs, error logs, syllabus progress and mock scores to an encrypted local JSON file.
                  </p>
                  <div class="flex items-center gap-2 pt-1">
                    <button onclick="exportFullDatabaseJSON()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition flex items-center gap-1.5">
                      <i data-lucide="download" class="w-3.5 h-3.5"></i>
                      <span>Export JSON</span>
                    </button>
                    <button onclick="document.getElementById('file-import-json').click()" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-200 rounded-lg font-semibold transition flex items-center gap-1.5">
                      <i data-lucide="upload" class="w-3.5 h-3.5"></i>
                      <span>Restore JSON</span>
                    </button>
                    <input type="file" id="file-import-json" onchange="importDatabaseJSON(event)" accept=".json" class="hidden">
                  </div>
                </div>

                <div class="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-2">
                  <span class="font-semibold text-white">CSV Export for Excel / Notion</span>
                  <p class="text-slate-400 text-[11px]">Download clean CSV spreadsheets of your PYQ Log and Error Log.</p>
                  <div class="flex items-center gap-2 pt-1">
                    <button onclick="exportTableToCSV('pyqEntries')" class="px-3 py-1.5 glass-panel hover:bg-slate-800 text-slate-300 rounded-lg transition">Export PYQs CSV</button>
                    <button onclick="exportTableToCSV('errorLog')" class="px-3 py-1.5 glass-panel hover:bg-slate-800 text-slate-300 rounded-lg transition">Export Errors CSV</button>
                  </div>
                </div>

                <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/20 space-y-2">
                  <span class="font-semibold text-rose-300">Danger Zone</span>
                  <p class="text-slate-400 text-[11px]">Factory reset will wipe all IndexedDB tables. Make sure to export a backup first.</p>
                  <button onclick="wipeAllDataModal()" class="px-4 py-2 bg-rose-600/80 hover:bg-rose-600 text-white rounded-lg font-semibold transition text-xs">
                    Factory Reset All Data
                  </button>
                </div>
              </div>
            </div>

          </div>

        </section>

        <!-- VIEW: HELP MANUAL & HOTKEYS -->
        <section id="view-help" class="app-view space-y-6 hidden animate-fadeIn">
          
          <div class="glass-panel p-5 rounded-2xl border border-white/10">
            <h3 class="text-lg font-bold text-white">The Gaokao 180-Day Method & System Hotkeys</h3>
            <p class="text-xs text-slate-400">Master the science of competitive exam performance</p>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 text-xs text-slate-300">
            
            <!-- Protocol Guide -->
            <div class="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
              <h4 class="text-sm font-bold text-brand-300 uppercase tracking-wider">The 3-Phase Gaokao Framework</h4>
              <div class="space-y-3 leading-relaxed">
                <div class="p-3 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
                  <strong class="text-white">Phase 1: Deep Foundation (Day 1 - 90)</strong>
                  <p class="text-slate-400 text-[11px]">
                    Goal: 100% syllabus topic coverage. Daily 3-block routine: Morning (Theory & Formulas), Afternoon (20 Topic PYQs), Night (SRS Error review).
                  </p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
                  <strong class="text-white">Phase 2: Error Eradication (Day 91 - 150)</strong>
                  <p class="text-slate-400 text-[11px]">
                    Goal: Complete 15 years of GATE PYQs twice. Move all errors through Leitner Box 1 to Box 5. Take Subject & Multi-subject tests every weekend.
                  </p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
                  <strong class="text-white">Phase 3: Speed & Full Mocks (Day 151 - 180)</strong>
                  <p class="text-slate-400 text-[11px]">
                    Goal: Take 20 full-length 3-hour mocks at 9:30 AM or 2:30 PM slot. 3 hours test + 3 hours autopsy analysis. Polish formula memory.
                  </p>
                </div>
              </div>
            </div>

            <!-- Keyboard Shortcuts Table -->
            <div class="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
              <h4 class="text-sm font-bold text-brand-300 uppercase tracking-wider">Keyboard Hotkeys</h4>
              
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>War Room Dashboard</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">D</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Schedule / Timetable</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">T</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Syllabus Matrix</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">S</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>PYQ Tracker</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">P</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Error Log & SRS</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">E</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Mock Tests</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">M</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>AI Test Center</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">A</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Analytics</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">N</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Settings</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-brand-400 font-mono rounded font-bold">O</kbd>
                </div>
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between">
                  <span>Close Open Modal</span>
                  <kbd class="px-2 py-0.5 bg-slate-800 text-slate-400 font-mono rounded font-bold">Esc</kbd>
                </div>
              </div>
            </div>

          </div>

        </section>

      </main>

    </div>

  </div>

  <!-- MODALS -->

  <!-- Modal: Add / Log PYQ -->
  <div id="modal-add-pyq" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-lg rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="layers" class="w-4 h-4 text-brand-400"></i>
          <span>Log GATE Previous Year Question</span>
        </h4>
        <button onclick="closeModal('modal-add-pyq')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Subject</label>
          <select id="m-pyq-subject" onchange="updateModalPyqTopics(this.value)" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <!-- Populated by JS -->
          </select>
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Topic</label>
          <select id="m-pyq-topic" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <!-- Populated by JS -->
          </select>
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">GATE Year</label>
          <input type="number" id="m-pyq-year" min="1990" max="2026" placeholder="2023" value="2023" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Question Number / Set</label>
          <input type="text" id="m-pyq-qnum" placeholder="Q14 (Set 1)" value="Q1" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Question Type</label>
          <select id="m-pyq-type" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <option value="MCQ 1M">MCQ 1 Mark (+1, -0.33)</option>
            <option value="MCQ 2M" selected>MCQ 2 Marks (+2, -0.66)</option>
            <option value="MSQ">MSQ Multi-Select (No Neg)</option>
            <option value="NAT">NAT Numerical (No Neg)</option>
          </select>
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Attempt Outcome</label>
          <select id="m-pyq-status" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <option value="Correct">Solved Correctly (1st Try)</option>
            <option value="Hint">Solved with Hints / Notes</option>
            <option value="Wrong">Wrong Mistake (Auto-add to SRS)</option>
            <option value="Skipped">Skipped / Unsure</option>
          </select>
        </div>
        <div class="sm:col-span-2">
          <label class="block text-slate-300 font-semibold mb-1">Mistake Reason / Key Takeaway</label>
          <input type="text" id="m-pyq-note" placeholder="e.g. Forgot that empty language is regular; check edge case" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-add-pyq')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveSinglePYQEntry()" class="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand">
          Save PYQ Entry
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Bulk Text PYQ Parser -->
  <div id="modal-bulk-pyq" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-xl rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="file-text" class="w-4 h-4 text-brand-400"></i>
          <span>Fast Bulk Text PYQ Parser</span>
        </h4>
        <button onclick="closeModal('modal-bulk-pyq')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <p class="text-xs text-slate-300 leading-relaxed">
        Paste your rough study session notes below. Supports lines or semicolons. Example format:
      </p>
      <div class="p-3 bg-slate-900/80 rounded-xl text-[11px] font-mono text-slate-400 border border-white/5 space-y-1">
        <div>DSA 2022 Q14 Correct;</div>
        <div>OS 2021 Q32 Wrong Silly;</div>
        <div>CN 2020 Q5 Wrong Concept Gap;</div>
        <div>DBMS 2023 Q12 Hint;</div>
      </div>

      <textarea id="m-bulk-pyq-input" rows="6" placeholder="Paste your bulk entries here..." class="w-full glass-input rounded-xl p-3 text-xs font-mono"></textarea>

      <div class="flex items-center justify-between pt-2 border-t border-white/10">
        <span id="m-bulk-parsed-preview" class="text-xs text-brand-400">Ready to parse</span>
        <div class="flex items-center gap-2">
          <button onclick="closeModal('modal-bulk-pyq')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
            Cancel
          </button>
          <button onclick="executeBulkPYQParse()" class="px-5 py-2 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand">
            Parse & Save All
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: Add Mistake / Error Entry -->
  <div id="modal-add-error" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-lg rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400"></i>
          <span>Log Mistake into SRS Error Notebook</span>
        </h4>
        <button onclick="closeModal('modal-add-error')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Subject</label>
          <select id="m-err-subject" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <!-- Populated by JS -->
          </select>
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Topic Name</label>
          <input type="text" id="m-err-topic" placeholder="e.g. Cache Memory Mapping" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div class="sm:col-span-2">
          <label class="block text-slate-300 font-semibold mb-1">Mistake Root Cause Category</label>
          <select id="m-err-category" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <option value="Concept Gap">Concept Gap (Understood underlying theory wrong)</option>
            <option value="Calculation Error">Calculation Error (Arithmetic or sign mistake)</option>
            <option value="Silly Mistake">Silly Mistake (Rushed / picked wrong bubble)</option>
            <option value="Misread Question">Misread Question (Missed "NOT" / wrong units)</option>
            <option value="Time Pressure">Time Pressure (Panicked near end)</option>
            <option value="Formula Forgotten">Formula Forgotten / Formula mixup</option>
          </select>
        </div>
        <div class="sm:col-span-2">
          <label class="block text-slate-300 font-semibold mb-1">Problem / Concept Question Snippet</label>
          <textarea id="m-err-snippet" rows="2" placeholder="What was the question asking? (e.g. Find tag bits for 4-way associative cache...)" class="w-full glass-input rounded-xl p-3 text-xs"></textarea>
        </div>
        <div class="sm:col-span-2">
          <label class="block text-slate-300 font-semibold mb-1">Correct Approach & What to Remember</label>
          <textarea id="m-err-solution" rows="3" placeholder="Key formula / correct logic: Number of sets = Cache Size / (Line size * Associativity)..." class="w-full glass-input rounded-xl p-3 text-xs"></textarea>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-add-error')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveErrorLogEntry()" class="px-5 py-2 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-xl transition shadow glow-rose">
          Save to Box 1 (SRS)
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Log Mock Test -->
  <div id="modal-add-mock" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-lg rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="target" class="w-4 h-4 text-amber-400"></i>
          <span>Log Mock Test Performance</span>
        </h4>
        <button onclick="closeModal('modal-add-mock')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div class="sm:col-span-2">
          <label class="block text-slate-300 font-semibold mb-1">Test Name / Series</label>
          <input type="text" id="m-mock-name" placeholder="e.g. Made Easy All-India Mock #3 (Full Syllabus)" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Total Marks</label>
          <input type="number" id="m-mock-total" value="100" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Marks Obtained</label>
          <input type="number" step="0.33" id="m-mock-score" placeholder="68.5" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Negative Marks Incurred</label>
          <input type="number" step="0.33" id="m-mock-neg" placeholder="4.66" value="0" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Date Taken</label>
          <input type="date" id="m-mock-date" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div class="sm:col-span-2">
          <label class="block text-slate-300 font-semibold mb-1">Post-Test Notes & Weak Sections</label>
          <input type="text" id="m-mock-notes" placeholder="e.g. Lost 6 marks in Compiler Design parsing; revise LL(1) tables" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-add-mock')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveMockTestEntry()" class="px-5 py-2 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand">
          Save Mock Test
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Add Custom Timetable Task -->
  <div id="modal-add-task" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-md rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="plus-circle" class="w-4 h-4 text-brand-400"></i>
          <span>Add Study Block to Schedule</span>
        </h4>
        <button onclick="closeModal('modal-add-task')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Scheduled Date</label>
          <input type="date" id="m-task-date" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Time Slot / Block</label>
          <select id="m-task-time" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
            <option value="Morning Slot (08:00 - 11:30)">Morning Slot (08:00 - 11:30) • Deep Theory</option>
            <option value="Afternoon Slot (14:00 - 17:30)">Afternoon Slot (14:00 - 17:30) • PYQs & Problems</option>
            <option value="Evening Slot (19:30 - 22:30)">Evening Slot (19:30 - 22:30) • SRS Review & Revision</option>
            <option value="Custom Slot">Custom Slot</option>
          </select>
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Task Title & Subject</label>
          <input type="text" id="m-task-title" placeholder="e.g. Operating Systems: Process Sync Semaphores" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-add-task')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveCustomTaskEntry()" class="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand">
          Add Block
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Timetable Frequency Warning Safety Modal -->
  <div id="modal-timetable-warning" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-md rounded-2xl p-6 border border-amber-500/50 shadow-2xl space-y-4 animate-fadeIn">
      <div class="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center mx-auto">
        <i data-lucide="alert-triangle" class="w-6 h-6"></i>
      </div>

      <div class="text-center space-y-2">
        <h4 class="text-base font-bold text-white">Frequent Timetable Changes Alert!</h4>
        <p class="text-xs text-slate-300 leading-relaxed">
          You have modified your study schedule <strong class="text-amber-400" id="m-warn-change-count">3</strong> times in the last 7 days. Continually changing timetables creates the illusion of productivity while breaking study continuity.
        </p>
        <p class="text-xs text-amber-300 font-medium">
          To proceed, type <span class="font-mono font-bold bg-slate-900 px-1.5 py-0.5 rounded text-white">CONFIRM</span> below:
        </p>
      </div>

      <input type="text" id="m-warn-confirm-input" placeholder="Type CONFIRM here..." class="w-full glass-input rounded-xl px-4 py-2.5 text-center text-sm font-mono tracking-widest uppercase">

      <div class="flex items-center justify-center gap-3 pt-2">
        <button onclick="closeModal('modal-timetable-warning')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Keep Current Timetable
        </button>
        <button onclick="executeConfirmedTimetableRegeneration()" id="btn-warn-confirm-action" class="px-5 py-2 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-xl transition shadow glow-amber">
          Override & Regenerate
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Spaced Repetition Flashcard Review Mode -->
  <div id="modal-srs-review" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-xl rounded-2xl p-6 border border-white/10 shadow-2xl space-y-5 animate-fadeIn">
      
      <!-- Review Header -->
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
          <h4 class="text-sm font-bold text-white">Daily SRS Flashcard Session</h4>
        </div>
        <div class="flex items-center gap-2">
          <span id="srs-card-idx-display" class="text-xs font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded">1 of 3</span>
          <button onclick="closeModal('modal-srs-review')" class="text-slate-400 hover:text-white p-1 rounded-lg">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Flashcard Content Area -->
      <div class="space-y-4">
        <div class="flex items-center justify-between text-xs">
          <span id="srs-card-subject" class="font-bold text-brand-400">Operating Systems</span>
          <span id="srs-card-category" class="font-mono bg-rose-950/60 text-rose-300 px-2 py-0.5 rounded border border-rose-500/30">Concept Gap</span>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/80 border border-white/5 space-y-2">
          <div class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Problem / Snippet:</div>
          <div id="srs-card-snippet" class="text-sm font-medium text-white select-text leading-relaxed">
            Loading error snippet...
          </div>
        </div>

        <!-- Hidden Solution (Revealed on click) -->
        <div id="srs-solution-container" class="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/30 space-y-2 hidden animate-fadeIn">
          <div class="text-[11px] font-semibold uppercase tracking-wider text-emerald-400">Correct Concept & Approach:</div>
          <div id="srs-card-solution" class="text-xs text-slate-200 select-text leading-relaxed">
            Loading solution...
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-2 border-t border-white/10">
        <div id="srs-btn-reveal-box">
          <button onclick="revealSrsSolution()" class="w-full py-2.5 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 text-white font-bold rounded-xl text-xs transition shadow glow-brand flex items-center justify-center gap-1.5">
            <i data-lucide="eye" class="w-4 h-4"></i>
            <span>Reveal Solution & Check Recall</span>
          </button>
        </div>

        <!-- Rating Buttons after reveal -->
        <div id="srs-rating-box" class="grid grid-cols-3 gap-2.5 hidden">
          <button onclick="rateSrsCard('hard')" class="py-2.5 bg-rose-600/30 hover:bg-rose-600 text-rose-300 hover:text-white rounded-xl text-xs font-semibold transition border border-rose-500/40 text-center">
            <div>Hard / Forgot</div>
            <div class="text-[10px] text-slate-400">Reset to Box 1 (1d)</div>
          </button>
          <button onclick="rateSrsCard('good')" class="py-2.5 bg-brand-600/30 hover:bg-brand-600 text-brand-300 hover:text-white rounded-xl text-xs font-semibold transition border border-brand-500/40 text-center">
            <div>Good Recall</div>
            <div class="text-[10px] text-slate-400">+1 Box Level</div>
          </button>
          <button onclick="rateSrsCard('easy')" class="py-2.5 bg-emerald-600/30 hover:bg-emerald-600 text-emerald-300 hover:text-white rounded-xl text-xs font-semibold transition border border-emerald-500/40 text-center">
            <div>Easy / Mastered</div>
            <div class="text-[10px] text-slate-400">Promote to Box 5 (30d)</div>
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- Modal: Topic Notes / Formula Cheat Sheet -->
  <div id="modal-topic-notes" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-lg rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 id="m-notes-title" class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="file-text" class="w-4 h-4 text-brand-400"></i>
          <span>Topic Formula Notes</span>
        </h4>
        <button onclick="closeModal('modal-topic-notes')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="space-y-2">
        <label class="block text-xs font-semibold text-slate-300">Key Formulas, Traps & High-Yield Summary</label>
        <textarea id="m-topic-notes-text" rows="8" placeholder="Enter formulas, key theorems, edge cases to remember..." class="w-full glass-input rounded-xl p-3 text-xs leading-relaxed font-mono"></textarea>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-topic-notes')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveTopicNotes()" class="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand">
          Save Notes
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Add Custom Subject -->
  <div id="modal-add-subject" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-md rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="plus-circle" class="w-4 h-4 text-brand-400"></i>
          <span>Add Custom Subject Module</span>
        </h4>
        <button onclick="closeModal('modal-add-subject')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Subject Name</label>
          <input type="text" id="m-sub-name" placeholder="e.g. Advanced Machine Learning" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">GATE Weightage Estimate</label>
          <input type="text" id="m-sub-weight" placeholder="e.g. ~8%" value="~6%" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Subtopics (comma separated)</label>
          <textarea id="m-sub-topics" rows="3" placeholder="Linear Models, Neural Networks, Decision Trees, SVM..." class="w-full glass-input rounded-xl p-3 text-xs"></textarea>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-add-subject')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveCustomSubjectModule()" class="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition shadow glow-brand">
          Create Subject
        </button>
      </div>
    </div>
  </div>

  <!-- Modal: Manual Study Time Log -->
  <div id="modal-manual-time" class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-md rounded-2xl p-6 border border-white/10 shadow-2xl space-y-4 animate-fadeIn">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="clock" class="w-4 h-4 text-cyan-400"></i>
          <span>Log Study Session Hours</span>
        </h4>
        <button onclick="closeModal('modal-manual-time')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Date</label>
          <input type="date" id="m-time-date" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Duration in Hours</label>
          <input type="number" step="0.5" id="m-time-hours" placeholder="2.5" value="2.0" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Subject / Focus Area</label>
          <input type="text" id="m-time-focus" placeholder="e.g. Discrete Mathematics Graph Theory" class="w-full glass-input rounded-lg px-3 py-2 text-xs">
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="closeModal('modal-manual-time')" class="px-4 py-2 glass-panel hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-xl transition">
          Cancel
        </button>
        <button onclick="saveManualStudyTime()" class="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold rounded-xl transition shadow">
          Log Hours
        </button>
      </div>
    </div>
  </div>

  <!-- Audio Beep Generator using Web Audio API -->
  <script>
    function playBeep(freq = 600, duration = 200) {
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration / 1000);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration / 1000);
      } catch (e) {
        console.log('Audio not enabled');
      }
    }
  </script>
'''
    return html_template

print("Base HTML template ready")
