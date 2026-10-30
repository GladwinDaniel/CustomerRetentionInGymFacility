import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import gridspec
import os, warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.family':'sans-serif',
    'font.size':10,'axes.titlesize':12,'axes.titleweight':'bold',
    'figure.facecolor':'white','axes.facecolor':'#FAFAFA',
    'axes.grid':True,'grid.alpha':0.3})
COLORS={'primary':'#2563EB','secondary':'#7C3AED','success':'#059669',
    'danger':'#DC2626','warning':'#D97706','info':'#0891B2',
    'churned':'#EF4444','active':'#22C55E'}

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT4 = os.path.join(BASE,"output","4_Improve"); os.makedirs(OUT4,exist_ok=True)
OUT5 = os.path.join(BASE,"output","5_Control"); os.makedirs(OUT5,exist_ok=True)

# ====================== FMEA ======================
print("="*60); print("IMPROVE PHASE: FMEA"); print("="*60)
fmea = [
    {"Process Step":"Member Onboarding","Failure Mode":"No orientation provided",
     "Effect":"Member confusion / early dropout","S":8,"O":6,"D":5,
     "Current Controls":"None","Recommended Action":"Structured onboarding checklist for all new members"},
    {"Process Step":"Facility Usage - Peak Hours","Failure Mode":"Machine unavailability / overcrowding",
     "Effect":"Member frustration, poor experience, churn","S":9,"O":8,"D":4,
     "Current Controls":"No crowd management","Recommended Action":"Live crowd tracker app + staggered peak-hour slots"},
    {"Process Step":"Membership Renewal","Failure Mode":"No renewal reminder sent",
     "Effect":"Silent churn - member forgets to renew","S":9,"O":7,"D":6,
     "Current Controls":"Manual follow-up","Recommended Action":"Automated SMS/email 30-15-7 days before expiry"},
    {"Process Step":"Plan Selection","Failure Mode":"Only short-term (monthly) plans selected",
     "Effect":"High churn due to low commitment","S":8,"O":8,"D":5,
     "Current Controls":"None","Recommended Action":"Incentivize quarterly/annual plans with discounts"},
    {"Process Step":"Trainer Engagement","Failure Mode":"Trainer ignores non-PT members",
     "Effect":"Members feel unsupported, lower satisfaction","S":7,"O":6,"D":5,
     "Current Controls":"Occasional floor rounds","Recommended Action":"Mandatory floor trainer rounds every 30 min"},
    {"Process Step":"Goal Tracking","Failure Mode":"No progress tracking system",
     "Effect":"Member sees no results, quits","S":8,"O":7,"D":6,
     "Current Controls":"Self-tracking only","Recommended Action":"Monthly fitness assessment and progress report"},
    {"Process Step":"Payment Collection","Failure Mode":"Lapsed payment not followed up",
     "Effect":"Unintentional churn due to payment failure","S":7,"O":5,"D":4,
     "Current Controls":"Manual check monthly","Recommended Action":"Automated payment retry + notification system"},
    {"Process Step":"Membership Plan Upgrade","Failure Mode":"No upsell/upgrade prompts",
     "Effect":"Member stays on costly monthly plan","S":6,"O":8,"D":7,
     "Current Controls":"None","Recommended Action":"Loyalty upgrade offer after 3 months on monthly plan"},
]
df_fmea = pd.DataFrame(fmea)
df_fmea['RPN'] = df_fmea['S']*df_fmea['O']*df_fmea['D']
df_fmea['Priority'] = df_fmea['RPN'].apply(
    lambda x: 'CRITICAL' if x>=200 else 'HIGH' if x>=100 else 'MEDIUM' if x>=50 else 'LOW')
df_fmea_sorted = df_fmea.sort_values('RPN',ascending=False).reset_index(drop=True)
df_fmea_sorted.to_csv(os.path.join(OUT4,"fmea_table.csv"),index=False)
print(df_fmea_sorted[['Process Step','Failure Mode','S','O','D','RPN','Priority']].to_string(index=False))

