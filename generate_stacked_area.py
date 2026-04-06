import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Read data
df = pd.read_excel('BP3_keyword_search_v2.xlsx', sheet_name='Keyword_Hits')

# Aggregate by keyword and year
agg = df.groupby(['keyword', 'year'])['count'].sum().reset_index()

# Define groups
flow_keywords = ['debt rescheduling', 'debt reprofiling', 'maturity extension']
stock_keywords = ['debt restructuring', 'debt reduction', 'debt relief', 'HIPC', 'debt forgiveness', 'haircut']

# Filter to period up to 2004
agg = agg[agg['year'] <= 2004]

# Build pivot tables (years as index, keywords as columns)
all_years = range(int(agg['year'].min()), 2005)

def build_pivot(keywords):
    sub = agg[agg['keyword'].isin(keywords)]
    piv = sub.pivot_table(index='year', columns='keyword', values='count', fill_value=0)
    piv = piv.reindex(all_years, fill_value=0)
    # Reorder columns to match the keyword list order (only existing ones)
    cols = [k for k in keywords if k in piv.columns]
    return piv[cols]

flow_data = build_pivot(flow_keywords)
stock_data = build_pivot(stock_keywords)

# Color palettes
flow_colors = ['#2166ac', '#67a9cf', '#d1e5f0']  # blues
stock_colors = ['#b2182b', '#ef8a62', '#fddbc7', '#f4a582', '#d6604d', '#878787']  # reds/warm

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=False)

# --- Flow treatment (left) ---
ax1.stackplot(flow_data.index, flow_data.values.T,
              labels=flow_data.columns, colors=flow_colors[:len(flow_data.columns)], alpha=0.85)
ax1.set_title('Flow Treatment Keywords', fontsize=14, fontweight='bold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Total keyword mentions (across all countries)')
ax1.legend(loc='upper left', fontsize=9)
ax1.set_xlim(flow_data.index.min(), flow_data.index.max())
ax1.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax1.axvline(x=1989, color='black', linestyle='--', linewidth=1, alpha=0.7, label='Brady Plan (1989)')

# --- Stock treatment (right) ---
ax2.stackplot(stock_data.index, stock_data.values.T,
              labels=stock_data.columns, colors=stock_colors[:len(stock_data.columns)], alpha=0.85)
ax2.set_title('Stock Treatment Keywords', fontsize=14, fontweight='bold')
ax2.set_xlabel('Year')
ax2.set_ylabel('Total keyword mentions (across all countries)')
ax2.legend(loc='upper left', fontsize=9)
ax2.set_xlim(stock_data.index.min(), stock_data.index.max())
ax2.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax2.axvline(x=1989, color='black', linestyle='--', linewidth=1, alpha=0.7, label='Brady Plan (1989)')

fig.suptitle('Keyword Trends Over Time: Flow vs Stock Treatment',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig('charts/keyword_flow_vs_stock_stacked.png', dpi=200, bbox_inches='tight')
print('Saved to charts/keyword_flow_vs_stock_stacked.png')
