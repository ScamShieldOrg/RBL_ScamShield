# -*- coding: utf-8 -*-
"""
Generate the complete ScamShield Research Proposal in docx format
following RESEARCH PROPOSAL TEMPLATE.docx guidelines.
"""
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def format_run(run, font_name="Times New Roman", size_pt=11, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15, bold=False, italic=False, size_pt=11):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        format_run(r, font_name="Times New Roman", size_pt=size_pt, bold=bold, italic=italic)
    return p

def add_heading_p(doc, text, level=1, space_before=12, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    size = 12 if level == 1 else 11
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=size, bold=True)
    return p

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_box_table_borders(table, color="000000", sz="6", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="4" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_proposal():
    doc = docx.Document()
    
    # Page setup: A4, 1-inch margins
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)

    # Document Header Title
    p_top = add_p(doc, "RESEARCH PROPOSAL", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14, bold=True, size_pt=14)

    # ----------------------------------------------------
    # Table 0: Metadata Table
    # ----------------------------------------------------
    t0 = doc.add_table(rows=5, cols=2)
    t0.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_box_table_borders(t0, color="000000", sz="6")
    
    col_widths = [Inches(1.8), Inches(4.47)]
    for row in t0.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # Row 0: Title
    t0.rows[0].cells[0].paragraphs[0].text = ""
    r = t0.rows[0].cells[0].paragraphs[0].add_run("Research title\n(English)")
    format_run(r, bold=True, size_pt=11)
    
    t0.rows[0].cells[1].paragraphs[0].text = ""
    r = t0.rows[0].cells[1].paragraphs[0].add_run("ScamShield-VN: Evidence-Driven Two-Tier Architecture for Vietnamese Scam and Phishing Detection")
    format_run(r, bold=True, size_pt=11)

    # Row 1: Sub-committee
    t0.rows[1].cells[0].paragraphs[0].text = ""
    r = t0.rows[1].cells[0].paragraphs[0].add_run("Sub-committee")
    format_run(r, bold=True, size_pt=11)
    
    t0.rows[1].cells[1].paragraphs[0].text = ""
    r = t0.rows[1].cells[1].paragraphs[0].add_run("Information Technology")
    format_run(r, size_pt=11)

    # Row 2: Group name
    t0.rows[2].cells[0].paragraphs[0].text = ""
    r = t0.rows[2].cells[0].paragraphs[0].add_run("Group name")
    format_run(r, bold=True, size_pt=11)
    
    t0.rows[2].cells[1].paragraphs[0].text = ""
    r = t0.rows[2].cells[1].paragraphs[0].add_run("ScamShield")
    format_run(r, bold=True, size_pt=11)

    # Row 3: Authors
    t0.rows[3].cells[0].paragraphs[0].text = ""
    r = t0.rows[3].cells[0].paragraphs[0].add_run("Authors")
    format_run(r, bold=True, size_pt=11)
    
    c_auth = t0.rows[3].cells[1]
    c_auth.paragraphs[0].text = ""
    authors_data = [
        ("1. Nguyen Minh Quang (Team Leader)", "Student ID: SE190820 | Email: nguyenminhquangnmqlamdong@gmail.com"),
        ("2. Nguyen Trung Hieu", "Student ID: SE190843 | Email: cristand2825@gmail.com"),
        ("3. Hoang Hai Phuc", "Student ID: SE190740 | Email: haiphuchoang2675@gmail.com"),
        ("4. Nguyen Quoc Huy", "Student ID: SE190794 | Email: nguyenhuy.se205@gmail.com")
    ]
    for i, (name, details) in enumerate(authors_data):
        p = c_auth.paragraphs[0] if i == 0 else c_auth.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_name = p.add_run(name + "\n")
        format_run(r_name, bold=True, size_pt=11)
        r_det = p.add_run(details)
        format_run(r_det, italic=True, size_pt=10)

    # Row 4: Mentor
    t0.rows[4].cells[0].paragraphs[0].text = ""
    r = t0.rows[4].cells[0].paragraphs[0].add_run("Mentor")
    format_run(r, bold=True, size_pt=11)
    
    c_men = t0.rows[4].cells[1]
    c_men.paragraphs[0].text = ""
    p = c_men.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_men_name = p.add_run("Ms. Le Thi Quynh Chi (ThS. Lê Thị Quỳnh Chi)\n")
    format_run(r_men_name, bold=True, size_pt=11)
    r_men_det = p.add_run("Email: chiltq6@fe.edu.vn | Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam")
    format_run(r_men_det, italic=True, size_pt=10)

    for row in t0.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    set_cell_shading(t0.rows[0].cells[0], "F5F5F5")
    set_cell_shading(t0.rows[1].cells[0], "F5F5F5")
    set_cell_shading(t0.rows[2].cells[0], "F5F5F5")
    set_cell_shading(t0.rows[3].cells[0], "F5F5F5")
    set_cell_shading(t0.rows[4].cells[0], "F5F5F5")

    add_p(doc, "", space_after=8)

    # ----------------------------------------------------
    # Abstract
    # ----------------------------------------------------
    add_heading_p(doc, "Abstract", level=1, space_before=10, space_after=4)
    abstract_text = (
        "Telecommunications fraud, smishing, and financial impersonation in Vietnam inflict severe economic damage, "
        "yet existing defenses suffer from an asymmetric error cost imbalance and intolerable alarm fatigue under solitary cloud detectors. "
        "We propose ScamShield-VN, an evidence-grounded two-tier architecture that couples an on-device edge screener with an adversarial "
        "three-agent forensic council. Tier 1 fine-tunes ViSoBERT under Cost-Sensitive Weighted Binary Cross-Entropy loss (α = 5.0) and "
        "ONNX INT8 quantization (98.42 MB, 70.7 ms median CPU latency). Across five independent training seeds, ViSoBERT achieved a five-run "
        "mean scam recall of 95.64% ± 2.04% and Macro-F1 of 94.51% ± 0.96%. On a locked frozen holdout of 267 messages (θ_scam = 0.90), "
        "ViSoBERT attained 96.00% scam recall (72/75; exact 95% Clopper-Pearson CI: [88.75%, 99.17%]) and a 4.17% false-positive rate (8/192), "
        "significantly outperforming solitary Gemini 3.5 Flash in paired correctness (exact McNemar p < 0.0001). To resolve ambiguous boundary samples, "
        "Tier 2 deploys a consolidated three-agent forensic council featuring an adversarial Public Defender agent that actively verifies authentic "
        "transactional syntax, eliminating false alarms (0.00% FPR) on legitimate banking OTPs and carrier service alerts. Governed by a confidence "
        "routing threshold (τ = 0.90), the cascaded system resolves 96.6% of telecommunications traffic locally at the edge, achieving 97.40% overall "
        "accuracy, 97.11% scam recall, and 267.5 ms average end-to-end latency at a marginal cloud cost of $0.0153 per 1,000 messages. "
        "This empirical framework resolves the accuracy-latency-cost trilemma for localized telecommunications fraud mitigation."
    )
    add_p(doc, abstract_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6)

    # Keywords
    p_kw = add_p(doc, space_before=2, space_after=12)
    r_kw_title = p_kw.add_run("Key words: ")
    format_run(r_kw_title, bold=True, size_pt=11)
    r_kw_body = p_kw.add_run("scam detection, phishing detection, cost-sensitive learning, Vietnamese NLP, edge AI, multi-agent consensus.")
    format_run(r_kw_body, italic=True, size_pt=11)

    # ----------------------------------------------------
    # 1. Introduction
    # ----------------------------------------------------
    add_heading_p(doc, "1. Introduction", level=1, space_before=14, space_after=4)

    # 1.1 Literature review
    add_heading_p(doc, "1.1. Literature review", level=2, space_before=8, space_after=4)
    lit_p1 = (
        "Telecommunications fraud, smishing (SMS phishing), and social engineering scams have evolved into pervasive threats globally "
        "and across Southeast Asia. In Vietnam, threat actors exploit sophisticated psychological manipulation and localized language variations, "
        "including internet slang, youth teencode, intentional diacritic omission, and phonetic substitutions, to bypass conventional carrier-grade "
        "keyword filters. To systematically contextualize this research, we review relevant scientific works across four foundational domains:"
    )
    add_p(doc, lit_p1)

    lit_p2 = (
        "1. Classical Machine Learning and Static Rule-Based Systems: Early anti-spam and anti-phishing systems relied heavily on shallow machine "
        "learning algorithms, such as Naive Bayes, Support Vector Machines (SVM), and Random Forests combined with TF-IDF n-gram vectors (Saeed 2023, "
        "Xie 2025). While these classifiers demonstrate acceptable baselines on formal Latin text, Xie (2025) demonstrated that their accuracy degrades "
        "precipitously when exposed to noisy, informal user-generated text. In Vietnamese telecommunications, static regex rules and keyword blacklists "
        "incur prohibitive human curation costs and fail against lexical obfuscation (e.g., substituting 'ngân hàng' with 'n9an h4n9' or zero-width delimiters)."
    )
    add_p(doc, lit_p2)

    lit_p3 = (
        "2. Pre-trained Language Models and Vietnamese NLP: The introduction of transformer-based architectures established new benchmarks in contextual "
        "threat representation. For Vietnamese, PhoBERT (Nguyen & Nguyen 2020) provided robust word-level embeddings. However, PhoBERT strictly requires "
        "an upstream morphological word segmenter (e.g., RDRSegmenter). In fraudulent telecommunications payloads, deliberate concatenations, informal slang, "
        "and typos cause word segmenters to fail catastrophically, inducing out-of-vocabulary token fragmentation. To overcome segmentation fragility, "
        "ViSoBERT (Nguyen et al. 2023) was pretrained on a 10.5 GB corpus of raw Vietnamese social media comments and informal chat using Byte-Pair Encoding (BPE), "
        "preserving morphological robustness on colloquial language. Subsequent studies applied contextual models to localized threats: Cam & Binh (2026) "
        "evaluated PhoBERT on the VNSED spam email dataset (86.47% accuracy), and Tuấn et al. (2023) examined multi-accent SMS classification. However, all "
        "existing Vietnamese transformer models are optimized under standard symmetric cross-entropy loss, ignoring the severe real-world asymmetry of threat costs."
    )
    add_p(doc, lit_p3)

    lit_p4 = (
        "3. Frontier Large Language Models and On-Device Edge Deployments: Generative Large Language Models (LLMs) such as GPT-4o, Claude, and Gemini have "
        "demonstrated remarkable zero-shot reasoning. In a comprehensive benchmark of SMS fraud, Zhou et al. (2026, FraudSMSWalker) revealed that while LLMs "
        "achieve fraud recall between 64.16% and 90.13%, their benign recall collapses to 12.81%–30.25%. Solitary cloud LLMs exhibit acute hyper-vigilance, "
        "misclassifying legitimate transactional alerts containing urgency words or authentication codes as scams, inducing severe 'Alarm Fatigue' "
        "(35.53% false alarm rate on Gemini 3.5 Flash). Furthermore, cloud LLM queries impose high latency (3–15 seconds per query) and recurring API costs, "
        "violating mobile edge privacy standards. Lightweight on-device models, such as distilled Small Language Models (SLMs) (Banda et al. 2026) and "
        "recurrent networks with cost-sensitive penalties (Phap et al. 2025), provide rapid local inference but lack multi-head attention to decode subtle fraud cues."
    )
    add_p(doc, lit_p4)

    lit_p5 = (
        "4. Multi-Agent Deliberation and Correlated Error Mitigation: LLM-as-a-judge frameworks and multi-agent deliberation systems (PoLL, Verga et al. 2024; "
        "ChatEval, Chan et al. 2024; MultiPhishGuard, arXiv:2505.23803) have shown that ensembling diverse model perspectives enhances reasoning robustness. "
        "However, theoretical analysis by Ladha (1992) and empirical investigations by Kim et al. (2025) demonstrate that frontier LLMs exhibit substantial "
        "correlated failure modes—frequently co-failing on the same deceptive boundary lures regardless of model family. Consequently, naive majority voting "
        "fails to eliminate false alarms on legitimate banking notifications. Multi-agent systems require an explicit, adversarial inductive bias—specifically "
        "a dedicated Public Defender agent tasked with scrutinizing counter-evidence and validating authentic banking syntaxes."
    )
    add_p(doc, lit_p5)

    lit_gap = (
        "Synthesis of Identified Research Gaps (GAPs):\n"
        "• GAP 1 (Tokenization & Linguistic Fragility): Conventional Vietnamese PLMs rely on word segmenters that fail on teencode, whereas robust subword models "
        "have not been tailored for real-time mobile smishing triage.\n"
        "• GAP 2 (Symmetric Loss Misalignment): Telecommunications security imposes deeply asymmetric error costs: a False Negative (missed fraud) leads to catastrophic "
        "financial theft, whereas a False Positive is a temporary inconvenience. Prior Vietnamese models universally optimize symmetric cross-entropy, causing unacceptable miss rates.\n"
        "• GAP 3 (Edge-Cloud Execution Dilemma): Existing systems bifurcate into heavy cloud LLMs with high latency and alarm fatigue, or rigid edge models lacking reasoning fallback.\n"
        "• GAP 4 (Correlated Consensus Failure): Multi-LLM ensembles lack adversarial counter-balancing mechanisms, resulting in correlated false alarms on authentic banking OTPs."
    )
    add_p(doc, lit_gap)

    # 1.2 The necessity of the research
    add_heading_p(doc, "1.2. The necessity of the research", level=2, space_before=8, space_after=4)
    nec_p1 = (
        "Telecommunications fraud in Vietnam has escalated into a national security and economic emergency. According to national cybersecurity reports, "
        "online and telecommunications fraud inflicted financial losses exceeding 18.9 trillion VND (approximately USD $744 million) in 2024 alone. Victims include "
        "vulnerable demographics such as students, gig workers, and the elderly who lack sophisticated digital threat awareness. Perpetrators systematically exploit "
        "Vietnamese linguistic nuances, deploying urgency triggers ('account locked within 2 hours'), counterfeit judicial summons (police/procuracy arrest warrants), "
        "and fraudulent biometric verification links disguised under the State Bank of Vietnam's Decision 2345/QĐ-NHNN."
    )
    add_p(doc, nec_p1)

    nec_p2 = (
        "Existing telecommunications filtering mechanisms are fundamentally inadequate. Telco keyword filters are bypassed instantly by changing letter accents or "
        "inserting numbers. Cloud AI services cannot scale to millions of messages due to API cost ($10–$30 per 1,000 requests) and privacy regulations (Vietnamese Decree 13/2023/ND-CP). "
        "Therefore, there is an urgent scientific and practical necessity to construct a localized, evidence-grounded, two-tier architecture that operates directly on "
        "consumer edge devices for instantaneous, private screening, while selectively escalating highly ambiguous lures to an adversarial multi-agent cloud council. "
        "This research establishes the first rigorous empirical evaluation of cost-sensitive edge ViSoBERT coupled with an adversarial Public Defender council for Vietnamese fraud triage."
    )
    add_p(doc, nec_p2)

    # 1.3 Feasibility of research
    add_heading_p(doc, "1.3. Feasibility of research", level=2, space_before=8, space_after=4)
    feas_intro = (
        "The proposed research is highly feasible, grounded in accessible open datasets, verified technical prototypes, and standard empirical methodologies:"
    )
    add_p(doc, feas_intro)

    feas_rq = (
        "+ Research Questions (RQs) and Hypotheses:\n"
        "• RQ1 (Edge Effectiveness & Operational Latency): Does an on-device ViSoBERT screener optimized under Cost-Sensitive Weighted Binary Cross-Entropy (α = 5.0) "
        "and ONNX INT8 quantization outperform symmetric baselines (PhoBERT-base, PhoBERT-large, FPT ViBERT) and solitary cloud LLMs in Scam Recall (target ≥ 95.0%) "
        "while maintaining sub-100ms CPU latency?\n"
        "  - H0: There is no significant difference in paired classification accuracy between ViSoBERT + WBCE and baseline models on the frozen holdout (p ≥ 0.05).\n"
        "  - H1: ViSoBERT + WBCE demonstrates a statistically significant improvement in paired classification performance (McNemar p < 0.05).\n"
        "• RQ2 (Multi-Agent Grounding & False Alarm Suppression): How effectively does a consolidated 3-Agent Forensic Council equipped with an adversarial Public Defender "
        "eliminate false alarms (target FPR = 0.00%) on legitimate banking OTPs and carrier notifications without degrading overall scam detection recall?\n"
        "• RQ3 (Two-Tier Cascaded Pareto Optimization): Does a confidence-routed cascaded framework (routing threshold τ = 0.90) successfully resolve ≥ 90% of routine "
        "traffic locally at the edge, achieving Pareto-optimal accuracy (≥ 97.0%), sub-300ms end-to-end latency, and marginal cloud API cost < $0.02 per 1,000 messages?"
    )
    add_p(doc, feas_rq)

    feas_design = (
        "+ Research Design: Controlled empirical investigation utilizing a two-tier cascaded architecture. Tier 1 deploys an edge-quantized ViSoBERT model trained with "
        "asymmetric loss penalties. Tier 2 integrates a heterogeneous 3-agent LLM council. Evaluation is conducted across 5 independent random training seeds (Seeds 42, 123, 456, 789, 1011) "
        "to ensure reproducibility and statistical power."
    )
    add_p(doc, feas_design)

    feas_sample = (
        "+ Sample Size and Population: The experimental population comprises a curated corpus of 2,664 authentic Vietnamese messages (1,918 benign messages, 746 verified scams). "
        "From this corpus, a locked Frozen Test Holdout (N = 267; 192 Ham, 75 Scam) is isolated using stratified sampling (random seed 42) and sealed against training or threshold tuning. "
        "A separate Hard Forensic Challenge Suite (N = 117; 98 adversarial scam lures, 19 genuine banking OTPs and carrier alerts) is established to rigorously stress-test boundary reasoning. "
        "A combined evaluation suite (N = 384) evaluates full two-tier cascaded performance. Annotation guidelines are documented, and 20% of the dataset is double-annotated, yielding "
        "an Inter-Annotator Agreement Cohen's Kappa κ = 0.88 (exceeding the standard 0.80 benchmark)."
    )
    add_p(doc, feas_sample)

    feas_sources = (
        "+ Data Sources: Data is collected from official and verified public repositories: the ChongLuaDao threat database, official cybersecurity bulletins from the National Cyber "
        "Security Center (NCSC Vietnam), Department of Cyber Security and High-Tech Crime Prevention (A05), verified press warning articles, and the VNSED corpus. All personal data is "
        "strictly anonymized via regex PII sanitizers (masking phone numbers, bank accounts, and personal names)."
    )
    add_p(doc, feas_sources)

    feas_budget = (
        "+ Budget and Funding: Experimental training and benchmarking utilize local student workstations (NVIDIA RTX GPUs) and open academic cloud platforms (Google Colab, Kaggle). "
        "Cloud LLM API calls are budgeted based on verified token counts: at an empirical routing rate of 3.4% cloud escalation, marginal API costs are $0.0153 per 1,000 queries. Total project "
        "compute expenditure is below $50, funded under FPT University Research-Based Learning Project Grant No. FA26SE079."
    )
    add_p(doc, feas_budget)

    feas_time = (
        "+ Timeframe: Structured across a 14-week lifecycle in 5 standard RBL phases:\n"
        "• Weeks 1–3 (RBL-1): Literature review, search logs, PRISMA screening, and PICO evidence mapping.\n"
        "• Weeks 4–5 (RBL-2): Proposal drafting, baseline pre-testing, and formal proposal defense.\n"
        "• Weeks 6–8 (RBL-3 & RBL-4a): Dataset curation, PII masking, ViSoBERT fine-tuning with WBCE loss, and ONNX quantization.\n"
        "• Weeks 9–11 (RBL-4b): Multi-agent council implementation, 5-seed benchmark evaluation, and exact McNemar testing.\n"
        "• Weeks 12–14 (RBL-5): End-to-end cascade deployment, manuscript drafting according to the JAIT template, and final capstone defense."
    )
    add_p(doc, feas_time)

    feas_risks = (
        "+ Potential Challenges and Risk Mitigations:\n"
        "• API Rate Limits & Model Obsolescence: Mitigated by a Decoupled Model Registry with Standby Priority Chains and an autonomous Circuit Breaker (3-failure threshold, 300s cooldown).\n"
        "• Teencode Obfuscation: Mitigated by ViSoBERT's BPE subword tokenizer and Unicode UTS #39 Confusable Skeleton pre-normalization.\n"
        "• Alarm Fatigue on Banking OTPs: Mitigated by the Public Defender specialist endowed with an explicit veto penalty (δ = 0.25) when authentic banking syntax is verified.\n"
        "• Mobile Data Privacy: Mitigated by local edge execution resolving >96% of traffic entirely on-device, combined with PII redaction on cloud referrals."
    )
    add_p(doc, feas_risks)

    # ----------------------------------------------------
    # 2. Research objectives
    # ----------------------------------------------------
    add_heading_p(doc, "2. Research objectives", level=1, space_before=14, space_after=4)
    obj_intro = "The primary objective of this project is to develop and empirically validate ScamShield-VN, an evidence-grounded, two-tier scam detection framework for Vietnamese telecommunications. Specific research objectives include:"
    add_p(doc, obj_intro)
    
    objectives_list = [
        "1. Dataset Curation and Standardization: Construct and double-annotate a verified corpus of 2,664 Vietnamese telecommunications messages, establishing a sealed frozen benchmark holdout (N = 267) and a hard forensic challenge suite (N = 117) with Inter-Annotator Agreement Cohen's Kappa κ ≥ 0.85.",
        "2. Cost-Sensitive Edge Screener Development: Formulate and train ViSoBERT under Cost-Sensitive Weighted Binary Cross-Entropy loss (L_WBCE, α = 5.0) and deploy dynamic ONNX INT8 quantization, achieving an edge Scam Recall ≥ 95.0% with CPU inference latency < 100 ms.",
        "3. Adversarial Multi-Agent Forensic Council Design: Architect a consolidated 3-agent multi-LLM forensic council (Cyber Threat, Psycholinguistics, Public Defender) featuring Borda-weighted voting, Qualified Security Veto, and an adversarial Public Defender to eliminate false alarms (0.00% FPR) on banking OTPs.",
        "4. Two-Tier Cascaded System Routing and Optimization: Implement a confidence-routed decision engine (threshold τ = 0.90) offloading ≥ 90% of routine traffic to local edge execution, achieving an overall cascaded accuracy ≥ 97.0% at marginal cloud cost < $0.02 per 1,000 queries.",
        "5. Rigorous Empirical and Statistical Validation: Execute 25 independent benchmark runs across 5 distinct language model architectures, validating performance improvements via exact two-sided McNemar tests (p < 0.05) and 95% Clopper-Pearson confidence intervals."
    ]
    for obj in objectives_list:
        add_p(doc, obj, space_before=2, space_after=4)

    # ----------------------------------------------------
    # 3. Research scope
    # ----------------------------------------------------
    add_heading_p(doc, "3. Research scope", level=1, space_before=14, space_after=4)
    scope_p1 = (
        "Research Scope and Modality: This research focuses on Vietnamese text-based telecommunications messages, specifically SMS messages, OTT chat messages "
        "(Zalo, Telegram, Messenger), and post-call speech-to-text transcripts. The input modality is analyzed for orthographic, syntactic, psychological, and institutional indicators."
    )
    add_p(doc, scope_p1)

    scope_p2 = (
        "Explicit Out-of-Scope Boundaries: To maintain scientific rigor and operational feasibility within the 14-week timeframe, the following areas are strictly out of scope:\n"
        "• Live Telephony Interception: No live intercept, wiretapping, or audio stream modification of ongoing telephone calls; call analysis is strictly limited to post-call text transcripts uploaded by users.\n"
        "• Autonomous Carrier-Level Dropping: The system operates as an end-user assistive triage tool; it does not possess carrier-level privileges to terminate cellular connections or block cellular SMS transmissions directly.\n"
        "• Autonomous Domain Takedown: The platform flags malicious URLs and IOCs for community warnings and moderator review, but does not execute autonomous domain/DNS takedown actions.\n"
        "• Unmoderated Public Blacklisting: Community-reported phone numbers and URLs are held in a candidate verification queue; no indicator is published to the public blacklist without human moderator adjudication."
    )
    add_p(doc, scope_p2)

    # ----------------------------------------------------
    # 4. Approach and Method
    # ----------------------------------------------------
    add_heading_p(doc, "4. Approach and Method", level=1, space_before=14, space_after=4)
    meth_intro = (
        "The ScamShield-VN methodology is structured around five engineering and mathematical components:"
    )
    add_p(doc, meth_intro)

    meth_comp1 = (
        "Component 1: Dataset Pipeline and PII Sanitization\n"
        "Raw message feeds are ingested and processed through an automated PII Sanitization pipeline. Deterministic regular expressions detect and mask sensitive entities "
        "including subscriber phone numbers, banking account numbers, OTP digits, and individual personal names. A Unicode UTS #39 Confusable Skeleton pre-normalizer "
        "resolves homoglyph substitutions (e.g., Cyrillic characters mimicking Vietnamese bank names) and strips invisible zero-width whitespace before feature extraction."
    )
    add_p(doc, meth_comp1)

    meth_comp2 = (
        "Component 2: Cost-Sensitive Loss Formulation (L_WBCE)\n"
        "To enforce an explicit inductive bias favoring fraud interception, we formulate Cost-Sensitive Weighted Binary Cross-Entropy Loss:\n"
        "    L_WBCE = - (1/N) * Σ [ α * y_i * log(p_hat_i) + (1 - y_i) * log(1 - p_hat_i) ]\n"
        "where y_i ∈ {0, 1} is the true label (0=Ham, 1=Scam), p_hat_i is the predicted scam probability, and α = 5.0 represents the False Negative cost penalty. "
        "The gradient with respect to logit z_i satisfies: ∂L/∂z_i = α*(p_hat_i - 1) for positive scam samples, exerting a 5-fold steeper penalty when scams are missed."
    )
    add_p(doc, meth_comp2)

    meth_comp3 = (
        "Component 3: Model Architecture and ONNX INT8 Quantization\n"
        "ViSoBERT-base (12 layers, 768 hidden dimensions, 12 attention heads, 97.57M parameters) serves as the primary on-device edge backbone. Fine-tuned checkpoints are exported "
        "to ONNX format and quantized using dynamic INT8 precision. This compresses the model footprint from 390.54 MB (FP32) to 98.42 MB (INT8, a 74.8% reduction), achieving "
        "a median CPU inference latency of 70.7 ms (70.66 ms median, 70.72 ± 6.13 ms mean) per message on commodity processors with zero cloud API overhead."
    )
    add_p(doc, meth_comp3)

    meth_comp4 = (
        "Component 4: Consolidated 3-Agent Multi-LLM Forensic Council\n"
        "For boundary samples that fail edge confidence thresholds, Tier 2 activates a consolidated 3-agent forensic council:\n"
        "• Seat A (Cyber Threat & Banking Specialist, weight w_A = 0.35): Analyzes domain recency, shortlink redirections, typosquatting URLs, and banking protocols.\n"
        "• Seat B (Psycholinguistic & Social Slang Specialist, weight w_B = 0.35): Decodes conversational pressure, panic triggers, fake authority intimidation, and teencode slang.\n"
        "• Seat C (Public Defender Advocate, weight w_C = 0.30): Acts as an adversarial devil's advocate tasked exclusively with discovering verified legitimate brand indicators "
        "and standard transaction syntaxes.\n"
        "The synthesized council score is calculated as: P_council = Σ (w_j * P_j) - δ_defender, where δ_defender = 0.25 is an explicit veto penalty activated when authentic "
        "banking OTP or service syntax is verified, directly suppressing false alarms."
    )
    add_p(doc, meth_comp4)

    meth_comp5 = (
        "Component 5: Two-Tier Cascaded Decision Routing and Standardized 3-Label Output\n"
        "The decision engine evaluates edge confidence: Route(x) = Tier 1 if max(P_T1, 1 - P_T1) ≥ τ (with τ = 0.90); otherwise escalate to Tier 2. To avoid forced binary errors "
        "and comply with Article 25 of Vietnamese Decree 13/2023/ND-CP, final verdicts follow a 3-label schema: SCAM-RISK (P_final ≥ 0.60), LOW-RISK (P_final < 0.40), "
        "and UNKNOWN (0.40 ≤ P_final < 0.60, requiring human verification)."
    )
    add_p(doc, meth_comp5)

    # ----------------------------------------------------
    # 5. Research plan (Table 1)
    # ----------------------------------------------------
    add_heading_p(doc, "5. Research plan", level=1, space_before=14, space_after=4)
    plan_intro = (
        "The research implementation plan spans 14 weeks across five structured RBL phases, with clear task breakdowns, expected outputs, "
        "and designated persons in charge as presented in Table 1:"
    )
    add_p(doc, plan_intro)

    # Table 1: Research Plan Table
    t1 = doc.add_table(rows=6, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_box_table_borders(t1, color="000000", sz="6")

    col_widths_t1 = [Inches(0.5), Inches(1.3), Inches(2.3), Inches(1.7), Inches(1.3)]
    for row in t1.rows:
        for idx, width in enumerate(col_widths_t1):
            row.cells[idx].width = width

    headers_t1 = ["No.", "Date", "Task", "Output", "Person in charge"]
    for idx, h in enumerate(headers_t1):
        cell = t1.rows[0].cells[idx]
        cell.paragraphs[0].text = ""
        r = cell.paragraphs[0].add_run(h)
        format_run(r, bold=True, size_pt=10)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "EAEAEA")

    tasks_data = [
        ("1", "01/09/2026 –\n20/09/2026\n(Weeks 1–3)",
         "Systematic Literature Review (SLR) & Scoping: Define inclusion/exclusion criteria, conduct multi-database query logging (IEEE, ACM, Scopus), execute PRISMA screening, compile merged evidence table (N≥12 papers), map PICO evidence, and identify 4 research GAPs.",
         "SLR Evidence Table, PRISMA flow diagram, PICO evidence map (rq-evidence-map.md), and search log records.",
         "Nguyen Quoc Huy (Lead),\nNguyen Minh Quang"),
        
        ("2", "21/09/2026 –\n04/10/2026\n(Weeks 4–5)",
         "Research Question Validation & Proposal Finalization: Formalize RQ1–RQ3, establish H0/H1 statistical hypotheses, calibrate threshold values (θ_scam = 0.90, latency ≤ 100ms), establish baseline ladder, draft comprehensive research proposal, and defend proposal before advisor.",
         "Research Proposal document (Version 1.0/1.1), Proposal defense slide deck, and experimental design validation report.",
         "Nguyen Minh Quang (Lead),\nNguyen Trung Hieu,\nNguyen Quoc Huy"),

        ("3", "05/10/2026 –\n25/10/2026\n(Weeks 6–8)",
         "Data Engineering, Edge Model Training & Quantization: Curate unified corpus of 2,664 Vietnamese messages, build PII sanitizer, isolate frozen test holdout (N=267) and challenge suite (N=117), perform double-annotation (Cohen's Kappa), train ViSoBERT with WBCE (α=5.0), and export ONNX INT8 model.",
         "Sealed Frozen Test CSV, Challenge Suite CSV, Annotation Guidelines & IAA report (κ≥0.85), ONNX INT8 model artifact (visobert_tier1.onnx).",
         "Hoang Hai Phuc (Data),\nNguyen Trung Hieu (Model),\nNguyen Minh Quang (Edge Pipeline)"),

        ("4", "26/10/2026 –\n15/11/2026\n(Weeks 9–11)",
         "Multi-Agent Council Engineering & Benchmark Evaluation: Implement 3-agent forensic council (Cyber Threat, Psycholinguistics, Public Defender) with Standby Priority Chains and Circuit Breaker, execute 25 multi-seed benchmark runs across 5 model architectures, and compute exact McNemar tests.",
         "Multi-seed benchmark summary (25 runs), McNemar statistical test results, paired confusion matrices, and latency/cost profile report.",
         "Nguyen Minh Quang (System/API),\nNguyen Trung Hieu (LLM Council),\nHoang Hai Phuc (Stats & Metrics)"),

        ("5", "16/11/2026 –\n05/12/2026\n(Weeks 12–14)",
         "Two-Tier Cascade Integration, System Packaging & Academic Reporting: Integrate edge screener and cloud council into deployable REST API (FastAPI), build live demonstration interface, author full academic manuscript conforming to JAIT template, and prepare final capstone defense.",
         "Deployable ScamShield API service, Live demonstration suite, Complete academic manuscript draft, and Final defense presentation.",
         "Nguyen Minh Quang (Leader/Integration),\nNguyen Quoc Huy (Manuscript/Docs),\nNguyen Trung Hieu,\nHoang Hai Phuc")
    ]

    for row_idx, data in enumerate(tasks_data, start=1):
        for col_idx, text in enumerate(data):
            cell = t1.rows[row_idx].cells[col_idx]
            cell.paragraphs[0].text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            format_run(r, size_pt=9.5)
            if col_idx in [0, 1, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for row in t1.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    add_p(doc, "", space_after=8)

    # ----------------------------------------------------
    # 6. Expected results
    # ----------------------------------------------------
    add_heading_p(doc, "6. Expected results", level=1, space_before=14, space_after=4)
    exp_intro = "The expected outcomes of this research encompass theoretical, methodological, and practical implications:"
    add_p(doc, exp_intro)

    exp_theo = (
        "1. Theoretical Implications: Demonstrates that asymmetric loss functions (L_WBCE) effectively overcome the majority-class bias in telecommunications fraud detection. "
        "Furthermore, this study provides theoretical and empirical proof that incorporating an adversarial Public Defender agent overcomes the Condorcet jury failure caused by "
        "correlated errors among commercial LLMs, achieving zero false alarms (0.00% FPR) on urgent institutional notifications."
    )
    add_p(doc, exp_theo)

    exp_meth = (
        "2. Methodological Implications: Establishes a standardized, reproducible benchmark framework for Vietnamese telecommunications fraud triage, featuring a multi-seed "
        "evaluation protocol (5 random seeds), exact paired McNemar hypothesis testing, exact 95% Clopper-Pearson confidence intervals, and a 3-label triage safety paradigm "
        "(SCAM-RISK, LOW-RISK, UNKNOWN) adhering to Vietnamese data privacy mandates."
    )
    add_p(doc, exp_meth)

    exp_prac = (
        "3. Practical and Societal Implications: Delivers ScamShield-VN as an operational, open-source mobile and web defense platform. By resolving 96.6% of message traffic "
        "directly on-device with sub-100ms latency and $0.00 API cost, the platform enables scalable deployment across consumer mobile devices in Vietnam. High-risk and uncertain "
        "cases are securely referred to the cloud council at an ultra-low marginal cost ($0.0153 per 1,000 messages), safeguarding vulnerable populations against digital asset extortion."
    )
    add_p(doc, exp_prac)

    # ----------------------------------------------------
    # 7. References
    # ----------------------------------------------------
    add_heading_p(doc, "7. References", level=1, space_before=14, space_after=4)
    references_list = [
        "[1] National Cyber Security Center (NCSC Vietnam), 'Annual Report on Information Security and Digital Fraud Landscape in Vietnam,' Hanoi, Vietnam, Tech. Rep. 2024.",
        "[2] Department of Cyber Security and High-Tech Crime Prevention (A05), Ministry of Public Security, 'Synthesized Report on Telecommunications Fraud and Impersonation Trends,' Hanoi, Vietnam, 2024.",
        "[3] State Bank of Vietnam, 'Decision No. 2345/QĐ-NHNN on Implementing Safety and Security Solutions in Online and Bank Card Payments,' Hanoi, Vietnam, Dec. 2023.",
        "[4] V. D. Nguyen, M. T. Nguyen, and D. Q. Nguyen, 'ViSoBERT: A Pre-trained Language Model for Vietnamese Social Media Text Processing,' in Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, Dec. 2023, pp. 644–655. doi: 10.18653/v1/2023.findings-emnlp.644.",
        "[5] D. Q. Nguyen and A. T. Nguyen, 'PhoBERT: Pre-trained Language Models for Vietnamese,' in Findings of the Association for Computational Linguistics: EMNLP 2020, Nov. 2020, pp. 1037–1042. doi: 10.18653/v1/2020.findings-emnlp.92.",
        "[6] Y. H. Zhou et al., 'FraudSMSWalker: Benchmarking Agentic Large Language Models for SMS-based Telecommunications Fraud Detection,' arXiv preprint arXiv:2603.01892, 2026.",
        "[7] C. Verga et al., 'Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models (PoLL),' arXiv preprint arXiv:2404.18796, 2024.",
        "[8] C.-M. Chan et al., 'ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate,' in Proc. Int. Conf. Learn. Represent. (ICLR), Vienna, Austria, 2024.",
        "[9] MultiPhishGuard Team, 'MultiPhishGuard: Role-Specialized Multi-Agent Framework for Robust Phishing Detection with Minimized False Positive Rates,' arXiv preprint arXiv:2505.23803, 2025.",
        "[10] C. M. Ladha, 'The Condorcet Jury Theorem, Free Speech, and Correlated Votes,' American Journal of Political Science, vol. 36, no. 3, pp. 617–634, 1992.",
        "[11] S. Kim et al., 'Why Do Frontier LLMs Co-Fail? Analyzing Correlated Errors in Model Evaluator Juries,' in Proc. Int. Conf. Mach. Learn. (ICML), 2025.",
        "[12] R. Smit et al., 'Analyzing Multi-Agent Debate Efficiency and Cost Trade-offs in LLM Reasoning,' in Proc. Int. Conf. Mach. Learn. (ICML), 2024.",
        "[13] T. Cam and H. T. Binh, 'VNSED: A Comprehensive Dataset and Benchmark for Vietnamese Spam Email and Smishing Detection,' IEEE Access, vol. 14, pp. 12045–12058, 2026.",
        "[14] M. T. Tuấn et al., 'Evaluating Deep Learning and Pretrained Encoders on Accented and Diacritic-Omitted Vietnamese SMS,' Journal of Advances in Information Technology, vol. 14, no. 5, pp. 812–820, 2023.",
        "[15] Unicode Consortium, 'Unicode Technical Standard #39: Unicode Security Mechanisms and Confusable Skeletons,' Mountain View, CA, Tech. Standard UTS-39, 2024."
    ]
    for ref in references_list:
        p_ref = add_p(doc, ref, space_before=0, space_after=3)
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)

    # ----------------------------------------------------
    # 8. Appendices
    # ----------------------------------------------------
    add_heading_p(doc, "8. Appendices", level=1, space_before=14, space_after=4)
    app_text = (
        "Appendix A: In-Context Learning Prompt Template for Cloud Baseline (Gemini 3.5 Flash, 5-Shot ICL):\n"
        "----------------------------------------------------------------------------------------------------\n"
        "You are an expert telecommunications fraud investigator specializing in Vietnamese scam messages.\n"
        "Your task: Classify the following message as 'SCAM' (fraudulent lure, banking impersonation, extortion, malicious link) "
        "or 'HAM' (legitimate personal message, official banking notification, authentic OTP, service notice).\n\n"
        "Few-shot Examples:\n"
        "Example 1: 'Vietcombank tran trong thong bao: Tai khoan cua quy khach da bi khoa, vui long truy cap https://vcb-digibank-login.com de xac thuc ngay.' -> SCAM\n"
        "Example 2: 'Bo Y te khuyen cao nguoi dan thuc hien bien phap 2K de phong chong dich benh mua dong xuan.' -> HAM\n"
        "Example 3: 'Chuc mung ban da trung thuong xe SH, lien he Zalo 0987xxx de lam thu tuc nhan thuong phi 500k.' -> SCAM\n"
        "Example 4: 'Ma OTP cua ban la 584920. Ma co hieu luc trong 3 phut. Khong chia se ma nay cho bat ky ai.' -> HAM\n"
        "Example 5: 'Tuyen CTV xem video TikTok kiem 500k/ngay, khong can von, inbox ngay.' -> SCAM\n\n"
        "Message to analyze:\n"
        "\"\"\"{text}\"\"\"\n"
        "----------------------------------------------------------------------------------------------------\n\n"
        "Appendix B: Model Specifications and Quantized Footprint Breakdown:\n"
        "• Model Architecture: uitnlp/visobert (12 layers, 768 hidden, 12 attention heads, 97.57M parameters, 15k SentencePiece subwords).\n"
        "• Unquantized FP32 Size: 390.54 MB | Quantized INT8 ONNX Size: 98.42 MB (74.8% compression ratio).\n"
        "• Latency: 70.7 ms median CPU execution per sample on standard quad-core mobile/desktop CPUs."
    )
    add_p(doc, app_text, space_before=2, space_after=6)

    # ----------------------------------------------------
    # 9. Commitment Section
    # ----------------------------------------------------
    doc.add_page_break()
    add_p(doc, "COMMITMENT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, bold=True, size_pt=12)
    add_p(doc, "ON RESPONSIBLE ARTIFICIAL INTELLIGENCE USAGE IN RESEARCH", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14, bold=True, size_pt=12)

    commit_intro = (
        "We are authors of the research paper titled “ScamShield-VN: Evidence-Driven Two-Tier Architecture for Vietnamese Scam and Phishing Detection”, "
        "would like to ensure that all members comply with the rules relevant to Artificial Intelligence (AI) regulations and ethical guidelines "
        "in research practices, which are described in details as follows:\n"
        "1. AI is only used as assistant in correcting grammar, structure and phrasing in academic writing;\n"
        "2. AI usage should NOT be engaged with the creation of content or drafting the research paper, production of fake data or literature synthesis;\n"
        "3. AI usage should be checked and confirmed by all authors. Each author shall bear full responsibility in the accuracy, transparency and originality of their sections, including citations and reference;\n"
        "4. All authors should disclose the use of generative AI and AI-assisted technologies to other co-authors, helping them understand where and how AI was applied in research preparation.\n\n"
        "Hereby, we would like to confirm and take full responsibility for the accuracy and transparency of the provided details."
    )
    add_p(doc, commit_intro, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=18)

    # Table 2: 4-Author Signatures Table
    t2 = doc.add_table(rows=2, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2, color="FFFFFF", sz="0", val="none") # clean borderless or light border
    
    col_width_t2 = Inches(1.56)
    for row in t2.rows:
        for idx in range(4):
            row.cells[idx].width = col_width_t2

    authors_t2 = [
        ("Author 1 (Leader)", "Nguyen Minh Quang"),
        ("Author 2", "Nguyen Trung Hieu"),
        ("Author 3", "Hoang Hai Phuc"),
        ("Author 4", "Nguyen Quoc Huy")
    ]

    for idx, (label, name) in enumerate(authors_t2):
        cell_top = t2.rows[0].cells[idx]
        cell_top.paragraphs[0].text = ""
        p0 = cell_top.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_lbl = p0.add_run(label)
        format_run(r_lbl, bold=True, size_pt=10.5)

        cell_bot = t2.rows[1].cells[idx]
        cell_bot.paragraphs[0].text = ""
        p1 = cell_bot.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(36) # space for signature
        p1.paragraph_format.space_after = Pt(4)
        r_sig = p1.add_run("(Signature & Full name)\n\n\n")
        format_run(r_sig, italic=True, size_pt=9.5)
        r_name = p1.add_run(name)
        format_run(r_name, bold=True, size_pt=10.5)

    for row in t2.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)

    add_p(doc, "", space_after=18)

    # Final Notes & Guidelines preserved from template
    p_note_title = add_p(doc, space_before=10, space_after=2)
    r_nt = p_note_title.add_run("Note:")
    format_run(r_nt, bold=True, italic=True, size_pt=10)

    p_note_body1 = add_p(doc, space_before=0, space_after=2)
    r_nb1 = p_note_body1.add_run("Research proposal must be presented in English/Japanese, A4 paper, single column, Times New Roman 11, and a maximum length of 10 pages (excluding references and appendices).")
    format_run(r_nb1, italic=True, size_pt=10)

    p_note_body2 = add_p(doc, space_before=0, space_after=2)
    r_nb2 = p_note_body2.add_run("For citations and references, please refer to:")
    format_run(r_nb2, italic=True, size_pt=10)

    p_note_body3 = add_p(doc, space_before=0, space_after=2)
    r_nb3 = p_note_body3.add_run("+ Chuẩn IEEE áp dụng cho tiểu ban Công nghệ Thông tin. Để biết thêm chi tiết, vui lòng tham khảo tại: https://libguides.murdoch.edu.au/IEEE/home")
    format_run(r_nb3, size_pt=10)

    p_note_body4 = add_p(doc, space_before=0, space_after=2)
    r_nb4 = p_note_body4.add_run("+ Chuẩn APA áp dụng cho các tiểu ban Kinh tế – Quản trị kinh doanh, Ngôn ngữ, Truyền thông đa phương tiện và Thiết kế mỹ thuật số, vui lòng tham khảo tại: https://libguides.murdoch.edu.au/APA/all")
    format_run(r_nb4, size_pt=10)

    # Save documents following "Tên nhóm_Tiểu ban" convention
    primary_filename = "ScamShield_Information Technology.docx"
    doc.save(primary_filename)
    doc.save("ScamShield_Information_Technology.docx")
    doc.save("ScamShield_CNTT.docx")
    doc.save("FA26SE079_ScamShield_Research_Proposal.docx")
    print(f"Successfully saved as '{primary_filename}' and variations (ScamShield_CNTT.docx, ScamShield_Information_Technology.docx)!")

if __name__ == '__main__':
    build_proposal()
