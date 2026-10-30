import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT      = os.path.join(BASE, "output")
IMG_HIER = os.path.join(OUT, "dmaic_hierarchy_diagram.png")
IMG2     = os.path.join(OUT, "2_Measure")
IMG3     = os.path.join(OUT, "3_Analyze")
IMG3S    = os.path.join(OUT, "3_Analyze", "Survey")
IMG4     = os.path.join(OUT, "4_Improve")
IMG5     = os.path.join(OUT, "5_Control")

# STRICT BLACK & WHITE TYPOGRAPHY
FONT_TITLE   = "Trebuchet MS"   # Executive, bold, distinctive title font
FONT_CONTENT = "Calibri"        # Clean, highly readable body & table font

RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)
RGB_DARK  = (30, 30, 30)
RGB_MUTED = (80, 80, 80)

HEX_BLACK       = "000000"
HEX_WHITE       = "FFFFFF"
HEX_LIGHT_GRAY  = "F8F9FA"
HEX_GRID_LINE   = "D1D5DB"

doc = Document()

# Configure page margins for compact, well-utilized pages
for section in doc.sections:
    section.page_height = Cm(29.7)
    section.page_width  = Cm(21.0)
    section.left_margin = section.right_margin = Cm(2.2)
    section.top_margin  = section.bottom_margin = Cm(2.2)

# 1. APPLY PURE BLACK PAGE BORDERS
def apply_page_borders_bw(doc, sz="8", space="18"):
    """Adds a clean, elegant pure Black page border around every page."""
    for section in doc.sections:
        sectPr = section._sectPr
        for child in list(sectPr):
            if child.tag.endswith('pgBorders'):
                sectPr.remove(child)
        pgBdr = OxmlElement('w:pgBorders')
        pgBdr.set(qn('w:offsetFrom'), 'page')
        for side in ['top', 'left', 'bottom', 'right']:
            b = OxmlElement(f'w:{side}')
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), sz)          # 8 = 1.0 pt crisp border
            b.set(qn('w:space'), space)     # distance in pt from page edge
            b.set(qn('w:color'), HEX_BLACK) # Pure Black
            pgBdr.append(b)
        sectPr.append(pgBdr)

# 2. RUN FONT SETTER WITH FULL OPENXML BINDINGS
def sf(run, font=FONT_CONTENT, size=10.5, bold=False, italic=False, color=RGB_BLACK):
    """Sets exact font properties on a text run with full XML font bindings in black/white."""
    run.font.name = font
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), font)
    rFonts.set(qn('w:hAnsi'), font)
    rFonts.set(qn('w:cs'), font)
    rFonts.set(qn('w:eastAsia'), font)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

# 3. TYPOGRAPHIC COMPONENTS - COMPACT & PURE BLACK/WHITE
def title_text(doc, text, size=22, bold=True, italic=False, center=True, space_before=0, space_after=4):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    sf(r, font=FONT_TITLE, size=size, bold=bold, italic=italic, color=RGB_BLACK)
    return p

def hd(doc, text, size=13, bold=True, center=False, space_before=8, space_after=2):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    sf(r, font=FONT_TITLE, size=size, bold=bold, color=RGB_BLACK)
    return p

def bd(doc, text, size=10.5, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    sf(r, font=FONT_CONTENT, size=size, bold=bold, italic=italic, color=RGB_BLACK)
    return p

def blt(doc, text, size=10, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        sf(r1, font=FONT_TITLE, size=size, bold=True, color=RGB_BLACK)
    r2 = p.add_run(text)
    sf(r2, font=FONT_CONTENT, size=size, color=RGB_BLACK)
    return p

def callout(doc, text, title="KEY TAKEAWAY"):
    """Clean Black & White callout box with a crisp black left border."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.15)
    p.paragraph_format.right_indent = Inches(0.15)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single'); left.set(qn('w:sz'), '20')
    left.set(qn('w:space'), '10'); left.set(qn('w:color'), HEX_BLACK)
    pBdr.append(left); pPr.append(pBdr)

    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), HEX_LIGHT_GRAY)
    pPr.append(shd)

    r_title = p.add_run(f"{title}: ")
    sf(r_title, font=FONT_TITLE, size=10, bold=True, color=RGB_BLACK)
    r_body = p.add_run(text)
    sf(r_body, font=FONT_CONTENT, size=10, italic=True, color=RGB_BLACK)
    return p

def sdiv(doc, title):
    """Major Section Divider in FONT_TITLE with solid Black bottom border rule."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(title)
    sf(r, font=FONT_TITLE, size=16, bold=True, color=RGB_BLACK)

    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '16')
    bot.set(qn('w:space'), '2'); bot.set(qn('w:color'), HEX_BLACK)
    pBdr.append(bot); pPr.append(pBdr)

def img(doc, path, width=Inches(5.4), caption=None):
    """Inserts image with tight spacing so it doesn't create unnecessary blank gaps."""
    if os.path.exists(path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(path, width=width)
    else:
        bd(doc, f"[Image not found: {os.path.basename(path)}]", italic=True)
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(1)
        cp.paragraph_format.space_after = Pt(4)
        if ":" in caption:
            parts = caption.split(":", 1)
            r1 = cp.add_run(parts[0] + ":")
            sf(r1, font=FONT_TITLE, size=9, bold=True, color=RGB_BLACK)
            r2 = cp.add_run(parts[1])
            sf(r2, font=FONT_CONTENT, size=9, italic=True, color=RGB_MUTED)
        else:
            r = cp.add_run(caption)
            sf(r, font=FONT_CONTENT, size=9, italic=True, color=RGB_MUTED)

def shade_cell(cell, fill):
    s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear'); s.set(qn('w:color'), 'auto'); s.set(qn('w:fill'), fill)
    cell._tc.get_or_add_tcPr().append(s)

def style_table_borders_bw(table):
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
    tblBorders = OxmlElement('w:tblBorders')
    
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single'); top.set(qn('w:sz'), '12')
    top.set(qn('w:space'), '0'); top.set(qn('w:color'), HEX_BLACK)
    tblBorders.append(top)
    
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '0'); bottom.set(qn('w:color'), HEX_BLACK)
    tblBorders.append(bottom)
    
    left = OxmlElement('w:left'); left.set(qn('w:val'), 'none')
    tblBorders.append(left)
    
    right = OxmlElement('w:right'); right.set(qn('w:val'), 'none')
    tblBorders.append(right)
    
    insideH = OxmlElement('w:insideH')
    insideH.set(qn('w:val'), 'single'); insideH.set(qn('w:sz'), '4')
    insideH.set(qn('w:space'), '0'); insideH.set(qn('w:color'), HEX_GRID_LINE)
    tblBorders.append(insideH)
    
    insideV = OxmlElement('w:insideV'); insideV.set(qn('w:val'), 'none')
    tblBorders.append(insideV)
    
    tblPr.append(tblBorders)

    # Tight cell margins to prevent vertical bloating
    tblCellMar = OxmlElement('w:tblCellMar')
    for m, val in [('top', '70'), ('bottom', '70'), ('left', '110'), ('right', '110')]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), val); node.set(qn('w:type'), 'dxa')
        tblCellMar.append(node)
    tblPr.append(tblCellMar)

