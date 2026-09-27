import matplotlib.pyplot as plt
import numpy as np

def test_figures():
    # 1. Pareto
    fig1, ax1 = plt.subplots(figsize=(8.5, 3.8), dpi=100)
    fig1.patch.set_facecolor("white")
    ax1.set_facecolor("white")
    defects = ["Slow Search", "Queue Waiting", "Duplicate UHID", "Report Freeze", "Doctor Conflict", "Billing Delays"]
    counts = [142, 118, 64, 38, 19, 11]
    cum_pct = np.cumsum(counts) / sum(counts) * 100
    bars = ax1.bar(defects, counts, color=["#2563EB" if p <= 80 else "#94A3B8" for p in cum_pct], width=0.5)
    ax2 = ax1.twinx()
    ax2.plot(defects, cum_pct, color="#DC2626", marker="o", linewidth=2.2, markersize=6)
    ax2.axhline(80, color="#F59E0B", linestyle="--", linewidth=1.5)
    print("Pareto figure created successfully")

    # 2. Fishbone
    fig2, ax = plt.subplots(figsize=(9.0, 4.2), dpi=100)
    fig2.patch.set_facecolor("white")
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.annotate("", xy=(8.8, 3.0), xytext=(0.6, 3.0), arrowprops=dict(arrowstyle="->", lw=3.0, color="#1E3A8A"))
    print("Fishbone figure created successfully")

    # 3. FMEA comparison
    fig3, ax3 = plt.subplots(figsize=(8.5, 3.4), dpi=100)
    fig3.patch.set_facecolor("white")
    modes = ["FM-01 Search", "FM-02 Wait", "FM-03 Duplicate", "FM-04 Report", "FM-05 Room", "FM-06 Tax"]
    pre_rpn = [392, 336, 288, 216, 120, 84]
    post_rpn = [14, 32, 12, 16, 18, 14]
    x = np.arange(len(modes))
    w = 0.35
    ax3.bar(x - w/2, pre_rpn, width=w, label="Pre-Mitigation RPN", color="#EF4444")
    ax3.bar(x + w/2, post_rpn, width=w, label="Post-Mitigation RPN (Q02)", color="#10B981")
    print("FMEA figure created successfully")

    plt.close("all")
    print("All figures tested successfully!")

if __name__ == "__main__":
    test_figures()
