import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import textwrap
import os

def create_five_whys_diagram(output_path, is_bw=False):
    """
    Generates a publication-grade Lean Six Sigma 5-Whys Root Cause Analysis diagram.
    Dimensions: 15.0 x 10.6 inches at 300 DPI.
    Optimized for executive clarity and crisp rendering in Microsoft Word reports.
    """
    fig = plt.figure(figsize=(15.0, 10.6), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 15.0)
    ax.set_ylim(0, 10.6)
    ax.axis('off')

    # Color definitions (Executive Six Sigma Palette)
    if is_bw:
        canvas_bg = '#FFFFFF'
        frame_edge = '#000000'
        hdr_bg = '#000000'
        hdr_text = '#FFFFFF'
        sub_text = '#CCCCCC'
        col_border = '#666666'
        footer_col = '#444444'
    else:
        canvas_bg = '#F8FAFC'
        frame_edge = '#CBD5E1'
        hdr_bg = '#0F172A'
        hdr_text = '#FFFFFF'
        sub_text = '#94A3B8'
        col_border = '#E2E8F0'
        footer_col = '#64748B'

    # Background canvas
    ax.add_patch(patches.Rectangle((0, 0), 15.0, 10.6, facecolor=canvas_bg, edgecolor='none'))

    # Outer decorative frame
    ax.add_patch(FancyBboxPatch((0.20, 0.20), 14.60, 10.20,
                                boxstyle="round,pad=0.04,rounding_size=0.12",
                                facecolor='#FFFFFF', edgecolor=frame_edge, linewidth=1.8, zorder=1))

    # ═══════════════════════════════════════════════════════════════════════════
    # TOP HEADER BANNER
    # ═══════════════════════════════════════════════════════════════════════════
    ax.add_patch(FancyBboxPatch((0.40, 9.55), 14.20, 0.72,
                                boxstyle="round,pad=0.03,rounding_size=0.08",
                                facecolor=hdr_bg, edgecolor=hdr_bg, linewidth=1.4, zorder=2))

    ax.text(7.50, 10.02, "5-WHYS ROOT CAUSE ANALYSIS — MEMBER RETENTION & CHURN",
            ha='center', va='center', fontsize=14.5, fontweight='bold', color=hdr_text,
            fontfamily='DejaVu Sans', zorder=3)
    ax.text(7.50, 9.74, "Lean Six Sigma DMAIC Analyze Phase · Ultimate Fitness Centre · Systemic Diagnostic Across Top Attrition Drivers",
            ha='center', va='center', fontsize=9.0, color=sub_text,
            fontfamily='DejaVu Sans', zorder=3)

    # ═══════════════════════════════════════════════════════════════════════════
    # BRANCH DEFINITIONS
    # ═══════════════════════════════════════════════════════════════════════════
    if is_bw:
        branches = [
            {
                'branch_num': 'BRANCH 1',
                'theme_color': '#000000',
                'accent_color': '#333333',
                'bg_light': '#F3F4F6',
                'title': 'RENEWAL & CRM AUTOMATION',
                'problem_title': 'High Non-Renewal & Silent Churn',
                'problem_stat': '77.0% Churn on 1-Month Plans · 53.8% Overall Total',
                'whys': [
                    ("Why do members fail to renew upon plan expiry?",
                     "Members lapse passively, lose daily workout habits, and forget their exact plan expiration date."),
                    ("Why do members lose track of expiration dates?",
                     "Zero automated reminders, renewal notifications, or invoices are delivered before lapse."),
                    ("Why does gym staff not follow up expiring members?",
                     "Front desk relies entirely on manual register lookups and ad-hoc verbal reminders."),
                    ("Why is expiry tracking not digitized or automated?",
                     "Gym uses static paper logs with no CRM software, trigger alerts, or renewal workflows."),
                    ("ROOT CAUSE IDENTIFIED",
                     "Complete absence of an automated CRM renewal reminder and lifecycle engagement communication system.")
                ],
                'countermeasure': 'Deploy automated SMS/WhatsApp renewal pipeline (T-30, T-15, T-7 days) with 1-click renewal links & lapse alerts.'
            },
            {
                'branch_num': 'BRANCH 2',
                'theme_color': '#000000',
                'accent_color': '#333333',
                'bg_light': '#F3F4F6',
                'title': 'CAPACITY & CROWD MANAGEMENT',
                'problem_title': 'Peak-Hour Congestion & Member Frustration',
                'problem_stat': 'Evening Peak (5:00 - 8:00 PM) · Machine Bottlenecks',
                'whys': [
                    ("Why do members express frustration and quit?",
                     "Severe equipment wait times (15–20+ mins) and overcrowding during evening peak hours."),
                    ("Why are machines unavailable during evening hours?",
                     "Over 68% of daily member visits are packed into a narrow 3-hour evening window."),
                    ("Why does member traffic cluster without distribution?",
                     "No slot reservation, live occupancy tracking, or tiered off-peak pricing exists."),
                    ("Why has management not instituted traffic balancing?",
                     "Facility lacks hourly attendance telemetry and live occupancy monitoring systems."),
                    ("ROOT CAUSE IDENTIFIED",
                     "Absence of crowd management mechanisms, capacity tracking, or demand-shifting pricing incentives.")
                ],
                'countermeasure': 'Introduce mobile live occupancy tracker, bookable peak workout slots, and a 20% discounted off-peak pricing tier.'
            },
            {
                'branch_num': 'BRANCH 3',
                'theme_color': '#000000',
                'accent_color': '#333333',
                'bg_light': '#F3F4F6',
                'title': 'ONBOARDING & GOAL TRACKING',
                'problem_title': 'Early Member Dropout & Motivation Loss',
                'problem_stat': 'Average Tenure 1.9 Months · Only 4% Enrolled in PT',
                'whys': [
                    ("Why do new members quit within the first 60 days?",
                     "Members lose initial enthusiasm, feel unsupported on the floor, and perceive zero progress."),
                    ("Why do members perceive zero measurable progress?",
                     "No initial baseline assessment, body composition check, or progress milestone tracking."),
                    ("Why are periodic fitness evaluations missing?",
                     "Floor trainers focus primarily on personal training clients (4%), leaving general members unguided."),
                    ("Why do trainers not engage general members?",
                     "No Standard Operating Procedure (SOP) or scheduled cadence exists for general member check-ins."),
                    ("ROOT CAUSE IDENTIFIED",
                     "Absence of a structured member onboarding journey and routine fitness milestone assessment cadence.")
                ],
                'countermeasure': 'Establish a mandatory 60-day onboarding SOP, bi-weekly trainer floor rounds, and monthly free fitness assessments.'
            }
        ]
    else:
        branches = [
            {
                'branch_num': 'BRANCH 1',
                'theme_color': '#1E3A8A',      # Deep Navy
                'accent_color': '#2563EB',     # Blue
                'bg_light': '#EFF6FF',
                'title': 'RENEWAL & CRM AUTOMATION',
                'problem_title': 'High Non-Renewal & Silent Churn',
                'problem_stat': '77.0% Churn on 1-Month Plans · 53.8% Overall Total',
                'whys': [
                    ("Why do members fail to renew upon plan expiry?",
                     "Members lapse passively, lose daily workout habits, and forget their exact plan expiration date."),
                    ("Why do members lose track of expiration dates?",
                     "Zero automated reminders, renewal notifications, or invoices are delivered before lapse."),
                    ("Why does gym staff not follow up expiring members?",
                     "Front desk relies entirely on manual register lookups and ad-hoc verbal reminders."),
                    ("Why is expiry tracking not digitized or automated?",
                     "Gym uses static paper logs with no CRM software, trigger alerts, or renewal workflows."),
                    ("ROOT CAUSE IDENTIFIED",
                     "Complete absence of an automated CRM renewal reminder and lifecycle engagement communication system.")
                ],
                'countermeasure': 'Deploy automated SMS/WhatsApp renewal pipeline (T-30, T-15, T-7 days) with 1-click renewal links & lapse alerts.'
            },
            {
                'branch_num': 'BRANCH 2',
                'theme_color': '#991B1B',      # Deep Red
                'accent_color': '#DC2626',     # Red
                'bg_light': '#FEF2F2',
                'title': 'CAPACITY & CROWD MANAGEMENT',
                'problem_title': 'Peak-Hour Congestion & Member Frustration',
                'problem_stat': 'Evening Peak (5:00 - 8:00 PM) · Machine Bottlenecks',
                'whys': [
                    ("Why do members express frustration and quit?",
                     "Severe equipment wait times (15–20+ mins) and overcrowding during evening peak hours."),
                    ("Why are machines unavailable during evening hours?",
                     "Over 68% of daily member visits are packed into a narrow 3-hour evening window."),
                    ("Why does member traffic cluster without distribution?",
                     "No slot reservation, live occupancy tracking, or tiered off-peak pricing exists."),
                    ("Why has management not instituted traffic balancing?",
                     "Facility lacks hourly attendance telemetry and live occupancy monitoring systems."),
                    ("ROOT CAUSE IDENTIFIED",
                     "Absence of crowd management mechanisms, capacity tracking, or demand-shifting pricing incentives.")
                ],
                'countermeasure': 'Introduce mobile live occupancy tracker, bookable peak workout slots, and a 20% discounted off-peak pricing tier.'
            },
            {
                'branch_num': 'BRANCH 3',
                'theme_color': '#065F46',      # Deep Forest Green
                'accent_color': '#059669',     # Green
                'bg_light': '#ECFDF5',
                'title': 'ONBOARDING & GOAL TRACKING',
                'problem_title': 'Early Member Dropout & Motivation Loss',
                'problem_stat': 'Average Tenure 1.9 Months · Only 4% Enrolled in PT',
                'whys': [
                    ("Why do new members quit within the first 60 days?",
                     "Members lose initial enthusiasm, feel unsupported on the floor, and perceive zero progress."),
                    ("Why do members perceive zero measurable progress?",
                     "No initial baseline assessment, body composition check, or progress milestone tracking."),
                    ("Why are periodic fitness evaluations missing?",
                     "Floor trainers focus primarily on personal training clients (4%), leaving general members unguided."),
                    ("Why do trainers not engage general members?",
                     "No Standard Operating Procedure (SOP) or scheduled cadence exists for general member check-ins."),
                    ("ROOT CAUSE IDENTIFIED",
                     "Absence of a structured member onboarding journey and routine fitness milestone assessment cadence.")
                ],
                'countermeasure': 'Establish a mandatory 60-day onboarding SOP, bi-weekly trainer floor rounds, and monthly free fitness assessments.'
            }
        ]

    col_w = 4.48
    col_gap = 0.38
    start_x = 0.40
    col_x_positions = [start_x + i * (col_w + col_gap) for i in range(3)]

    # Draw each branch column
    for col_idx, (b, cx) in enumerate(zip(branches, col_x_positions)):
        # Column container card
        ax.add_patch(FancyBboxPatch((cx, 0.42), col_w, 9.00,
                                   boxstyle="round,pad=0.03,rounding_size=0.09",
                                   facecolor='#FFFFFF', edgecolor=col_border, linewidth=1.3, zorder=2))

        # 1. Branch Header Badge
        ax.add_patch(FancyBboxPatch((cx + 0.12, 8.86), col_w - 0.24, 0.46,
                                   boxstyle="round,pad=0.02,rounding_size=0.06",
                                   facecolor=b['theme_color'], edgecolor='none', zorder=3))
        ax.text(cx + col_w / 2.0, 8.86 + 0.23, f"{b['branch_num']}: {b['title']}",
                ha='center', va='center', fontsize=9.6, fontweight='bold', color='#FFFFFF',
                fontfamily='DejaVu Sans', zorder=4)

        # 2. Problem Statement Box
        prob_y = 8.04
        prob_h = 0.68
        ax.add_patch(FancyBboxPatch((cx + 0.16, prob_y), col_w - 0.32, prob_h,
                                  boxstyle="round,pad=0.02,rounding_size=0.06",
                                  facecolor=b['bg_light'], edgecolor=b['accent_color'], linewidth=1.4, zorder=3))
        
        # Problem badge inside
        ax.add_patch(FancyBboxPatch((cx + 0.24, prob_y + prob_h - 0.20), 1.50, 0.17,
                                 boxstyle="round,pad=0.015,rounding_size=0.03",
                                 facecolor=b['accent_color'], edgecolor='none', zorder=4))
        ax.text(cx + 0.99, prob_y + prob_h - 0.115, "OBSERVED PROBLEM", ha='center', va='center',
                fontsize=6.8, fontweight='bold', color='#FFFFFF', fontfamily='DejaVu Sans', zorder=5)

        ax.text(cx + 0.24, prob_y + 0.30, b['problem_title'],
                ha='left', va='center', fontsize=8.6, fontweight='bold', color='#0F172A',
                fontfamily='DejaVu Sans', zorder=4)
        ax.text(cx + 0.24, prob_y + 0.13, b['problem_stat'],
                ha='left', va='center', fontsize=7.2, fontstyle='italic', color='#64748B',
                fontfamily='DejaVu Sans', zorder=4)

        # Down arrow from problem to Why 1
        ax.add_patch(FancyArrowPatch((cx + col_w / 2.0, prob_y), (cx + col_w / 2.0, 7.84),
                                     arrowstyle='->,head_width=3.0,head_length=4.0',
                                     color='#94A3B8', linewidth=1.5, zorder=3))

        # 3. The 5 Why steps
        why_y_starts = [7.04, 6.00, 4.96, 3.92, 2.45]
        card_heights = [0.80, 0.80, 0.80, 0.80, 1.25]

        for wi, ((q_text, a_text), y_pos, card_h) in enumerate(zip(b['whys'], why_y_starts, card_heights)):
            is_root = (wi == 4)
            card_top = y_pos + card_h

            if not is_root:
                # Regular Why Card (Why 1 to Why 4)
                ax.add_patch(FancyBboxPatch((cx + 0.16, y_pos), col_w - 0.32, card_h,
                                           boxstyle="round,pad=0.02,rounding_size=0.06",
                                           facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.1, zorder=3))

                # Why Pill (Level Indicator)
                ax.add_patch(FancyBboxPatch((cx + 0.24, card_top - 0.24), 0.80, 0.18,
                                          boxstyle="round,pad=0.015,rounding_size=0.03",
                                          facecolor=b['theme_color'], edgecolor='none', zorder=4))
                ax.text(cx + 0.64, card_top - 0.15, f"WHY #{wi+1}", ha='center', va='center',
                        fontsize=6.8, fontweight='bold', color='#FFFFFF', fontfamily='DejaVu Sans', zorder=5)

                # Question text
                q_wrapped = textwrap.fill(q_text, width=38)
                ax.text(cx + 1.12, card_top - 0.15, q_wrapped,
                        ha='left', va='center', fontsize=7.4, fontweight='bold', color=b['theme_color'],
                        fontfamily='DejaVu Sans', zorder=4)

                # Answer text with custom indented bullet
                a_wrapped = textwrap.fill(f"↳ {a_text}", width=44)
                ax.text(cx + 0.24, y_pos + 0.27, a_wrapped,
                        ha='left', va='center', fontsize=7.1, color='#334155',
                        fontfamily='DejaVu Sans', zorder=4)

                # Arrow connecting to next card
                if wi < 4:
                    next_top = why_y_starts[wi+1] + card_heights[wi+1]
                    ax.add_patch(FancyArrowPatch((cx + col_w / 2.0, y_pos), (cx + col_w / 2.0, next_top),
                                                arrowstyle='->,head_width=3.0,head_length=4.0',
                                                color='#94A3B8', linewidth=1.5, zorder=3))

            else:
                # ROOT CAUSE BOX (High Impact Red/Highlight Card)
                rc_bg = '#F3F4F6' if is_bw else '#FEF2F2'
                rc_edge = '#000000' if is_bw else '#DC2626'
                rc_badge_bg = '#000000' if is_bw else '#DC2626'
                rc_text_col = '#000000' if is_bw else '#991B1B'

                ax.add_patch(FancyBboxPatch((cx + 0.14, y_pos), col_w - 0.28, card_h,
                                              boxstyle="round,pad=0.02,rounding_size=0.07",
                                              facecolor=rc_bg, edgecolor=rc_edge, linewidth=1.8, zorder=4))

                # Root Cause Banner
                ax.add_patch(FancyBboxPatch((cx + 0.22, card_top - 0.26), col_w - 0.44, 0.22,
                                              boxstyle="round,pad=0.015,rounding_size=0.03",
                                              facecolor=rc_badge_bg, edgecolor='none', zorder=5))
                ax.text(cx + col_w / 2.0, card_top - 0.15, "★ ROOT CAUSE (SYSTEMIC DEFECT) ★",
                        ha='center', va='center', fontsize=7.4, fontweight='bold', color='#FFFFFF',
                        fontfamily='DejaVu Sans', zorder=6)

                # Root Cause Statement
                rc_wrapped = textwrap.fill(a_text, width=38)
                ax.text(cx + col_w / 2.0, y_pos + 0.48, rc_wrapped,
                        ha='center', va='center', fontsize=8.0, fontweight='bold', color=rc_text_col,
                        fontfamily='DejaVu Sans', zorder=5)

                # Arrow connecting to countermeasure
                cm_arr_col = '#333333' if is_bw else '#059669'
                ax.add_patch(FancyArrowPatch((cx + col_w / 2.0, y_pos), (cx + col_w / 2.0, 2.20),
                                               arrowstyle='->,head_width=3.0,head_length=4.0',
                                               color=cm_arr_col, linewidth=1.8, zorder=4))

        # 4. DMAIC Countermeasure Card (Improve Phase link)
        cm_y = 0.52
        cm_h = 1.68
        cm_bg = '#FAFAFA' if is_bw else '#F0FDF4'
        cm_edge = '#000000' if is_bw else '#16A34A'
        cm_badge_bg = '#333333' if is_bw else '#16A34A'
        cm_text_col = '#000000' if is_bw else '#14532D'

        ax.add_patch(FancyBboxPatch((cx + 0.16, cm_y), col_w - 0.32, cm_h,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor=cm_bg, edgecolor=cm_edge, linewidth=1.3, zorder=3))

        # Countermeasure Header Badge
        ax.add_patch(FancyBboxPatch((cx + 0.24, cm_y + cm_h - 0.24), col_w - 0.48, 0.21,
                                      boxstyle="round,pad=0.015,rounding_size=0.03",
                                      facecolor=cm_badge_bg, edgecolor='none', zorder=4))
        ax.text(cx + col_w / 2.0, cm_y + cm_h - 0.13, "DMAIC TARGETED COUNTERMEASURE",
                ha='center', va='center', fontsize=7.0, fontweight='bold', color='#FFFFFF',
                fontfamily='DejaVu Sans', zorder=5)

        cm_wrapped = textwrap.fill(b['countermeasure'], width=39)
        ax.text(cx + col_w / 2.0, cm_y + 0.65, cm_wrapped,
                ha='center', va='center', fontsize=7.3, color=cm_text_col,
                fontfamily='DejaVu Sans', zorder=4)

    # ═══════════════════════════════════════════════════════════════════════════
    # BOTTOM FOOTER NOTE
    # ═══════════════════════════════════════════════════════════════════════════
    footer_text = "Lean Six Sigma Conclusion: Member churn is driven by operational & engagement gaps (manual renewals, peak overcrowding, lack of onboarding), not facility quality."
    ax.text(7.50, 0.28, footer_text, ha='center', va='center',
            fontsize=7.8, fontstyle='italic', color=footer_col, fontfamily='DejaVu Sans', zorder=3)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated 5-Whys Diagram: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "output", "3_Analyze")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "five_whys_analysis.png")
    create_five_whys_diagram(out_file, is_bw=False)
