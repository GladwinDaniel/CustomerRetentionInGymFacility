"""
=============================================================================
LEAN SIX SIGMA — DMAIC PHASE 2: MEASURE
Ultimate Fitness Centre: Customer Churn Analysis
=============================================================================
Generates: Histograms, Pareto Charts, Descriptive Statistics
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Config ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.facecolor': 'white',
    'axes.facecolor': '#FAFAFA',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

COLORS = {
    'primary': '#2563EB',
    'secondary': '#7C3AED',
    'success': '#059669',
    'danger': '#DC2626',
    'warning': '#D97706',
    'info': '#0891B2',
    'churned': '#EF4444',
    'active': '#22C55E',
}
PALETTE = ['#2563EB', '#7C3AED', '#059669', '#DC2626', '#D97706', '#0891B2', '#EC4899', '#F59E0B']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "output", "2_Measure")
df = pd.read_csv(os.path.join(BASE_DIR, "output", "members_master_cleaned.csv"))

# Parse dates
for col in ['Member Added', 'Purchase Date', 'Expiry Date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

print("=" * 70)
print("DMAIC PHASE 2: MEASURE")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════
# DESCRIPTIVE STATISTICS TABLE
# ═══════════════════════════════════════════════════════════════════════════
print("\n📊 DESCRIPTIVE STATISTICS")
print("-" * 50)

desc_stats = df[['Plan Amount', 'Paid', 'Pending Amount', 'Membership_Duration_Days', 'Payment_Gap']].describe()
desc_stats.to_csv(os.path.join(OUT_DIR, "descriptive_statistics.csv"))
print(desc_stats.round(2).to_string())

# ═══════════════════════════════════════════════════════════════════════════
# HISTOGRAM 1: Membership Duration Distribution
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
churned_dur = df[df['Is_Churned']==1]['Membership_Duration_Days'].dropna()
active_dur = df[df['Is_Churned']==0]['Membership_Duration_Days'].dropna()

ax.hist(churned_dur, bins=20, alpha=0.7, color=COLORS['churned'], label=f'Churned (n={len(churned_dur)})', edgecolor='white')
ax.hist(active_dur, bins=20, alpha=0.7, color=COLORS['active'], label=f'Active (n={len(active_dur)})', edgecolor='white')
ax.set_xlabel('Membership Duration (Days)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Histogram 1: Membership Duration Distribution\n(Churned vs Active Members)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, framealpha=0.9)
ax.axvline(df['Membership_Duration_Days'].mean(), color='black', linestyle='--', linewidth=1, alpha=0.5, label=f"Mean = {df['Membership_Duration_Days'].mean():.0f} days")
ax.legend()

# Add stats box
stats_text = f"Mean: {df['Membership_Duration_Days'].mean():.0f} days\nMedian: {df['Membership_Duration_Days'].median():.0f} days\nStd Dev: {df['Membership_Duration_Days'].std():.0f} days"
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=9, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "histogram_1_membership_duration.png"), bbox_inches='tight')
plt.close()
print("\n✅ Histogram 1: Membership Duration — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# HISTOGRAM 2: Plan Amount Distribution
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
churned_amt = df[df['Is_Churned']==1]['Plan Amount'].dropna()
active_amt = df[df['Is_Churned']==0]['Plan Amount'].dropna()

ax.hist(churned_amt, bins=25, alpha=0.7, color=COLORS['churned'], label=f'Churned (n={len(churned_amt)})', edgecolor='white')
ax.hist(active_amt, bins=25, alpha=0.7, color=COLORS['active'], label=f'Active (n={len(active_amt)})', edgecolor='white')
ax.set_xlabel('Plan Amount (₹)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Histogram 2: Plan Amount Distribution\n(Churned vs Active Members)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

stats_text = f"Mean: ₹{df['Plan Amount'].mean():,.0f}\nMedian: ₹{df['Plan Amount'].median():,.0f}\nStd Dev: ₹{df['Plan Amount'].std():,.0f}"
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=9, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "histogram_2_plan_amount.png"), bbox_inches='tight')
plt.close()
print("✅ Histogram 2: Plan Amount — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# HISTOGRAM 3: Age Distribution (where available)
# ═══════════════════════════════════════════════════════════════════════════
age_data = df[df['Age'].notna()]
if len(age_data) > 5:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(age_data[age_data['Is_Churned']==1]['Age'], bins=15, alpha=0.7, color=COLORS['churned'],
            label=f'Churned', edgecolor='white')
    ax.hist(age_data[age_data['Is_Churned']==0]['Age'], bins=15, alpha=0.7, color=COLORS['active'],
            label=f'Active', edgecolor='white')
    ax.set_xlabel('Age', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Histogram 3: Age Distribution\n(Churned vs Active Members)', fontsize=14, fontweight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "histogram_3_age.png"), bbox_inches='tight')
    plt.close()
    print("✅ Histogram 3: Age — Saved")
else:
    print("⚠️ Histogram 3: Age — Insufficient data (most ages missing)")

# ═══════════════════════════════════════════════════════════════════════════
# HISTOGRAM 4: Plan Duration Category Distribution
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
duration_order = ['1 Month', '2 Months', '3 Months', '6 Months', '1 Year', 'Other']
duration_data = df.groupby(['Plan_Duration_Category', 'Status']).size().unstack(fill_value=0)
duration_data = duration_data.reindex([d for d in duration_order if d in duration_data.index])

bar_width = 0.35
x = np.arange(len(duration_data))
if 'Expired' in duration_data.columns:
    ax.bar(x - bar_width/2, duration_data['Expired'], bar_width, color=COLORS['churned'], label='Churned', edgecolor='white')
if 'Active' in duration_data.columns:
    ax.bar(x + bar_width/2, duration_data['Active'], bar_width, color=COLORS['active'], label='Active', edgecolor='white')

ax.set_xlabel('Plan Duration Category', fontsize=12)
ax.set_ylabel('Number of Members', fontsize=12)
ax.set_title('Histogram 4: Members by Plan Duration\n(Churned vs Active)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(duration_data.index, rotation=15)
ax.legend()

# Add count labels on bars
for i, idx in enumerate(duration_data.index):
    if 'Expired' in duration_data.columns:
        val = duration_data.loc[idx, 'Expired']
        ax.text(i - bar_width/2, val + 1, str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')
    if 'Active' in duration_data.columns:
        val = duration_data.loc[idx, 'Active']
        ax.text(i + bar_width/2, val + 1, str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "histogram_4_plan_duration.png"), bbox_inches='tight')
plt.close()
print("✅ Histogram 4: Plan Duration Categories — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# HISTOGRAM 5: Payment Gap Distribution
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
payment_gap = df['Payment_Gap'].dropna()
ax.hist(payment_gap[payment_gap > 0], bins=20, alpha=0.8, color=COLORS['warning'], edgecolor='white')
ax.set_xlabel('Payment Gap (Plan Amount − Paid) in ₹', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Histogram 5: Payment Gap Distribution\n(Members with Outstanding Payments)', fontsize=14, fontweight='bold')

non_zero_gap = payment_gap[payment_gap > 0]
stats_text = f"Members with gap: {len(non_zero_gap)}\nMean gap: ₹{non_zero_gap.mean():,.0f}\nMax gap: ₹{non_zero_gap.max():,.0f}"
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=9, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "histogram_5_payment_gap.png"), bbox_inches='tight')
plt.close()
print("✅ Histogram 5: Payment Gap — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# PARETO CHART 1: Plan Type vs Churn Count
# ═══════════════════════════════════════════════════════════════════════════
def create_pareto(data_series, title, xlabel, filename, color=COLORS['primary']):
    """Create a Pareto chart with cumulative percentage line."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Sort descending
    data_sorted = data_series.sort_values(ascending=False)
    cum_pct = data_sorted.cumsum() / data_sorted.sum() * 100

    # Bars
    bars = ax1.bar(range(len(data_sorted)), data_sorted.values, color=color, alpha=0.8, edgecolor='white', linewidth=0.5)
    ax1.set_xlabel(xlabel, fontsize=12)
    ax1.set_ylabel('Count', fontsize=12, color=color)
    ax1.set_xticks(range(len(data_sorted)))
    ax1.set_xticklabels(data_sorted.index, rotation=30, ha='right', fontsize=9)

    # Add count labels
    for bar, val in zip(bars, data_sorted.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val),
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Cumulative line
    ax2 = ax1.twinx()
    ax2.plot(range(len(cum_pct)), cum_pct.values, color=COLORS['danger'], marker='o', linewidth=2, markersize=6)
    ax2.set_ylabel('Cumulative %', fontsize=12, color=COLORS['danger'])
    ax2.set_ylim(0, 110)
    ax2.axhline(y=80, color=COLORS['danger'], linestyle='--', alpha=0.5, linewidth=1)
    ax2.text(len(data_sorted)-1, 82, '80% Line', fontsize=9, color=COLORS['danger'], alpha=0.7)

    # Add percentage labels on line
    for i, pct in enumerate(cum_pct.values):
        ax2.text(i, pct + 2, f'{pct:.0f}%', ha='center', fontsize=8, color=COLORS['danger'])

    ax1.set_title(title, fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, filename), bbox_inches='tight')
    plt.close()