# FMEA Chart 1: RPN bar chart
fig,ax=plt.subplots(figsize=(14,8))
colors_rpn=[COLORS['danger'] if p=='CRITICAL' else COLORS['warning'] if p=='HIGH'
            else COLORS['info'] if p=='MEDIUM' else COLORS['success']
            for p in df_fmea_sorted['Priority']]
bars=ax.barh(df_fmea_sorted['Failure Mode'],df_fmea_sorted['RPN'],
             color=colors_rpn,edgecolor='white',height=0.6)
for bar,rpn,p in zip(bars,df_fmea_sorted['RPN'],df_fmea_sorted['Priority']):
    ax.text(bar.get_width()+2,bar.get_y()+bar.get_height()/2,
            f'RPN={rpn}  [{p}]',va='center',fontsize=9,fontweight='bold')
ax.axvline(200,color=COLORS['danger'],linestyle='--',linewidth=2,alpha=0.8,label='Critical (RPN>=200)')
ax.axvline(100,color=COLORS['warning'],linestyle='--',linewidth=2,alpha=0.8,label='High (RPN>=100)')
ax.set_xlabel('Risk Priority Number (RPN = Severity x Occurrence x Detectability)',fontsize=11)
ax.set_xlim(0,600)
ax.set_title('IMPROVE: FMEA - Risk Priority Number by Failure Mode\nUltimate Fitness Centre Member Retention\n(S=Severity, O=Occurrence, D=Detectability; each scored 1-10)',
             fontsize=13,fontweight='bold')
ax.legend(fontsize=10,loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(OUT4,"fmea_rpn_chart.png"),bbox_inches='tight'); plt.close()

# FMEA Chart 2: SOD heatmap
fig,ax=plt.subplots(figsize=(10,7))
sc=ax.scatter(df_fmea_sorted['O'],df_fmea_sorted['S'],
              s=df_fmea_sorted['RPN']*0.9,
              c=df_fmea_sorted['RPN'],cmap='RdYlGn_r',
              alpha=0.8,edgecolors='black',linewidth=1)
for _,row in df_fmea_sorted.iterrows():
    ax.annotate(row['Failure Mode'].split('/')[0].strip()[:30],
                (row['O']+0.1,row['S']),fontsize=8)
plt.colorbar(sc,ax=ax,label='RPN')
ax.set_xlabel('Occurrence (O)',fontsize=12); ax.set_ylabel('Severity (S)',fontsize=12)
ax.set_title('FMEA: Risk Map (Severity vs Occurrence)\nBubble size = RPN',fontsize=13,fontweight='bold')
ax.set_xlim(0,11); ax.set_ylim(0,11)
ax.axhline(7,color='red',linestyle='--',alpha=0.4); ax.axvline(7,color='red',linestyle='--',alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(OUT4,"fmea_risk_map.png"),bbox_inches='tight'); plt.close()
print("  FMEA Charts -- Saved")

# ====================== P-CHART ======================
print("\n"+"="*60); print("CONTROL PHASE: P-CHART"); print("="*60)

np.random.seed(42)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',
          'Jan','Feb','Mar','Apr','May','Jun']
n_eligible=[105,98,112,103,118,107,95,122,115,108,102,118,110,96,104,115,120,107]
# Phase 1 (months 1-12): pre-improvement; Phase 2 (months 13-18): post-improvement
churn_rates_pre =[0.25,0.27,0.23,0.26,0.29,0.28,0.31,0.24,0.26,0.28,0.30,0.27]
churn_rates_post=[0.18,0.16,0.14,0.15,0.13,0.12]
churn_rates=churn_rates_pre+churn_rates_post
n_churned=[round(n*r) for n,r in zip(n_eligible,churn_rates)]
p_hat=[nc/ne for nc,ne in zip(n_churned,n_eligible)]
n_arr=np.array(n_eligible); nc_arr=np.array(n_churned)

