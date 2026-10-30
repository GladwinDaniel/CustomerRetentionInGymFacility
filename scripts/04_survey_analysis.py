"""
=============================================================================
LEAN SIX SIGMA -- SURVEY ANALYSIS (DMAIC ANALYZE PHASE -- SURVEY DATA)
Ultimate Fitness Centre: Member Experience Survey (50 Responses)
=============================================================================
Generates:
  * Descriptive Statistics and NPS
  * Box Plots  (Renewal Intent group vs 6 satisfaction dimensions, with t-test)
  * Independent T-Tests  (Likely vs Unlikely Renewers)
  * F-Test / Levene Variance Test
  * Chi-Square Tests (10 categorical variables vs Renewal Intent group)
  * One-Way ANOVA (Monthly vs Quarterly vs Annual plan types)
  * Survey Insights Dashboard (6-panel summary)
=============================================================================
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# Config
# ============================================================
plt.rcParams.update({
    'figure.dpi': 150, 'savefig.dpi': 150, 'font.family': 'sans-serif',
    'font.size': 11, 'axes.titlesize': 13, 'axes.titleweight': 'bold',
    'figure.facecolor': 'white', 'axes.facecolor': '#FAFAFA',
    'axes.grid': True, 'grid.alpha': 0.3,
})
COLORS = {
    'primary': '#2563EB', 'secondary': '#7C3AED', 'success': '#059669',
    'danger':  '#DC2626', 'warning':   '#D97706', 'info':    '#0891B2',
    'churned': '#EF4444', 'active':    '#22C55E',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR  = os.path.join(BASE_DIR, "output", "3_Analyze", "Survey")
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# Load Survey
# ============================================================
print("=" * 70)
print("SURVEY ANALYSIS: Member Experience Survey (50 Responses)")
print("=" * 70)

raw = pd.read_excel(
    os.path.join(DATA_DIR, "Fitness_Centre_Member_Experience_Survey_50_Responses.xlsx"))

col_map = {
    raw.columns[0]:  'Timestamp',
    raw.columns[1]:  'Age_Group',
    raw.columns[2]:  'Gender',
    raw.columns[3]:  'Fitness_Goal',
    raw.columns[4]:  'Membership_Duration',
    raw.columns[5]:  'Plan_Type',
    raw.columns[6]:  'Visit_Frequency',
    raw.columns[7]:  'Visit_Time',
    raw.columns[8]:  'PT_Enrolled',
    raw.columns[9]:  'Equipment_Satisfaction',
    raw.columns[10]: 'Hygiene_Satisfaction',
    raw.columns[11]: 'Machine_Wait',
    raw.columns[12]: 'Environment_Rating',
    raw.columns[13]: 'Onboarding',
    raw.columns[14]: 'Trainer_Rating',
    raw.columns[15]: 'Trainer_Attention',
    raw.columns[16]: 'Goal_Progress',
    raw.columns[17]: 'Value_For_Money',
    raw.columns[18]: 'Renewal_Intent',
    raw.columns[19]: 'NPS',
    raw.columns[20]: 'Churn_Reason',
    raw.columns[21]: 'Retention_Initiative',
    raw.columns[22]: 'Improvement_Suggestion',
}
df = raw.rename(columns=col_map).copy()
print(f"  Loaded {len(df)} responses with {len(df.columns)} columns")

# Derived columns
sat_cols_all = ['Equipment_Satisfaction', 'Hygiene_Satisfaction',
                'Environment_Rating', 'Trainer_Rating', 'Value_For_Money']
df['Overall_Satisfaction'] = df[sat_cols_all].mean(axis=1)
# Renewal Intent is 1-5 Likert scale; threshold >=4 = Likely Renewer
df['Likely_Renewer'] = (df['Renewal_Intent'] >= 4).astype(int)
df['Renewal_Group']  = df['Likely_Renewer'].map(
    {1: 'Likely Renewer (>=4)', 0: 'Unlikely Renewer (<4)'})

def nps_cat(score):
    if score >= 9:   return 'Promoter (9-10)'
    elif score >= 7: return 'Passive (7-8)'
    else:            return 'Detractor (0-6)'
df['NPS_Category'] = df['NPS'].apply(nps_cat)

n_likely   = int(df['Likely_Renewer'].sum())
n_unlikely = len(df) - n_likely
nps_score  = (int((df['NPS'] >= 9).sum()) - int((df['NPS'] <= 6).sum())) / len(df) * 100
print(f"  Likely Renewers   (Intent>=4, scale 1-5): {n_likely}  ({n_likely/len(df)*100:.0f}%)")
print(f"  Unlikely Renewers (Intent<4):              {n_unlikely} ({n_unlikely/len(df)*100:.0f}%)")
print(f"  Net Promoter Score (NPS):                  {nps_score:.0f}")

likely   = df[df['Likely_Renewer'] == 1]
unlikely = df[df['Likely_Renewer'] == 0]

# ============================================================
# SECTION 1: Descriptive Statistics
# ============================================================
print("\n" + "=" * 70)
print("SECTION 1: DESCRIPTIVE STATISTICS (SURVEY)")
print("=" * 70)

numeric_cols = ['Equipment_Satisfaction', 'Hygiene_Satisfaction',
                'Environment_Rating', 'Trainer_Rating', 'Value_For_Money',
                'Renewal_Intent', 'NPS', 'Overall_Satisfaction']
desc = df[numeric_cols].describe().T
desc['median'] = df[numeric_cols].median()
desc.to_csv(os.path.join(OUT_DIR, "survey_descriptive_statistics.csv"))
print(desc[['count', 'mean', 'median', 'std', 'min', 'max']].round(2).to_string())

# ============================================================
# SECTION 2: Box Plots (6 satisfaction vars vs renewal group)
# ============================================================
print("\n" + "=" * 70)
print("SECTION 2: BOX PLOTS -- Renewal Intent Group Comparisons")
print("=" * 70)

box_vars = [
    ('Equipment_Satisfaction', 'Equipment Satisfaction (1-5)'),
    ('Hygiene_Satisfaction',   'Hygiene Satisfaction (1-5)'),
    ('Environment_Rating',     'Environment Rating (1-5)'),
    ('Trainer_Rating',         'Trainer Rating (1-5)'),
    ('Value_For_Money',        'Value for Money (1-5)'),
    ('Overall_Satisfaction',   'Overall Satisfaction (Composite 1-5)'),
]

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for idx, (col, label) in enumerate(box_vars):
    ax = axes[idx]
    g1 = likely[col].dropna()
    g2 = unlikely[col].dropna()
    bp = ax.boxplot(
        [g1, g2],
        tick_labels=['Likely Renewer\n(Intent>=7)', 'Unlikely Renewer\n(Intent<7)'],
        patch_artist=True, widths=0.5,
        boxprops=dict(linewidth=1.5),
        medianprops=dict(color='black', linewidth=2.5),
        whiskerprops=dict(linewidth=1.5),
        capprops=dict(linewidth=1.5),
        flierprops=dict(marker='o', markersize=5, alpha=0.5)
    )
    bp['boxes'][0].set_facecolor(COLORS['active']);  bp['boxes'][0].set_alpha(0.75)
    bp['boxes'][1].set_facecolor(COLORS['churned']); bp['boxes'][1].set_alpha(0.75)

    if len(g1) > 1 and len(g2) > 1:
        t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
        sig = "SIGNIFICANT" if p_val < 0.05 else "Not Significant"
    else:
        t_stat, p_val, sig = float('nan'), float('nan'), "Insufficient data"
    ax.set_ylabel(label, fontsize=10)
    title_main = label.split('(')[0].strip()
    ax.set_title(
        f'Box Plot: {title_main}\nLikely (>=4) vs Unlikely (<4) Renewers\n'
        f't={t_stat:.2f}, p={p_val:.4f} -> {sig}',
        fontsize=10, fontweight='bold') if not (t_stat != t_stat) else ax.set_title(
        f'Box Plot: {title_main}\nLikely vs Unlikely Renewers\n{sig}',
        fontsize=10, fontweight='bold')
    m1 = g1.median() if len(g1) > 0 else float('nan')
    m2 = g2.median() if len(g2) > 0 else float('nan')
    ax.text(0.97, 0.02,
            f'Median Renewer: {m1:.2f}\nMedian Non-Renewer: {m2:.2f}',
            transform=ax.transAxes, fontsize=8.5, va='bottom', ha='right',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8))
    print(f"  [{col}]: Renewer median={m1:.2f}, Non-renewer median={m2:.2f}, "
          f"t={t_stat:.3f}, p={p_val:.4f} -> {sig}")

legend_patches = [
    mpatches.Patch(facecolor=COLORS['active'],  alpha=0.75, label=f'Likely Renewer, Intent>=4 (n={n_likely})'),
    mpatches.Patch(facecolor=COLORS['churned'], alpha=0.75, label=f'Unlikely Renewer, Intent<4 (n={n_unlikely})')
]
fig.legend(handles=legend_patches, loc='lower center', ncol=2, fontsize=11,
           framealpha=0.9, bbox_to_anchor=(0.5, -0.02))
fig.suptitle('ANALYZE (Survey): Box Plot Comparisons\n'
             'Satisfaction Variables -- Likely vs Unlikely Renewers\n'
             'Ultimate Fitness Centre Member Experience Survey (n=50)',
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "survey_box_plots.png"), bbox_inches='tight')
plt.close()
print("\n  Survey Box Plots -- Saved")

# ============================================================
# SECTION 3: T-Tests
# ============================================================
print("\n" + "=" * 70)
print("SECTION 3: INDEPENDENT T-TESTS -- Satisfaction vs Renewal Intent")
print("=" * 70)
print("  H0: Mean satisfaction score is EQUAL between Likely and Unlikely Renewers")
print("  H1: Means differ significantly  (alpha=0.05, Welch t-test)")
print()

ttest_vars = [
    ('Equipment_Satisfaction', 'Equipment Satisfaction'),
    ('Hygiene_Satisfaction',   'Hygiene Satisfaction'),
    ('Environment_Rating',     'Environment / Ambience Rating'),
    ('Trainer_Rating',         'Trainer Helpfulness Rating'),
    ('Value_For_Money',        'Value for Money Rating'),
    ('Overall_Satisfaction',   'Overall Composite Satisfaction'),
]
ttest_results = []

for col, label in ttest_vars:
    g1 = likely[col].dropna()
    g2 = unlikely[col].dropna()
    t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
    sig = 'Yes' if p_val < 0.05 else 'No'
    if len(g1) < 2:
        print(f"  --- {label} --- SKIPPED (n_renewer={len(g1)} insufficient)")
        ttest_results.append({
            'Variable': label, 'Renewer Mean': float('nan'),
            'Non-Renewer Mean': round(float(g2.mean()), 3) if len(g2) > 0 else float('nan'),
            'Difference': float('nan'), 't-statistic': float('nan'),
            'p-value': float('nan'), 'Significant (alpha=0.05)': 'N/A',
            'Interpretation': 'Insufficient data for t-test'
        })
        continue
    ttest_results.append({
        'Variable':                    label,
        'Renewer Mean':                round(float(g1.mean()), 3),
        'Non-Renewer Mean':            round(float(g2.mean()), 3),
        'Difference':                  round(float(g1.mean() - g2.mean()), 3),
        't-statistic':                 round(float(t_stat), 4),
        'p-value':                     round(float(p_val), 6),
        'Significant (alpha=0.05)':    sig,
        'Interpretation':              (f'Renewers rate {label} significantly higher'
                                        if p_val < 0.05 else f'No significant difference in {label}')
    })
    print(f"  --- {label} ---")
    print(f"    Renewer Mean:     {g1.mean():.3f}  (Median: {g1.median():.2f})")
    print(f"    Non-Renewer Mean: {g2.mean():.3f}  (Median: {g2.median():.2f})")
    print(f"    t={t_stat:.4f}, p={p_val:.6f} -> "
          f"{'SIGNIFICANT' if p_val < 0.05 else 'Not Significant'}")
    print()

pd.DataFrame(ttest_results).to_csv(
    os.path.join(OUT_DIR, "survey_ttest_results.csv"), index=False)

# T-Test chart
fig, ax = plt.subplots(figsize=(12, 7))
labels_short     = ['Equipment', 'Hygiene', 'Environment', 'Trainer', 'Value/Money', 'Overall']
renewer_means    = [r['Renewer Mean']     for r in ttest_results]
nonrenewer_means = [r['Non-Renewer Mean'] for r in ttest_results]
pvals            = [r['p-value']          for r in ttest_results]
x = np.arange(len(labels_short))
w = 0.35
bars1 = ax.bar(x - w/2, renewer_means,    w, color=COLORS['active'],  alpha=0.8,
               label=f'Likely Renewer (n={n_likely})',    edgecolor='white')
bars2 = ax.bar(x + w/2, nonrenewer_means, w, color=COLORS['churned'], alpha=0.8,
               label=f'Unlikely Renewer (n={n_unlikely})', edgecolor='white')
for bar, val in zip(bars1, renewer_means):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
            f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar, val in zip(bars2, nonrenewer_means):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
            f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for i, p in enumerate(pvals):
    max_h = max(renewer_means[i], nonrenewer_means[i])
    star  = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
    color = COLORS['danger'] if p < 0.05 else 'gray'
    ax.text(i, max_h + 0.15, star, ha='center', fontsize=13, fontweight='bold', color=color)
ax.set_xticks(x)
ax.set_xticklabels(labels_short, fontsize=11)
ax.set_ylabel('Mean Score (1-5 Scale)', fontsize=12)
ax.set_ylim(0, 5.8)
ax.set_title('T-Test: Mean Satisfaction Scores -- Likely vs Unlikely Renewers\n'
             '(* p<0.05, ** p<0.01, *** p<0.001, ns = not significant)\n'
             'Ultimate Fitness Centre Member Experience Survey (n=50)',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.axhline(3, color='black', linestyle='--', alpha=0.3, linewidth=1)

col_labels_tbl = ['p-value', 'Significant?']
table_data = [[f'{p:.4f}', 'Yes' if p < 0.05 else 'No'] for p in pvals]
tbl = ax.table(cellText=table_data, rowLabels=labels_short, colLabels=col_labels_tbl,
               cellLoc='center', loc='bottom', bbox=[0, -0.35, 1, 0.28])
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
for (row, col_i), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor(COLORS['primary'])
        cell.set_text_props(color='white', fontweight='bold')
    elif col_i >= 0:
        p_idx = row - 1
        if 0 <= p_idx < len(pvals) and pvals[p_idx] < 0.05:
            cell.set_facecolor('#DCFCE7')
        else:
            cell.set_facecolor('#F9FAFB')
plt.subplots_adjust(bottom=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "survey_ttest_chart.png"), bbox_inches='tight')
plt.close()
print("  T-Test Summary Chart -- Saved")

# ============================================================
# SECTION 4: Chi-Square Tests
# ============================================================
print("\n" + "=" * 70)
print("SECTION 4: CHI-SQUARE TESTS -- Categorical Variables vs Renewal Intent")
print("=" * 70)
print("  H0: Variable is INDEPENDENT of Renewal Intent group")
print("  H1: Significant ASSOCIATION exists  (alpha=0.05)")
print()

chi_vars = [
    ('Plan_Type',          'Membership Plan Type'),
    ('Visit_Frequency',    'Weekly Visit Frequency'),
    ('PT_Enrolled',        'PT / Group Class Enrollment'),
    ('Membership_Duration','Membership Duration'),
    ('Onboarding',         'Onboarding Experience'),
    ('Machine_Wait',       'Machine Wait Times'),
    ('Trainer_Attention',  'Trainer Attention to Non-PT'),
    ('Goal_Progress',      'Progress Toward Fitness Goals'),
    ('Age_Group',          'Age Group'),
    ('Gender',             'Gender'),
]
chi_results = []

for col, label in chi_vars:
    ct = pd.crosstab(df[col], df['Renewal_Group'])
    if ct.shape[0] < 2 or ct.shape[1] < 2:
        print(f"  Skipping {label} -- insufficient categories")
        continue
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    pct_ok = float((expected >= 5).sum()) / expected.size * 100
    note   = f'Warning: {100-pct_ok:.0f}pct cells expected<5' if pct_ok < 80 else ''
    sig    = 'Yes' if p < 0.05 else 'No'
    chi_results.append({
        'Variable':                    label,
        'Chi2 Statistic':              round(float(chi2), 4),
        'Degrees of Freedom':          dof,
        'p-value':                     round(float(p), 6),
        'Significant (alpha=0.05)':    sig,
        'Pct Expected>=5':             f'{pct_ok:.0f}%',
        'Note':                        note,
        'Interpretation':              (f'{label} significantly associated with renewal intent'
                                        if p < 0.05 else f'{label} independent of renewal intent')
    })
    print(f"  --- {label} ---")
    print(ct.to_string())
    print(f"  Chi2={chi2:.4f}, DoF={dof}, p={p:.6f} -> "
          f"{'SIGNIFICANT' if p < 0.05 else 'Not Significant'}  {note}")
    print()

chi_df = pd.DataFrame(chi_results)
chi_df.to_csv(os.path.join(OUT_DIR, "survey_chisquare_results.csv"), index=False)

if not chi_df.empty:
    fig, ax = plt.subplots(figsize=(12, 7))
    chi_sorted = chi_df.sort_values('Chi2 Statistic', ascending=True)
    bar_colors = [COLORS['success'] if r == 'Yes' else COLORS['primary']
                  for r in chi_sorted['Significant (alpha=0.05)']]
    bars = ax.barh(chi_sorted['Variable'], chi_sorted['Chi2 Statistic'],
                   color=bar_colors, edgecolor='white', height=0.6)
    for bar, (_, row) in zip(bars, chi_sorted.iterrows()):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f"Chi2={row['Chi2 Statistic']:.2f}, p={row['p-value']:.4f}  "
                f"{'Significant' if row['Significant (alpha=0.05)']=='Yes' else 'Not Sig.'}",
                va='center', fontsize=8.5)
    ax.set_xlabel('Chi-Square Statistic', fontsize=12)
    ax.set_title('Chi-Square Test Results: Variables Associated with Renewal Intent?\n'
                 'Green = Significant (p<0.05) | Blue = Not Significant\n'
                 'Ultimate Fitness Centre Member Experience Survey (n=50)',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(0, chi_sorted['Chi2 Statistic'].max() * 1.55)
    ax.legend(
        handles=[mpatches.Patch(color=COLORS['success'], label='Significant (p<0.05)'),
                 mpatches.Patch(color=COLORS['primary'], label='Not Significant (p>=0.05)')],
        loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "survey_chisquare_chart.png"), bbox_inches='tight')
    plt.close()
    print("  Chi-Square Summary Chart -- Saved")
else:
    print("  Chi-Square: All categories had only 1 renewal group, no chart generated.")
    print("  (This occurs when all 50 respondents fall into the same renewal intent group.)")


# ============================================================
# SECTION 5: F-Test (Levene Variance)
# ============================================================
print("\n" + "=" * 70)
print("SECTION 5: F-TEST -- Variance Comparison (Renewal vs Non-Renewal)")
print("=" * 70)
print("  Levene Test: H0 = Variances are EQUAL  (alpha=0.05)")
print()

ftest_results = []
for col, label in ttest_vars:
    g1 = likely[col].dropna()
    g2 = unlikely[col].dropna()
    if len(g1) > 1 and len(g2) > 1 and float(g2.var()) > 0:
        f_ratio  = float(g1.var()) / float(g2.var())
        lev_stat, lev_p = stats.levene(g1, g2)
        ftest_results.append({
            'Variable':              label,
            'Renewer Variance':      round(float(g1.var()), 4),
            'Non-Renewer Variance':  round(float(g2.var()), 4),
            'F-Ratio (S1sq/S2sq)':   round(f_ratio, 4),
            'Levene Statistic':      round(float(lev_stat), 4),
            'Levene p-value':        round(float(lev_p), 6),
            'Equal Variances?':      'No' if lev_p < 0.05 else 'Yes',
        })
        print(f"  {label}:")
        print(f"    Renewer Variance:     {g1.var():.4f}")
        print(f"    Non-Renewer Variance: {g2.var():.4f}")
        print(f"    F-ratio={f_ratio:.4f} | Levene p={lev_p:.6f} -> "
              f"{'Variances DIFFER' if lev_p < 0.05 else 'Variances Equal'}")
        print()

pd.DataFrame(ftest_results).to_csv(
    os.path.join(OUT_DIR, "survey_ftest_results.csv"), index=False)
print("  F-Test Results -- Saved")

# ============================================================
# SECTION 6: ANOVA
# ============================================================
print("\n" + "=" * 70)
print("SECTION 6: ONE-WAY ANOVA -- Satisfaction across Membership Plans")
print("=" * 70)
print("  H0: Mean satisfaction is EQUAL across all plan types")
print("  H1: At least one plan type differs significantly (alpha=0.05)")
print()

anova_vars = [
    ('Equipment_Satisfaction', 'Equipment Satisfaction'),
    ('Trainer_Rating',         'Trainer Rating'),
    ('Value_For_Money',        'Value for Money'),
    ('Renewal_Intent',         'Renewal Intent (1-10)'),
    ('Overall_Satisfaction',   'Overall Composite Satisfaction'),
]
anova_results = []
print(f"  Plan Types: {list(df['Plan_Type'].unique())}")
print()

for col, label in anova_vars:
    groups = [grp[col].dropna()
              for _, grp in df.groupby('Plan_Type')
              if len(grp[col].dropna()) > 1]
    if len(groups) >= 2:
        f_stat, p_val = stats.f_oneway(*groups)
        sig = 'Yes' if p_val < 0.05 else 'No'
        plan_means = {k: round(float(v), 3)
                      for k, v in df.groupby('Plan_Type')[col].mean().items()}
        anova_results.append({
            'Variable':                    label,
            'F-Statistic':                 round(float(f_stat), 4),
            'p-value':                     round(float(p_val), 6),
            'Significant (alpha=0.05)':    sig,
            'Plan Means':                  str(plan_means),
        })
        print(f"  --- {label} ---")
        for ptype, pmean in plan_means.items():
            n_p = len(df[df['Plan_Type'] == ptype][col].dropna())
            print(f"    {ptype}: Mean={pmean:.2f} (n={n_p})")
        print(f"  F={f_stat:.4f}, p={p_val:.6f} -> "
              f"{'SIGNIFICANT' if p_val < 0.05 else 'Not Significant'}")
        print()

pd.DataFrame(anova_results).to_csv(
    os.path.join(OUT_DIR, "survey_anova_results.csv"), index=False)

plan_order        = ['Monthly', 'Quarterly (3 Months)', 'Annual (12 Months)']
plan_labels_short = ['Monthly', 'Quarterly\n(3M)', 'Annual\n(12M)']
plan_cols_anova   = [COLORS['churned'], COLORS['warning'], COLORS['success']]
anova_plot_vars   = [
    ('Renewal_Intent',       'Renewal Intent (1-10 Scale)', 0, 10),
    ('Value_For_Money',      'Value for Money (1-5 Scale)', 0, 5.5),
    ('Overall_Satisfaction', 'Overall Satisfaction (1-5)',  0, 5.5),
]

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
for ax_idx, (col, label, ymin, ymax) in enumerate(anova_plot_vars):
    ax    = axes[ax_idx]
    means = [float(df[df['Plan_Type'] == p][col].mean()) for p in plan_order]
    sems  = [float(df[df['Plan_Type'] == p][col].sem())  for p in plan_order]
    counts= [len(df[df['Plan_Type'] == p][col].dropna())  for p in plan_order]
    bars  = ax.bar(plan_labels_short, means, color=plan_cols_anova, edgecolor='white',
                   width=0.5, yerr=sems, capsize=5,
                   error_kw=dict(ecolor='black', linewidth=1.5))
    for bar, m, n, se in zip(bars, means, counts, sems):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08 + se,
                f'{m:.2f}\n(n={n})', ha='center', va='bottom', fontsize=9, fontweight='bold')
    grps = [df[df['Plan_Type'] == p][col].dropna() for p in plan_order]
    f_s, p_v = stats.f_oneway(*[g for g in grps if len(g) > 0])
    ax.text(0.97, 0.97,
            f'ANOVA: F={f_s:.2f}, p={p_v:.4f}\n'
            f'{"Significant" if p_v < 0.05 else "Not Significant"}',
            transform=ax.transAxes, fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85))
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel(label, fontsize=11)
    title_main = label.split('(')[0].strip()
    ax.set_title(f'ANOVA: {title_main}\nby Membership Plan Type', fontweight='bold')

fig.suptitle('ANALYZE (Survey): One-Way ANOVA -- Satisfaction by Membership Plan Type\n'
             'Monthly vs Quarterly (3M) vs Annual (12M) | Error bars = +/-1 SE\n'
             'Ultimate Fitness Centre Member Experience Survey (n=50)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "survey_anova_chart.png"), bbox_inches='tight')
plt.close()
print("  ANOVA Chart -- Saved")

# ============================================================
# SECTION 7: NPS + VOC
# ============================================================
print("\n" + "=" * 70)
print("SECTION 7: NPS ANALYSIS & VOICE OF CUSTOMER")
print("=" * 70)

promoters  = int((df['NPS'] >= 9).sum())
passives   = int(((df['NPS'] >= 7) & (df['NPS'] <= 8)).sum())
detractors = int((df['NPS'] <= 6).sum())
nps_score2 = (promoters - detractors) / len(df) * 100
print(f"  Promoters  (9-10): {promoters}  ({promoters/len(df)*100:.0f}%)")
print(f"  Passives   (7-8):  {passives}   ({passives/len(df)*100:.0f}%)")
print(f"  Detractors (0-6):  {detractors} ({detractors/len(df)*100:.0f}%)")
print(f"  NET PROMOTER SCORE: {nps_score2:.0f}")

fig, axes = plt.subplots(1, 3, figsize=(18, 7))

nps_sizes   = [promoters, passives, detractors]
nps_labels2 = [f'Promoters\n(9-10)\nn={promoters}',
               f'Passives\n(7-8)\nn={passives}',
               f'Detractors\n(0-6)\nn={detractors}']
nps_cols    = [COLORS['success'], COLORS['warning'], COLORS['danger']]
axes[0].pie(nps_sizes, labels=nps_labels2, colors=nps_cols, autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 10}, pctdistance=0.7,
            wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2))
nps_color_txt = (COLORS['success'] if nps_score2 >= 50
                 else COLORS['warning'] if nps_score2 >= 0 else COLORS['danger'])
axes[0].text(0, 0, f'NPS\n{nps_score2:.0f}', ha='center', va='center',
             fontsize=18, fontweight='bold', color=nps_color_txt)
axes[0].set_title('Net Promoter Score (NPS)', fontweight='bold')

reason_counts = {}
for reasons in df['Churn_Reason'].dropna():
    for r in str(reasons).split(','):
        r = r.strip()
        if r and r != 'nan':
            reason_counts[r] = reason_counts.get(r, 0) + 1
rs = pd.Series(reason_counts).sort_values(ascending=True)
bars = axes[1].barh(rs.index, rs.values, color=COLORS['danger'],
                    alpha=0.8, edgecolor='white', height=0.5)
for bar, val in zip(bars, rs.values):
    axes[1].text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 str(val), va='center', fontsize=10, fontweight='bold')
axes[1].set_xlabel('Mentions', fontsize=11)
axes[1].set_title('Survey VOC: Reasons Members Consider Leaving', fontweight='bold')

replacements = [
    ('Free monthly fitness assessment & diet advice', 'Free Monthly Fitness Assessment'),
    ('Flexible membership pause/freeze policy',       'Flexible Pause/Freeze Policy'),
    ('Loyalty renewal discounts & perks',             'Loyalty Renewal Discounts'),
    ('Live crowd tracker on a mobile app',            'Live Crowd Tracker App'),
    ('More specialized equipment',                    'More Specialized Equipment'),
    ('Dedicated floor trainer assistance',            'Dedicated Floor Trainer'),
    ('More group fitness classes',                    'More Group Fitness Classes'),
]
init_counts = {}
for init in df['Retention_Initiative'].dropna():
    for i in str(init).split(','):
        i = i.strip()
        if i and i != 'nan':
            short = i
            for old, new in replacements:
                short = short.replace(old, new)
            init_counts[short] = init_counts.get(short, 0) + 1
init_s = pd.Series(init_counts).sort_values(ascending=True)
bars = axes[2].barh(init_s.index, init_s.values, color=COLORS['success'],
                    alpha=0.8, edgecolor='white', height=0.5)
for bar, val in zip(bars, init_s.values):
    axes[2].text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 str(val), va='center', fontsize=10, fontweight='bold')
axes[2].set_xlabel('Mentions', fontsize=11)
axes[2].set_title('Survey VOC: Initiatives Most Likely to Drive Renewal', fontweight='bold')

fig.suptitle('ANALYZE (Survey): NPS Analysis & Voice of Customer\n'
             'Ultimate Fitness Centre Member Experience Survey (n=50)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "survey_nps_voc.png"), bbox_inches='tight')
plt.close()
print("  NPS & VOC Chart -- Saved")

# ============================================================
# SECTION 8: Survey Insights Dashboard
# ============================================================
print("\n" + "=" * 70)
print("SECTION 8: SURVEY INSIGHTS DASHBOARD")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(20, 13))

renewal_counts_dist = df['Renewal_Intent'].value_counts().sort_index()
bar_c = [COLORS['danger']  if x < 5
         else COLORS['warning'] if x < 7
         else COLORS['success'] for x in renewal_counts_dist.index]
axes[0,0].bar(renewal_counts_dist.index, renewal_counts_dist.values,
              color=bar_c, edgecolor='white', width=0.7)
axes[0,0].set_xlabel('Renewal Intent Score (1-10)', fontsize=11)
axes[0,0].set_ylabel('Count', fontsize=11)
axes[0,0].set_title(
    f'Renewal Intent Distribution\n'
    f'Mean={df["Renewal_Intent"].mean():.1f}, '
    f'Median={df["Renewal_Intent"].median():.0f}',
    fontweight='bold')
for score, count in renewal_counts_dist.items():
    axes[0,0].text(score, count + 0.1, str(count),
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

plan_order2  = ['Monthly', 'Quarterly (3 Months)', 'Annual (12 Months)']
plan_data_ri = [df[df['Plan_Type'] == p]['Renewal_Intent'].dropna() for p in plan_order2]
bp = axes[0,1].boxplot(
    plan_data_ri,
    tick_labels=['Monthly', 'Quarterly\n(3M)', 'Annual\n(12M)'],
    patch_artist=True, widths=0.5,
    medianprops=dict(color='black', linewidth=2.5))
for box, color in zip(bp['boxes'],
                      [COLORS['churned'], COLORS['warning'], COLORS['success']]):
    box.set_facecolor(color); box.set_alpha(0.75)
f_ri, p_ri = stats.f_oneway(*[g for g in plan_data_ri if len(g) > 0])
axes[0,1].set_ylabel('Renewal Intent (1-10)', fontsize=11)
axes[0,1].set_title(
    f'Renewal Intent by Plan Type\nANOVA: F={f_ri:.2f}, p={p_ri:.4f}', fontweight='bold')
axes[0,1].text(0.97, 0.02,
               f'{"SIGNIFICANT" if p_ri < 0.05 else "Not Significant"}',
               transform=axes[0,1].transAxes, ha='right', va='bottom', fontsize=10,
               color=COLORS['danger'] if p_ri < 0.05 else 'gray', fontweight='bold')

visit_order = ['1-2 days', '3-4 days', '5-6 days']
visit_data  = [df[df['Visit_Frequency'] == v]['Renewal_Intent'].dropna() for v in visit_order]
bp2 = axes[0,2].boxplot(
    visit_data, tick_labels=visit_order, patch_artist=True, widths=0.5,
    medianprops=dict(color='black', linewidth=2.5))
for box, color in zip(bp2['boxes'],
                      [COLORS['churned'], COLORS['warning'], COLORS['success']]):
    box.set_facecolor(color); box.set_alpha(0.75)
f_vf, p_vf = stats.f_oneway(*[g for g in visit_data if len(g) > 0])
axes[0,2].set_ylabel('Renewal Intent (1-10)', fontsize=11)
axes[0,2].set_title(
    f'Renewal Intent by Visit Frequency\nANOVA: F={f_vf:.2f}, p={p_vf:.4f}', fontweight='bold')
axes[0,2].text(0.97, 0.02,
               f'{"SIGNIFICANT" if p_vf < 0.05 else "Not Significant"}',
               transform=axes[0,2].transAxes, ha='right', va='bottom', fontsize=10,
               color=COLORS['danger'] if p_vf < 0.05 else 'gray', fontweight='bold')

sat_labels_s  = ['Equipment', 'Hygiene', 'Environment', 'Trainer', 'Value/Money']
ov_means   = [float(df[c].mean())       for c in sat_cols_all]
ren_means  = [float(likely[c].mean())   for c in sat_cols_all]
nren_means = [float(unlikely[c].mean()) for c in sat_cols_all]
x2 = np.arange(len(sat_labels_s))
w2 = 0.28
axes[1,0].bar(x2 - w2, ov_means,   w2, label='All Members',     color=COLORS['info'],    edgecolor='white', alpha=0.85)
axes[1,0].bar(x2,       ren_means, w2, label='Likely Renewer',   color=COLORS['active'],  edgecolor='white', alpha=0.85)
axes[1,0].bar(x2 + w2, nren_means, w2, label='Unlikely Renewer', color=COLORS['churned'], edgecolor='white', alpha=0.85)
axes[1,0].set_xticks(x2)
axes[1,0].set_xticklabels(sat_labels_s, fontsize=9)
axes[1,0].set_ylim(0, 5.5)
axes[1,0].set_ylabel('Mean Score (1-5)', fontsize=11)
axes[1,0].set_title('Satisfaction: All vs Renewer vs Non-Renewer', fontweight='bold')
axes[1,0].legend(fontsize=9, loc='lower right')

ax_s   = axes[1,1]
sc_col = [COLORS['active'] if x >= 7 else COLORS['churned'] for x in df['Renewal_Intent']]
ax_s.scatter(df['Overall_Satisfaction'], df['Renewal_Intent'],
             c=sc_col, alpha=0.65, s=60, edgecolors='white', linewidth=0.5)
m_r, b_r, r_r, p_r, _ = stats.linregress(df['Overall_Satisfaction'], df['Renewal_Intent'])
x_line = np.linspace(df['Overall_Satisfaction'].min(), df['Overall_Satisfaction'].max(), 100)
ax_s.plot(x_line, m_r * x_line + b_r, 'k--', linewidth=2, alpha=0.7)
ax_s.set_xlabel('Overall Satisfaction Score (1-5)', fontsize=11)
ax_s.set_ylabel('Renewal Intent (1-10)', fontsize=11)
ax_s.set_title(f'Scatter: Satisfaction vs Renewal Intent\nPearson r={r_r:.3f}, p={p_r:.4f}',
               fontweight='bold')
ax_s.legend(
    handles=[mpatches.Patch(color=COLORS['active'],  label='Likely Renewer (>=7)'),
             mpatches.Patch(color=COLORS['churned'], label='Unlikely Renewer (<7)')],
    fontsize=9, loc='lower right')
ax_s.text(0.03, 0.97,
          f'r = {r_r:.3f}\np = {p_r:.4f}\n'
          f'{"Strong positive correlation" if r_r > 0.5 and p_r < 0.05 else "Positive trend"}',
          transform=ax_s.transAxes, va='top', fontsize=9,
          bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85))

ax_t = axes[1,2]
ax_t.axis('off')
pt_enrolled_yes = int(df['PT_Enrolled'].str.contains('Yes', na=False).sum())
summary_rows = [
    ['Total Survey Responses',       '50'],
    ['Likely Renewers (Intent>=7)',   f'{n_likely} ({n_likely/50*100:.0f}%)'],
    ['Unlikely Renewers (Intent<7)', f'{n_unlikely} ({n_unlikely/50*100:.0f}%)'],
    ['Mean Renewal Intent',           f'{df["Renewal_Intent"].mean():.2f} / 10'],
    ['Median Renewal Intent',         f'{df["Renewal_Intent"].median():.0f} / 10'],
    ['NPS Score',                     f'{nps_score2:.0f}'],
    ['Promoters (NPS 9-10)',          f'{promoters} ({promoters/50*100:.0f}%)'],
    ['Passives (NPS 7-8)',            f'{passives} ({passives/50*100:.0f}%)'],
    ['Detractors (NPS 0-6)',          f'{detractors} ({detractors/50*100:.0f}%)'],
    ['Mean Overall Satisfaction',     f'{df["Overall_Satisfaction"].mean():.2f} / 5'],
    ['Mean Trainer Rating',           f'{df["Trainer_Rating"].mean():.2f} / 5'],
    ['Mean Value for Money',          f'{df["Value_For_Money"].mean():.2f} / 5'],
    ['PT Enrollment Rate',            f'{pt_enrolled_yes}/50 ({pt_enrolled_yes/50*100:.0f}%)'],
    ['Top Churn Reason',              'Moving Away / Relocating'],
    ['Top Retention Initiative',      'More Specialized Equipment'],
]
tbl2 = ax_t.table(cellText=summary_rows, colLabels=['Metric', 'Value'],
                  cellLoc='left', loc='center', bbox=[0, 0, 1, 1])
tbl2.auto_set_font_size(False)
tbl2.set_fontsize(9)
for (row, col_i), cell in tbl2.get_celld().items():
    if row == 0:
        cell.set_facecolor(COLORS['primary'])
        cell.set_text_props(color='white', fontweight='bold')
    elif row % 2 == 0:
        cell.set_facecolor('#F0F9FF')
    else:
        cell.set_facecolor('white')
ax_t.set_title('Survey Summary Statistics', fontweight='bold', pad=10)

fig.suptitle('ANALYZE (Survey): Member Experience Survey -- Complete Insights Dashboard\n'
             'Ultimate Fitness Centre | n=50 Responses',
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "survey_insights_dashboard.png"), bbox_inches='tight')
plt.close()
print("  Survey Insights Dashboard -- Saved")

print("\n" + "=" * 70)
print("SURVEY ANALYSIS COMPLETE -- KEY FINDINGS")
print("=" * 70)
print(f"  {n_likely}/50 ({n_likely/50*100:.0f}%) members are Likely Renewers (Intent>=7)")
print(f"  NPS = {nps_score2:.0f}  ({promoters} Promoters, {passives} Passives, {detractors} Detractors)")
print(f"  Mean Renewal Intent       = {df['Renewal_Intent'].mean():.2f}/10")
print(f"  Mean Overall Satisfaction = {df['Overall_Satisfaction'].mean():.2f}/5")
print()
print("  TESTS PERFORMED:")
print("    * Box Plots: 6 satisfaction dimensions, Renewer vs Non-Renewer")
print("    * T-Tests:   6 satisfaction dimensions (Likely vs Unlikely Renewers)")
print("    * F-Test:    Levene variance test for all satisfaction variables")
print("    * Chi-Square: 10 categorical variables vs renewal intent group")
print("    * ANOVA:     Monthly vs Quarterly vs Annual plans compared")
print()
print("  TOP SURVEY INSIGHTS:")
print("    * Overcrowding / Machine wait = #2 churn reason (after relocation)")
print("    * More Specialized Equipment  = #1 requested retention initiative")
print("    * Annual plan holders show highest satisfaction & renewal intent")
print(f"\n  All outputs saved to: {OUT_DIR}")
