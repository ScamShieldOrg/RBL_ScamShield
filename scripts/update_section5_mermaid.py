import re

with open('c:/Users/USER/RBL_ScamShield/docs/08_UML_STATE_DIAGRAMS_REPORT4.md', 'r', encoding='utf-8') as f:
    text = f.read()

sec5_mermaid = '''### 5.3. Sơ Đồ Trạng Thái Mermaid (Black & White, Straight Lines)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000'}, 'flowchart': {'curve': 'linear'}}}%%
flowchart TD
    Start((Start)) --> SUB["Submission Pending Review:<br/>PENDING"]
    
    SUB -->|"Assign Compliance Officer"| REV["Under Review:<br/>ANALYZING"]
    
    REV -->|"False Credentials or Invalid Claims"| REJ["Rejected:<br/>REJECTED"]
    REJ --> End1((End))
    
    REV -->|"Documents Incomplete"| NMI["Needs Revision:<br/>NEEDS_REVISION"]
    NMI -->|"Supplementary Proof Uploaded"| REV
    NMI -->|"Grace Period Expired (7 Days)"| REJ
    
    REV -->|"Ownership & Technical Proof Verified"| VER["Verified Asset:<br/>VERIFIED"]
    
    VER -->|"Approved by Administrator"| APP["Active Whitelist:<br/>APPROVED_ACTIVE"]
    APP --> End2((End))
    
    APP -->|"Domain Hijacked / SIM Swap / Closure"| RVK["Revoked:<br/>REVOKED"]
    RVK --> End3((End))
    
    VER -->|"Blacklist Conflict Detected"| ESC["Escalated Conflict:<br/>ESCALATED_CONFLICT"]
    ESC --> End4((End))

    classDef default fill:#ffffff,stroke:#333333,stroke-width:1.5px,color:#000000;
    classDef circleNode fill:#ffffff,stroke:#333333,stroke-width:1.5px,color:#000000;
    class Start,End1,End2,End3,End4 circleNode;
```'''

text = re.sub(r'### 5\.3\. Sơ Đồ Trạng Thái Mermaid.*?(?=### 5\.4\.)', sec5_mermaid + '\n\n', text, flags=re.DOTALL)

with open('c:/Users/USER/RBL_ScamShield/docs/08_UML_STATE_DIAGRAMS_REPORT4.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Section 5.3 successfully!")
