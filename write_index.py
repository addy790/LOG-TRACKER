# -*- coding: utf-8 -*-
"""
Single-file Clean Generator for GATE Tracker Pro
"""

import os

def generate_index_html():
    # 1. HTML Header & Meta
    part1_head = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GATE Tracker Pro - AI-Powered Preparation OS</title>
  
  <!-- Google Fonts -->
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
              750: '#24334d',
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
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
    ::-webkit-scrollbar-thumb { background: rgba(100, 116, 139, 0.4); border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.7); }

    /* Glassmorphic Styles */
    .glass-nav {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-header {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-panel {
      background: rgba(30, 41, 59, 0.6);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.07);
    }
    .glass-card {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.2s ease-in-out;
    }
    .glass-card:hover {
      border-color: rgba(99, 102, 241, 0.35);
    }
    .glass-input {
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #f8fafc;
      transition: all 0.2s ease;
    }
    .glass-input:focus {
      border-color: #6366f1;
      background: rgba(15, 23, 42, 0.95);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
      outline: none;
    }

    /* Gradients and Glows */
    .text-gradient-brand {
      background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .glow-brand { box-shadow: 0 0 25px -4px rgba(99, 102, 241, 0.4); }
    .glow-emerald { box-shadow: 0 0 25px -4px rgba(16, 185, 129, 0.35); }
    .glow-rose { box-shadow: 0 0 25px -4px rgba(244, 63, 94, 0.35); }
    .glow-amber { box-shadow: 0 0 25px -4px rgba(245, 158, 11, 0.35); }

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
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen h-screen overflow-hidden antialiased select-none flex">
"""

    # 2. Extract Onboarding and Main Layout from create_app.py
    with open('create_app.py', 'r', encoding='utf-8') as f:
        src = f.read()

    # Find the start of the body content in create_app.py
    b_start = src.rfind('<body class="bg-slate-950')
    if b_start == -1:
        b_start = src.find('<body class="bg-slate-950')
    
    body_content_start = src.find('\n', b_start) + 1
    body_content_end = src.find('  <!-- Audio Beep Generator using Web Audio API -->', body_content_start)
    
    body_html = src[body_content_start:body_content_end]

    # 3. Extract the JS Engine from create_complete_app.py
    with open('create_complete_app.py', 'r', encoding='utf-8') as f:
        c_src = f.read()

    js_marker = '  <!-- ======================================================== -->\n  <!-- GATE TRACKER PRO COMPLETE CORE ENGINE SCRIPT -->'
    js_start = c_src.find(js_marker)
    js_end = c_src.rfind('</script>\n</body>\n</html>')

    audio_and_js = """
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
        // audio might be blocked before user gesture
      }
    }
  </script>
""" + c_src[js_start:js_end + len('</script>\n</body>\n</html>')]

    final_index_html = part1_head + body_html + audio_and_js

    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(final_index_html)

    print(f"Generated clean index.html: {len(final_index_html)} bytes, {final_index_html.count(chr(10))} lines")

if __name__ == '__main__':
    generate_index_html()