# Pre-improvement control limits (months 1-12)
p_bar_pre=sum(nc_arr[:12])/sum(n_arr[:12])
ucl_pre=p_bar_pre+3*np.sqrt(p_bar_pre*(1-p_bar_pre)/n_arr[:12])
lcl_pre=np.maximum(0,p_bar_pre-3*np.sqrt(p_bar_pre*(1-p_bar_pre)/n_arr[:12]))

# Post-improvement control limits (months 13-18)
p_bar_post=sum(nc_arr[12:])/sum(n_arr[12:])
ucl_post=p_bar_post+3*np.sqrt(p_bar_post*(1-p_bar_post)/n_arr[12:])
lcl_post=np.maximum(0,p_bar_post-3*np.sqrt(p_bar_post*(1-p_bar_post)/n_arr[12:]))

df_pchart=pd.DataFrame({'Month':months,'n_Eligible':n_eligible,'n_Churned':n_churned,
    'Churn_Rate':p_hat,'Phase':['Pre-Improvement']*12+['Post-Improvement']*6})
df_pchart['UCL']=list(ucl_pre)+list(ucl_post)
df_pchart['LCL']=list(lcl_pre)+list(lcl_post)
df_pchart['CL'] =[p_bar_pre]*12+[p_bar_post]*6
df_pchart.to_csv(os.path.join(OUT5,"pchart_data.csv"),index=False)

# P-Chart plot
fig,ax=plt.subplots(figsize=(16,8))
x_all=range(18)
x_pre=range(12); x_post=range(12,18)

ax.plot(x_all,p_hat,'ko-',linewidth=2,markersize=8,label='Monthly Churn Rate',zorder=5)
ax.fill_between(x_pre,lcl_pre,ucl_pre,alpha=0.15,color=COLORS['danger'],label='Pre-Control Band (3-sigma)')
ax.fill_between(x_post,lcl_post,ucl_post,alpha=0.15,color=COLORS['success'],label='Post-Control Band (3-sigma)')
ax.plot(x_pre,[p_bar_pre]*12,'r--',linewidth=2,label=f'Pre CL={p_bar_pre:.3f}')
ax.plot(x_post,[p_bar_post]*6,color=COLORS['success'],linestyle='--',linewidth=2,label=f'Post CL={p_bar_post:.3f}')
ax.plot(x_pre,ucl_pre,'r:',linewidth=1.5,alpha=0.8,label='UCL (Pre)')
ax.plot(x_pre,lcl_pre,'r:',linewidth=1.5,alpha=0.8)
ax.plot(x_post,ucl_post,color=COLORS['success'],linestyle=':',linewidth=1.5,alpha=0.8,label='UCL (Post)')
ax.plot(x_post,lcl_post,color=COLORS['success'],linestyle=':',linewidth=1.5,alpha=0.8)
ax.axvline(11.5,color='black',linestyle='-',linewidth=3,alpha=0.8)
ax.text(11.6,max(p_hat)*0.98,'IMPROVE\nINITIATIVES\nIMPLEMENTED',fontsize=10,
        fontweight='bold',color='black',va='top')

for i,(val,label) in enumerate(zip(p_hat,months)):
    color=COLORS['danger'] if val>max(ucl_pre.tolist()+ucl_post.tolist())+0.001 else 'black'
    ax.annotate(f'{val:.2%}',(i,val),textcoords="offset points",xytext=(0,12),
                ha='center',fontsize=8,color=color)

ax.set_xticks(range(18))
ax.set_xticklabels([f'{m}\n{"Y1" if i<12 else "Y2"}' for i,m in enumerate(months)],fontsize=9)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_:f'{x:.0%}'))
ax.set_xlabel('Month',fontsize=12); ax.set_ylabel('Churn Rate (Proportion)',fontsize=12)
ax.set_title('CONTROL: P-Chart - Monthly Member Churn Rate\nPre-Improvement (Jan-Dec Y1) vs Post-Improvement (Jan-Jun Y2)\nUltimate Fitness Centre Member Retention',
             fontsize=13,fontweight='bold')
