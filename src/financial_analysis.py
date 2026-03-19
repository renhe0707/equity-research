"""
泡泡玛特 (9992.HK) 财务分析与可视化
Pop Mart International Group - Financial Analysis & Visualization

Generates charts for the equity research report using publicly available financial data.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import os
import json

# ── Font Setup ──
_cjk_font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if os.path.exists(_cjk_font_path):
    fm.fontManager.addfont(_cjk_font_path)
    fm._load_fontmanager(try_read_cache=False)
    _cjk = "Noto Sans CJK JP"
else:
    _cjk = "DejaVu Sans"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.grid": True, "grid.alpha": 0.3, "grid.linestyle": "--",
    "font.size": 11, "axes.titlesize": 14, "axes.labelsize": 12,
    "legend.fontsize": 10, "figure.dpi": 150,
    "font.family": [_cjk, "DejaVu Sans", "sans-serif"],
    "axes.unicode_minus": False,
    "pdf.fonttype": 42,   # Embed TrueType fonts in PDF
    "savefig.dpi": 150,
})

# Color scheme
PRIMARY = "#1B4F72"
SECONDARY = "#E74C3C"
ACCENT1 = "#F39C12"
ACCENT2 = "#27AE60"
ACCENT3 = "#8E44AD"
ACCENT4 = "#E67E22"
LIGHT_BG = "#F8F9FA"

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "figures")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(OUTPUT_DIR, name), bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Saved: {name}")


# ════════════════════════════════════════════
# Financial Data (from public filings)
# ════════════════════════════════════════════

YEARS = [2020, 2021, 2022, 2023, 2024]
H1_2025 = "H1 2025"

financials = {
    "revenue": [25.13, 44.91, 46.17, 63.01, 130.38],         # 亿元
    "gross_profit": [15.94, 27.59, 26.55, 38.64, 87.08],
    "net_profit": [5.23, 8.55, 4.76, 10.89, 33.08],
    "adj_net_profit": [5.91, 10.02, 5.68, 11.90, 34.00],
    "gross_margin": [63.4, 61.4, 57.5, 61.3, 66.8],          # %
    "net_margin": [20.8, 19.0, 10.3, 17.3, 25.4],
    "total_assets": [69.71, 83.24, 85.80, 99.69, 148.71],
    "total_equity": [61.31, 68.20, 69.65, 77.80, 108.85],
    "total_liabilities": [8.40, 15.04, 16.15, 21.88, 39.86],
    # Revenue by geography (亿元)
    "china_revenue": [None, None, 39.15, 52.35, 79.72],
    "overseas_revenue": [None, None, 7.02, 10.66, 50.66],
    # IP revenue breakdown 2024
    "ip_names_2024": ["THE MONSTERS", "MOLLY", "SKULLPANDA", "CRYBABY", "DIMOO", "Others"],
    "ip_revenue_2024": [30.41, 20.93, 13.08, 11.65, 7.42, 46.89],
    # H1 2025
    "h1_2025_revenue": 138.80,
    "h1_2025_gross_margin": 70.3,
    "h1_2025_net_profit": 45.74,
    "h1_2025_adj_net_profit": 47.10,
    # Category breakdown 2024
    "category_names": ["手办 Figurines", "毛绒 Plush", "MEGA", "衍生品 Derivatives"],
    "category_revenue": [69.4, 28.3, 16.8, 15.9],
    # Overseas breakdown 2024
    "region_names": ["东南亚\nSoutheast Asia", "北美\nNorth America", "东亚\nEast Asia", "欧澳其他\nEurope & Others"],
    "region_revenue": [24.03, 7.23, 13.86, 5.54],
    # Store count
    "store_years": [2020, 2021, 2022, 2023, 2024, "H1 2025"],
    "china_stores": [187, 215, 329, 363, 401, 443],
    "overseas_stores": [0, 7, 43, 80, 130, 128],  # 128 = ex-China at H1 2025
    "robo_shops": [1351, 1553, 2067, 2190, 2300, 2597],
    # Valuation
    "eps_hkd": [None, None, None, None, 2.42],  # 2024 EPS in HKD
    "stock_price_hkd": 217.80,  # as of Mar 17 2026
    "shares_outstanding_m": 1343,  # million shares
    "market_cap_hkd_b": 292,  # billion HKD
}

# Save raw data
with open(os.path.join(DATA_DIR, "popmart_financials.json"), "w", encoding="utf-8") as f:
    # Convert to serializable
    data_out = {k: v for k, v in financials.items()}
    json.dump(data_out, f, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════
# Chart 1: Revenue & Net Profit Growth
# ════════════════════════════════════════════

def plot_revenue_profit():
    fig, ax1 = plt.subplots(figsize=(12, 6))

    x = np.arange(len(YEARS))
    w = 0.35

    bars1 = ax1.bar(x - w/2, financials["revenue"], w, label="Revenue 营收", color=PRIMARY, alpha=0.9)
    bars2 = ax1.bar(x + w/2, financials["net_profit"], w, label="Net Profit 净利润", color=ACCENT1, alpha=0.9)

    ax1.set_xlabel("")
    ax1.set_ylabel("RMB (Billion 亿元)")
    ax1.set_title("Pop Mart Revenue & Net Profit (2020-2024)\n泡泡玛特营收与净利润", fontsize=15, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(YEARS)
    ax1.legend(loc="upper left")

    # Add value labels
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}", ha="center", fontsize=9, fontweight="bold")
    for bar in bars2:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"{h:.1f}", ha="center", fontsize=9)

    # YoY growth line on secondary axis
    ax2 = ax1.twinx()
    rev_growth = [None] + [financials["revenue"][i]/financials["revenue"][i-1]-1 for i in range(1, len(YEARS))]
    ax2.plot(x[1:], [g*100 for g in rev_growth[1:]], 'o-', color=SECONDARY, linewidth=2, markersize=6, label="Revenue YoY Growth %")
    ax2.set_ylabel("YoY Growth %")
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax2.legend(loc="upper right")

    _save(fig, "01_revenue_profit.png")


# ════════════════════════════════════════════
# Chart 2: Margin Trends
# ════════════════════════════════════════════

def plot_margins():
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(YEARS, financials["gross_margin"], 'o-', color=PRIMARY, linewidth=2.5, markersize=8, label="Gross Margin 毛利率")
    ax.plot(YEARS, financials["net_margin"], 's-', color=ACCENT1, linewidth=2.5, markersize=8, label="Net Margin 净利率")

    # H1 2025 point
    ax.plot(2025.5, financials["h1_2025_gross_margin"], '^', color=PRIMARY, markersize=12, zorder=5)
    ax.annotate(f'H1 2025: {financials["h1_2025_gross_margin"]}%',
                xy=(2025.5, financials["h1_2025_gross_margin"]),
                xytext=(2025.5, financials["h1_2025_gross_margin"]+3),
                ha="center", fontsize=9, color=PRIMARY, fontweight="bold")

    for i, (gm, nm) in enumerate(zip(financials["gross_margin"], financials["net_margin"])):
        ax.text(YEARS[i], gm + 1.5, f"{gm}%", ha="center", fontsize=9, color=PRIMARY)
        ax.text(YEARS[i], nm - 3, f"{nm}%", ha="center", fontsize=9, color=ACCENT1)

    ax.set_ylabel("Margin %")
    ax.set_title("Pop Mart Profitability Trend (2020-H1 2025)\n泡泡玛特盈利能力趋势", fontsize=15, fontweight="bold")
    ax.legend()
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))

    _save(fig, "02_margins.png")


# ════════════════════════════════════════════
# Chart 3: Revenue by Geography
# ════════════════════════════════════════════

def plot_geography():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: stacked bar
    years_geo = [2022, 2023, 2024]
    china = [39.15, 52.35, 79.72]
    overseas = [7.02, 10.66, 50.66]

    x = np.arange(len(years_geo))
    ax1.bar(x, china, 0.5, label="China 中国", color=PRIMARY)
    ax1.bar(x, overseas, 0.5, bottom=china, label="Overseas 海外", color=ACCENT1)

    for i in range(len(years_geo)):
        ax1.text(x[i], china[i]/2, f"{china[i]:.1f}", ha="center", va="center", color="white", fontweight="bold")
        ax1.text(x[i], china[i]+overseas[i]/2, f"{overseas[i]:.1f}", ha="center", va="center", color="white", fontweight="bold")

    overseas_pct = [o/(c+o)*100 for c, o in zip(china, overseas)]
    for i in range(len(years_geo)):
        ax1.text(x[i], china[i]+overseas[i]+2, f"Overseas: {overseas_pct[i]:.0f}%", ha="center", fontsize=9, color=ACCENT1)

    ax1.set_xticks(x)
    ax1.set_xticklabels(years_geo)
    ax1.set_ylabel("RMB (Billion 亿元)")
    ax1.set_title("Revenue by Region 地区营收", fontsize=13, fontweight="bold")
    ax1.legend()

    # Right: overseas breakdown 2024 pie
    ax2.pie(financials["region_revenue"], labels=financials["region_names"],
            autopct='%1.1f%%', colors=[PRIMARY, SECONDARY, ACCENT2, ACCENT3],
            startangle=90, textprops={"fontsize": 9})
    ax2.set_title("2024 Overseas Revenue Split\n2024年海外营收分布", fontsize=13, fontweight="bold")

    fig.suptitle("Pop Mart Global Revenue Breakdown | 泡泡玛特全球营收拆解", fontsize=15, fontweight="bold", y=1.02)

    _save(fig, "03_geography.png")


# ════════════════════════════════════════════
# Chart 4: IP Revenue Breakdown 2024
# ════════════════════════════════════════════

def plot_ip_breakdown():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: IP pie
    colors = [SECONDARY, PRIMARY, ACCENT3, ACCENT1, ACCENT2, "#BDC3C7"]
    explode = [0.05, 0, 0, 0, 0, 0]
    ax1.pie(financials["ip_revenue_2024"], labels=financials["ip_names_2024"],
            autopct='%1.1f%%', colors=colors, explode=explode,
            startangle=140, textprops={"fontsize": 9})
    ax1.set_title("2024 IP Revenue Split\n2024年IP营收占比", fontsize=13, fontweight="bold")

    # Right: category breakdown
    cat_colors = [PRIMARY, ACCENT1, ACCENT2, ACCENT3]
    bars = ax2.barh(financials["category_names"], financials["category_revenue"], color=cat_colors, alpha=0.9)
    for bar, val in zip(bars, financials["category_revenue"]):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"¥{val:.1f}B", va="center", fontsize=10, fontweight="bold")
    ax2.set_xlabel("RMB (Billion 亿元)")
    ax2.set_title("2024 Product Category Revenue\n2024年品类营收", fontsize=13, fontweight="bold")
    ax2.invert_yaxis()

    fig.suptitle("Pop Mart IP & Product Portfolio | 泡泡玛特IP与品类组合", fontsize=15, fontweight="bold", y=1.02)

    _save(fig, "04_ip_breakdown.png")


# ════════════════════════════════════════════
# Chart 5: Store Expansion
# ════════════════════════════════════════════

def plot_stores():
    fig, ax = plt.subplots(figsize=(12, 5))

    x = np.arange(len(financials["store_years"]))
    labels = [str(y) for y in financials["store_years"]]
    w = 0.25

    ax.bar(x - w, financials["china_stores"], w, label="China Stores 中国门店", color=PRIMARY)
    ax.bar(x, financials["overseas_stores"], w, label="Overseas Stores 海外门店", color=ACCENT1)
    ax.bar(x + w, [r/10 for r in financials["robo_shops"]], w, label="Robo Shops (÷10) 机器人商店", color=ACCENT2, alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Count")
    ax.set_title("Pop Mart Retail Network Expansion (2020-H1 2025)\n泡泡玛特零售网络扩张", fontsize=15, fontweight="bold")
    ax.legend()

    # Annotate total stores
    for i in range(len(x)):
        total = financials["china_stores"][i] + financials["overseas_stores"][i]
        ax.text(x[i] - w, financials["china_stores"][i] + 5, str(financials["china_stores"][i]),
                ha="center", fontsize=8)
        ax.text(x[i], financials["overseas_stores"][i] + 5, str(financials["overseas_stores"][i]),
                ha="center", fontsize=8)

    _save(fig, "05_stores.png")


# ════════════════════════════════════════════
# Chart 6: DuPont ROE Decomposition
# ════════════════════════════════════════════

def plot_dupont():
    fig, ax = plt.subplots(figsize=(12, 6))

    # Compute DuPont components
    net_margin_pct = np.array(financials["net_margin"]) / 100
    asset_turnover = np.array(financials["revenue"]) / np.array(financials["total_assets"])
    equity_multiplier = np.array(financials["total_assets"]) / np.array(financials["total_equity"])
    roe = net_margin_pct * asset_turnover * equity_multiplier * 100

    x = np.arange(len(YEARS))
    w = 0.25

    # Bars for sub-components
    bars1 = ax.bar(x - w, np.array(financials["net_margin"]), w, alpha=0.6, color=ACCENT1, label="Net Margin 净利率 %")
    bars2 = ax.bar(x, asset_turnover * 100, w, alpha=0.6, color=ACCENT2, label="Asset Turnover 资产周转 ×100")
    bars3 = ax.bar(x + w, equity_multiplier * 10, w, alpha=0.6, color=ACCENT3, label="Equity Multiplier 权益乘数 ×10")

    # ROE line on secondary axis
    ax2 = ax.twinx()
    ax2.plot(x, roe, 'D-', color=PRIMARY, linewidth=2.5, markersize=10, label="ROE", zorder=5)
    ax2.fill_between(x, roe, alpha=0.08, color=PRIMARY)

    for i, r in enumerate(roe):
        ax2.text(x[i], r + 1.5, f"{r:.1f}%", ha="center", fontsize=11, fontweight="bold", color=PRIMARY)

    ax.set_xticks(x)
    ax.set_xticklabels(YEARS)
    ax.set_ylabel("Component Value")
    ax2.set_ylabel("ROE %")
    ax.set_title("DuPont ROE Decomposition (2020-2024)\n杜邦分析ROE拆解", fontsize=15, fontweight="bold")

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    _save(fig, "06_dupont_roe.png")


# ════════════════════════════════════════════
# Chart 7: DCF Sensitivity Table
# ════════════════════════════════════════════

def plot_dcf_sensitivity():
    """DCF fair value sensitivity analysis"""
    # Base assumptions
    base_fcf_2025e = 85.0  # 亿元 estimated 2025 FCF
    
    wacc_range = [0.09, 0.10, 0.11, 0.12, 0.13]
    tgr_range = [0.02, 0.03, 0.04, 0.05]  # terminal growth rate
    
    # Growth assumptions: 50% → 30% → 20% → 15% → TGR
    growth_rates = [0.50, 0.30, 0.20, 0.15]
    
    results = np.zeros((len(wacc_range), len(tgr_range)))
    
    shares = financials["shares_outstanding_m"]  # million shares
    
    for i, wacc in enumerate(wacc_range):
        for j, tgr in enumerate(tgr_range):
            # Project FCF
            fcf = base_fcf_2025e
            pv_sum = 0
            for yr, g in enumerate(growth_rates):
                fcf = fcf * (1 + g) if yr > 0 else fcf
                pv_sum += fcf / (1 + wacc) ** (yr + 1)
            
            # Terminal value
            terminal_fcf = fcf * (1 + tgr)
            terminal_value = terminal_fcf / (wacc - tgr)
            pv_terminal = terminal_value / (1 + wacc) ** len(growth_rates)
            
            # Per share (convert to HKD: ~1.1 rate)
            equity_value = (pv_sum + pv_terminal)  # in 亿元
            per_share_rmb = equity_value / shares * 10000  # 亿→万→元 per share (亿/百万=万分之一)
            # Actually: equity_value in 亿元 = equity_value * 1e8 RMB
            # shares in millions = shares * 1e6
            # per share = equity_value * 1e8 / (shares * 1e6) = equity_value * 100 / shares
            per_share_rmb = equity_value * 100 / shares
            per_share_hkd = per_share_rmb * 1.1  # rough RMB→HKD
            
            results[i, j] = per_share_hkd
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    
    # Build table
    col_labels = [f"TGR={g:.0%}" for g in tgr_range]
    row_labels = [f"WACC={w:.0%}" for w in wacc_range]
    
    cell_text = [[f"HK${v:.0f}" for v in row] for row in results]
    
    table = ax.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels,
                      loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.3, 1.8)
    
    # Style
    for j in range(len(col_labels)):
        table[0, j].set_facecolor(PRIMARY)
        table[0, j].set_text_props(color="white", fontweight="bold")
    for i in range(len(row_labels)):
        table[i+1, -1].set_facecolor("#E8EEF2")
        table[i+1, -1].set_text_props(fontweight="bold")
    
    # Highlight cells near current price
    current_price = financials["stock_price_hkd"]
    for i in range(len(wacc_range)):
        for j in range(len(tgr_range)):
            if abs(results[i, j] - current_price) / current_price < 0.15:
                table[i+1, j].set_facecolor("#FADBD8")
    
    ax.set_title(f"DCF Sensitivity Analysis (Current Price: HK${current_price:.0f})\nDCF估值敏感性分析",
                 fontsize=15, fontweight="bold", pad=20)
    
    _save(fig, "07_dcf_sensitivity.png")
    
    # Save DCF model data
    dcf_data = {
        "base_fcf_2025e_rmb_bn": base_fcf_2025e,
        "growth_path": growth_rates,
        "wacc_range": wacc_range,
        "tgr_range": tgr_range,
        "results_hkd_per_share": results.tolist(),
        "current_price_hkd": current_price,
    }
    with open(os.path.join(DATA_DIR, "dcf_model.json"), "w") as f:
        json.dump(dcf_data, f, indent=2)


# ════════════════════════════════════════════
# Generate All
# ════════════════════════════════════════════

def main():
    print("Generating Pop Mart equity research charts...")
    plot_revenue_profit()
    plot_margins()
    plot_geography()
    plot_ip_breakdown()
    plot_stores()
    plot_dupont()
    plot_dcf_sensitivity()
    print("\nAll charts generated!")


if __name__ == "__main__":
    main()
