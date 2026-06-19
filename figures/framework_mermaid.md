# Token Service Cross-Period Pricing & Demand Response Game Framework

```mermaid
---
config:
  layout: elk
  flowchart:
    curve: basis
    padding: 16
    nodeSpacing: 60
    rankSpacing: 80
---
flowchart TB
  %% Styles
  classDef title fill:#1B3A5C,color:#fff,fontSize:16px,fontWeight:bold,stroke:#1B3A5C,strokeWidth:2px,rx:8
  classDef userHeader fill:#007C7C,color:#fff,fontSize:13px,fontWeight:bold,stroke:#007C7C,strokeWidth:2px,rx:6
  classDef platformHeader fill:#E07A2B,color:#fff,fontSize:13px,fontWeight:bold,stroke:#E07A2B,strokeWidth:2px,rx:6
  classDef providerHeader fill:#2D8B4E,color:#fff,fontSize:13px,fontWeight:bold,stroke:#2D8B4E,strokeWidth:2px,rx:6
  classDef userBox fill:#E8F4F4,color:#333,stroke:#007C7C,strokeWidth:2px,rx:6
  classDef platformBox fill:#FFF3E8,color:#333,stroke:#E07A2B,strokeWidth:2px,rx:6
  classDef providerBox fill:#E8F4EC,color:#333,stroke:#2D8B4E,strokeWidth:2px,rx:6
  classDef aggDemand fill:#007C7C,color:#fff,fontWeight:bold,stroke:#007C7C,strokeWidth:2px,rx:6
  classDef algoBg fill:#D6E4F0,color:#1B3A5C,stroke:#1B3A5C,strokeWidth:2px,rx:8
  classDef algoBox fill:#fff,color:#333,stroke:#1B3A5C,strokeWidth:2px,rx:6
  classDef results fill:#1B3A5C,color:#fff,stroke:#1B3A5C,strokeWidth:2px,rx:6
  classDef edgeLabel fill:#fff,color:inherit,stroke:none

  %% Title
  Title["Token Service Cross-Period Pricing & Demand Response Game Framework"]
  class Title title

  %% ── Column Headers ──
  UserH["User Side"]
  PlatformH["Platform / Broker Side"]
  ProviderH["Provider / Supply Side"]
  class UserH userHeader
  class PlatformH platformHeader
  class ProviderH providerHeader

  %% ── User Side ──
  subgraph UserGroup[""]
    direction TB
    Rigid["<b>Rigid Users</b><br/>R₁ = R̄₁ · σ(β(vᵣ − p₁))<br/>Price-sensitive demand"]
    Elastic["<b>Elastic Users (Logit)</b><br/>F₁ = F̄ · g · m · s₁<br/>s₁ = exp(z₁) / Σ exp(z₁)<br/>Cross-period migration"]
    Agg["<b>Aggregate Demand</b><br/>D₁ = R₁ + F₁"]
  end
  class Rigid,Elastic userBox
  class Agg aggDemand

  %% ── Platform Side ──
  subgraph PlatformGroup[""]
    direction TB
    Price["<b>Price Vector</b><br/>p = (p₁,...,pₜ) ∈ [p̲, p̄]ᵀ<br/>Fixed mean: Σpₜ/T = p̄"]
    Stackelberg["<b>Stackelberg Leader</b><br/>Platform posts p before users respond<br/>First-mover advantage"]
    Profit["<b>Profit Maximization</b><br/>Π(p) = h Σ pₜ Dₜ q(uₜ) − h Σ w Dₜ<br/>− h Σ cᵣ(R̄ₜ−Rₜ) − h Σ cₙ[1−q(uₜ)]Rₜ"]
    Strategy["<b>Constraints &amp; Strategy</b><br/>Bounded Mean Projection (λ bisection, KKT)<br/>3 strategies: Uniform / Myopic / QoS-aware"]
  end
  class Price,Stackelberg,Profit,Strategy platformBox

  %% ── Provider Side ──
  subgraph ProviderGroup[""]
    direction TB
    GPU["<b>GPU Inference Cluster</b><br/>Capacity G<br/>vLLM / Ollama · RTX 4090<br/>Qwen2.5-0.5B/3B"]
    Util["<b>Utilization</b><br/>uₜ = Dₜ / G"]
    QoS["<b>QoS Degradation Proxy</b><br/>q(uₜ) = 1 (uₜ ≤ ū)<br/>q(uₜ) = exp[−κ(uₜ−ū)²] (uₜ &gt; ū)"]
    Empirical["<b>Empirical Validation</b><br/>TTFT · TPOT · Throughput · SLA<br/>Heuristic QoS mapping"]
  end
  class GPU,Util,QoS,Empirical providerBox

  %% ── Algorithm Layer ──
  AlgoBg["Algorithm &amp; Game Layer"]
  class AlgoBg algoBg

  subgraph AlgoGroup[""]
    direction TB
    Game["<b>Game Structure</b><br/>• Stackelberg Leader–Follower<br/>• Congestion externality<br/>• Welfare decomposition"]
    Opt["<b>Numerical Optimization</b><br/>• Multi-start SLSQP<br/>• Bounded Mean Projection<br/>• Scalability T:8→64"]
  end
  class Game,Opt algoBox

  %% ── Results ──
  Results["Key Results: QoS-aware vs Myopic +12.53% · QoS floor 0.6632 → 0.9918"]
  class Results results

  %% ── Connections ──
  PlatformH -.->|"Price Signal pₜ"| UserH
  Agg -->|"Demand Dₜ"| Price
  PlatformH -->|"Load / Scheduling"| ProviderH
  Util -.->|"QoS q(uₜ) / uₜ"| Price
  UserH -.->|"Congestion Externality"| ProviderH

  UserGroup --> AlgoBg
  PlatformGroup --> AlgoBg
  ProviderGroup --> AlgoBg
  AlgoBg --> Results
```