def tbl(doc, headers, rows, widths=None):
    """Pure Black & White table: Black header with white text, alternating white/light-gray rows."""
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders_bw(t)

    # Header Row (Solid Black background, White text)
    for h, c in zip(headers, t.rows[0].cells):
        c.text = ''
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        sf(r, font=FONT_TITLE, size=9.0, bold=True, color=RGB_WHITE)
        shade_cell(c, HEX_BLACK)

    # Data Rows
    for ri, rd in enumerate(rows):
        bg = HEX_LIGHT_GRAY if ri % 2 == 0 else HEX_WHITE
        for val, c in zip(rd, t.rows[ri+1].cells):
            c.text = ''
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            sf(r, font=FONT_CONTENT, size=8.5, color=RGB_BLACK)
            shade_cell(c, bg)

    if widths:
        for i, col in enumerate(t.columns):
            for c in col.cells:
                c.width = widths[i]
    return t

print("="*60)
print("BUILDING STRICT BLACK & WHITE, ZERO-WASTE DMAIC REPORT")
print(f"Title Font:   {FONT_TITLE}")
print(f"Content Font: {FONT_CONTENT}")
print("Color Scheme: Pure Black & White (Monochrome)")
print("Empty Spaces: Removed all artificial page breaks & empty paragraphs")
print("="*60)

# ==============================================================================
# TITLE PAGE (Fitted gracefully to single page without huge blank gaps)
# ==============================================================================
print("Generating Title Page...")

title_text(doc, 'MGT4003 - LEAN SIX SIGMA PRINCIPLES', size=15, bold=True, space_before=18, space_after=14)

title_text(doc, 'Improving Member Retention in a Fitness Centre', size=23, bold=True, space_before=10, space_after=6)
title_text(doc, 'Using DMAIC Methodology and Statistical Analysis', size=13, bold=False, italic=True, space_before=0, space_after=24)

title_text(doc, 'PROJECT REVIEW - 2', size=18, bold=True, space_before=12, space_after=18)

title_text(doc, 'Submitted by', size=11, bold=False, italic=True, space_before=6, space_after=4)
for name in ['Gladwin Daniel P', 'Karthikeyan A']:
    title_text(doc, name, size=15, bold=True, space_before=2, space_after=2)

title_text(doc, 'Under the Guidance of', size=11, bold=False, italic=True, space_before=14, space_after=4)
title_text(doc, 'Dr. Vadivel SM', size=15, bold=True, space_before=2, space_after=4)
title_text(doc, 'Department of Management Studies', size=11, bold=False, space_before=0, space_after=14)

title_text(doc, 'FALL SEMESTER 2026', size=12, bold=True, space_before=6, space_after=0)

doc.add_page_break()

# ==============================================================================
# TABLE OF CONTENTS
# ==============================================================================
print("Generating Table of Contents...")
hd(doc, 'TABLE OF CONTENTS', size=18, bold=True, center=True, space_before=6, space_after=8)

toc_entries = [
    ('1. Introduction', '3'),
    ('2. DMAIC Methodology & Analytical Hierarchy', '3'),
    ('   2.1 DMAIC Analytical Toolkit Hierarchy Diagram', '3'),
    ('   2.2 DMAIC Analytical Hierarchy Matrix', '4'),
    ('   2.3 Phase-by-Phase Methodological Breakdown', '4'),
    ('3. Project Overview', '5'),
    ('4. D - Define Phase', '6'),
    ('   4.1 Critical-to-Quality (CTQ) Metric', '6'),
    ('   4.2 Project Charter', '6'),
    ('   4.3 SIPOC Process Map', '7'),
    ('5. M - Measure Phase', '7'),
    ('   5.1 Baseline Metrics & Data Collection', '7'),
    ('   5.2 Baseline Metrics Dashboard', '8'),
    ('   5.3 Pareto Analysis - Top Churn Contributors', '8'),
    ('   5.4 Distribution Histograms', '9'),
    ('6. A - Analyze Phase', '10'),
    ('   6.1 Independent T-Test - Churned vs Active Members', '10'),
    ('   6.2 Chi-Square Test - Categorical Variables vs Churn', '11'),
    ('   6.3 F-Test - Variance Comparison (Levene Test)', '11'),
    ('   6.4 One-Way ANOVA - Satisfaction Across Plan Types', '12'),
    ('   6.5 Box Plot Comparisons', '12'),
    ('   6.6 Correlation & Regression Analysis', '13'),
    ('   6.7 Fishbone (Ishikawa) Diagram', '13'),
    ('   6.8 5-Whys Root Cause Analysis', '14'),
    ('   6.9 Voice of Customer (VOC) & Reviews Analysis', '14'),
    ('   6.10 Survey Data Analysis (n=50 Member Responses)', '15'),
    ('7. I - Improve Phase: FMEA', '17'),
    ('   7.1 Failure Mode and Effect Analysis (FMEA)', '17'),
    ('   7.2 Prioritised Improvement Action Plan', '18'),
    ('8. C - Control Phase: P-Chart', '19'),
    ('   8.1 P-Chart - Statistical Process Control', '19'),
    ('   8.2 P-Chart Results & Sustained Capability', '20'),
    ('9. Conclusion & Recommendations', '21'),
    ('10. References', '22'),
]

for entry, pg in toc_entries:
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.0))
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    is_major = not entry.startswith('   ')
    r1 = p.add_run(entry)
    sf(r1, font=FONT_TITLE if is_major else FONT_CONTENT, size=10, bold=is_major, color=RGB_BLACK)
    r2 = p.add_run(f'\t{pg}')
    sf(r2, font=FONT_TITLE if is_major else FONT_CONTENT, size=10, bold=is_major, color=RGB_MUTED)

doc.add_page_break()

# ==============================================================================
# SEC 1: INTRODUCTION
# ==============================================================================
print("Generating Section 1: Introduction...")
sdiv(doc, '1. INTRODUCTION')
bd(doc, 'The fitness and wellness industry has witnessed exponential growth over the past two decades. However, one of the most persistent challenges faced by fitness centre operators is customer retention. Despite attracting large numbers of new members, many facilities struggle to retain them beyond their initial subscription period. High membership churn impacts revenue, increases customer acquisition costs, erodes brand reputation, and disrupts long-term operational planning.')

bd(doc, 'This project applies the Lean Six Sigma DMAIC (Define, Measure, Analyze, Improve, Control) methodology to systematically investigate and address member attrition at the Ultimate Fitness Centre. The DMAIC framework is a data-driven quality strategy that provides a structured approach to identifying process defects, understanding root causes, and implementing sustainable improvements.')

bd(doc, 'The study integrates multiple data sources: historical membership transaction records, customer review sentiments, and a structured 50-response Member Experience Survey. Advanced statistical tools including Independent T-Tests, F-Tests (Levene\'s), Chi-Square tests, One-Way ANOVA, Box Plots, Pareto Analysis, Correlation Analysis, Fishbone Diagrams, and 5-Whys Analysis are applied systematically across the DMAIC phases.')

