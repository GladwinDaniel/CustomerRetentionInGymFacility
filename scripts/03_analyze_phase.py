"""
=============================================================================
LEAN SIX SIGMA — DMAIC PHASE 3: ANALYZE
Ultimate Fitness Centre: Customer Churn Analysis
=============================================================================
Generates: T-Tests, F-Tests (ANOVA), Chi-Square, Box Plots, Scatter Plots,
           Fishbone Diagram, Faculty/PT Analysis, Marketing Analysis,
           VOC/Reviews Sentiment Analysis
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
from collections import Counter
import os, re
import warnings
warnings.filterwarnings('ignore')

# ── Config ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi': 150, 'savefig.dpi': 150, 'font.family': 'sans-serif',
    'font.size': 11, 'axes.titlesize': 14, 'axes.titleweight': 'bold',
    'figure.facecolor': 'white', 'axes.facecolor': '#FAFAFA',
    'axes.grid': True, 'grid.alpha': 0.3,
})
COLORS = {
    'primary': '#2563EB', 'secondary': '#7C3AED', 'success': '#059669',
    'danger': '#DC2626', 'warning': '#D97706', 'info': '#0891B2',
    'churned': '#EF4444', 'active': '#22C55E',
}
PALETTE = ['#2563EB', '#7C3AED', '#059669', '#DC2626', '#D97706', '#0891B2', '#EC4899', '#F59E0B']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "output", "3_Analyze")
df = pd.read_csv(os.path.join(BASE_DIR, "output", "members_master_cleaned.csv"))
df_reviews = pd.read_csv(os.path.join(BASE_DIR, "output", "reviews_cleaned.csv"))

for col in ['Member Added', 'Purchase Date', 'Expiry Date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

churned = df[df['Is_Churned'] == 1]
active = df[df['Is_Churned'] == 0]

print("=" * 70)
print("DMAIC PHASE 3: ANALYZE")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: STATISTICAL HYPOTHESIS TESTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 1: STATISTICAL HYPOTHESIS TESTS")
print("=" * 70)

results_table = []

# ── T-TEST 1: Plan Amount — Churned vs Active ──────────────────────────────
print("\n--- T-Test 1: Plan Amount (Churned vs Active) ---")
t1_stat, t1_p = stats.ttest_ind(churned['Plan Amount'].dropna(), active['Plan Amount'].dropna(), equal_var=False)
print(f"  Churned Mean: ₹{churned['Plan Amount'].mean():,.0f}")
print(f"  Active Mean:  ₹{active['Plan Amount'].mean():,.0f}")
print(f"  t-statistic:  {t1_stat:.4f}")
print(f"  p-value:      {t1_p:.6f}")
print(f"  Result:       {'SIGNIFICANT ✅' if t1_p < 0.05 else 'NOT Significant ❌'} (α = 0.05)")
results_table.append({
    'Test': 'Independent T-Test', 'Variable': 'Plan Amount',
    'Comparison': 'Churned vs Active',
    'Group 1 Mean': f'₹{churned["Plan Amount"].mean():,.0f}',
    'Group 2 Mean': f'₹{active["Plan Amount"].mean():,.0f}',
    'Test Statistic': f't = {t1_stat:.4f}', 'p-value': f'{t1_p:.6f}',
    'Significant (α=0.05)': 'Yes' if t1_p < 0.05 else 'No',
    'Interpretation': 'Churned members pay significantly less' if t1_p < 0.05 else 'No significant price difference'
})

# ── T-TEST 2: Membership Duration — Churned vs Active ──────────────────────
print("\n--- T-Test 2: Membership Duration (Churned vs Active) ---")
t2_stat, t2_p = stats.ttest_ind(
    churned['Membership_Duration_Days'].dropna(),
    active['Membership_Duration_Days'].dropna(), equal_var=False)
print(f"  Churned Mean: {churned['Membership_Duration_Days'].mean():.0f} days")
print(f"  Active Mean:  {active['Membership_Duration_Days'].mean():.0f} days")
print(f"  t-statistic:  {t2_stat:.4f}")
print(f"  p-value:      {t2_p:.6f}")
print(f"  Result:       {'SIGNIFICANT ✅' if t2_p < 0.05 else 'NOT Significant ❌'}")
results_table.append({
    'Test': 'Independent T-Test', 'Variable': 'Membership Duration (Days)',
    'Comparison': 'Churned vs Active',
    'Group 1 Mean': f'{churned["Membership_Duration_Days"].mean():.0f} days',
    'Group 2 Mean': f'{active["Membership_Duration_Days"].mean():.0f} days',
    'Test Statistic': f't = {t2_stat:.4f}', 'p-value': f'{t2_p:.6f}',
    'Significant (α=0.05)': 'Yes' if t2_p < 0.05 else 'No',
    'Interpretation': 'Churned members have shorter memberships' if t2_p < 0.05 else 'No significant duration difference'
})

# ── T-TEST 3: Payment Gap — Churned vs Active ──────────────────────────────
print("\n--- T-Test 3: Payment Gap (Churned vs Active) ---")
t3_stat, t3_p = stats.ttest_ind(
    churned['Payment_Gap'].dropna(),
    active['Payment_Gap'].dropna(), equal_var=False)
print(f"  Churned Mean: ₹{churned['Payment_Gap'].mean():,.0f}")
print(f"  Active Mean:  ₹{active['Payment_Gap'].mean():,.0f}")
print(f"  t-statistic:  {t3_stat:.4f}")
print(f"  p-value:      {t3_p:.6f}")
print(f"  Result:       {'SIGNIFICANT ✅' if t3_p < 0.05 else 'NOT Significant ❌'}")
results_table.append({
    'Test': 'Independent T-Test', 'Variable': 'Payment Gap',
    'Comparison': 'Churned vs Active',
    'Group 1 Mean': f'₹{churned["Payment_Gap"].mean():,.0f}',
    'Group 2 Mean': f'₹{active["Payment_Gap"].mean():,.0f}',
    'Test Statistic': f't = {t3_stat:.4f}', 'p-value': f'{t3_p:.6f}',
    'Significant (α=0.05)': 'Yes' if t3_p < 0.05 else 'No',
    'Interpretation': 'Payment gap differs significantly between groups' if t3_p < 0.05 else 'No significant payment gap difference'
})

# ── ANOVA (F-TEST) 1: Plan Amount across Plan Duration Categories ──────────
print("\n--- F-Test (ANOVA) 1: Plan Amount across Duration Categories ---")
groups_duration = [group['Plan Amount'].dropna() for name, group in df.groupby('Plan_Duration_Category') if len(group) > 1]
f1_stat, f1_p = stats.f_oneway(*groups_duration)
print(f"  F-statistic:  {f1_stat:.4f}")
print(f"  p-value:      {f1_p:.6f}")
print(f"  Result:       {'SIGNIFICANT ✅' if f1_p < 0.05 else 'NOT Significant ❌'}")
results_table.append({
    'Test': 'One-Way ANOVA (F-Test)', 'Variable': 'Plan Amount',
    'Comparison': 'Across Plan Duration Categories',
    'Group 1 Mean': '-', 'Group 2 Mean': '-',
    'Test Statistic': f'F = {f1_stat:.4f}', 'p-value': f'{f1_p:.6f}',
    'Significant (α=0.05)': 'Yes' if f1_p < 0.05 else 'No',
    'Interpretation': 'Plan amounts differ significantly across durations' if f1_p < 0.05 else 'No significant difference across durations'
})

# ── ANOVA (F-TEST) 2: Churn Rate across Plan Types ─────────────────────────
print("\n--- F-Test (ANOVA) 2: Plan Amount across Plan Types ---")
groups_type = [group['Plan Amount'].dropna() for name, group in df.groupby('Plan_Type') if len(group) > 1]
f2_stat, f2_p = stats.f_oneway(*groups_type)
print(f"  F-statistic:  {f2_stat:.4f}")
print(f"  p-value:      {f2_p:.6f}")
print(f"  Result:       {'SIGNIFICANT ✅' if f2_p < 0.05 else 'NOT Significant ❌'}")
results_table.append({
    'Test': 'One-Way ANOVA (F-Test)', 'Variable': 'Plan Amount',
    'Comparison': 'Across Plan Types (Student/Regular/PT/Family/Promo)',
    'Group 1 Mean': '-', 'Group 2 Mean': '-',
    'Test Statistic': f'F = {f2_stat:.4f}', 'p-value': f'{f2_p:.6f}',
    'Significant (α=0.05)': 'Yes' if f2_p < 0.05 else 'No',
    'Interpretation': 'Plan amounts differ significantly across plan types' if f2_p < 0.05 else 'No significant difference across plan types'
})

# ── CHI-SQUARE 1: Churn vs Gender ──────────────────────────────────────────
print("\n--- Chi-Square Test 1: Churn vs Gender ---")
contingency1 = pd.crosstab(df['Gender'], df['Status'])
chi1_stat, chi1_p, chi1_dof, chi1_expected = stats.chi2_contingency(contingency1)
print(f"  Contingency Table:\n{contingency1}")
print(f"  Chi-Square:   {chi1_stat:.4f}")
print(f"  p-value:      {chi1_p:.6f}")
print(f"  DoF:          {chi1_dof}")
print(f"  Result:       {'SIGNIFICANT ✅' if chi1_p < 0.05 else 'NOT Significant ❌'}")
results_table.append({
    'Test': 'Chi-Square Test', 'Variable': 'Churn Status',
    'Comparison': 'Gender (Male vs Female)',
    'Group 1 Mean': f'Male churn: {df[df["Gender"]=="male"]["Is_Churned"].mean()*100:.1f}%',
    'Group 2 Mean': f'Female churn: {df[df["Gender"]=="female"]["Is_Churned"].mean()*100:.1f}%',
    'Test Statistic': f'χ² = {chi1_stat:.4f}', 'p-value': f'{chi1_p:.6f}',
    'Significant (α=0.05)': 'Yes' if chi1_p < 0.05 else 'No',
    'Interpretation': 'Churn is associated with gender' if chi1_p < 0.05 else 'Churn is independent of gender'
})

# ── CHI-SQUARE 2: Churn vs Plan Duration ───────────────────────────────────
print("\n--- Chi-Square Test 2: Churn vs Plan Duration Category ---")
contingency2 = pd.crosstab(df['Plan_Duration_Category'], df['Status'])
chi2_stat, chi2_p, chi2_dof, chi2_expected = stats.chi2_contingency(contingency2)
print(f"  Contingency Table:\n{contingency2}")
print(f"  Chi-Square:   {chi2_stat:.4f}")
print(f"  p-value:      {chi2_p:.6f}")
print(f"  DoF:          {chi2_dof}")
print(f"  Result:       {'SIGNIFICANT ✅' if chi2_p < 0.05 else 'NOT Significant ❌'}")
results_table.append({
    'Test': 'Chi-Square Test', 'Variable': 'Churn Status',
    'Comparison': 'Plan Duration Category',
    'Group 1 Mean': '-', 'Group 2 Mean': '-',
    'Test Statistic': f'χ² = {chi2_stat:.4f}', 'p-value': f'{chi2_p:.6f}',
    'Significant (α=0.05)': 'Yes' if chi2_p < 0.05 else 'No',
    'Interpretation': 'Churn is significantly associated with plan duration' if chi2_p < 0.05 else 'Churn is independent of plan duration'
})

# Save results table
results_df = pd.DataFrame(results_table)
results_df.to_csv(os.path.join(OUT_DIR, "statistical_tests_results.csv"), index=False)
print("\n✅ Statistical Test Results Table — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: BOX PLOTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 2: BOX PLOTS & SCATTER PLOTS")
print("=" * 70)

# Box Plot 1: Plan Amount by Status
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

bp1 = axes[0].boxplot(
    [churned['Plan Amount'].dropna(), active['Plan Amount'].dropna()],
    tick_labels=['Churned', 'Active'], patch_artist=True, widths=0.5,
    boxprops=dict(linewidth=1.5), medianprops=dict(color='black', linewidth=2),
    whiskerprops=dict(linewidth=1.5), capprops=dict(linewidth=1.5))
bp1['boxes'][0].set_facecolor(COLORS['churned'])
bp1['boxes'][1].set_facecolor(COLORS['active'])
bp1['boxes'][0].set_alpha(0.7)
bp1['boxes'][1].set_alpha(0.7)
axes[0].set_ylabel('Plan Amount (₹)', fontsize=12)
axes[0].set_title(f'Plan Amount: Churned vs Active\n(t={t1_stat:.2f}, p={t1_p:.4f})', fontweight='bold')

# Box Plot 2: Membership Duration by Status
bp2 = axes[1].boxplot(
    [churned['Membership_Duration_Days'].dropna(), active['Membership_Duration_Days'].dropna()],
    tick_labels=['Churned', 'Active'], patch_artist=True, widths=0.5,
    boxprops=dict(linewidth=1.5), medianprops=dict(color='black', linewidth=2),
    whiskerprops=dict(linewidth=1.5), capprops=dict(linewidth=1.5))
bp2['boxes'][0].set_facecolor(COLORS['churned'])
bp2['boxes'][1].set_facecolor(COLORS['active'])
bp2['boxes'][0].set_alpha(0.7)
bp2['boxes'][1].set_alpha(0.7)
axes[1].set_ylabel('Membership Duration (Days)', fontsize=12)
axes[1].set_title(f'Duration: Churned vs Active\n(t={t2_stat:.2f}, p={t2_p:.4f})', fontweight='bold')

# Box Plot 3: Plan Amount by Plan Type
plan_types_ordered = ['Student', 'Regular', 'Personal Training', 'Family/Couple', 'Promotional/Offer']
plan_data = [df[df['Plan_Type']==pt]['Plan Amount'].dropna() for pt in plan_types_ordered if pt in df['Plan_Type'].values]
plan_labels = [pt for pt in plan_types_ordered if pt in df['Plan_Type'].values]
bp3 = axes[2].boxplot(plan_data, tick_labels=plan_labels, patch_artist=True, widths=0.5,
    boxprops=dict(linewidth=1.5), medianprops=dict(color='black', linewidth=2),
    whiskerprops=dict(linewidth=1.5), capprops=dict(linewidth=1.5))
for box, color in zip(bp3['boxes'], PALETTE):
    box.set_facecolor(color)
    box.set_alpha(0.7)
axes[2].set_ylabel('Plan Amount (₹)', fontsize=12)
axes[2].set_title(f'Plan Amount by Plan Type\n(F={f2_stat:.2f}, p={f2_p:.4f})', fontweight='bold')
axes[2].set_xticklabels(plan_labels, rotation=20, ha='right', fontsize=9)

fig.suptitle('ANALYZE: Box Plot Comparisons (with Test Statistics)', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "box_plots_comparisons.png"), bbox_inches='tight')
plt.close()
print("✅ Box Plots — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SCATTER PLOT: Plan Amount vs Duration
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(churned['Plan Amount'], churned['Membership_Duration_Days'],
           c=COLORS['churned'], alpha=0.5, s=30, label='Churned', edgecolors='white', linewidth=0.5)
ax.scatter(active['Plan Amount'], active['Membership_Duration_Days'],
           c=COLORS['active'], alpha=0.5, s=30, label='Active', edgecolors='white', linewidth=0.5)
ax.set_xlabel('Plan Amount (₹)', fontsize=12)
ax.set_ylabel('Membership Duration (Days)', fontsize=12)
ax.set_title('Scatter Plot: Plan Amount vs Membership Duration\n(Churned vs Active)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)

# Correlation
corr, corr_p = stats.pearsonr(df['Plan Amount'].dropna(), df['Membership_Duration_Days'].dropna())
ax.text(0.97, 0.03, f'Pearson r = {corr:.3f}\np = {corr_p:.6f}',
        transform=ax.transAxes, fontsize=10, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "scatter_amount_vs_duration.png"), bbox_inches='tight')
plt.close()
print("✅ Scatter Plot — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# CORRELATION MATRIX
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 7))
corr_cols = ['Plan Amount', 'Paid', 'Pending Amount', 'Membership_Duration_Days', 'Payment_Gap', 'Is_Churned']
corr_matrix = df[corr_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            vmin=-1, vmax=1, ax=ax)
ax.set_title('Correlation Matrix\n(Key Numeric Variables)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "correlation_matrix.png"), bbox_inches='tight')
plt.close()
print("✅ Correlation Matrix — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: CHURN RATE COMPARISON CHART
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# By Plan Duration
dur_churn = df.groupby('Plan_Duration_Category')['Is_Churned'].mean().sort_values(ascending=True)
dur_order = ['1 Month', '2 Months', '3 Months', '6 Months', '1 Year', 'Other']
dur_churn = dur_churn.reindex([d for d in dur_order if d in dur_churn.index])
colors_dur = [COLORS['danger'] if v > 0.5 else COLORS['warning'] if v > 0.3 else COLORS['success'] for v in dur_churn]
bars = axes[0].barh(dur_churn.index, dur_churn.values * 100, color=colors_dur, edgecolor='white', height=0.5)
for bar, val in zip(bars, dur_churn.values):
    axes[0].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{val*100:.1f}%',
                va='center', fontsize=10, fontweight='bold')
axes[0].set_xlabel('Churn Rate (%)', fontsize=12)
axes[0].set_title('Churn Rate by Duration', fontweight='bold')
axes[0].axvline(53.75, color='black', linestyle='--', alpha=0.4, linewidth=1)
axes[0].set_xlim(0, 100)

# By Plan Type
type_churn = df.groupby('Plan_Type')['Is_Churned'].mean().sort_values(ascending=True)
colors_type = [COLORS['danger'] if v > 0.5 else COLORS['warning'] if v > 0.3 else COLORS['success'] for v in type_churn]
bars = axes[1].barh(type_churn.index, type_churn.values * 100, color=colors_type, edgecolor='white', height=0.5)
for bar, val in zip(bars, type_churn.values):
    axes[1].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{val*100:.1f}%',
                va='center', fontsize=10, fontweight='bold')
axes[1].set_xlabel('Churn Rate (%)', fontsize=12)
axes[1].set_title('Churn Rate by Plan Type', fontweight='bold')
axes[1].axvline(53.75, color='black', linestyle='--', alpha=0.4, linewidth=1)
axes[1].set_xlim(0, 100)

# By Price Bracket
price_churn = df.groupby('Price_Bracket')['Is_Churned'].mean().sort_values(ascending=True)
colors_price = [COLORS['danger'] if v > 0.5 else COLORS['warning'] if v > 0.3 else COLORS['success'] for v in price_churn]
bars = axes[2].barh(price_churn.index, price_churn.values * 100, color=colors_price, edgecolor='white', height=0.5)
for bar, val in zip(bars, price_churn.values):
    axes[2].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{val*100:.1f}%',
                va='center', fontsize=10, fontweight='bold')
axes[2].set_xlabel('Churn Rate (%)', fontsize=12)
axes[2].set_title('Churn Rate by Price Bracket', fontweight='bold')
axes[2].axvline(53.75, color='black', linestyle='--', alpha=0.4, linewidth=1)
axes[2].set_xlim(0, 100)

fig.suptitle('ANALYZE: Churn Rate Comparison Dashboard\n(Dashed line = Overall churn rate 53.75%)',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "churn_rate_comparison.png"), bbox_inches='tight')
plt.close()
print("✅ Churn Rate Comparison Dashboard — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: FISHBONE (ISHIKAWA) DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 4: FISHBONE (ISHIKAWA) DIAGRAM")
print("=" * 70)

fig, ax = plt.subplots(figsize=(18, 10))
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')

# Central spine
ax.annotate('', xy=(16, 5), xytext=(2, 5),
            arrowprops=dict(arrowstyle='->', lw=3, color='#333'))

# Effect box
ax.text(16.5, 5, 'CUSTOMER\nCHURN\n(53.75%)', fontsize=14, fontweight='bold',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor=COLORS['danger'], edgecolor='#333',
                  linewidth=2, alpha=0.9),
        color='white')

# Categories and causes
categories = {
    'PRICING &\nPAYMENT': {
        'pos': (4, 8.5), 'color': COLORS['primary'],
        'causes': ['Low-price plans → low commitment',
                   'Payment gaps (partial payments)',
                   'No EMI/installment options',
                   'Price-value mismatch']
    },
    'PLAN\nSTRUCTURE': {
        'pos': (7.5, 8.5), 'color': COLORS['secondary'],
        'causes': ['1-month plans: 77% churn rate',
                   'No bridge plans (2-month gap)',
                   'Student seasonal exits',
                   'Short plans = trial behavior']
    },
    'TRAINER &\nFACULTY': {
        'pos': (11, 8.5), 'color': COLORS['success'],
        'causes': ['Only 4% in Personal Training',
                   'PT churn: 62.5% (highest!)',
                   'Low trainer engagement',
                   'No onboarding guidance']
    },
    'MARKETING &\nACQUISITION': {
        'pos': (4, 1.5), 'color': COLORS['warning'],
        'causes': ['Promotional plans: 27.6% churn (best)',
                   'Student-heavy (47.8%)',
                   'Female only 16.3% of members',
                   'No renewal campaigns']
    },
    'FACILITIES &\nENVIRONMENT': {
        'pos': (7.5, 1.5), 'color': COLORS['info'],
        'causes': ['Equipment availability',
                   'Peak hour overcrowding',
                   'Cleanliness/hygiene',
                   'Ventilation & lighting']
    },
    'MEMBER\nENGAGEMENT': {
        'pos': (11, 1.5), 'color': '#EC4899',
        'causes': ['No visit tracking system',
                   'No renewal reminders',
                   'No progress tracking',
                   'Low community feel']
    },
}

for cat_name, cat_data in categories.items():
    x, y = cat_data['pos']
    color = cat_data['color']

    # Category box
    ax.text(x, y, cat_name, fontsize=10, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=color, edgecolor='#333',
                      linewidth=1.5, alpha=0.85), color='white')

    # Branch line to spine
    spine_y = 5
    ax.annotate('', xy=(x, spine_y), xytext=(x, y - 0.5 if y > 5 else y + 0.5),
                arrowprops=dict(arrowstyle='->', lw=2, color=color, alpha=0.7))

    # Cause lines
    for i, cause in enumerate(cat_data['causes']):
        if y > 5:  # Upper branches
            cy = y - 1.3 - i * 0.55
            ax.text(x, cy, f'• {cause}', fontsize=7.5, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))
        else:  # Lower branches
            cy = y + 1.3 + i * 0.55
            ax.text(x, cy, f'• {cause}', fontsize=7.5, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))

ax.set_title('Fishbone (Ishikawa) Diagram: Root Causes of Customer Churn\nUltimate Fitness Centre',
             fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fishbone_diagram.png"), bbox_inches='tight')
plt.close()
print("✅ Fishbone Diagram — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: FACULTY / PERSONAL TRAINING ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 5: FACULTY & TRAINER (PT) ANALYSIS")
print("=" * 70)

pt_members = df[df['Plan_Type'] == 'Personal Training']
non_pt_members = df[df['Plan_Type'] != 'Personal Training']

print(f"  PT Members:     {len(pt_members)} ({len(pt_members)/len(df)*100:.1f}%)")
print(f"  Non-PT Members: {len(non_pt_members)} ({len(non_pt_members)/len(df)*100:.1f}%)")
print(f"  PT Churn Rate:     {pt_members['Is_Churned'].mean()*100:.1f}%")
print(f"  Non-PT Churn Rate: {non_pt_members['Is_Churned'].mean()*100:.1f}%")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# PT vs Non-PT enrollment
labels = ['Non-PT\nMembers', 'Personal\nTraining']
sizes = [len(non_pt_members), len(pt_members)]
colors = [COLORS['primary'], COLORS['warning']]
axes[0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
            textprops={'fontsize': 11}, pctdistance=0.7,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
axes[0].set_title(f'PT Enrollment Rate\n(Only {len(pt_members)} of {len(df)} = {len(pt_members)/len(df)*100:.1f}%)',
                  fontweight='bold')

# PT Churn vs Non-PT Churn
churn_rates = [pt_members['Is_Churned'].mean()*100, non_pt_members['Is_Churned'].mean()*100]
bars = axes[1].bar(['PT Members', 'Non-PT Members'], churn_rates,
                    color=[COLORS['danger'], COLORS['primary']], edgecolor='white', width=0.5)
for bar, val in zip(bars, churn_rates):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Churn Rate (%)', fontsize=12)
axes[1].set_title('Churn Rate: PT vs Non-PT', fontweight='bold')
axes[1].set_ylim(0, 80)
axes[1].axhline(53.75, color='black', linestyle='--', alpha=0.4, linewidth=1)

# PT Plan Duration breakdown
pt_dur = pt_members['Plan_Duration_Category'].value_counts()
axes[2].bar(pt_dur.index, pt_dur.values, color=PALETTE[:len(pt_dur)], edgecolor='white', width=0.5)
for i, (idx, val) in enumerate(pt_dur.items()):
    churned_in_cat = pt_members[pt_members['Plan_Duration_Category']==idx]['Is_Churned'].sum()
    axes[2].text(i, val + 0.1, f'{val} (Churned: {churned_in_cat})',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
axes[2].set_ylabel('Number of Members', fontsize=12)
axes[2].set_title('PT Plans by Duration\n(with churn counts)', fontweight='bold')
axes[2].set_xticklabels(pt_dur.index, rotation=15, ha='right')

fig.suptitle('ANALYZE: Gym Faculty & Personal Training Impact on Retention',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "pt_trainer_analysis.png"), bbox_inches='tight')
plt.close()
print("✅ PT/Trainer Analysis — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: MARKETING & OFFER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 6: MARKETING & OFFER ANALYSIS")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Student vs Regular churn
student = df[df['Plan_Type'] == 'Student']
regular = df[df['Plan_Type'] == 'Regular']
promo = df[df['Plan_Type'] == 'Promotional/Offer']
family = df[df['Plan_Type'] == 'Family/Couple']

types = ['Student', 'Regular', 'Promo/Offer', 'Family/Couple']
churn_rates = [student['Is_Churned'].mean()*100, regular['Is_Churned'].mean()*100,
               promo['Is_Churned'].mean()*100, family['Is_Churned'].mean()*100]
counts = [len(student), len(regular), len(promo), len(family)]
colors_bar = [COLORS['danger'] if c > 50 else COLORS['warning'] if c > 30 else COLORS['success'] for c in churn_rates]

bars = axes[0,0].bar(types, churn_rates, color=colors_bar, edgecolor='white', width=0.5)
for bar, val, cnt in zip(bars, churn_rates, counts):
    axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                  f'{val:.1f}%\n(n={cnt})', ha='center', va='bottom', fontsize=10, fontweight='bold')
axes[0,0].set_ylabel('Churn Rate (%)', fontsize=12)
axes[0,0].set_title('Churn Rate by Plan Type\n(Marketing Channel Proxy)', fontweight='bold')
axes[0,0].set_ylim(0, 80)
axes[0,0].axhline(53.75, color='black', linestyle='--', alpha=0.4)

# 2. Gender split and churn
gender_data = df.groupby('Gender')['Is_Churned'].agg(['mean', 'count']).reset_index()
bars = axes[0,1].bar(gender_data['Gender'], gender_data['mean']*100,
                     color=[COLORS['primary'], COLORS['secondary']], edgecolor='white', width=0.4)
for bar, row in zip(bars, gender_data.itertuples()):
    axes[0,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                  f'{row.mean*100:.1f}%\n(n={row.count})', ha='center', va='bottom', fontsize=10, fontweight='bold')
axes[0,1].set_ylabel('Churn Rate (%)', fontsize=12)
axes[0,1].set_title('Churn Rate by Gender\n(Marketing Gap: Only 16.3% Female)', fontweight='bold')
axes[0,1].set_ylim(0, 75)

# 3. Seasonal enrollment
monthly_total = df.groupby(df['Purchase Date'].dt.strftime('%Y-%m')).size().sort_index()
monthly_churn = df[df['Is_Churned']==1].groupby(df[df['Is_Churned']==1]['Purchase Date'].dt.strftime('%Y-%m')).size().sort_index()
monthly_combined = pd.DataFrame({'Total': monthly_total, 'Churned': monthly_churn}).fillna(0)
axes[1,0].bar(range(len(monthly_combined)), monthly_combined['Total'], color=COLORS['primary'], alpha=0.6, label='Total Enrolled')
axes[1,0].bar(range(len(monthly_combined)), monthly_combined['Churned'], color=COLORS['danger'], alpha=0.8, label='Churned')
axes[1,0].set_xticks(range(len(monthly_combined)))
axes[1,0].set_xticklabels(monthly_combined.index, rotation=45, ha='right', fontsize=8)
axes[1,0].set_ylabel('Count', fontsize=12)
axes[1,0].set_title('Monthly Enrollment & Churn\n(Seasonal Marketing Impact)', fontweight='bold')
axes[1,0].legend()

# 4. Promotional vs Non-Promotional
promo_all = df[df['Plan_Type'] == 'Promotional/Offer']
non_promo = df[df['Plan_Type'] != 'Promotional/Offer']
promo_data = {
    'Category': ['Promotional/Offer Plans', 'Regular Plans'],
    'Churn Rate': [promo_all['Is_Churned'].mean()*100, non_promo['Is_Churned'].mean()*100],
    'Count': [len(promo_all), len(non_promo)],
    'Avg Amount': [promo_all['Plan Amount'].mean(), non_promo['Plan Amount'].mean()]
}
x = np.arange(2)
width = 0.35
bars1 = axes[1,1].bar(x - width/2, promo_data['Churn Rate'], width, color=COLORS['success'], label='Churn Rate %', edgecolor='white')
# Second axis for Avg Amount
ax_twin = axes[1,1].twinx()
bars2 = ax_twin.bar(x + width/2, promo_data['Avg Amount'], width, color=COLORS['info'], label='Avg Amount ₹', edgecolor='white', alpha=0.7)
axes[1,1].set_xticks(x)
axes[1,1].set_xticklabels(promo_data['Category'])
axes[1,1].set_ylabel('Churn Rate (%)', fontsize=12)
ax_twin.set_ylabel('Avg Plan Amount (₹)', fontsize=12)
axes[1,1].set_title('Promotional vs Regular Plans\n(Do Offers Improve Retention?)', fontweight='bold')
axes[1,1].legend(loc='upper left')
ax_twin.legend(loc='upper right')
for bar, val, cnt in zip(bars1, promo_data['Churn Rate'], promo_data['Count']):
    axes[1,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                  f'{val:.1f}%\n(n={cnt})', ha='center', fontsize=9, fontweight='bold')

fig.suptitle('ANALYZE: Marketing & Acquisition Impact on Churn',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "marketing_analysis.png"), bbox_inches='tight')
plt.close()
print("✅ Marketing Analysis — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: VOC — GOOGLE REVIEWS ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 7: VOICE OF CUSTOMER (VOC) — GOOGLE REVIEWS")
print("=" * 70)

print(f"  Total Reviews:    {len(df_reviews)}")
print(f"  Avg Rating:       {df_reviews['review_rating'].mean():.2f} / 5")
print(f"  5-star:           {len(df_reviews[df_reviews['review_rating']==5])} ({len(df_reviews[df_reviews['review_rating']==5])/len(df_reviews)*100:.1f}%)")
print(f"  4-star:           {len(df_reviews[df_reviews['review_rating']==4])}")
print(f"  1-3 star:         {len(df_reviews[df_reviews['review_rating']<=3])}")
print(f"  Reviews with text:{df_reviews['has_text'].sum()}")
print(f"  Owner replied:    {df_reviews['has_owner_reply'].sum()}")

# Keyword extraction from reviews
all_text = ' '.join(df_reviews['review_text'].dropna().astype(str)).lower()

# Define categories of keywords
keyword_categories = {
    'Trainer/Staff': ['trainer', 'coach', 'staff', 'instructor', 'friendly', 'helpful', 'guidance', 'support', 'encouraging'],
    'Equipment': ['equipment', 'machine', 'weights', 'treadmill', 'dumbbell', 'bench'],
    'Ambience/Environment': ['ambience', 'ambient', 'atmosphere', 'clean', 'hygiene', 'ventilation', 'spacious', 'peaceful', 'place'],
    'Pricing/Value': ['price', 'affordable', 'value', 'cost', 'reasonable', 'worth', 'money'],
    'Results/Fitness': ['fitness', 'workout', 'results', 'goals', 'transform', 'body', 'health', 'muscle', 'strength'],
    'Facilities': ['facility', 'facilities', 'amenities', 'parking', 'locker', 'water'],
}

keyword_counts = {}
for category, keywords in keyword_categories.items():
    count = sum(all_text.count(kw) for kw in keywords)
    keyword_counts[category] = count

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Rating distribution
rating_counts = df_reviews['review_rating'].value_counts().sort_index()
bars = axes[0].bar(rating_counts.index, rating_counts.values,
                   color=[COLORS['danger'] if r <= 2 else COLORS['warning'] if r == 3 else COLORS['active'] if r == 4 else COLORS['success'] for r in rating_counts.index],
                   edgecolor='white', width=0.6)
for bar, val in zip(bars, rating_counts.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val),
                ha='center', va='bottom', fontsize=11, fontweight='bold')
axes[0].set_xlabel('Rating (Stars)', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].set_title(f'Google Review Ratings\n(Avg: {df_reviews["review_rating"].mean():.2f}/5, n={len(df_reviews)})', fontweight='bold')

# Keyword category chart
kw_series = pd.Series(keyword_counts).sort_values(ascending=True)
bars = axes[1].barh(kw_series.index, kw_series.values, color=PALETTE[:len(kw_series)], edgecolor='white', height=0.5)
for bar, val in zip(bars, kw_series.values):
    axes[1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, str(val),
                va='center', fontsize=10, fontweight='bold')
axes[1].set_xlabel('Mention Count', fontsize=12)
axes[1].set_title('Review Keyword Analysis\n(What Customers Talk About)', fontweight='bold')

# Word cloud of most common words
from wordcloud import WordCloud
stop_words = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'it', 'i', 'my', 'at', 'this', 'was',
              'with', 'are', 'that', 'have', 'has', 'been', 'very', 'you', 'we', 'they', 'or', 'an',
              'be', 'on', 'not', 'from', 'so', 'do', 'its', 'but', 'can', 'all', 'just', 'also',
              'me', 'if', 'would', 'will', 'there', 'their', 'your', 'which', 'about', 'as', 'more',
              'than', 'who', 'them', 'had', 'our', 'am', 'up', 'out', 'one', 'well', 'really',
              'here', 'go', 'going', 'good', 'great', 'best', 'gym', 'fitness', 'centre', 'center',
              'ultimate', 'ufc', 'rathinamangalam'}
wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis',
               stopwords=stop_words, max_words=50, prefer_horizontal=0.7).generate(all_text)
axes[2].imshow(wc, interpolation='bilinear')
axes[2].axis('off')
axes[2].set_title('Review Word Cloud\n(Most Frequent Terms)', fontweight='bold')

fig.suptitle('ANALYZE: Voice of Customer (VOC) — Google Reviews Analysis',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "voc_reviews_analysis.png"), bbox_inches='tight')
plt.close()
print("✅ VOC Reviews Analysis — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8: 5-WHYS ANALYSIS (for top churn driver)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 8: 5-WHYS ANALYSIS")
print("=" * 70)

try:
    from generate_5whys_diagram import create_five_whys_diagram
    create_five_whys_diagram(os.path.join(OUT_DIR, "five_whys_analysis.png"))
    print("5-Whys Analysis — Saved")
except Exception as e:
    print(f"Error generating 5-whys: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("KEY FINDINGS SUMMARY")
print("=" * 70)
print("""
TOP ROOT CAUSES OF CHURN (Data-Driven):

1. SHORT-TERM PLANS = HIGH CHURN
   - 1-Month plans: 77.0% churn (vs 15.8% for 1-Year)
   - Low-price plans (≤₹1,500): 74.9% churn

2. STUDENT LIFECYCLE MISMATCH
   - Students = 47.8% of all members, but 60.2% churn rate
   - No semester-aligned or pause-able plans

3. LOW TRAINER ENGAGEMENT
   - Only 4% of members use Personal Training
   - PT members churn at 62.5% — trainer engagement alone isn't enough

4. PRICING-COMMITMENT LINK
   - Higher plan amount → significantly lower churn (p < 0.001)
   - High-tier members (>₹7,500): only 20% churn

5. MARKETING GAP
   - Only 16.3% female members
   - Promotional plans actually retain better (27.6% churn)
   - Family/Couple plans best retention (37.5% churn)
""")

print("\n✅ ANALYZE PHASE COMPLETE — All charts saved to:", OUT_DIR)
