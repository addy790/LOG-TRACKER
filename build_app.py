import os

# Create the full index.html file
html_content = '''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GATE Tracker Pro - AI-Powered Preparation OS</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
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
              850: '#131d31',
              900: '#0f172a',
              950: '#070c18'
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
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.6);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(100, 116, 139, 0.4);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(148, 163, 184, 0.7);
    }

    /* Glassmorphism Styles */
    .glass-panel {
      background: rgba(30, 41, 59, 0.65);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-panel-subtle {
      background: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .glass-card {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.07);
    }
    .glass-card:hover {
      border-color: rgba(99, 102, 241, 0.3);
    }
    .glass-input {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #f8fafc;
    }
    .glass-input:focus {
      border-color: #6366f1;
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
      outline: none;
    }

    /* Gradient Text & Glows */
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
    .glow-brand {
      box-shadow: 0 0 25px -5px rgba(99, 102, 241, 0.4);
    }
    .glow-emerald {
      box-shadow: 0 0 25px -5px rgba(16, 185, 129, 0.35);
    }

    /* Pulse animation for active blocks */
    @keyframes pulse-subtle {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }
    .animate-pulse-subtle {
      animation: pulse-subtle 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* Modal Backdrop */
    .modal-backdrop {
      background: rgba(3, 7, 18, 0.82);
      backdrop-filter: blur(8px);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen overflow-hidden antialiased select-none">
  <!-- Body Container -->
  <div id="app-root" class="relative w-screen h-screen flex overflow-hidden">
    <!-- Will be initialized by script -->
  </div>
</body>
</html>
'''

print("Script template ready")