# ==============================================================================
# SEC 2: METHODOLOGY & ANALYTICAL HIERARCHY (Flows naturally without page break)
# ==============================================================================
print("Generating Section 2: DMAIC Methodology & Hierarchy...")
sdiv(doc, '2. DMAIC METHODOLOGY & ANALYTICAL HIERARCHY')

bd(doc, 'DMAIC is the core problem-solving framework of Lean Six Sigma, specifically designed for improving existing processes. Unlike creative ideation methods, DMAIC is grounded in empirical data and statistical rigor, structured into five sequential phases:')

hd(doc, '2.1 DMAIC Analytical Toolkit Hierarchy Diagram', size=12)
bd(doc, 'The hierarchy diagram below illustrates the end-to-end analytical architecture developed for this retention project. Under each of the five DMAIC letters, every statistical hypothesis test, diagnostic visual chart, and quality engineering tool executed in this project is explicitly organized:')

# INSERT B&W HIERARCHY DIAGRAM
img(doc, IMG_HIER, width=Inches(6.2),
    caption="Figure 2.1: DMAIC Analytical Toolkit Hierarchy — Quality Frameworks, Statistical Hypothesis Tests, Visual Charts & SPC Controls Across DMAIC Phases")

hd(doc, '2.2 DMAIC Analytical Hierarchy Matrix', size=12)
bd(doc, 'The matrix below details the comprehensive analytical toolkit deployed across each phase of the project, including statistical tests, charts, frameworks, and verified outcomes:')

tbl(doc, ['Phase & Focus', 'Statistical Tests & Formulas', 'Diagnostic Charts & Plots', 'Quality Frameworks', 'Deliverable / Result'], [
    [
        'D - DEFINE\nProblem Scoping &\nVoice of Customer',
        '• Defect: Non-renewal = 1 defect\n• CTQ Formula: Churn % = (Lost/Active)×100%',
        '• CTQ Metric Flowdown Tree\n• SIPOC Process Map Matrix\n• Project Timeline Roadmap',
        '• Project Charter\n• SIPOC (5 Core Steps)\n• VOC Translation Matrix',
        'Charter signed off;\nBaseline churn ~27%;\nTarget <15% monthly churn'
    ],
    [
        'M - MEASURE\nBaseline Metrics &\nPareto Analysis',
        '• Process Sigma: Z = 2.1 σ\n• DPMO = 272,000 ppm\n• Churn Proportion: p = 0.272\n• Mean Duration: 4.2 mos\n• Payment Delay: 2.1 days',
        '• Baseline Metrics Dashboard\n• Pareto 1: Churn by Plan Type\n• Pareto 2: Churn by Duration\n• Histograms: Duration, Amount, Age\n• Monthly Enrollment Seasonality Trend',
        '• Master Data Cleaning (n=475+)\n• Pareto 80/20 Prioritization\n• Process Capability Baseline',
        'Baseline established at 2.1σ;\nMonthly plans identified as\nvital few (77% churn rate)'
    ],
    [
        'A - ANALYZE\nHypothesis Testing &\nRoot Cause Isolation',
        '• Welch T-Tests (5 vars, p<0.001)\n• Chi-Square Tests (χ²=87.4, p<0.001)\n• Levene\'s F-Test (p>0.05, equal var)\n• One-Way ANOVA (p=0.012, 0.019)\n• Survey Hypothesis Tests (n=50)',
        '• Box Plot Panels (Active vs Churned)\n• Survey 6-Dimension Box Plots\n• Correlation Heatmap (r > 0.7) & Scatter\n• Fishbone (6M Ishikawa) Diagram\n• 5-Whys Root Cause Tree\n• VOC Reviews Sentiment Themes\n• Survey Insights Dashboard & NPS Donut',
        '• 6M Fishbone Analysis\n• 5-Whys Root Cause Tree\n• Net Promoter Score (+44 NPS)\n• VOC Sentiment Coding',
        'Root causes statistically\nvalidated: Plan duration gap,\nmissing CRM reminders, peak\novercrowding & goal tracking'
    ],
    [
        'I - IMPROVE\nFMEA Risk Ranking &\nCountermeasures',
        '• FMEA Risk Priority Number formula:\n  RPN = Severity × Occurrence × Detection\n• 7 Failure Modes with RPN ≥ 200 (Critical)',
        '• FMEA RPN Pareto Ranking Chart\n• FMEA Risk Matrix (Bubble Scatter)\n• Countermeasure Roadmap',
        '• Failure Mode & Effects Analysis\n• Action Prioritization Matrix\n• Implementation Action Plan',
        '7 Critical Countermeasures\ndeployed: Auto reminders (378),\nFitness assessment (336),\nCrowd tracker, Plan discounts'
    ],
    [
        'C - CONTROL\nStatistical Process\nControl & SOPs',
        '• P-Chart SPC Formulas with 3σ limits:\n  CL = p-bar; UCL/LCL = p ± 3√(p(1-p)/n)\n• Nelson SPC Stability Rules (0 Viols)',
        '• P-Chart Monthly Churn Trend with\n  Pre (Y1) vs Post (Y2) Limits\n• SPC Summary Dashboard',
        '• Statistical Process Control (SPC)\n• Out-of-Control Plan (OCAP)\n• Standard Operating Procedures',
        '45.2% Churn Reduction achieved;\nMonthly churn sustained at 14.7%\n(<15% target met); 2.6 Sigma'
    ]
], widths=[Inches(1.15), Inches(1.5), Inches(1.55), Inches(1.1), Inches(1.3)])

hd(doc, '2.3 Phase-by-Phase Methodological Breakdown', size=12)

phases_breakdown = [
    ('D - DEFINE', 'Establishes the problem foundation, scopes business boundaries, and sets Critical-to-Quality (CTQ) specifications. Core tools include the Project Charter, SIPOC Process Map, and Voice of Customer (VOC) Translation Matrix. Primary CTQ is established as Monthly Churn Rate with an operational defect definition where any non-renewal upon plan expiry is recorded as one defect.'),
    ('M - MEASURE', 'Collects empirical baseline data across 475+ member records and 50 survey responses. Quantifies current state capability at 2.1 Sigma (DPMO ~272,000) with a monthly churn rate of 27.2%. Pareto analysis isolates monthly membership plans (77% churn) and short-tenure members (<3 months) as the vital few drivers generating >80% of total member attrition.'),
    ('A - ANALYZE', 'Conducts rigorous statistical hypothesis testing at alpha = 0.05. Independent Two-Sample T-Tests, Chi-Square Tests of Independence, Levene F-Tests, and One-Way ANOVA statistically confirm that plan duration, payment gap delays, and facility overcrowding are significant drivers. Root-cause diagrams including the 6M Fishbone and 5-Whys isolate lack of renewal alerts, goal stagnation, and peak crowding.'),
    ('I - IMPROVE', 'Utilizes Failure Mode and Effects Analysis (FMEA) to score failure modes across Severity, Occurrence, and Detection. Identifies 7 CRITICAL failure modes (RPN >= 200), led by lack of renewal reminders (RPN 378). Deploys targeted countermeasures including CRM 30-15-7 day automated reminders, monthly fitness assessments, live crowd monitoring, and annual plan upgrade discounts.'),
    ('C - CONTROL', 'Establishes Statistical Process Control (SPC) via the P-Chart (Proportion Defective) with 3-sigma control limits. Tracks monthly churn across 12 months pre-improvement vs 6 months post-improvement. Post-improvement mean churn drops from 26.9% to 14.7% (a 45.2% reduction), meeting the project objective (<15%) with zero out-of-control signals and improving process capability to 2.6 Sigma.'),
]

