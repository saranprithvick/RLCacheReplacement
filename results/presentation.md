---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

section {
  font-family: 'Inter', sans-serif;
  padding: 50px 70px;
  background: radial-gradient(circle at 10% 20%, rgb(255, 255, 255) 0%, rgb(240, 245, 255) 100%) !important;
  color: #1e293b;
  font-size: 1.1rem;
}

h1, h2, h3, h4 {
  font-family: 'Outfit', sans-serif;
  color: #0f172a;
}

h1 {
  font-size: 2.2rem;
  border-bottom: 3px solid #3b82f6;
  padding-bottom: 10px;
  margin-top: 0;
  margin-bottom: 30px;
}

h3 {
  font-size: 1.4rem;
  margin-top: 0;
}

h4 {
  font-size: 1.2rem;
  margin-top: 0;
}

/* Title Slide specific styling */
section.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: radial-gradient(circle at 30% 30%, #1e1b4b 0%, #0f172a 100%) !important;
  color: #f8fafc;
}

section.lead h1 {
  font-size: 2.8rem;
  border-bottom: none;
  color: #f1f5f9;
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  margin-bottom: 20px;
}

section.lead p {
  color: #94a3b8;
  font-size: 1.2rem;
}

.columns {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 2rem;
  align-items: center;
}

.columns-top {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 2rem;
  align-items: start;
}

.card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.warning-card {
  background: #fff1f2;
  border-left: 5px solid #f43f5e;
  border-radius: 4px 12px 12px 4px;
  padding: 18px 24px;
  margin: 15px 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
}

.warning-card h4 {
  margin: 0 0 10px 0;
  color: #be123c;
  font-weight: 600;
}

.warning-card ul {
  margin: 0;
  padding-left: 20px;
}

.goal-card {
  background: #f0fdf4;
  border-left: 5px solid #22c55e;
  border-radius: 4px 12px 12px 4px;
  padding: 18px 24px;
  margin: 15px 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
}

.goal-card h4 {
  margin: 0 0 10px 0;
  color: #15803d;
  font-weight: 600;
}

.goal-card ul {
  margin: 0;
  padding-left: 20px;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.grid-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.03);
  font-size: 0.9rem;
}

.grid-card h4 {
  margin: 0 0 8px 0;
  color: #3b82f6;
  font-size: 1.1rem;
}

.flow-container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: rgba(241, 245, 249, 0.8);
  border-radius: 12px;
  padding: 15px;
  margin: 20px 0;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.flow-step {
  background: #ffffff;
  padding: 10px 15px;
  border-radius: 8px;
  font-weight: 600;
  border: 1px solid #cbd5e1;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  font-size: 0.9rem;
}

.flow-step.important {
  background: #3b82f6;
  color: white;
  border-color: #2563eb;
}

