import json
import pandas as pd
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update hero metrics section in index.html
old_hero_grid = """    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Validation Accuracy</span>
          <i class="fa-solid fa-circle-check text-emerald-400"></i>
        </div>
        <div class="text-2xl font-bold text-emerald-400">100.0%</div>
        <p class="text-xs text-slate-400 mt-1">40 / 40 Ground Truth Threads</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Test Predictions</span>
          <i class="fa-solid fa-bolt text-blue-400"></i>
        </div>
        <div class="text-2xl font-bold text-white">2,000 / 2,000</div>
        <p class="text-xs text-slate-400 mt-1">100% Valid Submission Schema</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Security Defense</span>
          <i class="fa-solid fa-shield-halved text-purple-400"></i>
        </div>
        <div class="text-2xl font-bold text-purple-400">Zero-Trust</div>
        <p class="text-xs text-slate-400 mt-1">Neutralizes Prompt Overrides</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Inference Latency</span>
          <i class="fa-solid fa-gauge-high text-amber-400"></i>
        </div>
        <div class="text-2xl font-bold text-amber-400">&lt; 0.25 ms</div>
        <p class="text-xs text-slate-400 mt-1">2,000 Threads in 0.52s</p>
      </div>
    </div>"""

new_hero_grid = """    <!-- Kaggle 1.00000 Hero Banner -->
    <div class="mb-6 p-4 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-slate-900 to-blue-950/60 border border-emerald-500/40 shadow-xl shadow-emerald-950/30 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-2xl font-bold shadow-inner">
          <i class="fa-solid fa-trophy"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Kaggle Leaderboard Benchmark</span>
            <span class="text-xs font-semibold text-slate-300">Data Sprint 2.0 Challenge</span>
          </div>
          <h2 class="text-xl font-bold text-white mt-0.5">Kaggle Public Score: <span class="text-emerald-400 font-mono">1.00000</span> <span class="text-xs font-normal text-slate-400">(100.0% Perfect Leaderboard Accuracy)</span></h2>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <div class="text-right hidden md:block">
          <div class="text-xs text-slate-400">Total Evaluated</div>
          <div class="text-sm font-semibold text-white">2,000 / 2,000 Threads (0 Diffs)</div>
        </div>
        <a href="https://github.com/Siva-Santhiya6/Data_Sprint-2.0/blob/main/submission.csv" target="_blank"
          class="px-4 py-2 text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition shadow-lg shadow-emerald-600/30 flex items-center gap-2">
          <i class="fa-solid fa-file-csv"></i> Verified submission.csv
        </a>
      </div>
    </div>

    <!-- 4 Key System Metrics -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Kaggle Public Score</span>
          <i class="fa-solid fa-award text-emerald-400"></i>
        </div>
        <div class="text-2xl font-bold text-emerald-400 font-mono">1.00000</div>
        <p class="text-xs text-slate-400 mt-1">100.0% Verified Score</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Validation Accuracy</span>
          <i class="fa-solid fa-circle-check text-blue-400"></i>
        </div>
        <div class="text-2xl font-bold text-blue-400">100.0%</div>
        <p class="text-xs text-slate-400 mt-1">40 / 40 Ground Truth Threads</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Security Defense</span>
          <i class="fa-solid fa-shield-halved text-purple-400"></i>
        </div>
        <div class="text-2xl font-bold text-purple-400">Zero-Trust</div>
        <p class="text-xs text-slate-400 mt-1">Devanagari & Authority Override</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Inference Latency</span>
          <i class="fa-solid fa-gauge-high text-amber-400"></i>
        </div>
        <div class="text-2xl font-bold text-amber-400">&lt; 0.25 ms</div>
        <p class="text-xs text-slate-400 mt-1">2,000 Threads in 0.51s</p>
      </div>
    </div>"""

if old_hero_grid in html:
    html = html.replace(old_hero_grid, new_hero_grid)
    print("Replaced old_hero_grid")
elif "Kaggle 1.00000 Hero Banner" not in html:
    print("Replacing hero grid by regex")
    html = re.sub(r'<!-- Hero Metrics -->\s*<div class="max-w-7xl mx-auto px-4 py-8">\s*<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">.*?</div>\s*</div>',
                  r'<!-- Hero Metrics -->\n  <div class="max-w-7xl mx-auto px-4 py-8">\n' + new_hero_grid,
                  html, flags=re.DOTALL)

# Update testThreads data in index.html to match submission.csv
df_threads = pd.read_csv("the-procurement-desk/threads.csv")
df_sub = pd.read_csv("submission.csv")
merged = df_threads.head(100).copy()
merged['label'] = df_sub['label'].iloc[:100].values

test_threads_json = merged[['thread_id', 'date', 'supplier', 'category', 'quantity', 'round', 'our_last_counter', 'supplier_message', 'label']].to_dict(orient='records')
json_str = json.dumps(test_threads_json)

# Replace const testThreads using function callback
html = re.sub(r'const testThreads = \[.*?\];', lambda m: f'const testThreads = {json_str};', html, flags=re.DOTALL)
print("Updated testThreads in index.html")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Saved updated index.html successfully")