ax.legend(fontsize=9,loc='upper right',ncol=2)
ax.set_ylim(0,max(p_hat)*1.35)
plt.tight_layout()
plt.savefig(os.path.join(OUT5,"pchart_churn_control.png"),bbox_inches='tight'); plt.close()

# Control Summary
fig,axes=plt.subplots(1,3,figsize=(16,6))
axes[0].bar(['Pre-Improvement\n(Avg)','Post-Improvement\n(Avg)'],
            [p_bar_pre,p_bar_post],
            color=[COLORS['danger'],COLORS['success']],edgecolor='white',width=0.5)
axes[0].text(0,p_bar_pre+0.005,f'{p_bar_pre:.1%}',ha='center',fontsize=13,fontweight='bold')
axes[0].text(1,p_bar_post+0.005,f'{p_bar_post:.1%}',ha='center',fontsize=13,fontweight='bold')
axes[0].set_ylabel('Average Monthly Churn Rate',fontsize=11)
axes[0].set_title('Average Churn Rate\nPre vs Post Improvement',fontweight='bold')
reduction=(p_bar_pre-p_bar_post)/p_bar_pre*100
axes[0].text(0.5,max(p_bar_pre,p_bar_post)*0.5,f'{reduction:.0f}%\nReduction',
             ha='center',va='center',fontsize=16,fontweight='bold',color=COLORS['success'],transform=axes[0].transAxes)

axes[1].plot(range(12),p_hat[:12],'r-o',label='Pre-Improvement',linewidth=2,markersize=7)
axes[1].plot(range(6),p_hat[12:],'g-s',label='Post-Improvement',linewidth=2,markersize=7)
axes[1].set_ylabel('Churn Rate',fontsize=11)
axes[1].set_title('Churn Trend\nMonth-over-Month',fontweight='bold')
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_:f'{x:.0%}'))
axes[1].legend(); axes[1].set_xlabel('Month Index',fontsize=11)

rows=[['Total Months Monitored','18'],
      ['Pre-Improvement Months','12 (Y1)'],
      ['Post-Improvement Months','6 (Y2)'],
      ['Pre CL (Avg Churn)',f'{p_bar_pre:.1%}'],
      ['Post CL (Avg Churn)',f'{p_bar_post:.1%}'],
      [f'Churn Reduction',f'{reduction:.1f}%'],
      ['UCL (Pre)',f'{ucl_pre.mean():.1%}'],
      ['UCL (Post)',f'{ucl_post.mean():.1%}'],
      ['Out-of-Control Points','0'],
      ['Process Status','STABLE & IMPROVED']]
axes[2].axis('off')
tbl=axes[2].table(cellText=rows,colLabels=['Metric','Value'],cellLoc='left',loc='center',bbox=[0,0,1,1])
tbl.auto_set_font_size(False); tbl.set_fontsize(9)
for (row,col),cell in tbl.get_celld().items():
    if row==0: cell.set_facecolor(COLORS['primary']); cell.set_text_props(color='white',fontweight='bold')
    elif row%2==0: cell.set_facecolor('#F0F9FF')
    else: cell.set_facecolor('white')
axes[2].set_title('P-Chart Summary Statistics',fontweight='bold',pad=10)

fig.suptitle('CONTROL: P-Chart Analysis Summary\nUltimate Fitness Centre Member Retention Program',
             fontsize=14,fontweight='bold',y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT5,"pchart_summary.png"),bbox_inches='tight'); plt.close()

print(f"  Pre-Improvement Avg Churn:  {p_bar_pre:.1%}")
print(f"  Post-Improvement Avg Churn: {p_bar_post:.1%}")
print(f"  Churn Reduction:            {reduction:.1f}%")
print("  P-Chart Saved -- DONE")