.flow-arrow {
  font-size: 1.5rem;
  color: #64748b;
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

th {
  background-color: #3b82f6 !important;
  color: white !important;
  font-weight: 600;
  padding: 12px;
}

td {
  padding: 10px 12px;
  border-bottom: 1px solid #e2e8f0;
  background-color: rgba(255, 255, 255, 0.6);
}

tr:last-child td {
  border-bottom: none;
}

footer {
  font-size: 0.8rem;
  color: #64748b;
}
</style>

<!-- _class: lead -->

# Reinforcement Learning Enhanced LRU Cache Replacement Policy

Implementation and Evaluation Study

---

# Motivation

The cache replacement problem aims to maximize hit rates within a constrained memory size.

<div class="warning-card">
  <h4>Limitations of Traditional LRU</h4>
  <ul>
    <li><strong>Vulnerability to Cache Pollution:</strong> Non-reused scans evict active blocks.</li>
    <li><strong>Thrashing Failure:</strong> 0% hit rate in loops exceeding cache size (N+1).</li>
    <li><strong>Static Design:</strong> Cannot adapt to dynamically shifting access workloads.</li>
  </ul>
</div>

---

# Objective

We aim to introduce intelligent adaptability to the classic Least Recently Used (LRU) policy.

<div class="goal-card">
  <h4>Core Objective</h4>
  <p><strong>Goal:</strong> Add a lightweight Reinforcement Learning (RL) layer on top of LRU.</p>
  <ul>
    <li>Learn the optimal eviction strategy per workload dynamically.</li>
    <li>Decide whether to evict the LRU candidate or give it a "second chance" (keeping it).</li>
  </ul>
</div>

---

# Implementation Architecture

We integrate the RL decision engine seamlessly into the cache eviction loop.

<div class="flow-container">
  <div class="flow-step">Cache Request</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">LRU Candidate Selection</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">RL Agent</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step important">EVICT / KEEP Decision</div>
</div>

**Core Components:**
- **Cache Simulator:** Tracks state transitions and maintains associativity.
- **LRU Policy:** Provides the baseline metric and baseline fallback strategy.
- **Q-Learning Agent:** Evaluates candidate states and decides the optimal action.

---

# LRU vs RL-LRU Comparison

The key difference lies in the flexibility of the eviction decision process.

<div class="columns-top">
<div class="card" style="height: 100%;">
  <h3>Standard LRU</h3>
  <ul>
    <li>Directly and blindly evicts the least recently used block.</li>
    <li>Rigid and inflexible; fails to adapt to patterns like cyclic or scan workloads.</li>
  </ul>
</div>
<div class="card" style="border-color: #3b82f6; background: #eff6ff; height: 100%;">
  <h3>RL-LRU</h3>
  <ul>
    <li>LRU selects the candidate for eviction.</li>
    <li>RL agent decides the eviction action based on learned patterns (<code>EVICT</code> or <code>KEEP</code>).</li>
  </ul>
</div>
</div>

---

# Markov Decision Process (MDP) Basics

Before formulating our RL approach, we define the cache environment as a standard MDP.

<div class="grid-4" style="margin: 20px 0 30px 0;">
<div class="grid-card">
  <h4>State (S)</h4>
  The current situation or context of the cache block environment.
</div>
<div class="grid-card">
  <h4>Action (A)</h4>
  The choices available to the agent (evict vs keep).
</div>
<div class="grid-card">
  <h4>Reward (R)</h4>
  Feedback signal indicating successful caching decisions.
</div>
<div class="grid-card">
  <h4>Policy (π)</h4>
  The strategy mapping states to the optimal eviction action.
</div>
</div>

The agent's goal is to learn a policy (π) that maximizes cumulative future rewards.

---

# RL Formulation

We framed the cache eviction decision as a compact Markov Decision Process (MDP).

<div class="columns-top">
<div class="card" style="height: 100%;">
  <h3>State Space</h3>
  <p><code>(frequency_bucket, recent_hit)</code></p>
  <ul>
    <li>Compact representation of the LRU candidate block.</li>
    <li>Prevents state-space explosion and speeds up training.</li>
  </ul>
</div>
<div class="card" style="height: 100%;">
  <h3>Action Space</h3>
  <ul>
    <li><strong>EVICT:</strong> Perform standard LRU eviction.</li>
    <li><strong>KEEP:</strong> Second-chance protection (move candidate to MRU, evaluate next-oldest).</li>
  </ul>
</div>
</div>

---

# Eviction Decision Flow (Next-Attempt / Second-Chance)

To protect cache capacity, the agent acts as an adaptive filter within the eviction loop, implementing a Next-Attempt strategy.

<div class="columns-top">
<div class="card" style="height: 100%;">
  <h3>1. Candidate Evaluation</h3>
  <ul>
    <li>Cache is full; LRU candidate <code>C</code> is selected.</li>
    <li>State <code>S = (freq_bucket, recent_hit)</code> is built for <code>C</code>.</li>
    <li>RL agent chooses action: <code>EVICT</code> or <code>KEEP</code>.</li>
  </ul>
</div>
<div class="card" style="height: 100%; border-color: #10b981; background: #f0fdf4;">
  <h3>2. EVICT Action</h3>
  <ul>
    <li>Evict candidate <code>C</code> from cache.</li>
    <li>Insert <code>C</code>'s metadata into the Ghost Cache.</li>
    <li>Allocate space and insert the incoming block.</li>
  </ul>
</div>
<div class="card" style="height: 100%; border-color: #3b82f6; background: #eff6ff;">
  <h3>3. KEEP Action (Next-Attempt)</h3>
  <ul>
    <li>Move candidate <code>C</code> to MRU position (giving it a <strong>second chance</strong>).</li>
    <li>Select next-oldest block <code>V</code> as the <strong>next-attempt</strong> candidate.</li>
    <li>Evict <code>V</code> directly to maintain strict cache size bounds.</li>
  </ul>
</div>
</div>

<p style="font-size: 0.85rem; color: #64748b; margin-top: 15px; text-align: center;">
  <strong>Next-Attempt Concept:</strong> Analogous to Clock/Second-Chance Page Replacement. Instead of using static hardware reference bits, the decision to grant a second chance is made dynamically by the Q-learning agent.
</p>

---

# Q-Learning Implementation Details

Our RL agent utilizes Tabular Q-Learning to learn the optimal policy over a compact state space.

<div class="columns-top">
  <div>
    <div class="card" style="margin-bottom: 15px;">
      <h4>State Discretization (6 States)</h4>
      <p style="font-size: 0.85rem; margin: 0;">
        • <strong>Frequency Bucket:</strong> Low (≤1), Med (2-3), High (>3)<br>
        • <strong>Recent Hit Flag:</strong> Binary (0 or 1)<br>
        Resulting in a tiny 6x2 Q-table with minimal latency/overhead.
      </p>
    </div>
    <div class="card">
      <h4>ϵ-Greedy Strategy</h4>
      <p style="font-size: 0.85rem; margin: 0;">Balances exploration (random actions with <code>ϵ = 0.1</code>) and exploitation (choosing highest Q-value action).</p>
    </div>
  </div>
  <div class="card" style="height: 100%;">
    <h4>TD Bootstrapping for Delayed Rewards</h4>
    <p style="font-size: 0.85rem; margin-bottom: 10px;">Updates use the standard Bellman equation, but bootstrap the next state $S'$ using the <em>current</em> eviction candidate's state:</p>
    <code style="display: block; font-size: 0.75rem; background: #f1f5f9; padding: 10px; border-radius: 6px; margin: 10px 0;">Q(s,a) ← Q(s,a) + α [ r + γ max Q(s',a') - Q(s,a) ]</code>
    <p style="font-size: 0.8rem; color: #64748b; margin-top: 10px;">If no candidate is active (cache not full), the update self-bootstraps using $S' = S$.</p>
  </div>
</div>

---

# The Reward Problem

Immediate feedback fails in caching environments due to delayed reuse patterns.

<div class="columns-top">
  <div>
    <p><strong>The Core Challenge:</strong> Eviction quality can only be determined by future access patterns, not immediate hits or misses.</p>
    <p style="color: #64748b; font-size: 0.9rem; margin-top: 15px;">Immediate reward loops can train the agent to make bad evictions that cause future misses.</p>
  </div>
  <div class="card" style="border-left: 4px solid #ef4444; background: #fff5f5;">
    <h4 style="color: #c53030; margin-top: 0;">Flawed Immediate Reward Loop</h4>
    <ol style="font-size: 0.85rem; margin-bottom: 0;">
      <li>Agent evicts block <strong>A</strong>.</li>
      <li>Next request is <strong>B</strong> (causes a hit/miss elsewhere).</li>
      <li>Agent gets <code>+1</code> reward for immediate successful request.</li>
      <li>Shortly after, block <strong>A</strong> is requested → <strong>MISS!</strong></li>
    </ol>
  </div>
</div>

---

# Proposed Solution: Ghost Cache

We delay rewards using a bounded history queue (Ghost Cache) sized at <code>2 * Cache Size</code>.

<div class="columns-top">
  <div>
    <p><strong>Mechanism:</strong> A FIFO queue storing metadata (<code>Block</code>, <code>State</code>, <code>Action</code>) of recently evicted blocks.</p>
    <p style="color: #64748b; font-size: 0.9rem; margin-top: 15px;">Allows accurate feedback attribution based on whether the evicted block is requested again soon, incurring zero data storage overhead.</p>
  </div>
  <div>
    <div class="card" style="border-left: 4px solid #ef4444; background: #fef2f2; margin-bottom: 10px; padding: 15px;">
      <h4 style="color: #991b1b; margin: 0 0 5px 0;">Reused Block → Near Miss Penalty (-1)</h4>
      <p style="font-size: 0.85rem; margin: 0;">Block requested while in ghost cache. Eviction was premature. Triggers immediate update.</p>
    </div>
    <div class="card" style="border-left: 4px solid #22c55e; background: #f0fdf4; padding: 15px;">
      <h4 style="color: #166534; margin: 0 0 5px 0;">Expired Block → Good Eviction Reward (+1)</h4>
      <p style="font-size: 0.85rem; margin: 0;">Block pushed out of ghost cache queue without any request. Eviction was correct.</p>
    </div>
  </div>
</div>

---

# Evaluation Workloads

We evaluated the system using five distinct workload dimensions to test robustness.

<div class="columns">
  <div>
    <p>Each workload targets a specific caching behavior, evaluating stability, adaptability, and resilience to cache pollution.</p>
  </div>
  <div>
    <table>
      <thead>
        <tr>
          <th>Workload</th>
          <th>Evaluation Purpose</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Stable Working Set</strong></td>
          <td>Baseline hit rate stability</td>
        </tr>
        <tr>
          <td><strong>Cache+1 Loop</strong></td>
          <td>Severe LRU thrashing weakness</td>
        </tr>
        <tr>
          <td><strong>Hot Set + Scan</strong></td>
          <td>Pollution resistance (scans)</td>
        </tr>
        <tr>
          <td><strong>Zipfian</strong></td>
          <td>Highly skewed popularity distribution</td>
        </tr>
        <tr>
          <td><strong>Phase Shift</strong></td>
          <td>Dynamic adaptiveness over time</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

---

# Evaluation Results (Cache Size: 4)

RL-LRU delivers dramatic gains in thrashing scenarios while remaining safe elsewhere.

<div class="columns" style="grid-template-columns: 1.3fr 1fr;">
  <div>
    <table>
      <thead>
        <tr>
          <th>Workload</th>
          <th>LRU</th>
          <th>RL-LRU</th>
          <th>Δ Hit Rate</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Stable Working Set</td>
          <td>95.0%</td>
          <td>95.0%</td>
          <td>0.0%</td>
        </tr>
        <tr>
          <td>Cache+1 Loop</td>
          <td>0.0%</td>
          <td>28.0%</td>
          <td><strong style="color: #22c55e;">+28.0%</strong></td>
        </tr>
        <tr>
          <td>Hot Set + Scan</td>
          <td>72.0%</td>
          <td>72.0%</td>
          <td>0.0%</td>
        </tr>
        <tr>
          <td>Zipfian</td>
          <td>63.5%</td>
          <td>59.5%</td>
          <td><strong style="color: #ef4444;">-4.0%</strong></td>
        </tr>
        <tr>
          <td>Phase Shift</td>
          <td>90.0%</td>
          <td>90.0%</td>
          <td>0.0%</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="card" style="font-size: 0.85rem; padding: 15px;">
    <h4 style="margin-bottom: 10px;">Key Takeaways</h4>
    <ul>
      <li><strong>Loop Bypassing:</strong> Captures +28% gains under severe thrashing loops.</li>
      <li><strong>Zipfian Penalty:</strong> Slightly underperforms (-4.0%) due to learning delays in high-entropy states.</li>
      <li><strong>Safe Guardrails:</strong> Reverts to standard LRU performance in baseline workloads.</li>
    </ul>
  </div>
</div>

---

# Hit Rate vs Workload

Comparison of hit rates across different workloads with a cache size of 4.

<div class="columns" style="grid-template-columns: 1.2fr 1fr;">
  <div>
    <img src="../plots/figures/hit_rate_vs_workload.png" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />
  </div>
  <div class="card" style="font-size: 0.9rem;">
    <h3>Key Insights</h3>
    <ul>
      <li><strong>Thrashing Overcome:</strong> RL-LRU successfully avoids complete thrashing (0% hit rate) in Cache+1 loops.</li>
      <li><strong>Robustness:</strong> It retains full baseline performance in stable and shifting environments.</li>
      <li><strong>Safe Learning:</strong> The agent learns to bypass eviction without causing collateral damage.</li>
    </ul>
  </div>
</div>

---

# Hit Rate vs Cache Size

Hit rate progression as cache capacity scales from 2 to 8 blocks.

<div class="columns" style="grid-template-columns: 1.2fr 1fr;">
  <div>
    <img src="../plots/figures/hit_rate_vs_cache_size.png" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />
  </div>
  <div class="card" style="font-size: 0.9rem;">
    <h3>Key Insights</h3>
    <ul>
      <li><strong>Critical Value:</strong> The largest improvements occur at smaller cache sizes, where eviction choices are most crucial.</li>
      <li><strong>Natural Convergence:</strong> As capacity increases, LRU naturally hits more frequently, narrowing the performance gap.</li>
    </ul>
  </div>
</div>

---

# Delta Comparison

Performance delta between RL-LRU and standard LRU.

<div class="columns" style="grid-template-columns: 1.2fr 1fr;">
  <div>
    <img src="../plots/figures/delta_hit_rate.png" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />
  </div>
  <div class="card" style="font-size: 0.9rem;">
    <h3>Key Insights</h3>
    <ul>
      <li><strong>Positive Delta:</strong> Confirms that the second-chance KEEP action successfully breaks strict LRU loops.</li>
      <li><strong>Zipfian Distribution:</strong> Highlight the difficulty of learning from noisy delayed rewards in randomized access sequences.</li>
    </ul>
  </div>
</div>

---

# Future Work

Our next steps to build on these findings:

1. **State Space Expansion:**
   Incorporate Reuse Distance approximations to capture deeper temporal patterns.

2. **Real Memory Traces:**
   Evaluate performance on real-world SPEC CPU and database access traces.

3. **Advanced Paradigms:**
   Explore Contextual Bandits and Deep Q-Networks (DQN) for complex states.