for p_title, p_desc in phases_breakdown:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run(p_title + ': ')
    sf(r1, font=FONT_TITLE, size=10.5, bold=True, color=RGB_BLACK)
    r2 = p.add_run(p_desc)
    sf(r2, font=FONT_CONTENT, size=10.5, color=RGB_BLACK)

hd(doc, 'Why DMAIC for Member Retention?', size=12)
bd(doc, 'Member retention is an operational process problem. Members join, engage with services, and either renew or churn. This lifecycle has clearly identifiable inputs (plan type, engagement), process steps (onboarding, billing, renewal), and outputs (retained vs. churned members). DMAIC is ideally suited because it demands empirical measurement before action, and statistical evidence before conclusion.')

# ==============================================================================
# SEC 3: PROJECT OVERVIEW (Flows naturally)
# ==============================================================================
print("Generating Section 3: Project Overview...")
sdiv(doc, '3. PROJECT OVERVIEW')

hd(doc, 'ORGANIZATION: Ultimate Fitness Centre , RATHINAMANGALAM', size=12)
bd(doc, 'The Ultimate Fitness Centre is a mid-sized facility offering Monthly, Quarterly (3-Month), and Annual (12-Month) membership plans, with equipment, group classes, personal training, and wellness services. The facility primarily serves urban members aged 18-45.')

hd(doc, 'PROBLEM STATEMENT', size=12)
callout(doc, 'A significant proportion of the member base was found to be churning upon plan expiry, particularly acute among monthly plan members (77% churn rate). The cumulative effect was declining active memberships, reduced revenue predictability, and an unsustainable marketing acquisition burden.',
        title="PROBLEM STATEMENT")

hd(doc, 'PROJECT OBJECTIVES', size=12)
for obj in [
    'Quantify current member churn rate and establish performance baseline including Sigma Level',
    'Identify primary statistical drivers of member attrition through rigorous hypothesis testing',
    'Validate root causes using T-Tests, Chi-Square tests, ANOVA, and F-Tests',
    'Develop a prioritised improvement plan using FMEA (Risk Priority Number ranking)',
    'Implement and monitor improvements using the P-Chart (Statistical Process Control)',
    'Achieve a measurable churn reduction targeting less than 15% monthly churn rate',
]:
    blt(doc, obj)

hd(doc, 'DATA SOURCES', size=12)
tbl(doc, ['Source', 'Description', 'Volume'], [
    ['Membership Transactions', 'Sign-ups, renewals, and cancellations for all members', '475+ records'],
    ['Member Experience Survey', '23-variable questionnaire on satisfaction and renewal intent', '50 responses'],
    ['Customer Reviews', 'Text reviews for VOC and sentiment analysis', '60+ reviews'],
    ['Payment Records', 'Billing data, payment gaps, and plan pricing', 'All transactions'],
], widths=[Inches(2.0), Inches(3.4), Inches(1.2)])

# ==============================================================================
# SEC 4: DEFINE
# ==============================================================================
print("Generating Section 4: Define...")
doc.add_page_break()
sdiv(doc, '4. D - DEFINE PHASE')

hd(doc, '4.1 Critical-to-Quality (CTQ) Metric', size=12)
bd(doc, 'The Critical-to-Quality (CTQ) metric directly reflects customer requirements and operational success criteria. For this project:')

for item in [
    'PRIMARY CTQ: Monthly Member Churn Rate = (Members Lost) / (Total Active at Start) x 100%',
    'SECONDARY CTQ: Member Renewal Rate = (Members Renewed) / (Members Eligible) x 100%',
    'TARGET: Reduce monthly churn from baseline ~27% to below 15%',
    'DEFECT: Any member who does not renew upon plan expiry is counted as one defect',
]:
    blt(doc, item)

hd(doc, '4.2 Project Charter', size=12)
tbl(doc, ['Element', 'Details'], [
    ['Project Title', 'Improving Member Retention - Ultimate Fitness Centre (DMAIC)'],
    ['Business Case', 'High member churn (~27%/month) reduces revenue and increases acquisition costs'],
    ['Problem Statement', 'Member churn exceeds 25%, driven by plan type, poor engagement, and dissatisfaction'],
    ['Project Goal', 'Reduce monthly churn from 27% to below 15% within 6 months of implementation'],
    ['Project Scope', 'All active and churned members; Monthly, Quarterly, and Annual plan types'],
    ['CTQ Metric', 'Monthly Churn Rate (%) and Member Renewal Rate (%)'],
    ['Team Members', 'Gladwin Daniel P, Karthikeyan A'],
    ['Faculty Guide', 'Dr. Vadivel SM'],
    ['Timeline', '6 months (3 months DMAIC + 3 months post-implementation monitoring)'],
    ['Expected Benefits', '>25% churn reduction; improved member satisfaction; higher lifetime value'],
], widths=[Inches(2.0), Inches(4.6)])

hd(doc, '4.3 SIPOC Diagram', size=12)
bd(doc, 'The SIPOC maps the end-to-end membership process boundaries:')

tbl(doc, ['Suppliers', 'Inputs', 'Process Steps', 'Outputs', 'Customers'], [
    ['Equipment Vendors', 'New Member Applications', 'Member Onboarding', 'Oriented Members', 'Gym Members'],
    ['Trainers & Coaches', 'Membership Payments', 'Plan Selection & Billing', 'Active Memberships', 'Prospective Members'],
    ['Facility Management', 'Member Feedback Data', 'Engagement & Usage', 'Renewals & Retention', 'Revenue & Growth'],
    ['Marketing Team', 'Attendance Data', 'Performance Tracking', 'Churn Metrics', 'Management Reports'],
])

# ==============================================================================
# SEC 5: MEASURE
# ==============================================================================
print("Generating Section 5: Measure...")
doc.add_page_break()
sdiv(doc, '5. M - MEASURE PHASE')

hd(doc, '5.1 Baseline Metrics & Data Collection', size=12)
bd(doc, 'The Measure phase established the current state of member churn using historical transaction data. Four datasets were cleaned and unified into members_master_cleaned.csv (475+ records) with a binary churn indicator (Is_Churned=1 for non-renewals).')

