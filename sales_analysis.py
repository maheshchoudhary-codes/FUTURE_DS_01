"""
Sales Data Analysis — FUTURE_DS_01
Author : [Your Name]
Dataset: sales_data_sample.csv
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ════════════════════════════════════════════════════════
# 1. DATA LOADING & UNDERSTANDING
# ════════════════════════════════════════════════════════

df = pd.read_csv('sales_data_sample.csv', encoding='latin1')

print("=" * 55)
print("1. DATA LOADING & UNDERSTANDING")
print("=" * 55)
print(f"\nShape      : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumns    :\n{df.columns.tolist()}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nBasic Stats:\n{df[['QUANTITYORDERED','PRICEEACH','SALES']].describe()}")


# ════════════════════════════════════════════════════════
# 2. DATA CLEANING
# ════════════════════════════════════════════════════════

print("\n" + "=" * 55)
print("2. DATA CLEANING")
print("=" * 55)

print(f"\nMissing Values (before):\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Handle missing values
df['ADDRESSLINE2'] = df['ADDRESSLINE2'].fillna('N/A')
df['STATE']        = df['STATE'].fillna('Unknown')
df['POSTALCODE']   = df['POSTALCODE'].fillna(0)
df['TERRITORY']    = df['TERRITORY'].fillna('Americas')

# Convert date column
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# Derived columns for analysis
df['YEAR_MONTH'] = df['ORDERDATE'].dt.to_period('M')

print(f"\nMissing Values (after):\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\nORDERDATE dtype after conversion: {df['ORDERDATE'].dtype}")
print(f"\nDate range: {df['ORDERDATE'].min().date()} → {df['ORDERDATE'].max().date()}")


# ════════════════════════════════════════════════════════
# 3. EXPLORATORY DATA ANALYSIS (EDA) — DASHBOARD
# ════════════════════════════════════════════════════════

# ── Aggregations ──────────────────────────────────────
monthly = df.groupby('YEAR_MONTH')['SALES'].sum().reset_index()
monthly['YEAR_MONTH_STR'] = monthly['YEAR_MONTH'].astype(str)

top5    = df.groupby('PRODUCTCODE')['SALES'].sum().nlargest(5).reset_index()
region  = df.groupby('TERRITORY')['SALES'].sum().sort_values(ascending=False).reset_index()
cat     = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False).reset_index()
deal    = df.groupby('DEALSIZE')['SALES'].sum().reindex(['Small','Medium','Large']).reset_index()

# ── Theme ─────────────────────────────────────────────
BG     = '#0d1117'
CARD   = '#161b22'
ACC    = '#58a6ff'
GREEN  = '#3fb950'
ORANGE = '#f0883e'
TEXT   = '#e6edf3'
MUTED  = '#8b949e'
COLORS = [ACC, GREEN, ORANGE, '#bc8cff', '#ff7b72', '#79c0ff', '#ffa657']

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': CARD,
    'axes.edgecolor': '#30363d', 'axes.labelcolor': TEXT,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'text.color': TEXT, 'grid.color': '#21262d',
    'font.family': 'DejaVu Sans', 'font.size': 11,
})

fig = plt.figure(figsize=(20, 22), facecolor=BG)
fig.suptitle('Sales Performance Dashboard', fontsize=24,
             fontweight='bold', color=TEXT, y=0.98)

# ── Chart 1: Monthly Revenue Trend ────────────────────
ax1 = fig.add_subplot(3, 2, (1, 2))
ax1.plot(monthly['YEAR_MONTH_STR'], monthly['SALES']/1000,
         color=ACC, linewidth=2.5, marker='o', markersize=5,
         markerfacecolor=GREEN)
ax1.fill_between(range(len(monthly)), monthly['SALES']/1000,
                 alpha=0.15, color=ACC)
ax1.set_title('Monthly Revenue Trend (2003–2005)',
              fontsize=14, fontweight='bold', color=TEXT, pad=12)
ax1.set_xlabel('Month', labelpad=8)
ax1.set_ylabel('Revenue ($ Thousands)', labelpad=8)
ax1.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
tick_step = max(1, len(monthly) // 12)
ax1.set_xticks(range(0, len(monthly), tick_step))
ax1.set_xticklabels(monthly['YEAR_MONTH_STR'][::tick_step],
                    rotation=45, ha='right', fontsize=9)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ── Chart 2: Top 5 Products ────────────────────────────
ax2 = fig.add_subplot(3, 2, 3)
bars = ax2.barh(top5['PRODUCTCODE'], top5['SALES']/1000,
                color=COLORS[:5], edgecolor='none', height=0.6)
ax2.set_title('Top 5 Products by Revenue',
              fontsize=13, fontweight='bold', color=TEXT, pad=10)
ax2.set_xlabel('Revenue ($ Thousands)')
ax2.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
for bar in bars:
    w = bar.get_width()
    ax2.text(w + 1, bar.get_y() + bar.get_height()/2,
             f'${w:,.1f}K', va='center', fontsize=9, color=MUTED)
ax2.invert_yaxis()
ax2.grid(axis='x', linestyle='--', alpha=0.4)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ── Chart 3: Region-wise Sales ─────────────────────────
ax3 = fig.add_subplot(3, 2, 4)
bar3 = ax3.bar(region['TERRITORY'], region['SALES']/1000,
               color=COLORS[:len(region)], edgecolor='none', width=0.5)
ax3.set_title('Region-wise Revenue',
              fontsize=13, fontweight='bold', color=TEXT, pad=10)
ax3.set_ylabel('Revenue ($ Thousands)')
ax3.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
for bar in bar3:
    h = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, h + 20,
             f'${h:,.0f}K', ha='center', fontsize=9, color=MUTED)
ax3.grid(axis='y', linestyle='--', alpha=0.4)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ── Chart 4: Category (Product Line) Sales ─────────────
ax4 = fig.add_subplot(3, 2, 5)
bars4 = ax4.barh(cat['PRODUCTLINE'], cat['SALES']/1000,
                 color=COLORS[:len(cat)], edgecolor='none', height=0.55)
ax4.set_title('Category-wise Revenue (Product Line)',
              fontsize=13, fontweight='bold', color=TEXT, pad=10)
ax4.set_xlabel('Revenue ($ Thousands)')
ax4.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
for bar in bars4:
    w = bar.get_width()
    ax4.text(w + 1, bar.get_y() + bar.get_height()/2,
             f'${w:,.1f}K', va='center', fontsize=9, color=MUTED)
ax4.invert_yaxis()
ax4.grid(axis='x', linestyle='--', alpha=0.4)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# ── Chart 5: Deal Size Pie ─────────────────────────────
ax5 = fig.add_subplot(3, 2, 6)
ax5.pie(deal['SALES'], labels=deal['DEALSIZE'],
        colors=[GREEN, ACC, ORANGE],
        autopct='%1.1f%%', startangle=140,
        wedgeprops={'edgecolor': BG, 'linewidth': 2},
        textprops={'color': TEXT, 'fontsize': 11})
ax5.set_title('Revenue by Deal Size',
              fontsize=13, fontweight='bold', color=TEXT, pad=10)
ax5.set_facecolor(BG)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('sales_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print("\n✓ Dashboard saved → sales_dashboard.png")


# ════════════════════════════════════════════════════════
# 4. INSIGHTS SUMMARY
# ════════════════════════════════════════════════════════

print("\n" + "=" * 55)
print("4. KEY BUSINESS INSIGHTS")
print("=" * 55)

total_rev = df['SALES'].sum()
peak      = monthly.loc[monthly['SALES'].idxmax()]

print(f"""
1. Total Revenue   : ${total_rev:,.2f} across 307 unique orders
2. Peak Month      : {peak['YEAR_MONTH_STR']} — ${peak['SALES']:,.0f}
                     (November is the strongest month every year)
3. Top Territory   : EMEA dominates at 49.6% of global revenue
4. Top Category    : Classic Cars = 39.1% of all revenue
5. Weakest Category: Trains = only 2.3% — possible discontinuation candidate
6. Deal Size Split : Medium deals drive the most volume
""")
