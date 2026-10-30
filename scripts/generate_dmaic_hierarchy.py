import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import textwrap
import os

def create_hierarchy_diagram_bw(output_path):
    fig = plt.figure(figsize=(20, 13.0), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13.0)
    ax.axis('off')

    # Pure White Background
    bg = patches.Rectangle((0, 0), 20, 13.0, facecolor='#FFFFFF', edgecolor='none')
    ax.add_patch(bg)

    # Outer decorative black frame
    outer_card = FancyBboxPatch((0.25, 0.25), 19.5, 12.5,
                               boxstyle="round,pad=0.06,rounding_size=0.12",
                               facecolor='#FFFFFF', edgecolor='#000000', linewidth=2.0)
    ax.add_patch(outer_card)

    # 1. Master Title Banner (Solid Black with White Text)
    title_box = FancyBboxPatch((0.55, 11.55), 18.9, 1.02,
                               boxstyle="round,pad=0.04,rounding_size=0.10",
                               facecolor='#000000', edgecolor='#000000', linewidth=1.5)
    ax.add_patch(title_box)

    ax.text(10.0, 12.18, "LEAN SIX SIGMA DMAIC METHODOLOGY — ANALYTICAL TOOLKIT HIERARCHY",
            ha='center', va='center', fontsize=17, fontweight='bold', color='#FFFFFF', fontname='Segoe UI')
    ax.text(10.0, 11.82, "Ultimate Fitness Centre Retention Project: Complete Hierarchy of Quality Frameworks, Statistical Hypothesis Tests & SPC Charts",
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#E5E7EB', fontname='Segoe UI')

    # 2. DMAIC Central Methodology Hub (Hierarchy Level 0)
    hub_box = FancyBboxPatch((7.2, 10.45), 5.6, 0.82,
                             boxstyle="round,pad=0.04,rounding_size=0.08",
                             facecolor='#000000', edgecolor='#000000', linewidth=1.5, zorder=5)
    ax.add_patch(hub_box)
    ax.text(10.0, 10.98, "DMAIC PROBLEM-SOLVING FRAMEWORK",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#FFFFFF', fontname='Segoe UI', zorder=6)
    ax.text(10.0, 10.66, "Data-Driven Continuous Improvement & Defect Reduction Process",
            ha='center', va='center', fontsize=8.8, color='#E5E7EB', fontname='Segoe UI', zorder=6)

    # Hierarchy Connector Lines (Black Tree Branching)
    trunk = patches.ConnectionPatch((10.0, 10.45), (10.0, 10.15), "data", "data",
                                    arrowstyle="-", color='#000000', linewidth=2.5, zorder=4)
    ax.add_patch(trunk)

    col_width = 3.62
    col_gap = 0.22
    left_start = 0.55
    centers = [left_start + i * (col_width + col_gap) + col_width / 2.0 for i in range(5)]

    bus_line = patches.ConnectionPatch((centers[0], 10.15), (centers[-1], 10.15), "data", "data",
                                      arrowstyle="-", color='#000000', linewidth=2.5, zorder=4)
    ax.add_patch(bus_line)

    for c_x in centers:
        drop_line = patches.ConnectionPatch((c_x, 10.15), (c_x, 9.85), "data", "data",
                                           arrowstyle="->,head_width=0.2,head_length=0.25",
                                           color='#000000', linewidth=2.2, zorder=4)
        ax.add_patch(drop_line)

    # Phase Data Structure in Pure Black & White / Grayscale
    phases = [
        {
            'letter': 'D',
            'title': 'DEFINE',
            'subtitle': 'Scope & Voice of Customer',
            'objective': 'Define problem scope, defect metrics, project charter, and voice of customer requirements.',
            'groups': [
                {
                    'heading': 'QUALITY FRAMEWORKS',
                    'items': [
                        ('Project Charter', 'Scope, business case, team & milestones'),
                        ('SIPOC Map', 'End-to-end 5-step process boundaries'),
                        ('VOC Translation', 'Customer needs to CTQ metric tree')
                    ]
                },
                {
                    'heading': 'CHARTS & METRICS',
                    'items': [
                        ('Primary CTQ Metric', 'Monthly Churn Rate (Baseline ~27%)'),
                        ('Secondary CTQ Metric', 'Member Renewal Rate (%)'),
                        ('Defect Definition', 'Non-renewal upon plan expiration')
                    ]
                },
                {
                    'heading': 'TARGET & GOAL',
                    'items': [
                        ('Target Churn Rate', '< 15% monthly attrition'),
                        ('Target Timeframe', '6 months post-implementation')
                    ]
                }
            ],
            'bottom_kpi': 'DELIVERABLE: Charter & CTQs Defined'
        },
        {
            'letter': 'M',
            'title': 'MEASURE',
            'subtitle': 'Baseline & Pareto Analysis',
            'objective': 'Quantify current baseline, calculate Process Sigma & DPMO, and isolate vital few drivers.',
            'groups': [
                {
                    'heading': 'CHARTS & PLOTS',
                    'items': [
                        ('Baseline Dashboard', 'KPI overview cards & distribution'),
                        ('Pareto 1: By Plan', 'Monthly plans = 77% churn (80/20)'),
                        ('Pareto 2: By Duration', '< 3 months duration drives 80%+ churn'),
                        ('Histograms', 'Tenure (skewed), Amount (bimodal)'),
                        ('Trend Chart', 'Monthly enrollment seasonality')
                    ]
                },
                {
                    'heading': 'BASELINE MEASUREMENTS',
                    'items': [
                        ('Overall Churn Rate', '27.2% per month (1 in 4 members)'),
                        ('Monthly Plan Churn', '77% (Primary vital few failure)'),
                        ('Mean Duration', '4.2 months average tenure'),
                        ('Mean Payment Gap', '2.1 days billing delay')
                    ]
                },
                {
                    'heading': 'PROCESS CAPABILITY',
                    'items': [
                        ('Baseline Sigma', '2.1 σ (Below 3.0 σ benchmark)'),
                        ('DPMO Calculation', '272,000 Defects Per Million')
                    ]
                }
            ],
            'bottom_kpi': 'BASELINE: 27.2% Churn | 2.1 Sigma'
        },
        {
            'letter': 'A',
            'title': 'ANALYZE',
            'subtitle': 'Hypothesis Tests & Root Causes',
            'objective': 'Subject potential churn drivers to statistical tests (α=0.05) and determine root causes.',
            'groups': [
                {
                    'heading': 'STATISTICAL HYPOTHESIS TESTS',
                    'items': [
                        ('Independent T-Tests', 'Active vs Churned (5 vars, p<0.001)'),
                        ('Chi-Square Tests', 'Plan Type vs Churn (χ²=87.4, p<0.001)'),
                        ('Levene F-Test', 'Equal variance confirmed (p > 0.05)'),
                        ('One-Way ANOVA', 'Equipment (p=0.019), Overall (p=0.012)'),
                        ('Survey Hypothesis', 'T-Test & Chi² on 50 respondents')
                    ]
                },
                {
                    'heading': 'CHARTS & ROOT-CAUSE PLOTS',
                    'items': [
                        ('Box Plot Panels', '6 satisfaction dimensions compared'),
                        ('Correlation Heatmap', 'Plan amount vs duration (r > 0.7)'),
                        ('Fishbone Diagram', '6M root cause analysis of churn'),
                        ('5-Whys Analysis', 'Root cause drill-down tree'),
                        ('VOC Review Themes', 'Sentiment on crowd & pricing')
                    ]
                },
                {
                    'heading': 'SURVEY INSIGHTS (n=50)',
                    'items': [
                        ('NPS Score', '+44 Net Promoter Score (56% Prom.)'),
                        ('#2 Churn Reason', 'Machine wait times & overcrowding'),
                        ('Lowest Rating', 'Value for Money (4.02 / 5.0)')
                    ]
                }
            ],
            'bottom_kpi': 'ROOT CAUSES: Statistically Validated'
        },
        {
            'letter': 'I',
            'title': 'IMPROVE',
            'subtitle': 'FMEA Risk Priority & Actions',
            'objective': 'Evaluate failure modes via FMEA, prioritize with RPN, and execute targeted countermeasures.',
            'groups': [
                {
                    'heading': 'FMEA & RISK ASSESSMENT',
                    'items': [
                        ('FMEA Matrix', 'Scored Severity × Occurrence × Detect'),
                        ('Critical Failures', '7 failure modes with RPN ≥ 200'),
                        ('Top Risk Mode', 'No renewal reminders (RPN = 378)'),
                        ('#2 Risk Mode', 'No progress tracking (RPN = 336)')
                    ]
                },
                {
                    'heading': 'CHARTS & RISK VISUALS',
                    'items': [
                        ('RPN Pareto Chart', 'Failure modes ranked by RPN score'),
                        ('FMEA Risk Matrix', 'Severity vs Occurrence bubble plot'),
                        ('Implementation Plan', 'Owner, timeline & impact roadmap')
                    ]
                },
                {
                    'heading': 'TARGETED COUNTERMEASURES',
                    'items': [
                        ('CRM Auto Reminders', '30-15-7 days multi-channel alert'),
                        ('Member Assessment', 'Monthly fitness check & goal report'),
                        ('Crowd Management', 'Live capacity tracker for gym'),
                        ('Plan Upsell Offer', '10-15% discount for longer plans')
                    ]
                }
            ],
            'bottom_kpi': 'COUNTERMEASURES: 7 Deployed'
        },
        {
            'letter': 'C',
            'title': 'CONTROL',
            'subtitle': 'SPC P-Chart & Sustained Gains',
            'objective': 'Monitor churn with Statistical Process Control (P-Chart), sustain gains, and institutionalize SOPs.',
            'groups': [
                {
                    'heading': 'SPC CHARTS & FORMULAS',
                    'items': [
                        ('P-Chart Tracking', 'Proportion defective with 3σ limits'),
                        ('Pre vs Post Chart', 'Before (Y1) vs After (Y2) step-change'),
                        ('SPC Stability Rules', '0 points beyond UCL/LCL (stable)'),
                        ('Summary Dashboard', 'Trend, capability & variance summary')
                    ]
                },
                {
                    'heading': 'VERIFIED RESULTS',
                    'items': [
                        ('Baseline Churn (Y1)', 'CL = 26.9% monthly churn'),
                        ('Improved Churn (Y2)', 'CL = 14.7% monthly churn'),
                        ('Net Churn Reduction', '45.2% statistically verified reduction'),
                        ('Target Attained', 'Exceeded < 15% churn target'),
                        ('Sigma Level Gain', 'Improved from 2.1 σ to 2.6 σ')
                    ]
                },
                {
                    'heading': 'STANDARDIZATION & SOPS',
                    'items': [
                        ('Audit Protocol', 'Monthly SPC review cadence'),
                        ('Response Plan', 'Trigger protocol if churn exceeds 20%'),
                        ('SOP Documentation', 'Onboarding & reminder operations')
                    ]
                }
            ],
            'bottom_kpi': 'RESULT: 45.2% Churn Cut | 2.6 Sigma'
        }
    ]

    col_h = 9.35

    for i, p in enumerate(phases):
        x = left_start + i * (col_width + col_gap)

        # Column background card (White with Black border)
        card = FancyBboxPatch((x, 0.45), col_width, col_h,
                              boxstyle="round,pad=0.04,rounding_size=0.12",
                              facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.6, zorder=2)
        ax.add_patch(card)

        # Header Badge (Solid Black with White Text)
        badge_y = 8.85
        badge_h = 0.95
        badge_box = FancyBboxPatch((x + 0.08, badge_y), col_width - 0.16, badge_h,
                                   boxstyle="round,pad=0.03,rounding_size=0.08",
                                   facecolor='#000000', edgecolor='#000000', linewidth=1.2, zorder=3)
        ax.add_patch(badge_box)

        # Letter Icon Circle (White circle with Black text)
        circ = patches.Circle((x + 0.52, badge_y + 0.48), 0.35, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=4)
        ax.add_patch(circ)
        ax.text(x + 0.52, badge_y + 0.47, p['letter'], ha='center', va='center',
                fontsize=16, fontweight='bold', color='#000000', fontname='Segoe UI', zorder=5)

        # Title & Subtitle in Badge
        ax.text(x + 1.02, badge_y + 0.63, p['title'], ha='left', va='center',
                fontsize=13, fontweight='bold', color='#FFFFFF', fontname='Segoe UI', zorder=5)
        ax.text(x + 1.02, badge_y + 0.30, p['subtitle'], ha='left', va='center',
                fontsize=8.0, fontstyle='italic', color='#E5E7EB', fontname='Segoe UI', zorder=5)

        # Objective Pill Box (Light grayscale tint #F9FAFB with black border)
        obj_y = 8.16
        obj_h = 0.60
        obj_box = FancyBboxPatch((x + 0.10, obj_y), col_width - 0.20, obj_h,
                                 boxstyle="round,pad=0.02,rounding_size=0.06",
                                 facecolor='#F3F4F6', edgecolor='#000000', linewidth=0.9, zorder=3)
        ax.add_patch(obj_box)
        wrapped_obj = textwrap.fill(p['objective'], width=40)
        ax.text(x + col_width/2, obj_y + obj_h/2, wrapped_obj,
                ha='center', va='center', fontsize=7.2, color='#000000', fontname='Segoe UI',
                linespacing=1.2, zorder=4)

        # Content Groups
        curr_y = 8.04
        for g_idx, grp in enumerate(p['groups']):
            curr_y -= 0.28
            # Section Header Bar (Light Gray with Black border)
            header_w = col_width - 0.20
            sec_bar = FancyBboxPatch((x + 0.10, curr_y - 0.04), header_w, 0.27,
                                     boxstyle="round,pad=0.01,rounding_size=0.04",
                                     facecolor='#E5E7EB', edgecolor='#000000', linewidth=0.8, zorder=3)
            ax.add_patch(sec_bar)

            # Bullet dot in header
            dot = patches.Circle((x + 0.24, curr_y + 0.10), 0.042, facecolor='#000000', edgecolor='none', zorder=4)
            ax.add_patch(dot)

            ax.text(x + 0.36, curr_y + 0.10, grp['heading'],
                    ha='left', va='center', fontsize=7.6, fontweight='bold', color='#000000',
                    fontname='Segoe UI', zorder=4)

            for item_title, item_desc in grp['items']:
                curr_y -= 0.37
                # Bullet dot
                b_dot = patches.Circle((x + 0.22, curr_y + 0.14), 0.026, facecolor='#000000', edgecolor='none', zorder=4)
                ax.add_patch(b_dot)

                # Bold title (Black)
                ax.text(x + 0.32, curr_y + 0.16, item_title,
                        ha='left', va='center', fontsize=7.2, fontweight='bold', color='#000000',
                        fontname='Segoe UI', zorder=4)
                # Descriptive line (Charcoal Black)
                ax.text(x + 0.32, curr_y + 0.01, item_desc,
                        ha='left', va='center', fontsize=6.6, color='#1F2937',
                        fontname='Segoe UI', zorder=4)

        # Bottom KPI Outcome Badge (Solid Black with White Text)
        bot_box = FancyBboxPatch((x + 0.10, 0.55), col_width - 0.20, 0.44,
                                 boxstyle="round,pad=0.02,rounding_size=0.06",
                                 facecolor='#000000', edgecolor='#000000', linewidth=1.0, zorder=3)
        ax.add_patch(bot_box)
        ax.text(x + col_width/2, 0.77, p['bottom_kpi'],
                ha='center', va='center', fontsize=7.8, fontweight='bold',
                color='#FFFFFF', fontname='Segoe UI', zorder=4)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print(f"Successfully generated black-and-white hierarchy diagram at: {output_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_img = os.path.join(base_dir, "output", "dmaic_hierarchy_diagram.png")
    create_hierarchy_diagram_bw(out_img)