tbl(doc, ['Metric', 'Value', 'Interpretation'], [
    ['Total Members Analysed', '475+', 'Complete historical dataset'],
    ['Overall Churn Rate', '~27% per month', '1 in 4 members did not renew'],
    ['Monthly Plan Churn Rate', '77%', 'Critically high - short-term commitment gap'],
    ['Quarterly Plan Churn Rate', '21%', 'Moderate churn'],
    ['Annual Plan Churn Rate', '8%', 'Low churn - strong long-term commitment'],
    ['Process Sigma Level', '~2.1 sigma', 'Below industry benchmark of 3 sigma'],
    ['Mean Membership Duration', '~4.2 months', 'Short average tenure - early dropout pattern'],
    ['Mean Plan Amount', 'Rs. 1,847', 'Wide spread - two distinct pricing tiers'],
    ['Mean Payment Gap', '2.1 days', 'Payment delays correlated with churn'],
    ['DPMO', '~272,000', 'Based on 27.2% monthly churn rate'],
])

hd(doc, '5.2 Baseline Metrics Dashboard', size=12)
img(doc, os.path.join(IMG2, 'baseline_metrics_dashboard.png'), Inches(5.6),
    'Figure 5.1: Baseline Metrics Dashboard - Churn rates, plan distribution, and membership statistics')

hd(doc, '5.3 Pareto Analysis - Top Churn Contributors', size=12)
bd(doc, 'Pareto Analysis (80-20 Rule) identified the vital few factors driving the majority of member churn:')

img(doc, os.path.join(IMG2, 'pareto_1_churn_by_plan.png'), Inches(5.0),
    'Figure 5.2: Pareto Chart - Churn by Plan Type (Monthly plans: 77% churn rate)')

img(doc, os.path.join(IMG2, 'pareto_2_churn_by_duration.png'), Inches(5.0),
    'Figure 5.3: Pareto Chart - Churn by Membership Duration Category')

callout(doc, 'Monthly plan members and short-duration members (< 3 months) constitute the vital few driving 80%+ of total churn. These are the primary targets for improvement.',
        title="PARETO INSIGHT")

hd(doc, '5.4 Distribution Histograms', size=12)
img(doc, os.path.join(IMG2, 'histogram_1_membership_duration.png'), Inches(4.8),
    'Figure 5.4: Membership Duration - Right-skewed; majority of members churn within 1-3 months')

img(doc, os.path.join(IMG2, 'histogram_2_plan_amount.png'), Inches(4.8),
    'Figure 5.5: Plan Amount Distribution - Bimodal pattern indicates two pricing clusters')

img(doc, os.path.join(IMG2, 'monthly_enrollment_trend.png'), Inches(5.0),
    'Figure 5.6: Monthly Enrollment Trend - Seasonal peaks in January and June')

# ==============================================================================
# SEC 6: ANALYZE (Continuous, compact statistical flow)
# ==============================================================================
print("Generating Section 6: Analyze...")
doc.add_page_break()
sdiv(doc, '6. A - ANALYZE PHASE')
bd(doc, 'The Analyze phase is the statistical core of this DMAIC project. All tests use alpha = 0.05 significance threshold. Analysis is conducted across two layers: (1) historical transaction data and (2) primary survey data from 50 member responses.')

hd(doc, '6.1 Independent T-Test - Churned vs Active Members', size=12)
bd(doc, 'Welch\'s T-Test compared continuous variable means between churned and active member groups.')

callout(doc, 'H0: Mean is EQUAL between churned and active members\nH1: Significant DIFFERENCE exists between groups (alpha=0.05)',
        title="HYPOTHESIS FRAMEWORK")

tbl(doc, ['Variable', 'Active Mean', 'Churned Mean', 't-stat', 'p-value', 'Sig?', 'Interpretation'], [
    ['Membership Duration (months)', '6.8', '2.1', '12.45', '<0.001', 'YES', 'Churned members had shorter tenure'],
    ['Plan Amount (Rs)', '2,140', '1,420', '8.32', '<0.001', 'YES', 'Churned members paid lower amounts'],
    ['Payment Gap (days)', '0.8', '3.9', '-9.17', '<0.001', 'YES', 'Churned members had longer delays'],
    ['Member Age', '34.2', '29.8', '3.41', '0.001', 'YES', 'Younger members churn more'],
    ['Plan Duration (months)', '8.4', '1.9', '15.62', '<0.001', 'YES', 'Short plan duration predicts churn'],
], widths=[Inches(1.5), Inches(0.7), Inches(0.7), Inches(0.55), Inches(0.6), Inches(0.45), Inches(2.1)])

callout(doc, 'All five variables show significant differences (p<0.001). Membership duration and plan duration are the strongest continuous discriminators.',
        title="T-TEST CONCLUSION")

img(doc, os.path.join(IMG3, 'box_plots_comparisons.png'), Inches(5.5),
    'Figure 6.1: Box Plot Panel - Key Variables Compared Between Active and Churned Member Groups')

hd(doc, '6.2 Chi-Square Test - Categorical Variables vs Churn', size=12)
bd(doc, 'Chi-Square tests evaluated statistical associations between categorical variables and churn status.')

callout(doc, 'H0: Variable is INDEPENDENT of churn status\nH1: Significant ASSOCIATION exists (alpha=0.05)',
        title="HYPOTHESIS FRAMEWORK")

tbl(doc, ['Variable', 'Chi2', 'DoF', 'p-value', 'Significant?', 'Interpretation'], [
    ['Membership Plan Type', '87.43', '2', '<0.001', 'YES', 'Strong - Monthly plans drive churn'],
    ['Plan Duration Category', '95.12', '3', '<0.001', 'YES', 'Very strong association'],
    ['Payment Method', '12.31', '3', '0.006', 'YES', 'Significant association'],
    ['Gender', '2.14', '1', '0.143', 'NO', 'Independent of churn'],
    ['Branch/Location', '4.81', '2', '0.090', 'NO', 'Not significant at 0.05'],
])

callout(doc, 'Plan type (Chi2=87.43, p<0.001) and plan duration (Chi2=95.12, p<0.001) are the strongest categorical predictors of churn.',
        title="CHI-SQUARE CONCLUSION")

hd(doc, '6.3 F-Test - Variance Comparison (Levene Test)', size=12)
bd(doc, 'Levene\'s F-Test verified equality of variances between groups, a prerequisite for parametric T-Tests.')

callout(doc, 'H0: Variances are EQUAL between groups\nH1: Variances are SIGNIFICANTLY DIFFERENT (alpha=0.05)',
        title="HYPOTHESIS FRAMEWORK")

tbl(doc, ['Variable', 'Renewer Var.', 'Non-Renewer Var.', 'F-Ratio', 'Levene p-val', 'Equal Var?'], [
    ['Equipment Satisfaction', '0.513', '0.322', '1.591', '0.409', 'YES - Equal'],
    ['Hygiene Satisfaction', '0.199', '0.489', '0.408', '0.212', 'YES - Equal'],
    ['Environment Rating', '0.815', '0.267', '3.055', '0.560', 'YES - Equal'],
    ['Trainer Rating', '0.244', '0.544', '0.447', '0.164', 'YES - Equal'],
    ['Value for Money', '1.054', '0.500', '2.108', '0.147', 'YES - Equal'],
    ['Overall Satisfaction', '0.227', '0.144', '1.570', '0.329', 'YES - Equal'],
])

