"""
Statistical Quality Control (SQC) Visualizer for TQM Defects.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Includes Pareto Analysis and Ishikawa (Fishbone) Diagram generation.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from src.config import EXPORTS_DIR


def generate_pareto_chart(save_path: Path = None) -> Path:
    """
    Generate Pareto Chart of Hospital System Defects (80/20 Rule).
    Categorizes operational and performance bottlenecks.
    """
    if save_path is None:
        save_path = EXPORTS_DIR / "Pareto_Defect_Analysis.png"

    # Defect data reflecting baseline hospital management issues
    defects = [
        "Slow Patient Search",
        "Excessive Queue Wait Time",
        "Duplicate Patient Records",
        "Report Generation Freeze",
        "Doctor Slot Conflict",
        "Billing Calculation Delay"
    ]
    counts = [142, 118, 64, 38, 19, 11]

    # Calculate cumulative percentage
    total = sum(counts)
    cumulative_pct = np.cumsum(counts) / total * 100

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=100)

    # Bar plot for frequencies
    colors = ["#1E3A8A" if pct <= 80 else "#64748B" for pct in cumulative_pct]
    bars = ax1.bar(defects, counts, color=colors, width=0.55, edgecolor="#0F172A", alpha=0.85)
    ax1.set_ylabel("Defect Frequency (Incidents)", color="#0F172A", fontsize=11, fontweight="bold")
    ax1.set_title("Pareto Chart: Hospital Management Defects (80/20 Rule)\nBBAT104 TQM - Student: Bhupinder Singh (2410301011)", 
                  fontsize=13, fontweight="bold", pad=15)
    ax1.tick_params(axis="x", rotation=20, labelsize=9)
    ax1.set_ylim(0, max(counts) * 1.15)

    # Value labels on bars
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.0, yval + 2, int(yval), ha="center", va="bottom", fontsize=9, fontweight="bold")

    # Secondary axis for cumulative percentage
    ax2 = ax1.twinx()
    ax2.plot(defects, cumulative_pct, color="#DC2626", marker="o", linewidth=2.5, markersize=7, label="Cumulative %")
    ax2.axhline(80, color="#D97706", linestyle="--", linewidth=1.5, label="80% Cutoff (Vital Few)")
    ax2.set_ylabel("Cumulative Percentage (%)", color="#DC2626", fontsize=11, fontweight="bold")
    ax2.set_ylim(0, 110)
    ax2.grid(False)

    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path


def generate_fishbone_diagram(save_path: Path = None) -> Path:
    """
    Generate Ishikawa (Fishbone / Cause-and-Effect) Diagram for
    'Excessive Patient Wait Times & Duplicate Records'.
    """
    if save_path is None:
        save_path = EXPORTS_DIR / "Ishikawa_Fishbone_Diagram.png"

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=100)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Main horizontal spine
    ax.annotate("", xy=(9.0, 3.0), xytext=(0.5, 3.0),
                arrowprops=dict(arrowstyle="->", lw=3.5, color="#1E3A8A"))
    
    # Effect / Problem Box
    bbox_props = dict(boxstyle="square,pad=0.6", fc="#DC2626", ec="#991B1B", lw=2)
    ax.text(9.1, 3.0, "EFFECT:\nExcessive Patient\nWaiting Time & Record\nDuplication",
            ha="left", va="center", color="white", fontsize=10, fontweight="bold", bbox=bbox_props)

    # Ribs: Causes
    categories = [
        ("PEOPLE (Staff/Docs)", [(1.8, 4.8), (2.0, 3.0)], [
            ("Untrained reception staff", 1.9, 4.2),
            ("Doctor consultation delays", 2.2, 3.6),
            ("Manual record lookup confusion", 2.4, 3.2)
        ]),
        ("PROCESS (Workflow)", [(4.8, 4.8), (5.0, 3.0)], [
            ("No automated duplicate checking", 4.9, 4.2),
            ("Unsequenced token distribution", 5.2, 3.6),
            ("Lack of real-time queue visibility", 5.4, 3.2)
        ]),
        ("TECHNOLOGY (System)", [(1.8, 1.2), (2.0, 3.0)], [
            ("Unindexed DB table scans", 1.9, 1.8),
            ("Search thread UI freezing", 2.2, 2.3),
            ("Slow manual single-row inserts", 2.4, 2.7)
        ]),
        ("ENVIRONMENT (Surge)", [(4.8, 1.2), (5.0, 3.0)], [
            ("Peak morning OPD footfall rush", 4.9, 1.8),
            ("High walk-in without prior slot", 5.2, 2.3),
            ("Doctor emergency callouts", 5.4, 2.7)
        ])
    ]

    for cat_name, spine_coords, subcauses in categories:
        p_start, p_end = spine_coords
        ax.annotate("", xy=p_end, xytext=p_start,
                    arrowprops=dict(arrowstyle="-", lw=2.2, color="#0284C7"))
        
        # Category label box
        box_c = "#0284C7"
        ax.text(p_start[0], p_start[1], cat_name, ha="center", va="center",
                color="white", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", fc=box_c, ec="#0369A1", lw=1.5))
        
        # Subcauses branches
        for text, sx, sy in subcauses:
            ax.text(sx, sy, f"• {text}", fontsize=8, color="#0F172A", fontweight="semibold")

    plt.title("Ishikawa (Cause-and-Effect / Fishbone) Diagram: Root Causes of Patient Delays\nBBAT104 TQM - Student: Bhupinder Singh (2410301011)",
              fontsize=12, fontweight="bold", pad=20, color="#1E3A8A")

    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path
