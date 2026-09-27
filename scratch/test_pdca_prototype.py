"""
Prototype and verify the updated Deming PDCA Cycle Diagram.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from pathlib import Path
from typing import Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT_DIR = Path(__file__).resolve().parent.parent

def create_pdca_cycle_figure(figsize: Tuple[float, float] = (9.4, 5.0), dpi: int = 120) -> plt.Figure:
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)

    # 1. Top Banner Title & Academic Context
    ax.text(
        5.0, 6.18, "DEMING PDCA CONTINUOUS QUALITY IMPROVEMENT CYCLE",
        ha="center", va="center", fontsize=11.5, fontweight="bold", color="#003E5C"
    )
    ax.text(
        5.0, 5.86, "BBAT104 TQM Review 4 • Assigned Goal: Q02 - Improve Performance • Student: Bhupinder Singh (2410301011)",
        ha="center", va="center", fontsize=8.0, color="#64748B", fontweight="medium"
    )

    # 2. Four Phase Cards Configuration (x, y, w, h)
    cards = [
        (
            "1. PLAN", "Define & Target", "Root Cause Analysis & SLA Formulation",
            [
                "Identify patient search latency & queue wait delays",
                "Execute Pareto 80/20 analysis on clinical triage defects",
                "Establish target SLAs: Search < 100ms, Wait < 15 min",
            ],
            "TARGET: Search < 100ms | Queue Wait < 15m",
            "#F0F7FF", "#2563EB", "#1D4ED8",
            0.40, 3.35, 3.85, 2.15
        ),
        (
            "2. DO", "Implement & Execute", "Q02 Architectural Optimization",
            [
                "Construct 10 composite B-Tree indexes on core tables",
                "Enable SQLite WAL (Write-Ahead Logging) storage mode",
                "Deploy Poka-Yoke duplicate phone validation guard",
            ],
            "SOLUTION: 10 B-Trees + WAL + Poka-Yoke",
            "#F0FDF4", "#16A34A", "#15803D",
            5.75, 3.35, 3.85, 2.15
        ),
        (
            "3. CHECK", "Measure & Audit", "Live Telemetry & Benchmark Verification",
            [
                "Search Latency: 0.81ms (SLA: < 100ms) -> PASSED",
                "Average OPD Wait: 10.1 min (SLA: < 15m) -> PASSED",
                "Bulk CSV Import: 612 rps (SLA: > 500 rps) -> PASSED",
            ],
            "VERIFIED: Sub-1ms Latency | 100% SLA Compliance",
            "#FFFBEB", "#D97706", "#B45309",
            5.75, 0.40, 3.85, 2.15
        ),
        (
            "4. ACT", "Standardize & Sustain", "Institutionalize Quality & Continuous Kaizen",
            [
                "Standardize B-Tree index schema permanently in DDL",
                "Embed live real-time SLA pulse on executive dashboard",
                "Sustain 90%+ FMEA risk mitigation across all failure modes",
            ],
            "SUSTAINED: Permanent DDL Schema + SLA Pulse",
            "#FAF5FF", "#9333EA", "#7E22CE",
            0.40, 0.40, 3.85, 2.15
        ),
    ]

    for phase, sub_title, sub_desc, bullets, badge, bg_col, border_col, head_col, x, y, w, h in cards:
        # Card Body Background
        card_box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.08",
            facecolor=bg_col, edgecolor=border_col, linewidth=1.4, zorder=2
        )
        ax.add_patch(card_box)

        # Header Pill Strip
        pill_w = 1.15
        pill_h = 0.32
        pill_box = patches.FancyBboxPatch(
            (x + 0.14, y + h - pill_h - 0.12), pill_w, pill_h, boxstyle="round,pad=0.04",
            facecolor=head_col, edgecolor=head_col, linewidth=1, zorder=3
        )
        ax.add_patch(pill_box)
        ax.text(
            x + 0.14 + pill_w / 2.0, y + h - pill_h / 2.0 - 0.12, phase,
            ha="center", va="center", fontsize=7.5, fontweight="bold", color="#FFFFFF", zorder=4
        )

        # Subtitle
        ax.text(
            x + 0.14 + pill_w + 0.12, y + h - 0.28, sub_title,
            ha="left", va="center", fontsize=8.2, fontweight="bold", color="#0F172A", zorder=4
        )

        # Sub-desc
        ax.text(
            x + 0.15, y + h - 0.58, sub_desc,
            ha="left", va="center", fontsize=7.0, color="#64748B", zorder=4
        )

        # Separator line
        ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.72, y + h - 0.72], color=border_col, lw=0.6, alpha=0.45, zorder=3)

        # Bullet items
        b_y = y + h - 0.95
        for b_text in bullets:
            ax.text(
                x + 0.18, b_y, f"• {b_text}",
                ha="left", va="center", fontsize=7.0, color="#1E293B", zorder=4
            )
            b_y -= 0.27

        # Bottom Metric Highlight Pill
        m_pill = patches.FancyBboxPatch(
            (x + 0.15, y + 0.12), w - 0.30, 0.28, boxstyle="round,pad=0.04",
            facecolor="#FFFFFF", edgecolor=border_col, linewidth=0.9, zorder=3
        )
        ax.add_patch(m_pill)
        ax.text(
            x + w / 2.0, y + 0.26, badge,
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=head_col, zorder=4
        )

    # 3. Dynamic Cyclical Flow Connectors (PLAN -> DO -> CHECK -> ACT -> PLAN)
    arrow_props = dict(arrowstyle="-|>", lw=2.0, mutation_scale=13, zorder=5)

    # PLAN -> DO (Top Connector)
    ax.annotate("", xy=(5.62, 4.42), xytext=(4.38, 4.42),
                arrowprops=dict(**arrow_props, color="#16A34A"))
    ax.text(5.0, 4.68, "EXECUTE ->", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#16A34A",
            bbox=dict(boxstyle="round,pad=0.18", fc="#FFFFFF", ec="#16A34A", lw=0.8, zorder=6))

    # DO -> CHECK (Right Connector)
    ax.annotate("", xy=(7.67, 2.65), xytext=(7.67, 3.25),
                arrowprops=dict(**arrow_props, color="#D97706"))
    ax.text(8.40, 2.95, "MEASURE v", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#D97706",
            bbox=dict(boxstyle="round,pad=0.18", fc="#FFFFFF", ec="#D97706", lw=0.8, zorder=6))

    # CHECK -> ACT (Bottom Connector)
    ax.annotate("", xy=(4.38, 1.48), xytext=(5.62, 1.48),
                arrowprops=dict(**arrow_props, color="#9333EA"))
    ax.text(5.0, 1.22, "<- STANDARDIZE", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#9333EA",
            bbox=dict(boxstyle="round,pad=0.18", fc="#FFFFFF", ec="#9333EA", lw=0.8, zorder=6))

    # ACT -> PLAN (Left Connector)
    ax.annotate("", xy=(2.32, 3.25), xytext=(2.32, 2.65),
                arrowprops=dict(**arrow_props, color="#2563EB"))
    ax.text(1.60, 2.95, "SUSTAIN ^", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#2563EB",
            bbox=dict(boxstyle="round,pad=0.18", fc="#FFFFFF", ec="#2563EB", lw=0.8, zorder=6))

    # 4. Central Hub Medallion (Deming Core) - Sits in the open central void with NO OVERLAP
    c_w = 1.30
    c_h = 0.74
    c_x = 5.0 - c_w / 2.0
    c_y = 2.95 - c_h / 2.0

    hub_outer = patches.FancyBboxPatch(
        (c_x, c_y), c_w, c_h, boxstyle="round,pad=0.08",
        facecolor="#003E5C", edgecolor="#0284C7", linewidth=1.8, zorder=6
    )
    ax.add_patch(hub_outer)

    ax.text(5.0, 3.13, "DEMING WHEEL", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#FFFFFF", zorder=7)
    ax.text(5.0, 2.77, "Continuous Kaizen (Q02)", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#38BDF8", zorder=7)

    fig.tight_layout(pad=0.4)
    return fig


if __name__ == "__main__":
    test_path = ROOT_DIR / "scratch" / "test_pdca_render.png"
    fig = create_pdca_cycle_figure(figsize=(9.6, 5.8), dpi=150)
    fig.savefig(test_path, dpi=150)
    plt.close(fig)
    print("Saved test figure to:", test_path)