callout(doc, 'Equal variances confirmed for all satisfaction variables (all p>0.05). This validates parametric T-Test assumptions and indicates equal rating dispersion across groups.',
        title="F-TEST CONCLUSION")

hd(doc, '6.4 One-Way ANOVA - Satisfaction Across Plan Types', size=12)
bd(doc, 'ANOVA tested whether satisfaction and renewal intent differ across Monthly, Quarterly, and Annual plan types.')

callout(doc, 'H0: Mean scores are EQUAL across all three plan types\nH1: At least one group mean differs significantly (alpha=0.05)',
        title="HYPOTHESIS FRAMEWORK")

tbl(doc, ['Variable', 'Monthly Mean', 'Quarterly Mean', 'Annual Mean', 'F-stat', 'p-value', 'Sig?'], [
    ['Equipment Satisfaction', '4.28', '4.19', '4.91', '4.344', '0.0186', 'YES'],
    ['Trainer Rating', '4.56', '4.57', '4.82', '0.759', '0.4738', 'NO'],
    ['Value for Money', '3.94', '3.76', '4.64', '3.083', '0.0552', 'Marginal'],
    ['Renewal Intent (1-5)', '4.61', '4.38', '4.73', '0.754', '0.4760', 'NO'],
    ['Overall Satisfaction', '4.37', '4.31', '4.82', '4.887', '0.0118', 'YES'],
])

img(doc, os.path.join(IMG3S, 'survey_anova_chart.png'), Inches(5.5),
    'Figure 6.2: ANOVA - Satisfaction Scores by Plan Type. Error bars = +/-1 Standard Error.')

callout(doc, 'Annual plan members rate Equipment Satisfaction (F=4.34, p=0.019) and Overall Satisfaction (F=4.89, p=0.012) significantly higher. This strongly supports strategies to migrate monthly members to longer commitments.',
        title="ANOVA INTERPRETATION")

hd(doc, '6.5 Box Plot Comparisons', size=12)
bd(doc, 'Box plots display median, IQR, whiskers, and outliers simultaneously, making group differences immediately apparent across satisfaction dimensions:')

img(doc, os.path.join(IMG3S, 'survey_box_plots.png'), Inches(5.6),
    'Figure 6.3: Survey Box Plots - Satisfaction Dimensions: Likely vs Unlikely Renewers (n=50)')

callout(doc, 'Likely Renewers consistently score higher across all dimensions. Value for Money exhibits the widest separation between groups, making it the primary perceptual discriminator.',
        title="BOX PLOT INSIGHT")

hd(doc, '6.6 Correlation & Regression Analysis', size=12)
img(doc, os.path.join(IMG3, 'correlation_matrix.png'), Inches(4.8),
    'Figure 6.4: Correlation Matrix Heatmap - Pairwise correlations between key membership variables')

img(doc, os.path.join(IMG3, 'scatter_amount_vs_duration.png'), Inches(4.5),
    'Figure 6.5: Scatter Plot - Plan Amount vs Membership Duration, coloured by Churn Status')

callout(doc, 'Strong positive correlation (r>0.7) between membership duration and plan amount. Higher-value commitments correlate with longer tenure. Payment gap shows negative correlation with retention.',
        title="CORRELATION FINDINGS")

hd(doc, '6.7 Fishbone (Ishikawa) Diagram', size=12)
bd(doc, 'The Fishbone Diagram categorises potential root causes of member churn into six major categories (People, Process, Policy, Equipment, Promotion, Price):')

img(doc, os.path.join(IMG3, 'fishbone_diagram.png'), Inches(5.6),
    'Figure 6.6: Fishbone Diagram - Root Cause Analysis of Member Churn')

for root_c in [
    'PEOPLE: Trainer-member engagement gaps; lack of personalised attention for non-PT members',
    'PROCESS: Absence of structured onboarding; no automated renewal reminder system',
    'POLICY: No upgrade incentives; absence of membership freeze/pause policy during travel',
    'EQUIPMENT: Machine unavailability and long wait times during evening peak hours',
    'PROMOTION: No loyalty discounts for long tenure; lack of referral incentives',
    'PRICE: Perceived value mismatch for monthly plan members relative to features',
]:
    blt(doc, root_c)

hd(doc, '6.8 5-Whys Root Cause Analysis', size=12)
img(doc, os.path.join(IMG3, 'five_whys_analysis.png'), Inches(5.6),
    'Figure 6.7: 5-Whys Analysis - Drilling to root causes of member churn')

for why_item in [
    'Branch 1: No CRM automation = members forget to renew (Root: complete absence of reminder system)',
    'Branch 2: No crowd management = peak-hour frustration leads to churn (Root: no capacity tracking)',
    'Branch 3: No goal tracking = member sees no progress and quits (Root: no fitness assessment cadence)',
]:
    blt(doc, why_item)

hd(doc, '6.9 Voice of Customer (VOC) & Reviews Analysis', size=12)
img(doc, os.path.join(IMG3, 'voc_reviews_analysis.png'), Inches(5.4),
    'Figure 6.8: VOC Analysis - Sentiment from member reviews (positive/negative theme frequency)')

img(doc, os.path.join(IMG3, 'churn_rate_comparison.png'), Inches(4.8),
    'Figure 6.9: Churn Rate Comparison by Plan Type and Duration Category')

img(doc, os.path.join(IMG3, 'pt_trainer_analysis.png'), Inches(4.8),
    'Figure 6.10: Personal Training Enrollment and Impact on Retention')

hd(doc, '6.10 Survey Data Analysis - 50 Member Responses', size=12)
bd(doc, 'A structured Member Experience Survey (50 responses, 23 variables) captured primary data on satisfaction, renewal intent (1-5 Likert), NPS, churn reasons, and retention preferences. Members scoring >=4 = Likely Renewers; <4 = Unlikely Renewers.')

tbl(doc, ['Survey Metric', 'Result'], [
    ['Total Responses', '50'],
    ['Likely Renewers (Intent >= 4 on 1-5 scale)', '40 (80%)'],
    ['Unlikely Renewers (Intent < 4)', '10 (20%)'],
    ['Mean Renewal Intent', '4.54 / 5.00'],
    ['Net Promoter Score (NPS)', '+44'],
    ['Promoters (NPS 9-10)', '28 (56%)'],
    ['Passives (NPS 7-8)', '16 (32%)'],
    ['Detractors (NPS 0-6)', '6 (12%)'],
    ['Mean Equipment Satisfaction', '4.38 / 5.00'],
    ['Mean Hygiene Satisfaction', '4.78 / 5.00'],
    ['Mean Trainer Rating', '4.62 / 5.00'],
    ['Mean Value for Money', '4.02 / 5.00 (lowest - key pain point)'],
    ['Mean Overall Satisfaction', '4.44 / 5.00'],
    ['Annual Plan - Overall Satisfaction', '4.82 / 5.00 (ANOVA: F=4.89, p=0.012)'],
    ['ANOVA: Equipment Satisfaction', 'F=4.34, p=0.019 (Annual significantly higher)'],
    ['Top Churn Reason', 'Moving Away / Relocating'],
    ['#2 Churn Reason', 'Overcrowding and Machine Wait Times'],
    ['Top Retention Initiative', 'More Specialized Equipment'],
], widths=[Inches(3.3), Inches(3.3)])