# Pareto 1: Churn by Plan Name (top plans)
churn_by_plan = df[df['Is_Churned']==1]['Plan Name'].value_counts().head(10)
create_pareto(churn_by_plan,
    'Pareto Chart 1: Top Churn Contributing Plans\n(Vital Few — 80/20 Rule)',
    'Plan Name', 'pareto_1_churn_by_plan.png', COLORS['primary'])
print("\n✅ Pareto 1: Churn by Plan — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# PARETO CHART 2: Churn by Plan Duration Category
# ═══════════════════════════════════════════════════════════════════════════
churn_by_duration = df[df['Is_Churned']==1]['Plan_Duration_Category'].value_counts()
create_pareto(churn_by_duration,
    'Pareto Chart 2: Churn by Plan Duration Category\n(Which Durations Drive Most Churn?)',
    'Plan Duration', 'pareto_2_churn_by_duration.png', COLORS['secondary'])
print("✅ Pareto 2: Churn by Duration — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# PARETO CHART 3: Churn by Plan Type
# ═══════════════════════════════════════════════════════════════════════════
churn_by_type = df[df['Is_Churned']==1]['Plan_Type'].value_counts()
create_pareto(churn_by_type,
    'Pareto Chart 3: Churn by Plan Type\n(Student vs Regular vs PT vs Family)',
    'Plan Type', 'pareto_3_churn_by_plan_type.png', COLORS['info'])
print("✅ Pareto 3: Churn by Plan Type — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# PARETO CHART 4: Churn by Price Bracket
# ═══════════════════════════════════════════════════════════════════════════
churn_by_price = df[df['Is_Churned']==1]['Price_Bracket'].value_counts()
create_pareto(churn_by_price,
    'Pareto Chart 4: Churn by Price Bracket\n(Price Sensitivity Analysis)',
    'Price Bracket', 'pareto_4_churn_by_price.png', COLORS['warning'])
print("✅ Pareto 4: Churn by Price — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# BASELINE CHURN RATE SUMMARY CHART
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Pie 1: Overall Churn
labels1 = ['Churned\n(Expired)', 'Active\n(Retained)']
sizes1 = [len(df[df['Is_Churned']==1]), len(df[df['Is_Churned']==0])]
colors1 = [COLORS['churned'], COLORS['active']]
wedges1, texts1, autotexts1 = axes[0].pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%',
    startangle=90, textprops={'fontsize': 11}, pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
axes[0].set_title('Overall Churn Rate', fontweight='bold', fontsize=13)

# Pie 2: Gender
gender_counts = df['Gender'].value_counts()
colors2 = [COLORS['primary'], COLORS['secondary']]
wedges2, texts2, autotexts2 = axes[1].pie(gender_counts.values,
    labels=[f'Male\n(n={gender_counts.get("male",0)})', f'Female\n(n={gender_counts.get("female",0)})'],
    colors=colors2, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11},
    pctdistance=0.75, wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
axes[1].set_title('Gender Distribution', fontweight='bold', fontsize=13)

# Pie 3: Plan Type
plan_type_counts = df['Plan_Type'].value_counts()
colors3 = PALETTE[:len(plan_type_counts)]
wedges3, texts3, autotexts3 = axes[2].pie(plan_type_counts.values,
    labels=[f'{k}\n(n={v})' for k, v in plan_type_counts.items()],
    colors=colors3, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9},
    pctdistance=0.75, wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
axes[2].set_title('Plan Type Distribution', fontweight='bold', fontsize=13)

fig.suptitle('MEASURE PHASE: Baseline Metrics Dashboard', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "baseline_metrics_dashboard.png"), bbox_inches='tight')
plt.close()
print("\n✅ Baseline Metrics Dashboard — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# MONTHLY ENROLLMENT TREND
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 5))
monthly = df.groupby([df['Purchase Date'].dt.to_period('M'), 'Status']).size().unstack(fill_value=0)
monthly.index = monthly.index.astype(str)

if 'Expired' in monthly.columns:
    ax.bar(range(len(monthly)), monthly.get('Expired', 0), color=COLORS['churned'], alpha=0.8, label='Churned', edgecolor='white')
if 'Active' in monthly.columns:
    ax.bar(range(len(monthly)), monthly.get('Active', 0), bottom=monthly.get('Expired', 0),
           color=COLORS['active'], alpha=0.8, label='Active', edgecolor='white')
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly.index, rotation=45, ha='right', fontsize=8)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Members Enrolled', fontsize=12)
ax.set_title('Monthly Enrollment Trend\n(Churned vs Active by Enrollment Month)', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "monthly_enrollment_trend.png"), bbox_inches='tight')
plt.close()
print("✅ Monthly Enrollment Trend — Saved")

# ═══════════════════════════════════════════════════════════════════════════
# CHURN RATE BY CATEGORY TABLE
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("CHURN RATE BREAKDOWN")
print("=" * 70)

for cat_col in ['Plan_Duration_Category', 'Plan_Type', 'Gender', 'Price_Bracket']:
    print(f"\n--- {cat_col} ---")
    summary = df.groupby(cat_col).agg(
        Total=('Is_Churned', 'count'),
        Churned=('Is_Churned', 'sum'),
        Churn_Rate=('Is_Churned', 'mean')
    ).sort_values('Churn_Rate', ascending=False)
    summary['Churn_Rate'] = (summary['Churn_Rate'] * 100).round(1).astype(str) + '%'
    print(summary.to_string())

print("\n\n✅ MEASURE PHASE COMPLETE — All charts saved to:", OUT_DIR)
