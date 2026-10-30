# Improving Member Retention in a Fitness Centre

## Lean Six Sigma DMAIC Project

<div align="center">

### Project Review - 2

**MGT4003 - Lean Six Sigma Principles**  
**Department of Management Studies**  
**Fall Semester 2026**

</div>

---

## Project Team

| Role | Name |
|---|---|
| Author | **Gladwin Daniel P** |
| Author | **Karthikeyan A** |
| Faculty Guide | **Dr. Vadivel SM** |

---

## Project at a Glance

This project applies the **DMAIC methodology** and statistical analysis to understand and reduce member churn at a fitness centre.

The study combines membership records, payment information, member experience survey responses, and customer reviews to identify the main causes of non-renewal and recommend practical retention improvements.

### Business Objective

Reduce monthly member churn from an estimated baseline of approximately **27%** to below **15%** through data-driven operational and engagement improvements.

### Critical-to-Quality Metrics

- **Monthly Member Churn Rate** = Members Lost / Total Active Members at Start
- **Member Renewal Rate** = Members Renewed / Members Eligible for Renewal
- **Defect** = A member who does not renew when their plan expires

---

## What We Have Done

### 1. Define

- Defined the member-retention problem and project scope.
- Established churn and renewal rate as the primary performance measures.
- Created the project charter and SIPOC process view.
- Identified the key customer and business requirements.

### 2. Measure

- Collected and combined membership, payment, survey, and review data.
- Cleaned and standardized the source datasets.
- Created a master member dataset with a binary `Is_Churned` indicator.
- Calculated descriptive statistics and baseline churn metrics.
- Produced histograms, Pareto charts, and enrollment trend visualizations.

### 3. Analyze

- Compared churned and active members using statistical tests.
- Examined the relationship between churn and:
  - Plan duration and plan type
  - Plan price and payment behaviour
  - Member demographics
  - Personal training and trainer engagement
  - Marketing and promotional plans
- Performed t-tests, chi-square tests, variance tests, ANOVA, correlation analysis, and regression analysis.
- Analysed member survey responses and customer-review sentiment.
- Used fishbone and Five Whys analysis to identify root causes.

### 4. Improve

- Developed an FMEA to rank process risks.
- Proposed structured member onboarding.
- Recommended automated renewal reminders at 30, 15, and 7 days before expiry.
- Recommended improved peak-hour capacity management.
- Proposed semester-aligned and pause-able plans for student members.
- Recommended stronger engagement and retention actions for members outside personal training plans.

### 5. Control

- Created control-chart and monitoring outputs for churn.
- Defined follow-up metrics for renewal, engagement, and member experience.
- Recommended ongoing review of churn by plan, price, duration, and member segment.
- Prepared a practical monitoring structure for post-implementation review.

---

## Key Findings

| Finding | Evidence |
|---|---|
| Short-term plans have the highest churn | 1-month plans: approximately **77.0%** churn |
| Annual commitment improves retention | 1-year plans: approximately **15.8%** churn |
| Lower-priced plans are more vulnerable | Plans at or below ₹1,500: approximately **74.9%** churn |
| Student members need a tailored retention strategy | Students represent approximately **47.8%** of members and have approximately **60.2%** churn |
| Price and commitment are strongly connected to retention | Higher plan amount is associated with significantly lower churn |
| Promotional and family plans show better retention | Promotional plans: approximately **27.6%** churn; Family/Couple plans: approximately **37.5%** churn |

### Main Root Causes Identified

1. Low-commitment monthly plans create a high renewal risk.
2. Student plans do not sufficiently reflect semester-based member lifecycles.
3. Renewal follow-up is not automated or consistently timed.
4. Peak-hour overcrowding can reduce the member experience.
5. Onboarding and engagement are not sufficiently structured.
6. Trainer or personal-training participation alone does not guarantee retention.

---

## Repository Contents

```text
LeanSixSigma/
├── data/             # Original Excel datasets and survey data
├── documents/        # Reports and survey PDF
├── images/           # Source images
├── output/           # Generated charts, tables, cleaned data, and VSM
├── presentations/    # Project presentation files
├── scripts/          # Data preparation, analysis, and report scripts
└── README.md         # Project overview and documentation
```

### Important Deliverables

- [Final project report](documents/Lean_Six_Sigma_DMAIC_Project_Report.docx)
- [Final manuscript](documents/Improving_Member_Retention_Fitness_Centre_DMAIC_Final_Manuscript.docx)
- [Project presentations](presentations/)
- [Measure outputs](output/2_Measure/)
- [Analyze outputs](output/3_Analyze/)
- [Improve outputs](output/4_Improve/)
- [Control outputs](output/5_Control/)
- [Cleaned datasets](output/)

---

## Running the Analysis

From the project root:

```powershell
python scripts/01_data_preparation.py
python scripts/02_measure_phase.py
python scripts/03_analyze_phase.py
python scripts/04_survey_analysis.py
python scripts/05_improve_control.py
python scripts/06_generate_report.py
```

The scripts use paths relative to the project directory and write generated results into `output/`.

### Expected Python Packages

- pandas
- numpy
- matplotlib
- seaborn
- scipy
- openpyxl
- python-docx

---

## Project Outcome

The analysis indicates that member churn is driven primarily by **low commitment, weak renewal follow-up, student lifecycle mismatch, peak-hour experience issues, and inconsistent engagement** rather than by a single facility-quality issue.

The recommended DMAIC solution combines better plan design, proactive renewal communication, structured onboarding, improved capacity management, and continuous churn monitoring.

---

## Credits

Prepared by **Gladwin Daniel P** and **Karthikeyan A**  
Under the guidance of **Dr. Vadivel SM**

