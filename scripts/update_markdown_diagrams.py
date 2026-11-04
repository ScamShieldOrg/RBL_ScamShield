import re

with open('c:/Users/USER/RBL_ScamShield/docs/08_UML_STATE_DIAGRAMS_REPORT4.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Section 2.3 (Scam Report Management)
sec2_mermaid = '''### 2.3. Sơ Đồ Trạng Thái Mermaid (Black & White, Straight Lines)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000'}, 'flowchart': {'curve': 'linear'}}}%%
stateDiagram-v2
    direction TB

    [*] --> SubmissionPendingReview: User submits scam report with evidence
    SubmissionPendingReview --> UnderReview: Auto-triage dispatcher assigns moderator
    
    UnderReview --> Rejected: [False alarm / Malformed IOC / Invalid evidence] Dismiss report
    UnderReview --> VerifiedReport: [Threat authenticity and evidence verified] Verify report
    
    VerifiedReport --> DuplicateMerged: [Identical IOC in active investigation]
    VerifiedReport --> CandidateCreated: [Zero-day or unique threat IOC]
    
    CandidateCreated --> Confirmed: [Approved by moderator or council >= 0.70]
    CandidateCreated --> EscalatedLocked: [Target conflicts with partner whitelist]
    
    DuplicateMerged --> [*]: Merged into parent report
    Confirmed --> [*]: Promoted to global blacklist
    Rejected --> [*]: Rejection audit logged
    EscalatedLocked --> [*]: Auto-locked for admin adjudication
```'''

# 2. Update Section 3.3 (Dispute & Appeal Management)
sec3_mermaid = '''### 3.3. Sơ Đồ Trạng Thái Mermaid (Black & White, Straight Lines)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000'}, 'flowchart': {'curve': 'linear'}}}%%
stateDiagram-v2
    direction TB

    [*] --> DisputePendingReview: Contested indicator & ownership proof submitted
    DisputePendingReview --> UnderReview: Dispute compliance officer assigned
    
    UnderReview --> DisputeRejected: [Counter-evidence invalid or malice persists] Reject appeal
    UnderReview --> VerifiedAppeal: [Ownership authenticity and benign status confirmed] Verify claim
    UnderReview --> NeedsMoreInfo: [Documentation deficient / Illegible proof uploaded]
    
    NeedsMoreInfo --> UnderReview: [Supplementary proof uploaded within 7 days]
    NeedsMoreInfo --> DisputeRejected: [7-day grace period expired without response]
    
    VerifiedAppeal --> DisputeUpheld: [Retraction decision approved by officer]
    DisputeUpheld --> IndicatorRetracted: [Execute delisting from active blacklist]
    
    IndicatorRetracted --> [*]: Removed from active blacklist
    DisputeRejected --> [*]: Retained on active blacklist
```'''

# 3. Update Section 4.3 (Scam Check Engine)
sec4_mermaid = '''### 4.3. Sơ Đồ Trạng Thái Mermaid (Black & White, Straight Lines)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000'}, 'flowchart': {'curve': 'linear'}}}%%
stateDiagram-v2
    direction TB

    [*] --> RequestReceived: Client submits scan request (POST /api/v1/scan)
    RequestReceived --> RequestRejected: [Malformed payload OR Rate limit / Quota exceeded]
    RequestReceived --> InputPreprocessed: [Payload valid & user quota available]
    
    InputPreprocessed --> ScreeningAnalysis: Dispatched to hybrid two-tier pipeline
    
    ScreeningAnalysis --> DeterministicMatch: [Exact match in cache / verified lists]
    ScreeningAnalysis --> EdgeTier1Resolved: [Edge ViSoBERT high confidence: P <= 0.10 or P >= 0.90]
    ScreeningAnalysis --> CouncilDeliberating: [Ambiguity band: 0.10 < P < 0.90 OR UTS #39 evasion]
    ScreeningAnalysis --> HeuristicFallback: [Inference timeout > 3000ms OR Circuit breaker open]
    
    DeterministicMatch --> LowRisk: [Whitelist match or benign pattern]
    DeterministicMatch --> ScamRisk: [Blacklist match]
    
    EdgeTier1Resolved --> LowRisk: [Calibrated P <= 0.10]
    EdgeTier1Resolved --> ScamRisk: [Calibrated P >= 0.90]
    
    CouncilDeliberating --> LowRisk: [Consensus score < 0.40]
    CouncilDeliberating --> ScamRisk: [Consensus score >= 0.60]
    CouncilDeliberating --> UncertainReview: [Ambiguity preserved: 0.40 <= P < 0.60]
    
    LowRisk --> [*]: Persist scan history (LOW_RISK)
    ScamRisk --> [*]: Persist scan history (SCAM_RISK)
    UncertainReview --> [*]: Persist scan history (UNKNOWN)
    RequestRejected --> [*]: Return 400/429 error
    HeuristicFallback --> [*]: Deliver fallback advisory
```'''

# Replace Section 2.3
text = re.sub(r'### 2\.3\. Sơ Đồ Trạng Thái Mermaid.*?(?=### 2\.4\.)', sec2_mermaid + '\n\n', text, flags=re.DOTALL)
# Replace Section 3.3
text = re.sub(r'### 3\.3\. Sơ Đồ Trạng Thái Mermaid.*?(?=### 3\.4\.)', sec3_mermaid + '\n\n', text, flags=re.DOTALL)
# Replace Section 4.3
text = re.sub(r'### 4\.3\. Sơ Đồ Trạng Thái Mermaid.*?(?=### 4\.4\.)', sec4_mermaid + '\n\n', text, flags=re.DOTALL)

with open('c:/Users/USER/RBL_ScamShield/docs/08_UML_STATE_DIAGRAMS_REPORT4.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated 08_UML_STATE_DIAGRAMS_REPORT4.md!")
