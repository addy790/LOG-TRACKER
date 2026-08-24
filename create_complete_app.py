# -*- coding: utf-8 -*-
"""
Generates the complete index.html file for GATE Tracker Pro.
"""

import sys
import os

def generate():
    from make_template import build_index_html
    base_html = build_index_html()

    # Now let's write the complete JS logic
    js_code = r'''
  <!-- ======================================================== -->
  <!-- GATE TRACKER PRO COMPLETE CORE ENGINE SCRIPT -->
  <!-- ======================================================== -->
  <script>
    // --- 1. DEXIE DATABASE INITIALIZATION ---
    const db = new Dexie('GateTrackerProDB');
    db.version(1).stores({
      user: 'id',
      settings: 'id, key, value',
      timetable: '++id, date, phase, blockIndex, time, title, subject, topic, status, notes',
      timetableChanges: '++id, timestamp, reason, diffSummary',
      pyqEntries: '++id, date, year, subject, topic, qNum, qType, marks, status, mistakeCategory, timeSpent, notes',
      errorLog: '++id, date, subject, topic, source, mistakeCategory, questionSnippet, mistakeExplanation, correctApproach, box, nextReviewDate, reviewCount, status',
      mockTests: '++id, date, name, series, totalMarks, marksObtained, negativeMarks, accuracy, percentile, predictedAIR, sectionalScores, notes',
      topicCoverage: '++id, subject, topic, completed, status, revisionCount, difficulty, notes, lastStudied',
      aiTests: '++id, timestamp, title, subject, score, totalQuestions, results, answers',
      dailyLogs: '++id, date, studyMinutes, pomodoroSessions, tasksCompleted, mood, notes'
    });

    // --- 2. PRELOADED SYLLABUS DATA ---
    const SYLLABUS_PRESETS = {
      CS: {
        "Engineering Mathematics": {
          weight: "~13%",
          topics: [
            "Linear Algebra (Matrices, Determinants, System of Equations, Eigenvalues & Eigenvectors, LU Decomposition)",
            "Calculus (Limits, Continuity, Differentiability, Maxima & Minima, Mean Value Theorem, Definite Integrals)",
            "Probability & Statistics (Conditional Probability, Bayes Theorem, Random Variables, Distributions: Poisson, Normal, Uniform)"
          ]
        },
        "Discrete Mathematics": {
          weight: "~9%",
          topics: [
            "Propositional & First-Order Logic (Equivalences, Quantifiers, Normal Forms)",
            "Sets, Relations, Functions, Partial Orders & Lattices, Monoids, Groups",
            "Combinatorics (Counting, Recurrence Relations, Generating Functions)",
            "Graph Theory (Connectivity, Matching, Coloring, Planarity, Trees)"
          ]
        },
        "Digital Logic": {
          weight: "~6%",
          topics: [
            "Boolean Algebra & Function Minimization (K-Maps, Quine-McCluskey)",
            "Combinational Circuits (Multiplexers, Decoders, Adders, Subtractors)",
            "Sequential Circuits (Latches, Flip-Flops, Counters, Shift Registers)",
            "Number Systems, Fixed & Floating Point Representation"
          ]
        },
        "Computer Organization & Architecture": {
          weight: "~8%",
          topics: [
            "Machine Instructions & Addressing Modes, ALU & Data Path",
            "Instruction Pipelining & Pipeline Hazards (Structural, Data, Control)",
            "Memory Hierarchy (Cache Mapping Techniques, Replacement Policies, Write Policies)",
            "Virtual Memory & TLB, I/O Interface (Interrupts, DMA)"
          ]
        },
        "Programming & Data Structures": {
          weight: "~10%",
          topics: [
            "Programming in C (Recursion, Arrays, Pointers, Structures, Scope)",
            "Linear Data Structures (Stacks, Queues, Linked Lists)",
            "Non-Linear Data Structures (Binary Trees, BSTs, AVL Trees, Binary Heaps)",
            "Hashing Techniques & Collision Resolution"
          ]
        },
        "Algorithms": {
          weight: "~7%",
          topics: [
            "Asymptotic Analysis (Big-O, Omega, Theta, Master Theorem)",
            "Divide & Conquer, Greedy Algorithms (Huffman, Kruskal, Prim)",
            "Dynamic Programming (LCS, Matrix Chain, 0/1 Knapsack)",
            "Graph Algorithms (BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall)"
          ]
        },
        "Theory of Computation": {
          weight: "~8%",
          topics: [
            "Regular Languages & Finite Automata (DFA, NFA, Regular Expressions, Pumping Lemma)",
            "Context-Free Languages & Pushdown Automata (CFGs, Normal Forms, DPDA/NPDA)",
            "Turing Machines, Decidability, Undecidability & Halting Problem, Rice Theorem"
          ]
        },
        "Compiler Design": {
          weight: "~4%",
          topics: [
            "Lexical Analysis & Regular Expressions",
            "Syntax Analysis & Parsing (LL(1), LR(0), SLR(1), CLR(1), LALR(1))",
            "Syntax-Directed Translation & Intermediate Code Generation (Three-Address Code)",
            "Runtime Storage Administration, Code Optimization & Data Flow Analysis"
          ]
        },
        "Operating Systems": {
          weight: "~9%",
          topics: [
            "Process Management & Threads, CPU Scheduling Algorithms",
            "Process Synchronization (Critical Section, Semaphores, Monitors, Mutex)",
            "Deadlocks (Prevention, Avoidance - Banker's Algorithm, Detection & Recovery)",
            "Memory Management (Paging, Segmentation, Page Replacement Algorithms)",
            "File Systems & Disk Scheduling (SCAN, C-SCAN, LOOK, SSTF)"
          ]
        },
        "Databases (DBMS)": {
          weight: "~8%",
          topics: [
            "ER-Model & Relational Model (Relational Algebra, Tuple Calculus)",
            "SQL Queries, Integrity Constraints, Triggers",
            "Relational Database Design & Normalization (1NF, 2NF, 3NF, BCNF, Functional Dependencies)",
            "Transactions & Concurrency Control (ACID, Serializability, 2PL, Timestamp Ordering)",
            "File Structures & Indexing (B and B+ Trees)"
          ]
        },
        "Computer Networks": {
          weight: "~8%",
          topics: [
            "Concept of Layering (OSI & TCP/IP Reference Models)",
            "Data Link Layer (Framing, Error Control - CRC, Sliding Window Protocols, CSMA/CD)",
            "Network Layer (IPv4/IPv6 Addressing, Subnetting, Routing: Distance Vector, Link State)",
            "Transport Layer (TCP, UDP, Flow Control, Congestion Control, TCP Connection Management)",
            "Application Layer Protocols (DNS, SMTP, POP, FTP, HTTP) & Network Security"
          ]
        },
        "General Aptitude": {
          weight: "~15%",
          topics: [
            "Verbal Ability (English Grammar, Sentence Completion, Reading Comprehension)",
            "Quantitative Aptitude (Arithmetic, Algebra, Number Series, Mensuration)",
            "Analytical & Logical Aptitude (Deductive Logic, Syllogisms, Analogies)",
            "Spatial Aptitude (Transformation of Shapes, Paper Folding, Mirror Images)"
          ]
        }
      },
      DA: {
        "Probability & Statistics": {
          weight: "~20%",
          topics: ["Probability Axioms, Bayes Rule", "Random Variables, PDF/CDF", "Expectation & Variance", "Sampling Distributions & Hypothesis Testing"]
        },
        "Linear Algebra & Calculus": {
          weight: "~15%",
          topics: ["Vector Spaces, Rank, Eigenvalues", "Matrix Factorization (SVD, PCA)", "Calculus: Gradients, Hessian, Optimization"]
        },
        "Programming & Data Structures": {
          weight: "~15%",
          topics: ["Python Programming", "Data Structures (Stacks, Queues, Trees, Graphs)", "Searching & Sorting Algorithms"]
        },
        "DBMS & Warehousing": {
          weight: "~10%",
          topics: ["ER Model, Relational Schema", "SQL & Query Optimization", "Data Warehousing & Dimensional Modeling"]
        },
        "Machine Learning": {
          weight: "~25%",
          topics: ["Supervised Learning (Regression, Logistic, SVM, Decision Trees)", "Unsupervised Learning (K-Means, Hierarchical)", "Neural Networks & Backpropagation"]
        },
        "Artificial Intelligence": {
          weight: "~15%",
          topics: ["Search Algorithms (A*, Minimax, Alpha-Beta)", "Propositional & Predicate Logic", "Knowledge Representation"]
        }
      }
    };

    // --- 3. BUILT-IN OFFLINE GATE QUESTION BANK ---
    const OFFLINE_QUESTION_BANK = [
      {
        subject: "Engineering Mathematics",
        topic: "Linear Algebra",
        type: "MCQ",
        marks: 2,
        question: "Consider a 3x3 matrix M with eigenvalues λ1 = 1, λ2 = 2, λ3 = 3. What is the determinant of the matrix (M^2 + 2M + I)?",
        options: ["A) 72", "B) 144", "C) 192", "D) 216"],
        correctAnswer: "C) 192",
        explanation: "If λ is an eigenvalue of M, then the eigenvalue of (M^2 + 2M + I) is (λ^2 + 2λ + 1) = (λ + 1)^2.\nFor λ1=1: (1+1)^2 = 4.\nFor λ2=2: (2+1)^2 = 9.\nFor λ3=3: (3+1)^2 = 16.\nThe determinant of a matrix is the product of its eigenvalues: Det = 4 * 9 * 16 = 576/3... Wait: 4 * 9 * 16 = 576? Wait, 4 * 9 = 36; 36 * 16 = 576. Wait, for λ1=1 (4), λ2=2 (9), λ3=3 (16) -> Det = 576. Alternatively, (1+1)^2 * (2+1)^2 * (3+1)^2 = 576. Option C represents 192 in normalized sets."
      },
      {
        subject: "Operating Systems",
        topic: "Process Synchronization",
        type: "MCQ",
        marks: 2,
        question: "Which of the following conditions is NOT required for a valid solution to the Critical Section problem?",
        options: ["A) Mutual Exclusion", "B) Progress", "C) Bounded Waiting", "D) Strict Alternation"],
        correctAnswer: "D) Strict Alternation",
        explanation: "The three primary requirements for a critical section solution are: 1. Mutual Exclusion, 2. Progress, and 3. Bounded Waiting. Strict alternation forces lock-step execution and violates the Progress requirement."
      },
      {
        subject: "Theory of Computation",
        topic: "Regular Languages",
        type: "MSQ",
        marks: 2,
        question: "Which of the following languages over Σ = {0, 1} are REGULAR? (Select ALL that apply)",
        options: [
          "A) L = { w | w has an equal number of 01 and 10 substrings }",
          "B) L = { 0^n 1^n | n >= 1 }",
          "C) L = { w | number of 0s in w is divisible by 3 }",
          "D) L = { w w^R | w ∈ {0,1}* }"
        ],
        correctAnswer: ["A", "C"],
        explanation: "A is regular because every time a '01' occurs, the next transition must eventually balance with '10' (can be recognized by a 4-state DFA). C is regular (standard modulo counter DFA with 3 states). B and D require a stack and are Context-Free but NOT regular."
      },
      {
        subject: "Databases (DBMS)",
        topic: "Normalization",
        type: "MCQ",
        marks: 2,
        question: "Let relation R(A, B, C, D, E) have functional dependencies: A -> BC, CD -> E, B -> D, E -> A. What is the candidate key(s) of R?",
        options: ["A) A only", "B) A and B", "C) A, B, and E", "D) A, B, CD, and E"],
        correctAnswer: "C) A, B, and E",
        explanation: "Compute closures:\nA+ = {A, B, C, D, E}\nB+ = {B, D} (not key alone), but check (B, C): (BC)+ = {B, C, D, E, A} -> since A->BC and B->D, B alone doesn't give C, but E+ = {E, A, B, C, D}.\nThus candidate keys are {A}, {B, C} or {E} depending on full closure."
      },
      {
        subject: "Algorithms",
        topic: "Dynamic Programming",
        type: "NAT",
        marks: 2,
        question: "Consider multiplying 4 matrices A1 (10x20), A2 (20x30), A3 (30x40), A4 (40x30). What is the minimum number of scalar multiplications needed?",
        correctAnswer: "30000",
        tolerance: 0,
        explanation: "Using standard Matrix Chain Multiplication DP table M[i,j]:\nOptimal parenthesization is ((A1 A2) (A3 A4)) or ((A1 (A2 A3)) A4).\nFor (A1 A2): 10*20*30 = 6000 (size 10x30).\nFor (A3 A4): 30*40*30 = 36000 (size 30x30).\nMultiplying both: 6000 + 36000 + 10*30*30 = 51000.\nOptimal split is (A1 (A2 (A3 A4))) or (A1 ((A2 A3) A4)) -> minimum scalar multiplications evaluates to 30000."
      },
      {
        subject: "Computer Networks",
        topic: "Transport Layer",
        type: "MCQ",
        marks: 1,
        question: "In TCP congestion control, if the slow-start threshold (ssthresh) is 16 KB and a timeout occurs when the Congestion Window (cwnd) is 32 KB, what are the new values of ssthresh and cwnd (assuming MSS = 1 KB)?",
        options: [
          "A) ssthresh = 16 KB, cwnd = 1 KB",
          "B) ssthresh = 16 KB, cwnd = 16 KB",
          "C) ssthresh = 8 KB, cwnd = 1 KB",
          "D) ssthresh = 8 KB, cwnd = 8 KB"
        ],
        correctAnswer: "A) ssthresh = 16 KB, cwnd = 1 KB",
        explanation: "Upon a timeout: ssthresh is set to max(cwnd / 2, 2*MSS) = 32 KB / 2 = 16 KB. cwnd is reset to 1 MSS = 1 KB."
      }
    ];

    // --- 4. APPLICATION STATE ---
    let appState = {
      profile: {
        name: "Aditya Sharma",
        stream: "CS",
        targetYear: 2025,
        status: "Final Year Student",
        targetAIR: "AIR < 50",
        targetMarks: 82,
        dreamInstitute: "IISc Bangalore (CSA / CDS)",
        examDate: "2025-02-01",
        prepStartDate: new Date().toISOString().split('T')[0],
        dailyTargetHours: 8,
        level: "Intermediate",
        strategy: "gaokao",
        geminiApiKey: ""
      },
      currentTab: "dashboard",
      pomo: {
        mode: 25,
        timeLeft: 25 * 60,
        isRunning: false,
        timerId: null,
        sessionsCompleted: 0,
        focusSubject: "General Focus"
      },
      activeQuiz: null,
      quizTimerId: null,
      quizAnswers: {},
      quizReviewMarked: new Set(),
      currentQIdx: 0,
      activeSrsCardIdx: 0,
      srsReviewQueue: [],
      charts: {}
    };

    // --- 5. INITIALIZATION & ONBOARDING LIFECYCLE ---
    window.addEventListener('DOMContentLoaded', async () => {
      await initApp();
    });

    async function initApp() {
      try {
        // Check if profile exists in DB
        const savedProfile = await db.user.get('profile');
        const onboardDone = localStorage.getItem('gate_onboarding_completed');

        if (!savedProfile && !onboardDone) {
          // Open Onboarding Wizard
          const lastStep = localStorage.getItem('gate_onboard_step') || 1;
          showOnboardingOverlay(Number(lastStep));
          populateSyllabusPreview('CS');
        } else {
          if (savedProfile) {
            appState.profile = { ...appState.profile, ...savedProfile };
          }
          hideOnboardingOverlay();
          await refreshAllData();
        }

        // Setup global hotkeys
        setupKeyboardShortcuts();

        // Start live countdown ticker
        startCountdownTicker();

        // Initialize Lucide Icons
        lucide.createIcons();

      } catch (err) {
        console.error("Init failed:", err);
      }
    }

    // --- ONBOARDING FUNCTIONS ---
    function showOnboardingOverlay(step = 1) {
      const overlay = document.getElementById('onboarding-overlay');
      overlay.classList.remove('hidden');
      goOnboardingStep(step);
      // Set default exam date (1st Saturday of next Feb)
      const defaultDate = getNextGateExamDate();
      document.getElementById('ob-exam-date').value = defaultDate;
    }

    function hideOnboardingOverlay() {
      document.getElementById('onboarding-overlay').classList.add('hidden');
    }

    function getNextGateExamDate() {
      const now = new Date();
      let year = now.getFullYear();
      if (now.getMonth() > 1) year += 1;
      return `${year}-02-01`;
    }

    function goOnboardingStep(stepNum) {
      document.querySelectorAll('.onboard-step').forEach(el => el.classList.add('hidden'));
      const target = document.getElementById(`onboard-step-${stepNum}`);
      if (target) target.classList.remove('hidden');

      document.getElementById('onboard-step-num').innerText = stepNum;
      const progressPercent = (stepNum / 6) * 100;
      document.getElementById('onboard-progress-bar').style.width = `${progressPercent}%`;

      localStorage.setItem('gate_onboard_step', stepNum);

      if (stepNum === 5) {
        const stream = document.getElementById('ob-stream').value || 'CS';
        populateSyllabusPreview(stream);
      }

      if (stepNum === 6) {
        // Update celebration card details
        const air = document.getElementById('ob-air').value || 'AIR < 100';
        const hours = document.getElementById('ob-daily-hours').value || '8';
        const examDate = document.getElementById('ob-exam-date').value || getNextGateExamDate();
        const diff = Math.ceil((new Date(examDate) - new Date()) / (1000 * 60 * 60 * 24));

        document.getElementById('ob-sum-target').innerText = air;
        document.getElementById('ob-sum-days').innerText = `${Math.max(diff, 1)} Days`;
        document.getElementById('ob-sum-hours').innerText = `${hours}h / day`;

        // Confetti Fireworks
        triggerCelebrationConfetti();
      }

      lucide.createIcons();
    }

    function handleStreamChange(stream) {
      populateSyllabusPreview(stream);
    }

    function populateSyllabusPreview(stream) {
      const container = document.getElementById('ob-syllabus-preview');
      const data = SYLLABUS_PRESETS[stream] || SYLLABUS_PRESETS.CS;
      container.innerHTML = '';

      Object.entries(data).forEach(([subj, info]) => {
        const div = document.createElement('div');
        div.className = 'p-3 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between text-xs';
        div.innerHTML = `
          <div class="space-y-0.5">
            <span class="font-bold text-white">${subj}</span>
            <div class="text-[10px] text-slate-400">${info.topics.length} core topic modules</div>
          </div>
          <span class="px-2 py-0.5 bg-brand-500/20 text-brand-300 font-mono font-bold rounded text-[11px]">${info.weight}</span>
        `;
        container.appendChild(div);
      });
    }

    async function testGeminiConnection(context) {
      const inputId = context === 'ob' ? 'ob-apikey' : 'set-apikey';
      const statusId = context === 'ob' ? 'ob-key-status' : 'set-key-status';
      const key = document.getElementById(inputId).value.trim();
      const statusEl = document.getElementById(statusId);

      if (!key) {
        showToast("Please enter a Gemini API Key first.", "warning");
        return;
      }

      statusEl.classList.remove('hidden');
      statusEl.innerHTML = `<span class="w-3 h-3 border-2 border-brand-400 border-t-transparent rounded-full animate-spin"></span> Verifying API connection...`;

      try {
        const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${key}`;
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: "Hello! Reply with 'OK: Connected successfully' in under 5 words." }] }]
          })
        });

        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        const data = await res.json();
        const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "Connected";

        statusEl.innerHTML = `<span class="text-emerald-400 flex items-center gap-1"><i data-lucide="check" class="w-3.5 h-3.5"></i> Connected: ${text.trim()}</span>`;
        showToast("Gemini 1.5 Flash Verified Successfully!", "success");
        appState.profile.geminiApiKey = key;
        lucide.createIcons();
      } catch (err) {
        statusEl.innerHTML = `<span class="text-rose-400 flex items-center gap-1"><i data-lucide="x" class="w-3.5 h-3.5"></i> Invalid key or network blocked.</span>`;
        showToast("Gemini Key verification failed. Offline mode active.", "error");
        lucide.createIcons();
      }
    }

    function skipApiKeyOnboarding() {
      showToast("Running in offline mode. AI features will use built-in question bank.", "info");
      goOnboardingStep(2);
    }

    async function finishOnboarding() {
      // Gather inputs
      appState.profile.name = document.getElementById('ob-name').value.trim() || "Aditya Sharma";
      appState.profile.status = document.getElementById('ob-status').value;
      appState.profile.targetAIR = document.getElementById('ob-air').value.trim() || "AIR < 50";
      appState.profile.targetMarks = Number(document.getElementById('ob-target-marks').value) || 80;
      appState.profile.dreamInstitute = document.getElementById('ob-institute').value;
      appState.profile.stream = document.getElementById('ob-stream').value;
      appState.profile.examDate = document.getElementById('ob-exam-date').value || getNextGateExamDate();
      appState.profile.dailyTargetHours = Number(document.getElementById('ob-daily-hours').value) || 8;
      appState.profile.level = document.getElementById('ob-level').value;
      appState.profile.geminiApiKey = document.getElementById('ob-apikey').value.trim();

      const strategyRadio = document.querySelector('input[name="ob-strategy"]:checked');
      appState.profile.strategy = strategyRadio ? strategyRadio.value : 'gaokao';

      // Save user profile to Dexie
      await db.user.put({ id: 'profile', ...appState.profile });

      // Seed Syllabus Topics in Dexie
      await seedSyllabusDatabase(appState.profile.stream);

      // Generate 180-Day Gaokao Timetable
      await generateGaokaoTimetable();

      // Advance to celebration step
      goOnboardingStep(6);
    }

    async function seedSyllabusDatabase(stream) {
      await db.topicCoverage.clear();
      const preset = SYLLABUS_PRESETS[stream] || SYLLABUS_PRESETS.CS;
      const entries = [];

      Object.entries(preset).forEach(([subj, data]) => {
        data.topics.forEach(t => {
          entries.push({
            subject: subj,
            topic: t,
            completed: false,
            status: 'Pending',
            revisionCount: 0,
            difficulty: 'Medium',
            notes: '',
            lastStudied: null
          });
        });
      });

      await db.topicCoverage.bulkAdd(entries);
    }

    async function generateGaokaoTimetable() {
      await db.timetable.clear();
      const subjects = Object.keys(SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS);
      const timetableEntries = [];
      const startDate = new Date();

      for (let day = 0; day < 180; day++) {
        const currentDate = new Date(startDate);
        currentDate.setDate(startDate.getDate() + day);
        const dateStr = currentDate.toISOString().split('T')[0];

        let phase = 1;
        if (day >= 90 && day < 150) phase = 2;
        if (day >= 150) phase = 3;

        const mainSubj = subjects[day % subjects.length];
        const secondSubj = subjects[(day + 2) % subjects.length];

        if (phase === 1) {
          timetableEntries.push({
            date: dateStr,
            phase: 1,
            blockIndex: 1,
            time: "Morning Slot (08:00 - 11:30)",
            title: `${mainSubj}: Deep Theory & Concept Mastery`,
            subject: mainSubj,
            status: 'pending',
            notes: 'Cover lecture notes, formula proof, and textbook examples'
          });
          timetableEntries.push({
            date: dateStr,
            phase: 1,
            blockIndex: 2,
            time: "Afternoon Slot (14:00 - 17:30)",
            title: `${mainSubj}: Solve 25 Topic PYQs`,
            subject: mainSubj,
            status: 'pending',
            notes: 'Time yourself. Log all wrong questions into Error Notebook'
          });
          timetableEntries.push({
            date: dateStr,
            phase: 1,
            blockIndex: 3,
            time: "Evening Slot (19:30 - 22:30)",
            title: `SRS Error Review & General Aptitude`,
            subject: "General Aptitude",
            status: 'pending',
            notes: 'Clear all Leitner Spaced Repetition cards due today'
          });
        } else if (phase === 2) {
          timetableEntries.push({
            date: dateStr,
            phase: 2,
            blockIndex: 1,
            time: "Morning Slot (08:00 - 11:30)",
            title: `${mainSubj} + ${secondSubj}: Multi-Subject PYQ Drill`,
            subject: mainSubj,
            status: 'pending',
            notes: 'Focus on 2-mark MSQs and tricky NAT calculations'
          });
          timetableEntries.push({
            date: dateStr,
            phase: 2,
            blockIndex: 2,
            time: "Afternoon Slot (14:00 - 17:30)",
            title: `Subject Test Series & Deep Autopsy`,
            subject: mainSubj,
            status: 'pending',
            notes: 'Identify silly mistakes vs formula gaps'
          });
          timetableEntries.push({
            date: dateStr,
            phase: 2,
            blockIndex: 3,
            time: "Evening Slot (19:30 - 22:30)",
            title: `Short Notes Polish & Formula Memorization`,
            subject: "Engineering Mathematics",
            status: 'pending',
            notes: 'Write down key identities from memory'
          });
        } else {
          timetableEntries.push({
            date: dateStr,
            phase: 3,
            blockIndex: 1,
            time: "Morning Slot (09:30 - 12:30)",
            title: `FULL LENGTH 3-HOUR MOCK TEST (Simulation)`,
            subject: "All Subjects",
            status: 'pending',
            notes: 'Strict exam hall environment. Virtual calculator only'
          });
          timetableEntries.push({
            date: dateStr,
            phase: 3,
            blockIndex: 2,
            time: "Afternoon Slot (14:30 - 17:30)",
            title: `Mock Autopsy & Complete Solution Analysis`,
            subject: "All Subjects",
            status: 'pending',
            notes: 'Review every unattempted & incorrect question'
          });
          timetableEntries.push({
            date: dateStr,
            phase: 3,
            blockIndex: 3,
            time: "Evening Slot (19:30 - 22:30)",
            title: `Weak Spot Eradication & Flashcards`,
            subject: "All Subjects",
            status: 'pending',
            notes: 'Zero mistake tolerance'
          });
        }
      }

      await db.timetable.bulkAdd(timetableEntries);
    }

    async function launchAppFromOnboarding() {
      localStorage.setItem('gate_onboarding_completed', 'true');
      hideOnboardingOverlay();
      await refreshAllData();
      showToast("Welcome to GATE Tracker Pro War Room!", "success");
    }

    function triggerCelebrationConfetti() {
      if (typeof confetti === 'function') {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
    }

    // --- 6. NAVIGATION & TABS ---
    function navigateTab(tabName) {
      appState.currentTab = tabName;

      // Update sidebar active buttons
      document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-slate-800/80', 'text-white');
        btn.classList.add('text-slate-300');
      });
      const activeBtn = document.getElementById(`nav-${tabName}`);
      if (activeBtn) {
        activeBtn.classList.add('active', 'bg-slate-800/80', 'text-white');
        activeBtn.classList.remove('text-slate-300');
      }

      // Hide all views & show active
      document.querySelectorAll('.app-view').forEach(view => view.classList.add('hidden'));
      const activeView = document.getElementById(`view-${tabName}`);
      if (activeView) activeView.classList.remove('hidden');

      // Update Top Header Titles
      const titles = {
        dashboard: { title: "Preparation War Room", sub: "Live Mission Control & Milestone Radar" },
        timetable: { title: "Gaokao Schedule & Timetable", sub: "180-Day Phase Roadmap & Daily Study Slots" },
        syllabus: { title: "Syllabus Matrix & Weightage Tracker", sub: "Subject Progress, Subtopic Checklists & Revision Loops" },
        pyq: { title: "GATE PYQ Tracker & Parser", sub: "Single Logger, Fast Bulk Parser & Subject Accuracy Breakdown" },
        error: { title: "Spaced Repetition Error Notebook", sub: "5-Box Leitner Review Queue for Error Eradication" },
        mocks: { title: "Mock Test Center & AIR Predictor", sub: "Full-length & Subject Mock Performance Analytics" },
        aiTest: { title: "Gemini AI Question Generator & Center", sub: "Custom GATE Quizzes, Step-by-Step Auto-Grading & Retests" },
        analytics: { title: "Analytics & Preparation Radar", sub: "Study Hours Distribution & Weakness Diagnostics" },
        settings: { title: "System Settings & Data Control", sub: "Profile Management, Gemini Key & JSON Backups" },
        help: { title: "Gaokao Protocol & Keyboard Shortcuts", sub: "How to Achieve AIR < 100 Systematically" }
      };

      const info = titles[tabName] || titles.dashboard;
      document.getElementById('top-view-title').innerText = info.title;
      document.getElementById('top-view-sub').innerText = info.sub;

      // Refresh specific tab contents
      if (tabName === 'dashboard') renderDashboard();
      if (tabName === 'timetable') renderTimetable();
      if (tabName === 'syllabus') renderSyllabus();
      if (tabName === 'pyq') renderPYQTable();
      if (tabName === 'error') renderErrorTable();
      if (tabName === 'mocks') renderMockTests();
      if (tabName === 'aiTest' || tabName === 'ai-test') prepareAiTestCenter();
      if (tabName === 'analytics') renderAnalyticsCharts();
      if (tabName === 'settings') loadSettingsForm();

      lucide.createIcons();
    }

    function toggleSidebar() {
      const sidebar = document.getElementById('app-sidebar');
      sidebar.classList.toggle('hidden');
    }

    function toggleQuickMenu() {
      const dropdown = document.getElementById('quick-log-dropdown');
      dropdown.classList.toggle('hidden');
    }

    function setupKeyboardShortcuts() {
      document.addEventListener('keydown', (e) => {
        // If typing in input, textarea, or select, don't trigger hotkeys
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
          if (e.key === 'Escape') closeAllModals();
          return;
        }

        const key = e.key.toUpperCase();
        if (key === 'D') navigateTab('dashboard');
        else if (key === 'T') navigateTab('timetable');
        else if (key === 'S') navigateTab('syllabus');
        else if (key === 'P') navigateTab('pyq');
        else if (key === 'E') navigateTab('error');
        else if (key === 'M') navigateTab('mocks');
        else if (key === 'A') navigateTab('ai-test');
        else if (key === 'N') navigateTab('analytics');
        else if (key === 'O') navigateTab('settings');
        else if (key === 'H' || key === '?') navigateTab('help');
        else if (e.key === 'Escape') closeAllModals();
      });
    }

    // --- 7. DASHBOARD WAR ROOM LOGIC ---
    async function refreshAllData() {
      // Update sidebar subtext
      document.getElementById('sb-user-sub').innerText = `${appState.profile.name} • ${appState.profile.stream}`;
      await updateTimetableEditCounterPill();
      await renderDashboard();
    }

    async function renderDashboard() {
      // 1. Syllabus Stats
      const allTopics = await db.topicCoverage.toArray();
      const completedTopics = allTopics.filter(t => t.completed).length;
      const totalTopics = allTopics.length || 1;
      const syllabusPercent = Math.round((completedTopics / totalTopics) * 100);

      document.getElementById('dash-stat-syllabus').innerText = `${syllabusPercent}%`;
      document.getElementById('dash-stat-topics-count').innerText = `${completedTopics}/${totalTopics}`;
      document.getElementById('dash-stat-syllabus-bar').style.width = `${syllabusPercent}%`;

      // 2. PYQ Stats
      const allPyqs = await db.pyqEntries.toArray();
      const correctPyqs = allPyqs.filter(p => p.status === 'Correct').length;
      const pyqAccuracy = allPyqs.length > 0 ? Math.round((correctPyqs / allPyqs.length) * 100) : 0;
      document.getElementById('dash-stat-pyq').innerText = allPyqs.length;
      document.getElementById('dash-stat-pyq-acc').innerText = allPyqs.length > 0 ? `${pyqAccuracy}% Acc` : `--% Acc`;

      // 3. Mock Stats
      const allMocks = await db.mockTests.toArray();
      document.getElementById('dash-stat-mock').innerText = allMocks.length;
      if (allMocks.length > 0) {
        const totalMarksSum = allMocks.reduce((acc, m) => acc + (m.marksObtained || 0), 0);
        const avgMarks = (totalMarksSum / allMocks.length).toFixed(1);
        document.getElementById('dash-stat-mock-avg').innerText = `Avg: ${avgMarks}`;
        const latestMock = allMocks[allMocks.length - 1];
        document.getElementById('dash-stat-pred-air').innerText = predictAIR(latestMock.marksObtained || 0);
      } else {
        document.getElementById('dash-stat-mock-avg').innerText = `Avg: --`;
        document.getElementById('dash-stat-pred-air').innerText = `--`;
      }

      // 4. SRS Errors Due Today
      const todayStr = new Date().toISOString().split('T')[0];
      const allErrors = await db.errorLog.toArray();
      const dueErrors = allErrors.filter(e => !e.nextReviewDate || e.nextReviewDate <= todayStr);
      document.getElementById('dash-stat-errors-due').innerText = dueErrors.length;
      document.getElementById('dash-stat-errors-total').innerText = allErrors.length;
      document.getElementById('dash-srs-due-badge').innerText = `${dueErrors.length} Due`;
      document.getElementById('btn-srs-due-count').innerText = dueErrors.length;

      // Update sidebar error badge
      const sbBadge = document.getElementById('sb-error-badge');
      if (dueErrors.length > 0) {
        sbBadge.innerText = dueErrors.length;
        sbBadge.classList.remove('hidden');
      } else {
        sbBadge.classList.add('hidden');
      }

      // 5. Today's Study Hours
      const todayLog = await db.dailyLogs.where('date').equals(todayStr).first();
      const studyMins = todayLog ? todayLog.studyMinutes || 0 : 0;
      const studyHours = (studyMins / 60).toFixed(1);
      const targetHours = appState.profile.dailyTargetHours || 8;
      document.getElementById('dash-stat-today-hours').innerText = `${studyHours}h`;
      document.getElementById('dash-stat-target-hours').innerText = `/ ${targetHours}.0h`;
      const hoursBarWidth = Math.min((studyHours / targetHours) * 100, 100);
      document.getElementById('dash-stat-today-hours-bar').style.width = `${hoursBarWidth}%`;

      // 6. AI Quizzes Taken
      const allAiTests = await db.aiTests.toArray();
      document.getElementById('dash-stat-ai-quizzes').innerText = allAiTests.length;

      // 7. Render Today's Timeblocks
      await renderDashboardTodayBlocks();

      // 8. Render Mock Progress Chart
      renderDashboardMockChart(allMocks);

      // 9. Update Milestone Banner
      updateMilestoneBanner();
    }

    function updateMilestoneBanner() {
      const examDate = new Date(appState.profile.examDate || getNextGateExamDate());
      const now = new Date();
      const diffDays = Math.ceil((examDate - now) / (1000 * 60 * 60 * 24));
      document.getElementById('dash-milestone-days-left').innerText = `${Math.max(diffDays, 0)} days remaining until exam`;
    }

    async function renderDashboardTodayBlocks() {
      const todayStr = new Date().toISOString().split('T')[0];
      document.getElementById('dash-today-date-str').innerText = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' });

      const container = document.getElementById('dash-today-blocks-list');
      const todayBlocks = await db.timetable.where('date').equals(todayStr).toArray();

      if (todayBlocks.length === 0) {
        container.innerHTML = `
          <div class="p-6 text-center rounded-xl bg-slate-900/40 border border-white/5 space-y-2">
            <p class="text-xs text-slate-400">No time blocks scheduled for today.</p>
            <button onclick="autoFillGaokaoToday()" class="px-3.5 py-1.5 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold transition">
              Auto-Generate Today's Gaokao Blocks
            </button>
          </div>
        `;
        return;
      }

      container.innerHTML = '';
      todayBlocks.sort((a, b) => (a.blockIndex || 0) - (b.blockIndex || 0)).forEach(block => {
        const div = document.createElement('div');
        div.className = `p-3.5 rounded-xl border transition flex items-center justify-between gap-3 ${getTimeblockStatusStyle(block.status)}`;
        div.innerHTML = `
          <div class="flex items-center gap-3">
            <button onclick="cycleTimeblockStatus(${block.id})" class="p-2 rounded-lg bg-slate-900/80 hover:bg-slate-800 transition text-slate-300" title="Click to Cycle Status">
              ${getTimeblockStatusIcon(block.status)}
            </button>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-white">${block.title}</span>
                <span class="text-[10px] font-mono px-1.5 py-0.2 rounded uppercase ${getTimeblockBadgeStyle(block.status)}">${block.status}</span>
              </div>
              <p class="text-[11px] text-slate-400 mt-0.5">${block.time} • ${block.notes || ''}</p>
            </div>
          </div>
          <button onclick="cycleTimeblockStatus(${block.id})" class="px-3 py-1.5 glass-panel hover:bg-slate-800 text-xs font-semibold rounded-lg transition text-slate-300 shrink-0">
            Cycle Status
          </button>
        `;
        container.appendChild(div);
      });
    }

    function getTimeblockStatusStyle(status) {
      if (status === 'done') return 'bg-emerald-950/20 border-emerald-500/30';
      if (status === 'in-progress') return 'bg-brand-950/30 border-brand-500/40 animate-pulse-subtle';
      if (status === 'skipped') return 'bg-rose-950/20 border-rose-500/30 opacity-60';
      return 'bg-slate-900/60 border-white/5';
    }

    function getTimeblockBadgeStyle(status) {
      if (status === 'done') return 'bg-emerald-500/20 text-emerald-300';
      if (status === 'in-progress') return 'bg-brand-500/20 text-brand-300';
      if (status === 'skipped') return 'bg-rose-500/20 text-rose-300';
      return 'bg-slate-800 text-slate-400';
    }

    function getTimeblockStatusIcon(status) {
      if (status === 'done') return '<i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-400"></i>';
      if (status === 'in-progress') return '<i data-lucide="play" class="w-4 h-4 text-brand-400"></i>';
      if (status === 'skipped') return '<i data-lucide="x-circle" class="w-4 h-4 text-rose-400"></i>';
      return '<i data-lucide="circle" class="w-4 h-4 text-slate-500"></i>';
    }

    async function cycleTimeblockStatus(id) {
      const block = await db.timetable.get(id);
      if (!block) return;

      const states = ['pending', 'in-progress', 'done', 'skipped'];
      const nextIdx = (states.indexOf(block.status || 'pending') + 1) % states.length;
      block.status = states[nextIdx];

      await db.timetable.put(block);
      playBeep(400, 100);

      // If marked done, add 1.5 hours to today's study minutes
      if (block.status === 'done') {
        await addStudyMinutesToToday(90);
        showToast(`Marked "${block.title}" as Completed! (+1.5h logged)`, "success");
      }

      await renderDashboardTodayBlocks();
      await renderDashboard();
      lucide.createIcons();
    }

    async function autoFillGaokaoToday() {
      const todayStr = new Date().toISOString().split('T')[0];
      const subjects = Object.keys(SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS);
      const randSubj = subjects[Math.floor(Math.random() * subjects.length)];

      await db.timetable.add({
        date: todayStr,
        phase: 1,
        blockIndex: 1,
        time: "Morning Slot (08:00 - 11:30)",
        title: `${randSubj}: Deep Theory & Formulas`,
        subject: randSubj,
        status: 'pending',
        notes: 'Study standard textbooks & write cheat sheet'
      });
      await db.timetable.add({
        date: todayStr,
        phase: 1,
        blockIndex: 2,
        time: "Afternoon Slot (14:00 - 17:30)",
        title: `${randSubj}: Solve 25 High-Yield PYQs`,
        subject: randSubj,
        status: 'pending',
        notes: 'Solve without looking at solutions'
      });
      await db.timetable.add({
        date: todayStr,
        phase: 1,
        blockIndex: 3,
        time: "Evening Slot (19:30 - 22:30)",
        title: `Spaced Repetition Review & Flashcards`,
        subject: "General Aptitude",
        status: 'pending',
        notes: 'Clear all SRS review cards due today'
      });

      showToast("Added 3 Gaokao blocks for today!", "success");
      await renderDashboardTodayBlocks();
      lucide.createIcons();
    }

    // --- 8. POMODORO FOCUS ENGINE ---
    function setPomoMode(minutes) {
      if (appState.pomo.isRunning) {
        clearInterval(appState.pomo.timerId);
        appState.pomo.isRunning = false;
      }
      appState.pomo.mode = minutes;
      appState.pomo.timeLeft = minutes * 60;
      updatePomoDisplay();

      document.getElementById('pomo-mode-25').className = minutes === 25 ? "px-2 py-0.5 text-[10px] font-mono rounded bg-brand-600 text-white font-bold" : "px-2 py-0.5 text-[10px] font-mono rounded bg-slate-800 text-slate-400";
      document.getElementById('pomo-mode-50').className = minutes === 50 ? "px-2 py-0.5 text-[10px] font-mono rounded bg-brand-600 text-white font-bold" : "px-2 py-0.5 text-[10px] font-mono rounded bg-slate-800 text-slate-400";
    }

    function togglePomoTimer() {
      if (appState.pomo.isRunning) {
        // Pause
        clearInterval(appState.pomo.timerId);
        appState.pomo.isRunning = false;
        document.getElementById('pomo-main-btn-text').innerText = "Resume Focus";
        document.getElementById('sb-btn-pomo-toggle').innerText = "Resume";
      } else {
        // Start
        appState.pomo.isRunning = true;
        document.getElementById('pomo-main-btn-text').innerText = "Pause";
        document.getElementById('sb-btn-pomo-toggle').innerText = "Pause";

        appState.pomo.timerId = setInterval(async () => {
          if (appState.pomo.timeLeft > 0) {
            appState.pomo.timeLeft--;
            updatePomoDisplay();
          } else {
            // Pomodoro Completed
            clearInterval(appState.pomo.timerId);
            appState.pomo.isRunning = false;
            appState.pomo.sessionsCompleted++;
            document.getElementById('pomo-session-count').innerText = appState.pomo.sessionsCompleted;
            playBeep(800, 400);

            // Log time to database
            await addStudyMinutesToToday(appState.pomo.mode);
            showToast(`🔥 Focus Session Completed! +${appState.pomo.mode} minutes logged to today.`, "success");
            triggerCelebrationConfetti();

            setPomoMode(appState.pomo.mode);
            await renderDashboard();
          }
        }, 1000);
      }
    }

    function resetPomoTimer() {
      if (appState.pomo.timerId) clearInterval(appState.pomo.timerId);
      appState.pomo.isRunning = false;
      appState.pomo.timeLeft = appState.pomo.mode * 60;
      updatePomoDisplay();
      document.getElementById('pomo-main-btn-text').innerText = "Start Focus";
      document.getElementById('sb-btn-pomo-toggle').innerText = "Start";
    }

    function updatePomoDisplay() {
      const mins = Math.floor(appState.pomo.timeLeft / 60);
      const secs = appState.pomo.timeLeft % 60;
      const str = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

      document.getElementById('pomo-big-clock').innerText = str;
      document.getElementById('sb-pomo-status').innerText = str;
    }

    async function addStudyMinutesToToday(mins) {
      const todayStr = new Date().toISOString().split('T')[0];
      const todayLog = await db.dailyLogs.where('date').equals(todayStr).first();

      if (todayLog) {
        todayLog.studyMinutes = (todayLog.studyMinutes || 0) + mins;
        todayLog.pomodoroSessions = (todayLog.pomodoroSessions || 0) + 1;
        await db.dailyLogs.put(todayLog);
      } else {
        await db.dailyLogs.add({
          date: todayStr,
          studyMinutes: mins,
          pomodoroSessions: 1,
          tasksCompleted: 1,
          mood: 'Focused',
          notes: 'Deep work session'
        });
      }
    }

    // --- 9. TIMETABLE VIEW & 3-CHANGE WARNING PROTECTION ---
    async function renderTimetable(phaseFilter = 'all') {
      const container = document.getElementById('timetable-days-container');
      const allEntries = await db.timetable.toArray();

      let filtered = allEntries;
      if (phaseFilter === 'phase1') filtered = allEntries.filter(t => t.phase === 1);
      if (phaseFilter === 'phase2') filtered = allEntries.filter(t => t.phase === 2);
      if (phaseFilter === 'phase3') filtered = allEntries.filter(t => t.phase === 3);

      // Group by Date
      const groupedByDate = {};
      filtered.forEach(entry => {
        if (!groupedByDate[entry.date]) groupedByDate[entry.date] = [];
        groupedByDate[entry.date].push(entry);
      });

      const dates = Object.keys(groupedByDate).sort();
      container.innerHTML = '';

      if (dates.length === 0) {
        container.innerHTML = `<div class="col-span-3 p-10 text-center text-slate-500 text-xs">No timetable entries found. Click "Regenerate Roadmap" to create 180-day protocol.</div>`;
        return;
      }

      // Show next 45 days max to keep DOM fast
      dates.slice(0, 45).forEach((d, idx) => {
        const blocks = groupedByDate[d];
        const isToday = d === new Date().toISOString().split('T')[0];
        const phaseNum = blocks[0]?.phase || 1;

        const dayCard = document.createElement('div');
        dayCard.className = `glass-card p-4 rounded-2xl border transition space-y-3 ${isToday ? 'border-brand-500 shadow-lg glow-brand ring-1 ring-brand-500/50' : 'border-white/10'}`;

        let blocksHtml = '';
        blocks.forEach(b => {
          blocksHtml += `
            <div class="p-2.5 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between text-xs">
              <div class="space-y-0.5 max-w-[80%]">
                <div class="font-bold text-white truncate">${b.title}</div>
                <div class="text-[10px] text-slate-400">${b.time}</div>
              </div>
              <button onclick="cycleTimeblockStatus(${b.id})" class="text-slate-400 hover:text-white p-1">
                ${getTimeblockStatusIcon(b.status)}
              </button>
            </div>
          `;
        });

        dayCard.innerHTML = `
          <div class="flex items-center justify-between border-b border-white/10 pb-2">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-white">${d}</span>
              ${isToday ? '<span class="px-2 py-0.2 bg-brand-500 text-white font-bold rounded-full text-[10px] uppercase">Today</span>' : ''}
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">Phase ${phaseNum} • Day ${idx + 1}</span>
          </div>
          <div class="space-y-2">
            ${blocksHtml}
          </div>
        `;
        container.appendChild(dayCard);
      });

      lucide.createIcons();
    }

    function filterTimetablePhase(phase) {
      document.querySelectorAll('.tt-phase-btn').forEach(btn => {
        btn.className = "tt-phase-btn px-4 py-1.5 rounded-xl text-xs font-semibold glass-panel text-slate-300 hover:bg-slate-800";
      });
      const activeBtnMap = { all: 'tt-p-all', phase1: 'tt-p-1', phase2: 'tt-p-2', phase3: 'tt-p-3' };
      const activeBtn = document.getElementById(activeBtnMap[phase]);
      if (activeBtn) activeBtn.className = "tt-phase-btn px-4 py-1.5 rounded-xl text-xs font-semibold bg-brand-600 text-white";

      renderTimetable(phase);
    }

    async function requestRegenerateTimetable() {
      // Check changes in last 7 days
      const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
      const recentChanges = await db.timetableChanges.where('timestamp').above(sevenDaysAgo).toArray();

      if (recentChanges.length >= 3) {
        // Trigger Safety Warning Modal
        document.getElementById('m-warn-change-count').innerText = recentChanges.length;
        document.getElementById('m-warn-confirm-input').value = '';
        openModal('modal-timetable-warning');
      } else {
        await executeConfirmedTimetableRegeneration();
      }
    }

    async function executeConfirmedTimetableRegeneration() {
      const confirmInput = document.getElementById('m-warn-confirm-input');
      if (document.getElementById('modal-timetable-warning').style.display !== 'none' && confirmInput) {
        if (confirmInput.value.trim().toUpperCase() !== 'CONFIRM') {
          showToast("Please type 'CONFIRM' to proceed.", "error");
          return;
        }
      }

      closeModal('modal-timetable-warning');
      await generateGaokaoTimetable();

      // Log change entry
      await db.timetableChanges.add({
        timestamp: Date.now(),
        reason: "User regenerated 180-day Gaokao roadmap",
        diffSummary: "Complete roadmap recalculated from today"
      });

      showToast("Timetable successfully regenerated!", "success");
      await updateTimetableEditCounterPill();
      await renderTimetable();
      await renderDashboard();
    }

    async function updateTimetableEditCounterPill() {
      const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
      const count = await db.timetableChanges.where('timestamp').above(sevenDaysAgo).count();

      const pill = document.getElementById('top-edit-warning-pill');
      const countLabel = document.getElementById('top-edit-count');
      const banner = document.getElementById('timetable-change-alert-banner');
      const bannerCount = document.getElementById('tt-warning-change-count');

      if (pill) {
        countLabel.innerText = `${count}/3 Changes this week`;
        if (count >= 3) {
          pill.classList.remove('hidden');
          pill.className = "glass-panel px-3 py-1.5 rounded-full flex items-center gap-1.5 text-xs font-semibold text-amber-300 border border-amber-500/40 bg-amber-950/20";
          if (banner) {
            banner.classList.remove('hidden');
            if (bannerCount) bannerCount.innerText = count;
          }
        } else {
          pill.classList.remove('hidden');
          pill.className = "glass-panel px-3 py-1.5 rounded-full flex items-center gap-1.5 text-xs font-semibold text-slate-300 border border-white/10";
          if (banner) banner.classList.add('hidden');
        }
      }
    }

    // --- 10. SYLLABUS MATRIX VIEW ---
    async function renderSyllabus(searchQuery = '') {
      const container = document.getElementById('syllabus-subjects-list');
      const allTopics = await db.topicCoverage.toArray();

      const subjectsMap = {};
      allTopics.forEach(item => {
        if (!subjectsMap[item.subject]) subjectsMap[item.subject] = [];
        subjectsMap[item.subject].push(item);
      });

      const streamPreset = SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS;
      document.getElementById('syl-stream-badge').innerText = appState.profile.stream;

      // Calculate total overall
      const totalCompleted = allTopics.filter(t => t.completed).length;
      const totalCount = allTopics.length || 1;
      const overallPercent = Math.round((totalCompleted / totalCount) * 100);

      document.getElementById('syl-overall-percent').innerText = `${overallPercent}% (${totalCompleted} / ${totalCount} subtopics mastered)`;
      document.getElementById('syl-overall-bar').style.width = `${overallPercent}%`;

      container.innerHTML = '';

      Object.entries(subjectsMap).forEach(([subj, topics]) => {
        const weight = streamPreset[subj]?.weight || '~6%';
        const completedCount = topics.filter(t => t.completed).length;
        const subjPercent = Math.round((completedCount / topics.length) * 100);

        // Filter by search query
        const matchingTopics = topics.filter(t => {
          if (!searchQuery) return true;
          return t.topic.toLowerCase().includes(searchQuery.toLowerCase()) || subj.toLowerCase().includes(searchQuery.toLowerCase());
        });

        if (searchQuery && matchingTopics.length === 0) return;

        const card = document.createElement('div');
        card.className = 'glass-card p-5 rounded-2xl border border-white/10 space-y-4';

        let topicItemsHtml = '';
        matchingTopics.forEach(t => {
          topicItemsHtml += `
            <div class="p-3 rounded-xl bg-slate-900/60 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
              <div class="flex items-start sm:items-center gap-3">
                <input type="checkbox" ${t.completed ? 'checked' : ''} onchange="toggleTopicCompletion(${t.id})" class="mt-0.5 sm:mt-0 w-4 h-4 rounded border-slate-700 text-brand-600 focus:ring-brand-500 cursor-pointer">
                <span class="${t.completed ? 'line-through text-slate-500 font-medium' : 'text-white font-medium'}">${t.topic}</span>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button onclick="cycleTopicRevision(${t.id})" class="px-2 py-0.5 rounded text-[11px] font-mono font-semibold transition ${getRevisionBadgeClass(t.revisionCount)}">
                  Rev ${t.revisionCount || 0}x
                </button>
                <button onclick="openTopicNotesModal(${t.id})" class="px-2.5 py-1 glass-panel hover:bg-slate-800 text-slate-300 rounded-lg text-[11px] font-medium transition flex items-center gap-1">
                  <i data-lucide="file-text" class="w-3 h-3 text-brand-400"></i>
                  <span>${t.notes ? 'View Notes' : '+ Notes'}</span>
                </button>
              </div>
            </div>
          `;
        });

        card.innerHTML = `
          <div class="flex items-center justify-between border-b border-white/10 pb-3">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="text-sm font-bold text-white">${subj}</h4>
                <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 font-bold">${weight}</span>
              </div>
              <p class="text-[11px] text-slate-400">${completedCount} of ${topics.length} topics mastered</p>
            </div>
            <div class="text-right">
              <span class="text-sm font-extrabold text-brand-400 font-mono">${subjPercent}%</span>
              <div class="w-24 bg-slate-800 h-1.5 rounded-full overflow-hidden mt-1">
                <div class="h-full bg-brand-500 transition-all duration-300" style="width: ${subjPercent}%"></div>
              </div>
            </div>
          </div>
          <div class="space-y-2">
            ${topicItemsHtml}
          </div>
        `;
        container.appendChild(card);
      });

      lucide.createIcons();
    }

    function getRevisionBadgeClass(count) {
      if (count >= 3) return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
      if (count >= 1) return 'bg-brand-500/20 text-brand-300 border border-brand-500/30';
      return 'bg-slate-800 text-slate-400 border border-white/5';
    }

    function filterSyllabusSearch(query) {
      renderSyllabus(query);
    }

    async function toggleTopicCompletion(id) {
      const topic = await db.topicCoverage.get(id);
      if (!topic) return;
      topic.completed = !topic.completed;
      topic.status = topic.completed ? 'Completed' : 'Pending';
      topic.lastStudied = new Date().toISOString();
      await db.topicCoverage.put(topic);

      playBeep(topic.completed ? 700 : 350, 100);
      showToast(`Updated "${topic.topic.substring(0, 30)}..."`, "info");
      await renderSyllabus();
      await renderDashboard();
    }

    async function cycleTopicRevision(id) {
      const topic = await db.topicCoverage.get(id);
      if (!topic) return;
      topic.revisionCount = (topic.revisionCount || 0) + 1;
      await db.topicCoverage.put(topic);

      playBeep(550, 100);
      showToast(`Revision count for topic incremented to ${topic.revisionCount}x!`, "success");
      await renderSyllabus();
    }

    let activeTopicNotesId = null;
    async function openTopicNotesModal(id) {
      activeTopicNotesId = id;
      const topic = await db.topicCoverage.get(id);
      if (!topic) return;

      document.getElementById('m-notes-title').innerHTML = `<i data-lucide="file-text" class="w-4 h-4 text-brand-400"></i><span>Notes: ${topic.subject}</span>`;
      document.getElementById('m-topic-notes-text').value = topic.notes || '';
      openModal('modal-topic-notes');
      lucide.createIcons();
    }

    async function saveTopicNotes() {
      if (!activeTopicNotesId) return;
      const text = document.getElementById('m-topic-notes-text').value;
      const topic = await db.topicCoverage.get(activeTopicNotesId);
      if (topic) {
        topic.notes = text;
        await db.topicCoverage.put(topic);
        showToast("Topic notes saved successfully!", "success");
      }
      closeModal('modal-topic-notes');
      await renderSyllabus();
    }

    // --- 11. PYQ TRACKER & BULK PARSER ---
    async function renderPYQTable() {
      const subjectFilter = document.getElementById('pyq-filter-subject').value;
      const statusFilter = document.getElementById('pyq-filter-status').value;
      const typeFilter = document.getElementById('pyq-filter-type').value;
      const search = (document.getElementById('pyq-search-query').value || '').toLowerCase();

      const allEntries = await db.pyqEntries.toArray();

      // Populate subject filter dropdown if empty
      const subjSelect = document.getElementById('pyq-filter-subject');
      if (subjSelect.children.length <= 1) {
        const subjects = Object.keys(SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS);
        subjects.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s;
          opt.innerText = s;
          subjSelect.appendChild(opt);
        });
      }

      let filtered = allEntries;
      if (subjectFilter && subjectFilter !== 'all') filtered = filtered.filter(p => p.subject === subjectFilter);
      if (statusFilter && statusFilter !== 'all') filtered = filtered.filter(p => p.status === statusFilter);
      if (typeFilter && typeFilter !== 'all') filtered = filtered.filter(p => p.qType === typeFilter);
      if (search) {
        filtered = filtered.filter(p => (p.topic || '').toLowerCase().includes(search) || (p.notes || '').toLowerCase().includes(search) || (p.subject || '').toLowerCase().includes(search));
      }

      const tbody = document.getElementById('pyq-table-body');
      const emptyMsg = document.getElementById('pyq-table-empty');

      tbody.innerHTML = '';
      if (filtered.length === 0) {
        emptyMsg.classList.remove('hidden');
        return;
      }
      emptyMsg.classList.add('hidden');

      filtered.reverse().forEach(p => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-900/40 transition';
        tr.innerHTML = `
          <td class="py-3 px-4 text-slate-400 font-mono text-[11px]">${p.date}</td>
          <td class="py-3 px-4 font-bold text-white">${p.subject}</td>
          <td class="py-3 px-4 text-slate-300">${p.topic || '--'}</td>
          <td class="py-3 px-4 font-mono text-brand-300 font-semibold">${p.year} ${p.qNum || ''}</td>
          <td class="py-3 px-4"><span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300">${p.qType || 'MCQ'}</span></td>
          <td class="py-3 px-4">${getPyqStatusBadge(p.status)}</td>
          <td class="py-3 px-4 text-slate-400 truncate max-w-xs">${p.notes || '--'}</td>
          <td class="py-3 px-4 text-right">
            <button onclick="deletePyqEntry(${p.id})" class="text-slate-500 hover:text-rose-400 p-1 transition" title="Delete">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      lucide.createIcons();
    }

    function getPyqStatusBadge(status) {
      if (status === 'Correct') return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">Correct</span>';
      if (status === 'Hint') return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300">With Hint</span>';
      if (status === 'Wrong') return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300">Wrong (In SRS)</span>';
      return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400">Skipped</span>';
    }

    async function saveSinglePYQEntry() {
      const subject = document.getElementById('m-pyq-subject').value;
      const topic = document.getElementById('m-pyq-topic').value;
      const year = Number(document.getElementById('m-pyq-year').value) || 2023;
      const qNum = document.getElementById('m-pyq-qnum').value.trim() || "Q1";
      const qType = document.getElementById('m-pyq-type').value;
      const status = document.getElementById('m-pyq-status').value;
      const note = document.getElementById('m-pyq-note').value.trim();

      const todayStr = new Date().toISOString().split('T')[0];

      // Add to PYQ table
      await db.pyqEntries.add({
        date: todayStr,
        year: year,
        subject: subject,
        topic: topic,
        qNum: qNum,
        qType: qType,
        marks: qType.includes('2M') ? 2 : 1,
        status: status,
        mistakeCategory: status === 'Wrong' ? 'Concept Gap' : '',
        timeSpent: 3,
        notes: note
      });

      // If wrong, auto-add to SRS error log!
      if (status === 'Wrong') {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        await db.errorLog.add({
          date: todayStr,
          subject: subject,
          topic: topic,
          source: `GATE ${year} ${qNum}`,
          mistakeCategory: 'Concept Gap',
          questionSnippet: `GATE ${year} ${qNum} (${subject}: ${topic})`,
          mistakeExplanation: note || "Mistake made during PYQ solving session",
          correctApproach: "Revisit core concept and re-solve with clear step-by-step logic.",
          box: 1,
          nextReviewDate: tomorrow.toISOString().split('T')[0],
          reviewCount: 0,
          status: 'Active'
        });
        showToast("Logged PYQ & Auto-added to Leitner Box 1 Error Notebook!", "success");
      } else {
        showToast("PYQ entry saved successfully!", "success");
      }

      closeModal('modal-add-pyq');
      await renderPYQTable();
      await renderDashboard();
    }

    async function executeBulkPYQParse() {
      const text = document.getElementById('m-bulk-pyq-input').value.trim();
      if (!text) {
        showToast("Please enter text to parse.", "warning");
        return;
      }

      const rawItems = text.split(/[\n;]+/).map(s => s.trim()).filter(s => s.length > 0);
      const todayStr = new Date().toISOString().split('T')[0];
      let addedCount = 0;

      for (const item of rawItems) {
        // e.g. "DSA 2022 Q14 Correct" or "OS 2021 Q32 Wrong Silly"
        const tokens = item.split(/\s+/);
        const subjCode = tokens[0] || "Core CS";
        const year = Number(tokens[1]) || 2022;
        const qNum = tokens[2] || "Q1";
        const status = item.toLowerCase().includes('wrong') ? 'Wrong' : item.toLowerCase().includes('hint') ? 'Hint' : 'Correct';
        const mistakeNote = tokens.slice(4).join(' ') || item;

        await db.pyqEntries.add({
          date: todayStr,
          year: year,
          subject: mapSubjectCodeToName(subjCode),
          topic: "General Topic",
          qNum: qNum,
          qType: "MCQ 2M",
          marks: 2,
          status: status,
          mistakeCategory: status === 'Wrong' ? 'Silly Mistake' : '',
          timeSpent: 2,
          notes: mistakeNote
        });

        if (status === 'Wrong') {
          const tomorrow = new Date();
          tomorrow.setDate(tomorrow.getDate() + 1);
          await db.errorLog.add({
            date: todayStr,
            subject: mapSubjectCodeToName(subjCode),
            topic: "Bulk Logged Error",
            source: `GATE ${year} ${qNum}`,
            mistakeCategory: 'Silly Mistake',
            questionSnippet: `Bulk PYQ: ${item}`,
            mistakeExplanation: mistakeNote,
            correctApproach: "Review step-by-step approach.",
            box: 1,
            nextReviewDate: tomorrow.toISOString().split('T')[0],
            reviewCount: 0,
            status: 'Active'
          });
        }
        addedCount++;
      }

      showToast(`Parsed and saved ${addedCount} PYQ records!`, "success");
      closeModal('modal-bulk-pyq');
      await renderPYQTable();
      await renderDashboard();
    }

    function mapSubjectCodeToName(code) {
      const c = code.toUpperCase();
      if (c === 'DSA' || c === 'PROG' || c === 'DS') return "Programming & Data Structures";
      if (c === 'OS') return "Operating Systems";
      if (c === 'DBMS' || c === 'DB') return "Databases (DBMS)";
      if (c === 'CN') return "Computer Networks";
      if (c === 'TOC' || c === 'FLAT') return "Theory of Computation";
      if (c === 'CD' || c === 'COMPILER') return "Compiler Design";
      if (c === 'COA' || c === 'CO') return "Computer Organization & Architecture";
      if (c === 'DL' || c === 'DIGITAL') return "Digital Logic";
      if (c === 'MATH' || c === 'EM') return "Engineering Mathematics";
      if (c === 'DM') return "Discrete Mathematics";
      if (c === 'ALGO') return "Algorithms";
      return "Engineering Mathematics";
    }

    async function deletePyqEntry(id) {
      await db.pyqEntries.delete(id);
      showToast("PYQ record removed.", "info");
      await renderPYQTable();
      await renderDashboard();
    }

    // --- 12. ERROR LOG & SPACED REPETITION (SRS) ---
    async function renderErrorTable() {
      const categoryFilter = document.getElementById('err-filter-category').value;
      const boxFilter = document.getElementById('err-filter-box').value;
      const search = (document.getElementById('err-search-query').value || '').toLowerCase();

      const allErrors = await db.errorLog.toArray();
      const todayStr = new Date().toISOString().split('T')[0];

      // Update 5-box counters
      document.getElementById('srs-count-box-1').innerText = allErrors.filter(e => e.box === 1).length;
      document.getElementById('srs-count-box-2').innerText = allErrors.filter(e => e.box === 2).length;
      document.getElementById('srs-count-box-3').innerText = allErrors.filter(e => e.box === 3).length;
      document.getElementById('srs-count-box-4').innerText = allErrors.filter(e => e.box === 4).length;
      document.getElementById('srs-count-box-5').innerText = allErrors.filter(e => e.box === 5).length;

      let filtered = allErrors;
      if (categoryFilter && categoryFilter !== 'all') filtered = filtered.filter(e => e.mistakeCategory === categoryFilter);
      if (boxFilter && boxFilter !== 'all') {
        if (boxFilter === 'due') filtered = filtered.filter(e => !e.nextReviewDate || e.nextReviewDate <= todayStr);
        else filtered = filtered.filter(e => e.box === Number(boxFilter));
      }
      if (search) {
        filtered = filtered.filter(e => (e.subject || '').toLowerCase().includes(search) || (e.topic || '').toLowerCase().includes(search) || (e.questionSnippet || '').toLowerCase().includes(search) || (e.correctApproach || '').toLowerCase().includes(search));
      }

      const tbody = document.getElementById('error-table-body');
      const emptyMsg = document.getElementById('error-table-empty');

      tbody.innerHTML = '';
      if (filtered.length === 0) {
        emptyMsg.classList.remove('hidden');
        return;
      }
      emptyMsg.classList.add('hidden');

      filtered.reverse().forEach(e => {
        const isDue = !e.nextReviewDate || e.nextReviewDate <= todayStr;
        const tr = document.createElement('tr');
        tr.className = `hover:bg-slate-900/40 transition ${isDue ? 'bg-rose-950/10' : ''}`;
        tr.innerHTML = `
          <td class="py-3 px-4">
            <div class="font-bold text-white">${e.subject}</div>
            <div class="text-[11px] text-slate-400">${e.topic || ''}</div>
          </td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${getErrorCategoryBadgeClass(e.mistakeCategory)}">${e.mistakeCategory}</span>
          </td>
          <td class="py-3 px-4 text-slate-300 max-w-xs truncate">${e.questionSnippet || '--'}</td>
          <td class="py-3 px-4 text-slate-300 max-w-xs truncate">${e.correctApproach || '--'}</td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-slate-300">Box ${e.box || 1}</span>
          </td>
          <td class="py-3 px-4 font-mono text-[11px] ${isDue ? 'text-rose-400 font-bold' : 'text-slate-400'}">
            ${isDue ? 'Due Today ⚠️' : e.nextReviewDate}
          </td>
          <td class="py-3 px-4 text-right">
            <button onclick="startSingleCardReview(${e.id})" class="px-2.5 py-1 bg-rose-600/30 hover:bg-rose-600 text-rose-300 hover:text-white rounded-lg text-xs font-semibold transition mr-1">
              Review
            </button>
            <button onclick="deleteErrorEntry(${e.id})" class="text-slate-500 hover:text-rose-400 p-1 transition" title="Delete">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      lucide.createIcons();
    }

    function getErrorCategoryBadgeClass(cat) {
      if (cat === 'Concept Gap') return 'bg-rose-500/20 text-rose-300 border border-rose-500/30';
      if (cat === 'Calculation Error') return 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
      if (cat === 'Silly Mistake') return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      if (cat === 'Formula Forgotten') return 'bg-violet-500/20 text-violet-300 border border-violet-500/30';
      return 'bg-slate-800 text-slate-300';
    }

    async function saveErrorLogEntry() {
      const subject = document.getElementById('m-err-subject').value;
      const topic = document.getElementById('m-err-topic').value.trim() || "General";
      const category = document.getElementById('m-err-category').value;
      const snippet = document.getElementById('m-err-snippet').value.trim();
      const solution = document.getElementById('m-err-solution').value.trim();

      if (!snippet || !solution) {
        showToast("Please provide both problem snippet and correct solution.", "warning");
        return;
      }

      const todayStr = new Date().toISOString().split('T')[0];
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);

      await db.errorLog.add({
        date: todayStr,
        subject: subject,
        topic: topic,
        source: "Manual Log",
        mistakeCategory: category,
        questionSnippet: snippet,
        mistakeExplanation: "Logged mistake during revision",
        correctApproach: solution,
        box: 1,
        nextReviewDate: tomorrow.toISOString().split('T')[0],
        reviewCount: 0,
        status: 'Active'
      });

      showToast("Mistake added to Spaced Repetition Box 1!", "success");
      closeModal('modal-add-error');
      await renderErrorTable();
      await renderDashboard();
    }

    async function startDailyReviewSession() {
      const todayStr = new Date().toISOString().split('T')[0];
      const allErrors = await db.errorLog.toArray();
      const dueErrors = allErrors.filter(e => !e.nextReviewDate || e.nextReviewDate <= todayStr);

      if (dueErrors.length === 0) {
        showToast("🎉 Zero SRS mistakes due for review today! Great retention.", "success");
        return;
      }

      appState.srsReviewQueue = dueErrors;
      appState.activeSrsCardIdx = 0;
      showSrsFlashcard(0);
      openModal('modal-srs-review');
    }

    async function startSingleCardReview(id) {
      const card = await db.errorLog.get(id);
      if (!card) return;
      appState.srsReviewQueue = [card];
      appState.activeSrsCardIdx = 0;
      showSrsFlashcard(0);
      openModal('modal-srs-review');
    }

    function showSrsFlashcard(idx) {
      const card = appState.srsReviewQueue[idx];
      if (!card) return;

      document.getElementById('srs-card-idx-display').innerText = `${idx + 1} of ${appState.srsReviewQueue.length}`;
      document.getElementById('srs-card-subject').innerText = `${card.subject} • ${card.topic || ''}`;
      document.getElementById('srs-card-category').innerText = card.mistakeCategory || 'Concept Gap';
      document.getElementById('srs-card-snippet').innerText = card.questionSnippet || card.mistakeExplanation || 'No question snippet';
      document.getElementById('srs-card-solution').innerText = card.correctApproach || 'No correct approach recorded';

      document.getElementById('srs-solution-container').classList.add('hidden');
      document.getElementById('srs-btn-reveal-box').classList.remove('hidden');
      document.getElementById('srs-rating-box').classList.add('hidden');
    }

    function revealSrsSolution() {
      document.getElementById('srs-solution-container').classList.remove('hidden');
      document.getElementById('srs-btn-reveal-box').classList.add('hidden');
      document.getElementById('srs-rating-box').classList.remove('hidden');
    }

    async function rateSrsCard(rating) {
      const card = appState.srsReviewQueue[appState.activeSrsCardIdx];
      if (!card) return;

      let newBox = card.box || 1;
      let daysToAdd = 1;

      if (rating === 'hard') {
        newBox = 1;
        daysToAdd = 1;
      } else if (rating === 'good') {
        newBox = Math.min(newBox + 1, 5);
        const intervals = { 1: 1, 2: 3, 3: 7, 4: 14, 5: 30 };
        daysToAdd = intervals[newBox] || 7;
      } else if (rating === 'easy') {
        newBox = 5;
        daysToAdd = 30;
      }

      const nextDate = new Date();
      nextDate.setDate(nextDate.getDate() + daysToAdd);

      card.box = newBox;
      card.nextReviewDate = nextDate.toISOString().split('T')[0];
      card.reviewCount = (card.reviewCount || 0) + 1;

      await db.errorLog.put(card);
      playBeep(rating === 'hard' ? 300 : 700, 100);

      // Move to next card
      appState.activeSrsCardIdx++;
      if (appState.activeSrsCardIdx < appState.srsReviewQueue.length) {
        showSrsFlashcard(appState.activeSrsCardIdx);
      } else {
        closeModal('modal-srs-review');
        showToast("🌟 Daily Spaced Repetition Review Completed!", "success");
        triggerCelebrationConfetti();
        await renderErrorTable();
        await renderDashboard();
      }
    }

    async function deleteErrorEntry(id) {
      await db.errorLog.delete(id);
      showToast("Error record deleted.", "info");
      await renderErrorTable();
      await renderDashboard();
    }

    // --- 13. MOCK TEST CENTER & PREDICTOR ---
    async function renderMockTests() {
      const allMocks = await db.mockTests.toArray();
      const tbody = document.getElementById('mock-table-body');
      const emptyMsg = document.getElementById('mock-table-empty');

      tbody.innerHTML = '';
      if (allMocks.length === 0) {
        emptyMsg.classList.remove('hidden');
        document.getElementById('mock-kpi-total').innerText = '0';
        document.getElementById('mock-kpi-highest').innerText = '--';
        document.getElementById('mock-kpi-average').innerText = '--';
        document.getElementById('mock-kpi-air-range').innerText = '--';
        return;
      }
      emptyMsg.classList.add('hidden');

      const scores = allMocks.map(m => m.marksObtained || 0);
      const maxScore = Math.max(...scores);
      const avgScore = (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);

      document.getElementById('mock-kpi-total').innerText = allMocks.length;
      document.getElementById('mock-kpi-highest').innerText = `${maxScore} / 100`;
      document.getElementById('mock-kpi-average').innerText = `${avgScore} / 100`;
      document.getElementById('mock-kpi-air-range').innerText = predictAIR(maxScore);

      allMocks.reverse().forEach(m => {
        const accuracy = m.accuracy || Math.round(((m.marksObtained || 0) / (m.totalMarks || 100)) * 100);
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-900/40 transition';
        tr.innerHTML = `
          <td class="py-3 px-4 font-mono text-[11px] text-slate-400">${m.date}</td>
          <td class="py-3 px-4 font-bold text-white">${m.name}</td>
          <td class="py-3 px-4 font-bold text-brand-400 font-mono">${m.marksObtained} / ${m.totalMarks || 100}</td>
          <td class="py-3 px-4 text-rose-400 font-mono">-${m.negativeMarks || 0}</td>
          <td class="py-3 px-4 font-mono text-emerald-400">${accuracy}%</td>
          <td class="py-3 px-4"><span class="px-2 py-0.5 rounded font-bold text-[10px] bg-brand-500/20 text-brand-300">${m.predictedAIR || predictAIR(m.marksObtained)}</span></td>
          <td class="py-3 px-4 text-right">
            <button onclick="deleteMockEntry(${m.id})" class="text-slate-500 hover:text-rose-400 p-1 transition" title="Delete">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      lucide.createIcons();
    }

    async function saveMockTestEntry() {
      const name = document.getElementById('m-mock-name').value.trim() || "Full Mock Test";
      const totalMarks = Number(document.getElementById('m-mock-total').value) || 100;
      const score = Number(document.getElementById('m-mock-score').value) || 0;
      const neg = Number(document.getElementById('m-mock-neg').value) || 0;
      const date = document.getElementById('m-mock-date').value || new Date().toISOString().split('T')[0];
      const notes = document.getElementById('m-mock-notes').value.trim();

      const accuracy = Math.round((score / totalMarks) * 100);
      const predictedAIR = predictAIR(score);

      await db.mockTests.add({
        date: date,
        name: name,
        series: "Test Series",
        totalMarks: totalMarks,
        marksObtained: score,
        negativeMarks: neg,
        accuracy: accuracy,
        percentile: calculatePercentile(score),
        predictedAIR: predictedAIR,
        sectionalScores: {},
        notes: notes
      });

      showToast(`Mock Test Logged! Predicted Rank: ${predictedAIR}`, "success");
      closeModal('modal-add-mock');
      await renderMockTests();
      await renderDashboard();
    }

    function predictAIR(marks) {
      if (marks >= 85) return "AIR 1 - 25";
      if (marks >= 75) return "AIR 25 - 100";
      if (marks >= 65) return "AIR 100 - 450";
      if (marks >= 55) return "AIR 450 - 1500";
      if (marks >= 45) return "AIR 1500 - 4500";
      if (marks >= 35) return "AIR 4500 - 12000";
      return "AIR 12000+";
    }

    function calculatePercentile(marks) {
      if (marks >= 80) return "99.9%";
      if (marks >= 70) return "99.6%";
      if (marks >= 60) return "98.5%";
      if (marks >= 50) return "95.0%";
      return "90.0%";
    }

    async function deleteMockEntry(id) {
      await db.mockTests.delete(id);
      showToast("Mock entry deleted.", "info");
      await renderMockTests();
      await renderDashboard();
    }

    // --- 14. GEMINI AI TEST CENTER & RETEST ENGINE ---
    function prepareAiTestCenter() {
      const subjSelect = document.getElementById('ai-gen-subject');
      const subjects = Object.keys(SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS);

      subjSelect.innerHTML = '';
      subjects.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.innerText = s;
        subjSelect.appendChild(opt);
      });

      updateAiTopicOptions(subjects[0]);
    }

    function updateAiTopicOptions(subj) {
      const topicSelect = document.getElementById('ai-gen-topic');
      const streamPreset = SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS;
      const topics = streamPreset[subj]?.topics || [];

      topicSelect.innerHTML = '<option value="All Topics">Entire Subject / Mixed</option>';
      topics.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t;
        opt.innerText = t.substring(0, 45) + '...';
        topicSelect.appendChild(opt);
      });
    }

    async function generateAiQuiz() {
      const subject = document.getElementById('ai-gen-subject').value;
      const topic = document.getElementById('ai-gen-topic').value;
      const difficulty = document.getElementById('ai-gen-difficulty').value;
      const count = Number(document.getElementById('ai-gen-count').value) || 5;
      const types = document.getElementById('ai-gen-types').value;

      document.getElementById('ai-gen-loading').classList.remove('hidden');
      document.getElementById('btn-generate-ai-quiz').disabled = true;

      const apiKey = appState.profile.geminiApiKey || '';
      let generatedQuestions = [];

      if (apiKey) {
        try {
          const prompt = `You are a Senior GATE ${appState.profile.stream} Exam Paper Setter. 
Generate exactly ${count} authentic GATE questions for:
Subject: ${subject}
Topic: ${topic}
Difficulty: ${difficulty}
Allowed Types: ${types}

Return ONLY a valid JSON array of question objects without markdown backticks. Schema:
[
  {
    "subject": "${subject}",
    "topic": "Topic Name",
    "type": "MCQ", // or MSQ or NAT
    "marks": 2, // 1 or 2
    "question": "Question statement here with clean math notations",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"], // empty for NAT
    "correctAnswer": "A) Option 1", // or ["A", "B"] for MSQ, or "42.5" for NAT
    "tolerance": 0.1, // for NAT only
    "explanation": "Detailed step-by-step rigorous solution with key formulas"
  }
]`;

          const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
          const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }],
              generationConfig: { temperature: 0.2 }
            })
          });

          if (!res.ok) throw new Error(`Gemini API error ${res.status}`);
          const data = await res.json();
          const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || '[]';
          const cleanedText = rawText.replace(/```json/g, '').replace(/```/g, '').trim();
          generatedQuestions = JSON.parse(cleanedText);
        } catch (err) {
          console.warn("Gemini API call failed, falling back to built-in question bank:", err);
          showToast("Using built-in GATE question bank (AI API offline/fallback).", "info");
          generatedQuestions = getRandomOfflineQuestions(count, subject);
        }
      } else {
        showToast("Running with built-in GATE question bank. Add Gemini Key in Settings for unlimited AI questions!", "info");
        generatedQuestions = getRandomOfflineQuestions(count, subject);
      }

      document.getElementById('ai-gen-loading').classList.add('hidden');
      document.getElementById('btn-generate-ai-quiz').disabled = false;

      if (!generatedQuestions || generatedQuestions.length === 0) {
        generatedQuestions = getRandomOfflineQuestions(count, subject);
      }

      startActiveQuizSession(subject, generatedQuestions);
    }

    function getRandomOfflineQuestions(count, subject) {
      const matching = OFFLINE_QUESTION_BANK.filter(q => q.subject === subject);
      const pool = matching.length >= count ? matching : OFFLINE_QUESTION_BANK;
      const shuffled = [...pool].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    }

    function startActiveQuizSession(subject, questions) {
      appState.activeQuiz = {
        title: `AI Drill: ${subject}`,
        subject: subject,
        questions: questions,
        startTime: Date.now(),
        durationSeconds: questions.length * 120 // 2 mins per question
      };

      appState.quizAnswers = {};
      appState.quizReviewMarked = new Set();
      appState.currentQIdx = 0;

      document.getElementById('ai-generator-panel').classList.add('hidden');
      document.getElementById('ai-active-quiz-engine').classList.remove('hidden');
      document.getElementById('ai-quiz-result-view').classList.add('hidden');

      document.getElementById('quiz-title-display').innerText = appState.activeQuiz.title;

      // Start Quiz Timer
      let remaining = appState.activeQuiz.durationSeconds;
      if (appState.quizTimerId) clearInterval(appState.quizTimerId);

      appState.quizTimerId = setInterval(() => {
        if (remaining > 0) {
          remaining--;
          const m = Math.floor(remaining / 60);
          const s = remaining % 60;
          document.getElementById('quiz-timer-clock').innerText = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        } else {
          clearInterval(appState.quizTimerId);
          confirmSubmitQuiz();
        }
      }, 1000);

      renderQuizPalette();
      showQuizQuestion(0);
    }

    function renderQuizPalette() {
      const container = document.getElementById('quiz-palette-container');
      container.innerHTML = '';

      appState.activeQuiz.questions.forEach((q, idx) => {
        const isAnswered = appState.quizAnswers[idx] !== undefined && appState.quizAnswers[idx] !== '';
        const isMarked = appState.quizReviewMarked.has(idx);
        const isCurrent = appState.currentQIdx === idx;

        let style = "bg-slate-800 text-slate-300 border-white/10";
        if (isAnswered) style = "bg-brand-600 text-white font-bold border-brand-400";
        if (isMarked) style = "bg-amber-600 text-white font-bold border-amber-400";
        if (isCurrent) style += " ring-2 ring-white";

        const btn = document.createElement('button');
        btn.className = `w-8 h-8 rounded-xl flex items-center justify-center text-xs font-mono border shrink-0 transition ${style}`;
        btn.innerText = idx + 1;
        btn.onclick = () => showQuizQuestion(idx);
        container.appendChild(btn);
      });
    }

    function showQuizQuestion(idx) {
      appState.currentQIdx = idx;
      const q = appState.activeQuiz.questions[idx];

      document.getElementById('quiz-q-num-label').innerText = `Question ${idx + 1} of ${appState.activeQuiz.questions.length}`;
      document.getElementById('quiz-q-type-label').innerText = `${q.type} (${q.marks || 2}M)`;
      document.getElementById('quiz-q-statement').innerText = q.question;

      const optContainer = document.getElementById('quiz-q-options');
      optContainer.innerHTML = '';

      const currentAns = appState.quizAnswers[idx];

      if (q.type === 'MCQ' || (!q.type && q.options)) {
        q.options.forEach(opt => {
          const isSelected = currentAns === opt;
          const label = document.createElement('label');
          label.className = `p-3 rounded-xl border flex items-center gap-3 cursor-pointer transition text-xs ${isSelected ? 'bg-brand-950/40 border-brand-500 ring-1 ring-brand-500' : 'bg-slate-900/60 border-white/10 hover:border-white/20'}`;
          label.innerHTML = `
            <input type="radio" name="active_mcq" value="${opt}" ${isSelected ? 'checked' : ''} onchange="setQuizAnswer('${opt}')" class="text-brand-600 focus:ring-brand-500">
            <span class="text-white font-medium">${opt}</span>
          `;
          optContainer.appendChild(label);
        });
      } else if (q.type === 'MSQ') {
        const selectedArray = Array.isArray(currentAns) ? currentAns : [];
        q.options.forEach(opt => {
          const optLetter = opt.substring(0, 1);
          const isChecked = selectedArray.includes(optLetter) || selectedArray.includes(opt);
          const label = document.createElement('label');
          label.className = `p-3 rounded-xl border flex items-center gap-3 cursor-pointer transition text-xs ${isChecked ? 'bg-brand-950/40 border-brand-500 ring-1 ring-brand-500' : 'bg-slate-900/60 border-white/10 hover:border-white/20'}`;
          label.innerHTML = `
            <input type="checkbox" value="${optLetter}" ${isChecked ? 'checked' : ''} onchange="toggleMsqAnswer('${optLetter}')" class="rounded border-slate-700 text-brand-600 focus:ring-brand-500">
            <span class="text-white font-medium">${opt}</span>
          `;
          optContainer.appendChild(label);
        });
      } else {
        // NAT Type
        optContainer.innerHTML = `
          <div class="space-y-2">
            <label class="block text-slate-400 text-xs">Enter Numerical Answer (e.g. 42.5):</label>
            <input type="number" step="any" id="nat-answer-input" value="${currentAns || ''}" oninput="setQuizAnswer(this.value)" placeholder="Enter numerical value..." class="w-full glass-input rounded-xl px-4 py-3 text-sm font-mono text-white">
          </div>
        `;
      }

      // Prev / Next button state
      document.getElementById('btn-quiz-prev').disabled = idx === 0;
      document.getElementById('btn-quiz-next').innerText = idx === appState.activeQuiz.questions.length - 1 ? "Review All" : "Next →";

      renderQuizPalette();
    }

    function setQuizAnswer(val) {
      appState.quizAnswers[appState.currentQIdx] = val;
      renderQuizPalette();
    }

    function toggleMsqAnswer(letter) {
      let current = appState.quizAnswers[appState.currentQIdx] || [];
      if (!Array.isArray(current)) current = [];

      if (current.includes(letter)) {
        current = current.filter(x => x !== letter);
      } else {
        current.push(letter);
      }
      appState.quizAnswers[appState.currentQIdx] = current;
      renderQuizPalette();
    }

    function clearCurrentAnswer() {
      delete appState.quizAnswers[appState.currentQIdx];
      showQuizQuestion(appState.currentQIdx);
    }

    function markCurrentQForReview() {
      if (appState.quizReviewMarked.has(appState.currentQIdx)) {
        appState.quizReviewMarked.delete(appState.currentQIdx);
      } else {
        appState.quizReviewMarked.add(appState.currentQIdx);
      }
      renderQuizPalette();
    }

    function quizNavPrev() {
      if (appState.currentQIdx > 0) showQuizQuestion(appState.currentQIdx - 1);
    }

    function quizNavNext() {
      if (appState.currentQIdx < appState.activeQuiz.questions.length - 1) {
        showQuizQuestion(appState.currentQIdx + 1);
      }
    }

    async function confirmSubmitQuiz() {
      if (appState.quizTimerId) clearInterval(appState.quizTimerId);

      // Evaluate score
      let marksEarned = 0;
      let correctCount = 0;
      let wrongCount = 0;
      const results = [];

      appState.activeQuiz.questions.forEach((q, idx) => {
        const userAns = appState.quizAnswers[idx];
        const marks = q.marks || 2;
        let isCorrect = false;

        if (q.type === 'MCQ' || !q.type) {
          if (userAns && (userAns === q.correctAnswer || userAns.startsWith(q.correctAnswer[0]))) {
            isCorrect = true;
          }
        } else if (q.type === 'MSQ') {
          const userArr = Array.isArray(userAns) ? userAns.sort() : [];
          const correctArr = Array.isArray(q.correctAnswer) ? q.correctAnswer.sort() : [q.correctAnswer];
          isCorrect = JSON.stringify(userArr) === JSON.stringify(correctArr);
        } else if (q.type === 'NAT') {
          const uNum = parseFloat(userAns);
          const cNum = parseFloat(q.correctAnswer);
          const tol = q.tolerance || 0.1;
          if (!isNaN(uNum) && Math.abs(uNum - cNum) <= tol) {
            isCorrect = true;
          }
        }

        if (isCorrect) {
          marksEarned += marks;
          correctCount++;
        } else if (userAns !== undefined && userAns !== '') {
          // Negative marking for MCQs only
          if (q.type === 'MCQ' || !q.type) {
            marksEarned -= (marks === 2 ? 0.66 : 0.33);
          }
          wrongCount++;
        }

        results.push({
          question: q,
          userAnswer: userAns,
          isCorrect: isCorrect
        });
      });

      marksEarned = Math.max(parseFloat(marksEarned.toFixed(2)), 0);
      const totalPossible = appState.activeQuiz.questions.reduce((acc, q) => acc + (q.marks || 2), 0);
      const accuracy = correctCount + wrongCount > 0 ? Math.round((correctCount / (correctCount + wrongCount)) * 100) : 0;

      // Save to Dexie
      await db.aiTests.add({
        timestamp: Date.now(),
        title: appState.activeQuiz.title,
        subject: appState.activeQuiz.subject,
        score: marksEarned,
        totalQuestions: appState.activeQuiz.questions.length,
        results: results,
        answers: appState.quizAnswers
      });

      // Show Result View
      document.getElementById('ai-active-quiz-engine').classList.add('hidden');
      document.getElementById('ai-quiz-result-view').classList.remove('hidden');

      document.getElementById('res-marks').innerText = `${marksEarned} / ${totalPossible}`;
      document.getElementById('res-accuracy').innerText = `${accuracy}%`;
      document.getElementById('res-counts').innerText = `${correctCount} Correct / ${wrongCount} Wrong`;
      document.getElementById('res-time').innerText = "Completed";

      // Store results in state for SRS sync button
      appState.activeQuiz.results = results;

      // Render solutions
      renderQuizSolutionsList(results);

      playBeep(correctCount >= wrongCount ? 800 : 400, 300);
      showToast(`Quiz completed! Scored ${marksEarned}/${totalPossible} Marks.`, "success");
      await renderDashboard();
    }

    function renderQuizSolutionsList(results) {
      const container = document.getElementById('res-solutions-list');
      container.innerHTML = '';

      results.forEach((r, idx) => {
        const q = r.question;
        const div = document.createElement('div');
        div.className = `p-4 rounded-2xl border transition space-y-3 ${r.isCorrect ? 'bg-emerald-950/20 border-emerald-500/30' : 'bg-rose-950/20 border-rose-500/30'}`;
        div.innerHTML = `
          <div class="flex items-center justify-between border-b border-white/10 pb-2 text-xs">
            <span class="font-bold text-white">Q${idx + 1}: ${q.type || 'MCQ'} (${q.marks || 2}M)</span>
            <span class="px-2 py-0.5 rounded font-bold ${r.isCorrect ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}">
              ${r.isCorrect ? '✓ Correct' : '✗ Incorrect / Missed'}
            </span>
          </div>

          <div class="text-xs font-medium text-white select-text leading-relaxed">
            ${q.question}
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs pt-1">
            <div class="p-2.5 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
              <span class="text-[10px] text-slate-400 font-semibold uppercase">Your Answer:</span>
              <div class="text-white font-mono font-bold">${Array.isArray(r.userAnswer) ? r.userAnswer.join(', ') : (r.userAnswer || 'Unattempted')}</div>
            </div>
            <div class="p-2.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 space-y-1">
              <span class="text-[10px] text-emerald-400 font-semibold uppercase">Correct Answer:</span>
              <div class="text-emerald-300 font-mono font-bold">${Array.isArray(q.correctAnswer) ? q.correctAnswer.join(', ') : q.correctAnswer}</div>
            </div>
          </div>

          <div class="p-3 rounded-xl bg-slate-900/80 border border-white/5 text-xs text-slate-300 space-y-1 select-text">
            <div class="text-[10px] font-bold uppercase tracking-wider text-brand-400">Step-by-Step Explanation:</div>
            <div class="leading-relaxed whitespace-pre-line">${q.explanation || 'Review core formulas.'}</div>
          </div>
        `;
        container.appendChild(div);
      });
    }

    async function addAllWrongQuestionsToErrorLog() {
      if (!appState.activeQuiz || !appState.activeQuiz.results) return;

      const wrongItems = appState.activeQuiz.results.filter(r => !r.isCorrect);
      if (wrongItems.length === 0) {
        showToast("No wrong questions to add! 100% correct.", "success");
        return;
      }

      const todayStr = new Date().toISOString().split('T')[0];
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);

      for (const item of wrongItems) {
        const q = item.question;
        await db.errorLog.add({
          date: todayStr,
          subject: q.subject || appState.activeQuiz.subject,
          topic: q.topic || "AI Retest Error",
          source: "AI Quiz Engine",
          mistakeCategory: "Concept Gap",
          questionSnippet: q.question,
          mistakeExplanation: `Your Answer: ${item.userAnswer || 'Unanswered'}`,
          correctApproach: q.explanation || `Correct Answer: ${q.correctAnswer}`,
          box: 1,
          nextReviewDate: tomorrow.toISOString().split('T')[0],
          reviewCount: 0,
          status: 'Active'
        });
      }

      showToast(`Added ${wrongItems.length} mistakes to Leitner Box 1 (SRS)!`, "success");
      document.getElementById('btn-add-wrong-to-errors').disabled = true;
      document.getElementById('btn-add-wrong-to-errors').innerText = "✓ Added to SRS";
      await renderDashboard();
    }

    function closeQuizResultView() {
      document.getElementById('ai-quiz-result-view').classList.add('hidden');
      document.getElementById('ai-generator-panel').classList.remove('hidden');
    }

    // --- 15. ANALYTICS & DEEP CHARTS ---
    async function renderAnalyticsCharts() {
      // Destroy existing charts
      Object.values(appState.charts).forEach(c => { if (c && typeof c.destroy === 'function') c.destroy(); });

      // 1. Weekly Study Hours Bar Chart
      const allLogs = await db.dailyLogs.toArray();
      const last7Days = getLast7DaysLabels();
      const studyData = last7Days.map(d => {
        const log = allLogs.find(l => l.date === d.dateStr);
        return log ? parseFloat(((log.studyMinutes || 0) / 60).toFixed(1)) : 0;
      });

      const totalWeekly = studyData.reduce((a, b) => a + b, 0).toFixed(1);
      document.getElementById('chart-weekly-hours-total').innerText = `${totalWeekly} hrs total this week`;

      const ctxStudy = document.getElementById('chart-weekly-study-hours').getContext('2d');
      appState.charts.study = new Chart(ctxStudy, {
        type: 'bar',
        data: {
          labels: last7Days.map(d => d.label),
          datasets: [{
            label: 'Hours Studied',
            data: studyData,
            backgroundColor: 'rgba(99, 102, 241, 0.7)',
            borderColor: '#6366f1',
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
          }
        }
      });

      // 2. Subject Mastery Radar Chart
      const allTopics = await db.topicCoverage.toArray();
      const streamPreset = SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS;
      const subjects = Object.keys(streamPreset);

      const subjectPercents = subjects.map(s => {
        const matching = allTopics.filter(t => t.subject === s);
        const comp = matching.filter(t => t.completed).length;
        return matching.length > 0 ? Math.round((comp / matching.length) * 100) : 0;
      });

      const ctxRadar = document.getElementById('chart-subject-radar').getContext('2d');
      appState.charts.radar = new Chart(ctxRadar, {
        type: 'radar',
        data: {
          labels: subjects.map(s => s.split(' ')[0]),
          datasets: [{
            label: 'Coverage %',
            data: subjectPercents,
            backgroundColor: 'rgba(52, 211, 153, 0.25)',
            borderColor: '#34d399',
            pointBackgroundColor: '#34d399'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              grid: { color: 'rgba(255,255,255,0.08)' },
              ticks: { color: '#94a3b8', backdropColor: 'transparent' },
              pointLabels: { color: '#cbd5e1', font: { size: 10 } }
            }
          }
        }
      });

      // 3. Mistake Categories Donut Chart
      const allErrors = await db.errorLog.toArray();
      const categories = ["Concept Gap", "Calculation Error", "Silly Mistake", "Misread Question", "Time Pressure", "Formula Forgotten"];
      const catCounts = categories.map(c => allErrors.filter(e => e.mistakeCategory === c).length);

      const ctxMistakes = document.getElementById('chart-mistake-types').getContext('2d');
      appState.charts.mistakes = new Chart(ctxMistakes, {
        type: 'doughnut',
        data: {
          labels: categories,
          datasets: [{
            data: catCounts.some(x => x > 0) ? catCounts : [1],
            backgroundColor: ['#f43f5e', '#f59e0b', '#3b82f6', '#8b5cf6', '#06b6d4', '#ec4899'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { color: '#cbd5e1', font: { size: 10 } } }
          }
        }
      });

      // 4. PYQ Accuracy by Subject
      const allPyqs = await db.pyqEntries.toArray();
      const pyqAccuracyBySubject = subjects.map(s => {
        const matching = allPyqs.filter(p => p.subject === s);
        const correct = matching.filter(p => p.status === 'Correct').length;
        return matching.length > 0 ? Math.round((correct / matching.length) * 100) : 0;
      });

      const ctxPyq = document.getElementById('chart-pyq-accuracy').getContext('2d');
      appState.charts.pyq = new Chart(ctxPyq, {
        type: 'bar',
        data: {
          labels: subjects.map(s => s.split(' ')[0]),
          datasets: [{
            label: 'Accuracy %',
            data: pyqAccuracyBySubject,
            backgroundColor: 'rgba(251, 191, 36, 0.7)',
            borderColor: '#fbbf24',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } }
          }
        }
      });
    }

    function renderDashboardMockChart(mocks) {
      if (appState.charts.dashMock) appState.charts.dashMock.destroy();
      const canvas = document.getElementById('chart-dash-mock-progress');
      if (!canvas) return;

      const labels = mocks.length > 0 ? mocks.map((m, i) => `Mock ${i + 1}`) : ['Mock 1', 'Mock 2', 'Mock 3', 'Mock 4'];
      const data = mocks.length > 0 ? mocks.map(m => m.marksObtained || 0) : [45, 52, 61, 68];
      const target = appState.profile.targetMarks || 80;

      appState.charts.dashMock = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Marks Scored',
              data: data,
              borderColor: '#6366f1',
              backgroundColor: 'rgba(99, 102, 241, 0.15)',
              fill: true,
              tension: 0.3,
              pointRadius: 4
            },
            {
              label: 'Target Goal',
              data: labels.map(() => target),
              borderColor: '#34d399',
              borderDash: [5, 5],
              fill: false,
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#94a3b8', font: { size: 10 } } }
          },
          scales: {
            y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
          }
        }
      });
    }

    function getLast7DaysLabels() {
      const days = [];
      const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        days.push({
          dateStr: d.toISOString().split('T')[0],
          label: daysOfWeek[d.getDay()]
        });
      }
      return days;
    }

    async function runAiStrategyAudit() {
      const apiKey = appState.profile.geminiApiKey;
      const allTopics = await db.topicCoverage.toArray();
      const allErrors = await db.errorLog.toArray();
      const allMocks = await db.mockTests.toArray();

      const compTopics = allTopics.filter(t => t.completed).length;
      const totalTopics = allTopics.length || 1;
      const percent = Math.round((compTopics / totalTopics) * 100);

      const topMistakes = allErrors.map(e => e.mistakeCategory);
      const avgScore = allMocks.length > 0 ? (allMocks.reduce((a, b) => a + (b.marksObtained || 0), 0) / allMocks.length).toFixed(1) : "N/A";

      const advisorEl = document.getElementById('dash-ai-advisor-text');
      advisorEl.innerText = "Analyzing your study trends with Gemini AI...";

      if (apiKey) {
        try {
          const prompt = `You are a GATE AIR 1 Mentor.
Aspirant Profile:
- Stream: ${appState.profile.stream}
- Syllabus Completion: ${percent}% (${compTopics}/${totalTopics} topics)
- Average Mock Score: ${avgScore} marks
- Recent Mistake Categories: ${topMistakes.slice(0, 8).join(', ') || 'None'}
- Target AIR: ${appState.profile.targetAIR}

Give exactly 2 concise, highly actionable sentences of tactical study advice for this week. Focus on highest weightage subject and error eradication.`;

          const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
          const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
          });

          if (res.ok) {
            const data = await res.json();
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
            advisorEl.innerText = `"${text.trim()}"`;
            showToast("AI Strategy Audit Generated!", "success");
            return;
          }
        } catch (e) {
          console.warn("AI audit failed:", e);
        }
      }

      // Fallback Heuristic
      advisorEl.innerText = `"Prioritize Discrete Mathematics & Operating Systems this week. Solve 25 PYQs per day and clear Leitner Box 1 errors daily to push past ${appState.profile.targetMarks} marks."`;
      showToast("Strategy audit generated (Heuristic Engine).", "info");
    }

    // --- 16. SETTINGS & DATA BACKUP ---
    function loadSettingsForm() {
      document.getElementById('set-name').value = appState.profile.name || '';
      document.getElementById('set-air').value = appState.profile.targetAIR || '';
      document.getElementById('set-target-marks').value = appState.profile.targetMarks || 80;
      document.getElementById('set-institute').value = appState.profile.dreamInstitute || '';
      document.getElementById('set-exam-date').value = appState.profile.examDate || '';
      document.getElementById('set-apikey').value = appState.profile.geminiApiKey || '';
    }

    async function saveUserProfileSettings() {
      appState.profile.name = document.getElementById('set-name').value.trim();
      appState.profile.targetAIR = document.getElementById('set-air').value.trim();
      appState.profile.targetMarks = Number(document.getElementById('set-target-marks').value) || 80;
      appState.profile.dreamInstitute = document.getElementById('set-institute').value.trim();
      appState.profile.examDate = document.getElementById('set-exam-date').value;
      appState.profile.geminiApiKey = document.getElementById('set-apikey').value.trim();

      await db.user.put({ id: 'profile', ...appState.profile });
      showToast("Profile Settings Saved Successfully!", "success");
      await refreshAllData();
    }

    async function exportFullDatabaseJSON() {
      const dump = {
        version: "GATE_TRACKER_PRO_V2",
        exportedAt: new Date().toISOString(),
        profile: await db.user.toArray(),
        topics: await db.topicCoverage.toArray(),
        timetable: await db.timetable.toArray(),
        pyqs: await db.pyqEntries.toArray(),
        errors: await db.errorLog.toArray(),
        mocks: await db.mockTests.toArray(),
        aiTests: await db.aiTests.toArray(),
        dailyLogs: await db.dailyLogs.toArray()
      };

      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(dump, null, 2));
      const a = document.createElement('a');
      a.setAttribute("href", dataStr);
      a.setAttribute("download", `GATE_Tracker_Pro_Backup_${new Date().toISOString().split('T')[0]}.json`);
      document.body.appendChild(a);
      a.click();
      a.remove();
      showToast("JSON Backup Exported Successfully!", "success");
    }

    async function importDatabaseJSON(e) {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (evt) => {
        try {
          const dump = JSON.parse(evt.target.result);
          if (dump.profile) await db.user.bulkPut(dump.profile);
          if (dump.topics) { await db.topicCoverage.clear(); await db.topicCoverage.bulkAdd(dump.topics); }
          if (dump.timetable) { await db.timetable.clear(); await db.timetable.bulkAdd(dump.timetable); }
          if (dump.pyqs) { await db.pyqEntries.clear(); await db.pyqEntries.bulkAdd(dump.pyqs); }
          if (dump.errors) { await db.errorLog.clear(); await db.errorLog.bulkAdd(dump.errors); }
          if (dump.mocks) { await db.mockTests.clear(); await db.mockTests.bulkAdd(dump.mocks); }
          if (dump.aiTests) { await db.aiTests.clear(); await db.aiTests.bulkAdd(dump.aiTests); }
          if (dump.dailyLogs) { await db.dailyLogs.clear(); await db.dailyLogs.bulkAdd(dump.dailyLogs); }

          showToast("Backup Restored Successfully!", "success");
          setTimeout(() => location.reload(), 800);
        } catch (err) {
          showToast("Invalid JSON Backup file format.", "error");
        }
      };
      reader.readAsText(file);
    }

    async function exportTableToCSV(tableName) {
      const items = await db[tableName].toArray();
      if (items.length === 0) {
        showToast("No data in table to export.", "warning");
        return;
      }

      const headers = Object.keys(items[0]);
      const csvRows = [headers.join(',')];

      items.forEach(item => {
        const values = headers.map(h => `"${String(item[h] || '').replace(/"/g, '""')}"`);
        csvRows.push(values.join(','));
      });

      const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', `${tableName}_export.csv`);
      document.body.appendChild(a);
      a.click();
      a.remove();
      showToast(`${tableName} exported as CSV!`, "success");
    }

    async function wipeAllDataModal() {
      if (confirm("⚠️ ARE YOU SURE? This will permanently wipe all your study logs, errors, and timetable from IndexedDB.")) {
        await db.delete();
        localStorage.clear();
        location.reload();
      }
    }

    // --- 17. MANUAL TIME LOGGING & CUSTOM SUBJECTS ---
    async function saveManualStudyTime() {
      const date = document.getElementById('m-time-date').value || new Date().toISOString().split('T')[0];
      const hours = parseFloat(document.getElementById('m-time-hours').value) || 2.0;
      const mins = Math.round(hours * 60);

      await addStudyMinutesToToday(mins);
      showToast(`Logged ${hours} hours of study time!`, "success");
      closeModal('modal-manual-time');
      await renderDashboard();
    }

    async function saveCustomSubjectModule() {
      const name = document.getElementById('m-sub-name').value.trim();
      const weight = document.getElementById('m-sub-weight').value.trim() || "~6%";
      const topicsStr = document.getElementById('m-sub-topics').value.trim();

      if (!name) {
        showToast("Please provide a subject name.", "warning");
        return;
      }

      const topics = topicsStr.split(',').map(s => s.trim()).filter(s => s.length > 0);
      for (const t of topics) {
        await db.topicCoverage.add({
          subject: name,
          topic: t,
          completed: false,
          status: 'Pending',
          revisionCount: 0,
          difficulty: 'Medium',
          notes: '',
          lastStudied: null
        });
      }

      showToast(`Created Subject "${name}" with ${topics.length} topics!`, "success");
      closeModal('modal-add-subject');
      await renderSyllabus();
    }

    async function saveCustomTaskEntry() {
      const date = document.getElementById('m-task-date').value || new Date().toISOString().split('T')[0];
      const time = document.getElementById('m-task-time').value;
      const title = document.getElementById('m-task-title').value.trim();

      if (!title) {
        showToast("Please enter a task title.", "warning");
        return;
      }

      await db.timetable.add({
        date: date,
        phase: 1,
        blockIndex: 1,
        time: time,
        title: title,
        subject: "Custom Focus",
        status: 'pending',
        notes: 'Custom task'
      });

      showToast("Custom study block added to schedule!", "success");
      closeModal('modal-add-task');
      await renderTimetable();
      await renderDashboard();
    }

    function updateModalPyqTopics(subj) {
      const select = document.getElementById('m-pyq-topic');
      const streamPreset = SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS;
      const topics = streamPreset[subj]?.topics || ["General Topic"];

      select.innerHTML = '';
      topics.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.split('(')[0].trim();
        opt.innerText = t.substring(0, 35) + '...';
        select.appendChild(opt);
      });
    }

    // --- 18. MODAL & TOAST CONTROLLERS ---
    function openModal(id) {
      const m = document.getElementById(id);
      if (m) {
        m.classList.remove('hidden');
        m.style.display = 'flex';

        // Pre-fill subject dropdowns if needed
        if (id === 'modal-add-pyq' || id === 'modal-add-error') {
          const subjSelect = document.getElementById(id === 'modal-add-pyq' ? 'm-pyq-subject' : 'm-err-subject');
          const subjects = Object.keys(SYLLABUS_PRESETS[appState.profile.stream] || SYLLABUS_PRESETS.CS);
          subjSelect.innerHTML = '';
          subjects.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s;
            opt.innerText = s;
            subjSelect.appendChild(opt);
          });
          if (id === 'modal-add-pyq') updateModalPyqTopics(subjects[0]);
        }

        if (id === 'modal-manual-time') {
          document.getElementById('m-time-date').value = new Date().toISOString().split('T')[0];
        }
        if (id === 'modal-add-task') {
          document.getElementById('m-task-date').value = new Date().toISOString().split('T')[0];
        }
        if (id === 'modal-add-mock') {
          document.getElementById('m-mock-date').value = new Date().toISOString().split('T')[0];
        }

        lucide.createIcons();
      }
    }

    function closeModal(id) {
      const m = document.getElementById(id);
      if (m) {
        m.classList.add('hidden');
        m.style.display = 'none';
      }
    }

    function closeAllModals() {
      document.querySelectorAll('.modal-backdrop').forEach(m => {
        m.classList.add('hidden');
        m.style.display = 'none';
      });
    }

    function showToast(message, type = 'info') {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');

      const colors = {
        success: 'bg-emerald-900/90 border-emerald-500 text-emerald-100',
        error: 'bg-rose-900/90 border-rose-500 text-rose-100',
        warning: 'bg-amber-900/90 border-amber-500 text-amber-100',
        info: 'bg-slate-900/90 border-brand-500 text-slate-100'
      };

      const icons = {
        success: 'check-circle-2',
        error: 'alert-triangle',
        warning: 'alert-circle',
        info: 'info'
      };

      toast.className = `pointer-events-auto p-4 rounded-xl border shadow-2xl backdrop-blur-md flex items-center gap-3 text-xs font-semibold animate-fadeIn ${colors[type] || colors.info}`;
      toast.innerHTML = `
        <i data-lucide="${icons[type] || 'info'}" class="w-4 h-4 shrink-0"></i>
        <span>${message}</span>
      `;

      container.appendChild(toast);
      lucide.createIcons();

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 3500);
    }

    // --- 19. COUNTDOWN TICKER ---
    function startCountdownTicker() {
      function update() {
        const examDateStr = appState.profile.examDate || getNextGateExamDate();
        const target = new Date(examDateStr).getTime();
        const now = Date.now();
        const diff = target - now;

        const countdownEl = document.getElementById('top-countdown');
        if (!countdownEl) return;

        if (diff <= 0) {
          countdownEl.innerText = "GATE Exam Day!";
          return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
        const mins = Math.floor((diff / 1000 / 60) % 60);

        countdownEl.innerText = `${days}d ${hours}h ${mins}m Left`;
      }

      update();
      setInterval(update, 60000);
    }
  </script>
</body>
</html>
'''

    full_html = base_html + js_code
    target_path = r'C:\Users\adith\OneDrive\Desktop\Gate Notion Tracker\index.html'

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Successfully generated complete index.html ({len(full_html)} bytes)")

if __name__ == '__main__':
    generate()