img(doc, os.path.join(IMG3S, 'survey_nps_voc.png'), Inches(5.6),
    'Figure 6.11: NPS Donut | VOC Churn Reasons | Desired Retention Initiatives (Survey n=50)')

img(doc, os.path.join(IMG3S, 'survey_ttest_chart.png'), Inches(5.0),
    'Figure 6.12: T-Test Results - Satisfaction Scores: Likely vs Unlikely Renewers')

img(doc, os.path.join(IMG3S, 'survey_chisquare_chart.png'), Inches(5.0),
    'Figure 6.13: Chi-Square - Categorical Variables vs Renewal Intent Group')

img(doc, os.path.join(IMG3S, 'survey_insights_dashboard.png'), Inches(5.6),
    'Figure 6.14: Survey Insights Dashboard - Complete 6-panel Analysis (n=50)')

# ==============================================================================
# SEC 7: IMPROVE
# ==============================================================================
print("Generating Section 7: Improve...")
doc.add_page_break()
sdiv(doc, '7. I - IMPROVE PHASE: FMEA')

hd(doc, '7.1 Failure Mode and Effect Analysis (FMEA)', size=12)
bd(doc, 'FMEA is a proactive risk analysis method that identifies process failure modes, evaluates their impact (Severity x Occurrence x Detectability = RPN), and prioritises corrective actions.')

for fmea_item in [
    'Severity (S 1-10): Impact of failure on member experience. 9-10 = member churns.',
    'Occurrence (O 1-10): Likelihood of failure. 9-10 = almost certain.',
    'Detectability (D 1-10): Difficulty of detecting failure before it impacts customer. 9-10 = impossible.',
    'RPN = S x O x D  |  CRITICAL: >=200  |  HIGH: 100-199  |  MEDIUM: 50-99',
]:
    blt(doc, fmea_item)

tbl(doc, ['Process Step', 'Failure Mode', 'Effect', 'S', 'O', 'D', 'RPN', 'Priority', 'Action'], [
    ['Membership Renewal', 'No renewal reminder sent', 'Silent churn', '9', '7', '6', '378', 'CRITICAL', 'Automated SMS/email 30-15-7 days pre-expiry'],
    ['Goal Tracking', 'No progress tracking system', 'Member quits - no results', '8', '7', '6', '336', 'CRITICAL', 'Monthly fitness assessment + progress report'],
    ['Plan Upgrade', 'No upsell/upgrade prompts', 'Stays on costly monthly plan', '6', '8', '7', '336', 'CRITICAL', 'Loyalty upgrade offer after 3 months on monthly'],
    ['Plan Selection', 'Only monthly plans chosen', 'High churn - low commitment', '8', '8', '5', '320', 'CRITICAL', 'Incentivise quarterly/annual with discounts'],
    ['Peak Hour Facility', 'Machine unavailability', 'Frustration and churn', '9', '8', '4', '288', 'CRITICAL', 'Live crowd tracker + staggered peak slots'],
    ['Member Onboarding', 'No orientation provided', 'Confusion and early dropout', '8', '6', '5', '240', 'CRITICAL', 'Structured 7-day onboarding checklist'],
    ['Trainer Engagement', 'Trainer ignores non-PT members', 'Members feel unsupported', '7', '6', '5', '210', 'CRITICAL', 'Mandatory 30-min floor trainer rounds'],
    ['Payment Collection', 'Lapsed payment ignored', 'Unintentional churn', '7', '5', '4', '140', 'HIGH', 'Auto payment retry + WhatsApp billing alert'],
], widths=[Inches(0.9), Inches(1.1), Inches(0.9), Inches(0.25), Inches(0.25), Inches(0.25), Inches(0.4), Inches(0.65), Inches(1.85)])

img(doc, os.path.join(IMG4, 'fmea_rpn_chart.png'), Inches(5.6),
    'Figure 7.1: FMEA - Risk Priority Number by Failure Mode. 7 failures rated CRITICAL (RPN>=200).')

img(doc, os.path.join(IMG4, 'fmea_risk_map.png'), Inches(4.8),
    'Figure 7.2: FMEA Risk Map - Severity vs Occurrence (Bubble size = RPN)')

hd(doc, '7.2 Prioritised Improvement Action Plan', size=12)
tbl(doc, ['#', 'Priority', 'Action', 'Owner', 'Timeline', 'Expected Impact'], [
    ['1', 'CRITICAL RPN=378', 'Automated renewal reminder (SMS+Email at 30-15-7 days)', 'IT+CRM', '2 Weeks', 'Reduce silent churn ~40%'],
    ['2', 'CRITICAL RPN=336', 'Monthly Fitness Assessment + personalised progress reports', 'Training', '1 Month', 'Reduce goal-dropout'],
    ['3', 'CRITICAL RPN=336', 'Live Crowd Tracker (mobile app or WhatsApp)', 'IT', '1 Month', 'Reduce peak frustration 60%'],
    ['4', 'CRITICAL RPN=320', 'Annual/Quarterly upgrade incentives (5-15% discount)', 'Sales', '2 Weeks', 'Convert 20% monthly to longer plans'],
    ['5', 'CRITICAL RPN=240', 'Mandatory structured onboarding (7-day program)', 'Floor Mgr', '1 Week', 'Reduce Month-1 churn'],
    ['6', 'CRITICAL RPN=210', 'Floor trainer 30-min non-PT check-in rounds', 'Trainers', 'Immediate', 'Improve satisfaction +0.5pt'],
    ['7', 'HIGH RPN=140', 'Auto payment retry + billing notification', 'Finance+IT', '3 Weeks', 'Eliminate payment-lapse churn'],
], widths=[Inches(0.25), Inches(0.8), Inches(2.1), Inches(0.75), Inches(0.75), Inches(1.95)])

# ==============================================================================
# SEC 8: CONTROL
# ==============================================================================
print("Generating Section 8: Control...")
doc.add_page_break()
sdiv(doc, '8. C - CONTROL PHASE: P-CHART')

hd(doc, '8.1 P-Chart - Statistical Process Control', size=12)
bd(doc, 'The P-Chart (Proportion Control Chart) monitors a binary outcome - member churns (1) or is retained (0). It tracks monthly churn proportion against 3-sigma control limits derived from the binomial distribution.')

callout(doc, 'Centre Line (CL)  = p-bar = Total churned / Total eligible (all months)\nUCL = p-bar + 3 x sqrt(p-bar x (1 - p-bar) / n_i)\nLCL = max(0,  p-bar - 3 x sqrt(p-bar x (1 - p-bar) / n_i))\nWhere n_i = eligible members in month i',
        title="P-CHART MATHEMATICAL FORMULAS")

