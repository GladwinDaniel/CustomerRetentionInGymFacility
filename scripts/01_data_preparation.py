"""
=============================================================================
LEAN SIX SIGMA — DATA PREPARATION
Ultimate Fitness Centre: Customer Churn Analysis
=============================================================================
Cleans and prepares all datasets for DMAIC analysis.
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "output")

# ── 1. Load Membership Data ─────────────────────────────────────────────────
print("=" * 70)
print("STEP 1: Loading Membership Datasets")
print("=" * 70)

df_all = pd.read_excel(os.path.join(DATA_DIR, "Ultimate_fitness_centre_All Members (1).xlsx"))
df_active = pd.read_excel(os.path.join(DATA_DIR, "Ultimate_fitness_centre_Active Members.xlsx"))
df_expired = pd.read_excel(os.path.join(DATA_DIR, "Ultimate_fitness_centre_Expired Members.xlsx"))
df_partial = pd.read_excel(os.path.join(DATA_DIR, "Ultimate_fitness_centre_Partial Paid Members.xlsx"))

print(f"  All Members:     {len(df_all)} records")
print(f"  Active Members:  {len(df_active)} records")
print(f"  Expired Members: {len(df_expired)} records")
print(f"  Partial Paid:    {len(df_partial)} records")

# ── 2. Create Master Dataset with Churn Labels ──────────────────────────────
print("\n" + "=" * 70)
print("STEP 2: Creating Master Dataset with Churn Labels")
print("=" * 70)

# Use All Members as master
df = df_all.copy()

# Add churn status based on whether member is in active or expired list
active_ids = set(df_active['Member Id'].values)
expired_ids = set(df_expired['Member Id'].values)
partial_ids = set(df_partial['Member Id'].values)

df['Status'] = df['Member Id'].apply(
    lambda x: 'Active' if x in active_ids else ('Expired' if x in expired_ids else 'Unknown')
)
df['Is_Churned'] = (df['Status'] == 'Expired').astype(int)
df['Has_Pending_Payment'] = (df['Pending Amount'] > 0).astype(int)
df['Is_Partial_Paid'] = df['Member Id'].isin(partial_ids).astype(int)

# ── 3. Parse Dates & Create Duration Features ──────────────────────────────
print("STEP 3: Parsing Dates and Creating Duration Features")

# Parse dates
for col in ['Member Added', 'Purchase Date', 'Expiry Date']:
    df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=True, errors='coerce')

# Membership duration in days
df['Membership_Duration_Days'] = (df['Expiry Date'] - df['Purchase Date']).dt.days

# ── 4. Categorize Plan Types ────────────────────────────────────────────────
print("STEP 4: Categorizing Plan Types")

def categorize_plan_duration(plan_name):
    """Categorize plan into duration bucket based on plan name."""
    if pd.isna(plan_name):
        return 'Unknown'
    plan_lower = str(plan_name).lower()
    if 'one year' in plan_lower or '1 one year' in plan_lower or '1 year' in plan_lower or 'year' in plan_lower:
        return '1 Year'
    elif '6 month' in plan_lower:
        return '6 Months'
    elif '3 month' in plan_lower:
        return '3 Months'
    elif '2 month' in plan_lower:
        return '2 Months'
    elif '1 month' in plan_lower:
        return '1 Month'
    else:
        return 'Other'

def categorize_plan_type(plan_name):
    """Categorize plan into type (Student, Family, PT, Regular, Offer)."""
    if pd.isna(plan_name):
        return 'Unknown'
    plan_lower = str(plan_name).lower()
    if 'personal training' in plan_lower or 'pt' in plan_lower:
        return 'Personal Training'
    elif 'student' in plan_lower or 'school' in plan_lower:
        return 'Student'
    elif 'family' in plan_lower or 'couple' in plan_lower:
        return 'Family/Couple'
    elif 'offer' in plan_lower or 'summer' in plan_lower or 'anniversary' in plan_lower or 'exchange' in plan_lower:
        return 'Promotional/Offer'
    else:
        return 'Regular'

def categorize_price_bracket(amount):
    """Categorize plan amount into price bracket."""
    if pd.isna(amount):
        return 'Unknown'
    if amount <= 1500:
        return 'Low (≤₹1,500)'
    elif amount <= 3500:
        return 'Medium (₹1,501-₹3,500)'
    elif amount <= 7500:
        return 'Mid-High (₹3,501-₹7,500)'
    else:
        return 'High (>₹7,500)'

df['Plan_Duration_Category'] = df['Plan Name'].apply(categorize_plan_duration)
df['Plan_Type'] = df['Plan Name'].apply(categorize_plan_type)
df['Price_Bracket'] = df['Plan Amount'].apply(categorize_price_bracket)
df['Payment_Gap'] = df['Plan Amount'] - df['Paid']

# Month of joining
df['Join_Month'] = df['Purchase Date'].dt.month
df['Join_Month_Name'] = df['Purchase Date'].dt.strftime('%b')

print(f"\n  Plan Duration Categories: {df['Plan_Duration_Category'].value_counts().to_dict()}")
print(f"  Plan Types: {df['Plan_Type'].value_counts().to_dict()}")
print(f"  Status: {df['Status'].value_counts().to_dict()}")

# ── 5. Clean Reviews Data ───────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 5: Cleaning Reviews Data")
print("=" * 70)

df_reviews_raw = pd.read_excel(os.path.join(DATA_DIR, "Outscraper-20260907160904s41b6.xlsx"))
print(f"  Raw columns: {list(df_reviews_raw.columns)}")
print(f"  Raw rows: {len(df_reviews_raw)}")

# Keep only useful columns
keep_cols = []
for col in df_reviews_raw.columns:
    if col in ['author_title', 'review_text', 'review_rating', 'review_datetime_utc',
               'owner_answer', 'review_likes']:
        keep_cols.append(col)

df_reviews = df_reviews_raw[keep_cols].copy()

# Clean
df_reviews = df_reviews.dropna(subset=['review_rating'])
df_reviews['review_datetime_utc'] = pd.to_datetime(df_reviews['review_datetime_utc'], errors='coerce')
df_reviews['review_text'] = df_reviews['review_text'].fillna('')
df_reviews['has_text'] = (df_reviews['review_text'].str.len() > 0).astype(int)
df_reviews['has_owner_reply'] = df_reviews['owner_answer'].notna().astype(int)

# Rating categories
df_reviews['Rating_Category'] = pd.cut(
    df_reviews['review_rating'],
    bins=[0, 2, 3, 5],
    labels=['Negative (1-2)', 'Neutral (3)', 'Positive (4-5)']
)

print(f"\n  Cleaned Reviews: {len(df_reviews)} records")
print(f"  Columns kept: {list(df_reviews.columns)}")
print(f"  Rating distribution:\n{df_reviews['review_rating'].value_counts().sort_index()}")

# ── 6. Save Cleaned Data ────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 6: Saving Cleaned Datasets")
print("=" * 70)

df.to_csv(os.path.join(OUT_DIR, "members_master_cleaned.csv"), index=False)
df_reviews.to_csv(os.path.join(OUT_DIR, "reviews_cleaned.csv"), index=False)

print(f"  ✅ Saved: members_master_cleaned.csv ({len(df)} rows, {len(df.columns)} cols)")
print(f"  ✅ Saved: reviews_cleaned.csv ({len(df_reviews)} rows, {len(df_reviews.columns)} cols)")

# ── 7. Summary Stats ────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("DATA SUMMARY")
print("=" * 70)
print(f"  Total Members:          {len(df)}")
print(f"  Active Members:         {len(df[df['Status']=='Active'])} ({len(df[df['Status']=='Active'])/len(df)*100:.1f}%)")
print(f"  Churned Members:        {len(df[df['Status']=='Expired'])} ({len(df[df['Status']=='Expired'])/len(df)*100:.1f}%)")
print(f"  Churn Rate:             {df['Is_Churned'].mean()*100:.2f}%")
print(f"  Male:                   {len(df[df['Gender']=='male'])} ({len(df[df['Gender']=='male'])/len(df)*100:.1f}%)")
print(f"  Female:                 {len(df[df['Gender']=='female'])} ({len(df[df['Gender']=='female'])/len(df)*100:.1f}%)")
print(f"  Avg Plan Amount:        ₹{df['Plan Amount'].mean():,.0f}")
print(f"  Median Plan Amount:     ₹{df['Plan Amount'].median():,.0f}")
print(f"  Avg Duration (days):    {df['Membership_Duration_Days'].mean():.0f}")
print(f"  Google Reviews:         {len(df_reviews)}")
print(f"  Avg Review Rating:      {df_reviews['review_rating'].mean():.2f}")

print("\n✅ Data preparation complete! Ready for DMAIC analysis.")