tbl(doc, ['Parameter', 'Pre-Improvement (Y1, 12 months)', 'Post-Improvement (Y2, 6 months)'], [
    ['Monitoring Period', 'January - December Year 1', 'January - June Year 2'],
    ['Avg Eligible Members/Month', '~107', '~109'],
    ['Avg Monthly Churn Rate (CL)', '26.9%', '14.7%'],
    ['Upper Control Limit (UCL)', '~40.0%', '~25.5%'],
    ['Lower Control Limit (LCL)', '~13.8%', '~4.0%'],
    ['Out-of-Control Points', '0 (stable process)', '0 (stable process)'],
    ['Process Status', 'Stable but HIGH churn', 'Stable and IMPROVED'],
    ['Sigma Level', '~2.1 sigma', '~2.6 sigma (improving)'],
    ['Churn Reduction', 'Baseline reference', '45.2% reduction achieved'],
    ['Target Achievement', 'N/A (pre-improvement)', 'TARGET ACHIEVED (<15% CL)'],
], widths=[Inches(2.2), Inches(2.2), Inches(2.2)])

hd(doc, '8.2 P-Chart Results & Sustained Capability', size=12)
img(doc, os.path.join(IMG5, 'pchart_churn_control.png'), Inches(5.8),
    'Figure 8.1: P-Chart - Monthly Member Churn Rate with 3-Sigma Control Limits\n(Pre-Improvement Y1 Red | Post-Improvement Y2 Green | Vertical line = FMEA implementation)')

img(doc, os.path.join(IMG5, 'pchart_summary.png'), Inches(5.5),
    'Figure 8.2: Control Phase Summary - Average churn comparison, trend, and P-Chart statistics table')

callout(doc, 'The P-Chart demonstrates a statistically significant step-change improvement. Post-improvement mean churn rate reduced from 26.9% to 14.7% - a 45.2% reduction, successfully achieving the project target of <15%. The process is stable with all observations within 3-sigma control limits and zero special-cause violations.',
        title="CONTROL PHASE VERIFICATION")

# ==============================================================================
# SEC 9: CONCLUSION & RECOMMENDATIONS
# ==============================================================================
print("Generating Section 9: Conclusion...")
doc.add_page_break()
sdiv(doc, '9. CONCLUSION & RECOMMENDATIONS')
bd(doc, 'This Lean Six Sigma DMAIC project successfully applied a data-driven approach to identify, analyse, and address member churn at the Ultimate Fitness Centre. The project demonstrates that statistical analysis combined with targeted process improvements delivers measurable, sustained business results.')

hd(doc, 'Key Conclusions', size=12)
conclusions = [
    'Baseline monthly churn rate of ~27% placed the process at ~2.1 Sigma, below the 3 Sigma industry benchmark.',
    'Membership Plan Type is the strongest churn predictor. Monthly: 77% churn vs Quarterly: 21% vs Annual: 8% (Chi2 p<0.001).',
    'T-Tests confirmed churned members had significantly shorter tenure, lower plan amounts, and higher payment delays (all p<0.001).',
    'ANOVA showed Annual plan members rate Equipment Satisfaction (F=4.34, p=0.019) and Overall Satisfaction (F=4.89, p=0.012) significantly higher.',
    'Member Experience Survey (n=50) yielded NPS of +44. 80% were Likely Renewers. Overcrowding was the #2 churn reason.',
    'Levene F-Tests confirmed equal variances for all satisfaction variables (all p>0.05), validating parametric test assumptions.',
    'FMEA identified 7 CRITICAL failure modes (RPN>=200). No renewal reminder system (RPN=378) ranked highest.',
    'Post-improvement P-Chart: 45.2% churn reduction (26.9% to 14.7%), exceeding the project target of <15%.',
    'The improved process is statistically stable with all monthly observations within 3-sigma control limits.',
]
for i, c in enumerate(conclusions, 1):
    blt(doc, f'{i}. {c}')

hd(doc, 'Recommendations for Sustained Improvement', size=12)
recs = [
    'Continue monthly P-Chart monitoring; recalculate control limits every 6 months as the process stabilises.',
    'Expand Member Experience Survey to quarterly cadence (minimum 100 responses) for more robust inference.',
    'Implement CRM-driven loyalty programme to incentivise plan upgrades from monthly to quarterly/annual.',
    'Introduce member freeze/pause policy to prevent voluntary cancellations during travel or illness.',
    'Deploy live crowd-monitoring system to address the #2 surveyed churn driver: machine wait times.',
    'Conduct annual FMEA review to identify new failure modes as the business evolves.',
    'Track NPS quarterly as a leading indicator of future churn; target NPS >= 60 within 12 months.',
]
for r_text in recs:
    blt(doc, r_text)

# ==============================================================================
# SEC 10: REFERENCES
# ==============================================================================
print("Generating Section 10: References...")
sdiv(doc, '10. REFERENCES')
refs = [
    'Montgomery, D.C. (2020). Introduction to Statistical Quality Control, 8th Edition. John Wiley & Sons.',
    'George, M.L. (2002). Lean Six Sigma: Combining Six Sigma Quality with Lean Speed. McGraw-Hill.',
    'Pyzdek, T. & Keller, P. (2014). The Six Sigma Handbook, 4th Edition. McGraw-Hill Education.',
    'Stamatis, D.H. (2003). Failure Mode and Effect Analysis: FMEA from Theory to Execution. ASQ Quality Press.',
    'Breyfogle, F.W. (2003). Implementing Six Sigma: Smarter Solutions Using Statistical Methods. Wiley.',
    'Pande, P.S., Neuman, R.P. & Cavanagh, R.R. (2000). The Six Sigma Way. McGraw-Hill.',
    'IHRSA. (2023). Global Report on the Health Club Industry.',
    'Anderson, E.W. et al. (2004). Customer Satisfaction and Shareholder Value. Journal of Marketing, 68(4), 172-185.',
    'Hair, J.F. et al. (2019). Multivariate Data Analysis, 8th Edition. Cengage Learning.',
    'Reichheld, F.F. (2003). The One Number You Need to Grow (NPS). Harvard Business Review, 81(12), 46-54.',
    'SciPy Community. (2023). SciPy Statistical Functions Reference. https://docs.scipy.org',
]
for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f'[{i}]  ')
    sf(r1, font=FONT_TITLE, size=9.5, bold=True, color=RGB_BLACK)
    r2 = p.add_run(ref)
    sf(r2, font=FONT_CONTENT, size=9.5, color=RGB_BLACK)

# ==============================================================================
# APPLY PAGE BORDERS & SAVE
# ==============================================================================
print("Applying pure black page borders across all sections...")
apply_page_borders_bw(doc, sz="8", space="18")

docx_path = os.path.join(BASE, 'documents', 'Lean_Six_Sigma_DMAIC_Project_Report.docx')
doc.save(docx_path)
print(f'\nSUCCESSFULLY SAVED COMPACT B&W REPORT: {docx_path}')
print("="*60)
