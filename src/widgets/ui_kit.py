"""
Modern UI Toolkit & Design System for MedCare HMS.
Clean, Light, Semi-Transparent Aesthetic with 2D Icons, Soft Shadows, and Hover Elevation:
- Anti-aliased Pillow-rendered Rounded Cards with Gaussian Drop Shadows & Interactive Hover Lift
- Clean 2D Vector-style Icon Badges with Semi-Transparent Pastel Backdrops
- Light Frosted Welcome Hero Banner (Light Azure with 2D Medical Glyph)
- Light Coral/Rose Emergency Triage Banner with 2D Emergency Shield & Instant Token Dispenser
- Soft Pastel Stat Cards (Blue, Champagne, Rose) with 2D Icons & Shadow Elevation
- Clean Borderless Table & Search Box Styling

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance
"""

from typing import Optional, Callable
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFilter, ImageTk

from src.config import THEME


def apply_global_styles(root: tk.Tk):
    """Configures high-end modern ttk styles with spacious rows and clean headers."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # 1. Modern Spacious Table (Treeview)
    style.configure(
        "Treeview",
        background="#FFFFFF",
        foreground="#0C2340",
        rowheight=36,
        fieldbackground="#FFFFFF",
        font=("Segoe UI", 9),
        borderwidth=0,
        relief="flat"
    )
    style.configure(
        "Treeview.Heading",
        background="#F1F5F9",
        foreground="#475569",
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        borderwidth=0,
        padding=(10, 8)
    )
    style.map(
        "Treeview",
        background=[("selected", "#EFF6FF")],
        foreground=[("selected", "#1E5DB4")]
    )

    # 2. Modern Minimalist Scrollbar
    style.configure(
        "Vertical.TScrollbar",
        background="#E2E8F0",
        troughcolor="#F8FAFC",
        borderwidth=0,
        arrowsize=12,
        relief="flat"
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", "#CBD5E1"), ("pressed", "#94A3B8")]
    )

    # 3. Modern Combobox
    style.configure(
        "TCombobox",
        fieldbackground="#FFFFFF",
        background="#FFFFFF",
        foreground="#0C2340",
        font=("Segoe UI", 9),
        padding=4
    )


class RoundedCard(tk.Canvas):
    """
    Ultra-Smooth Modern Card with Real Gaussian Drop Shadow & Interactive Hover Lift.
    - Semi-transparent, light-colored background.
    - Soft blurred drop shadow (anti-aliased).
    - On hover: card smoothly elevates upward by 2px and shadow deepens with higher blur.
    - Caches rendered frames for sub-millisecond redraws.
    """
    _img_cache = {}

    def __init__(self, parent, bg_color: str = "#FFFFFF", border_color: str = "#E2E8F0",
                 hover_bg: Optional[str] = None, hover_border: Optional[str] = None,
                 radius: int = 16, border_width: int = 1, pad_shadow: int = 6, padx: int = 14, pady: int = 12,
                 shadow_alpha: int = 20, hover_shadow_alpha: int = 38, **kwargs):
        p_bg = parent.cget("bg") if hasattr(parent, "cget") else THEME["background"]
        super().__init__(parent, highlightthickness=0, bd=0, bg=p_bg, **kwargs)

        self.bg_color = bg_color
        self.border_color = border_color
        self.hover_bg = hover_bg or bg_color
        self.hover_border = hover_border or border_color
        self.radius = radius
        self.border_width = border_width
        self.pad_shadow = pad_shadow
        self.pad_x = padx
        self.pad_y = pady
        self.shadow_alpha = shadow_alpha
        self.hover_shadow_alpha = hover_shadow_alpha
        self.is_hovered = False
        self._bg_img_id = None
        self._current_tk_img = None

        # Inner container for child widgets
        self.inner = tk.Frame(self, bg=self.bg_color)
        self.window_id = self.create_window(
            (self.pad_shadow + self.pad_x, self.pad_shadow + self.pad_y),
            window=self.inner, anchor="nw"
        )

        self.bind("<Configure>", self._on_configure)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _render_card_with_shadow(self, w: int, h: int, is_hovered: bool) -> ImageTk.PhotoImage:
        fill = self.hover_bg if is_hovered else self.bg_color
        outline = self.hover_border if is_hovered else self.border_color
        key = (w, h, self.radius, self.pad_shadow, is_hovered, fill, outline)
        if key in self._img_cache:
            return self._img_cache[key]

        scale = 2
        sw, sh = max(1, w * scale), max(1, h * scale)
        sp = self.pad_shadow * scale
        sr = self.radius * scale

        # Card elevation lift on hover (2px in screen space -> 4px in supersampled space)
        lift = (2 * scale) if is_hovered else 0
        card_x1 = sp
        card_y1 = sp - lift
        card_x2 = sw - sp
        card_y2 = sh - sp - lift

        img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))

        # 1. Soft blurred drop shadow
        s_offset_y = (6 * scale) if is_hovered else (3 * scale)
        s_blur = (9 * scale) if is_hovered else (5 * scale)
        s_alpha = self.hover_shadow_alpha if is_hovered else self.shadow_alpha

        s_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(s_img)
        sdraw.rounded_rectangle(
            [card_x1, card_y1 + s_offset_y, card_x2, card_y2 + s_offset_y],
            radius=sr,
            fill=(15, 23, 42, s_alpha)
        )
        s_blurred = s_img.filter(ImageFilter.GaussianBlur(s_blur / 2))
        img.paste(s_blurred, (0, 0), s_blurred)

        # 2. Card Body with crisp rounded rectangle and subtle border
        cdraw = ImageDraw.Draw(img)
        cdraw.rounded_rectangle(
            [card_x1, card_y1, card_x2, card_y2],
            radius=sr,
            fill=fill,
            outline=outline,
            width=scale
        )

        final_img = img.resize((w, h), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(final_img)
        self._img_cache[key] = tk_img
        return tk_img

    def _update_card(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 15 or h < 15:
            return

        fill = self.hover_bg if self.is_hovered else self.bg_color
        self._current_tk_img = self._render_card_with_shadow(w, h, self.is_hovered)

        if self._bg_img_id:
            self.delete(self._bg_img_id)
        self._bg_img_id = self.create_image(0, 0, image=self._current_tk_img, anchor="nw")
        self.tag_lower(self._bg_img_id)

        lift = 2 if self.is_hovered else 0
        ix = self.pad_shadow + self.pad_x
        iy = self.pad_shadow + self.pad_y - lift
        iw = max(1, w - 2 * (self.pad_shadow + self.pad_x))
        ih = max(1, h - 2 * (self.pad_shadow + self.pad_y))

        self.inner.config(bg=fill)
        self.coords(self.window_id, ix, iy)
        self.itemconfigure(self.window_id, width=iw, height=ih)

        # Update child widget backgrounds if they are not explicitly styled
        self._sync_children_bg(self.inner, fill)

    def _sync_children_bg(self, parent_widget, fill_color: str):
        for child in parent_widget.winfo_children():
            if getattr(child, "_keep_own_bg", False):
                continue
            try:
                child.config(bg=fill_color)
            except Exception:
                pass
            self._sync_children_bg(child, fill_color)

    def _on_configure(self, event):
        self._update_card()

    def _on_enter(self, event):
        self.is_hovered = True
        self._update_card()

    def _on_leave(self, event):
        try:
            x, y = self.winfo_pointerxy()
            wx, wy = self.winfo_rootx(), self.winfo_rooty()
            w, h = self.winfo_width(), self.winfo_height()
            if wx <= x < wx + w and wy <= y < wy + h:
                return
        except Exception:
            pass
        self.is_hovered = False
        self._update_card()


class CircleBadge(tk.Canvas):
    """Clean 2D Icon Badge in an anti-aliased semi-transparent or white circle."""
    _badge_cache = {}

    def __init__(self, parent, icon: str = "👥", size: int = 44,
                 bg_color: str = "#FFFFFF", border_color: str = "#E2E8F0",
                 fg_color: str = "#0C2340", font_size: int = 14, **kwargs):
        p_bg = parent.cget("bg") if hasattr(parent, "cget") else THEME["surface"]
        super().__init__(parent, width=size, height=size, highlightthickness=0, bd=0, bg=p_bg, **kwargs)
        self._keep_own_bg = True
        self.size = size
        self.icon = icon
        self.bg_color = bg_color
        self.border_color = border_color
        self.fg_color = fg_color
        self.font_size = font_size
        self._draw_badge()

    def _draw_badge(self):
        key = (self.size, self.bg_color, self.border_color)
        if key not in self._badge_cache:
            scale = 2
            s = self.size * scale
            img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse([2, 2, s - 3, s - 3], fill=self.bg_color, outline=self.border_color, width=scale)
            img_smooth = img.resize((self.size, self.size), Image.Resampling.LANCZOS)
            self._badge_cache[key] = ImageTk.PhotoImage(img_smooth)

        self._img = self._badge_cache[key]
        self.create_image(0, 0, image=self._img, anchor="nw")
        self.create_text(
            self.size // 2, self.size // 2,
            text=self.icon, font=("Segoe UI", self.font_size),
            fill=self.fg_color, anchor="center"
        )


class PastelStatCard(RoundedCard):
    """
    Light-colored, Semi-Transparent Pastel Metric Card with 2D Icon, Soft Shadow & Hover Lift:
    - Card 1: Light Sky Blue (#F0F7FF) -> 3,500 Total Patients
    - Card 2: Light Warm Champagne (#FFFDF0) -> 500 Available Staff
    - Card 3: Light Soft Rose (#FFF5F5) -> 300 Available Doctors
    """

    def __init__(self, parent, title: str, value: str, icon: str = "👥",
                 card_type: str = "blue", sub_text: str = "", **kwargs):
        palettes = {
            "blue": {
                "bg": "#F0F7FF",
                "border": "#D6E8FC",
                "hover_bg": "#E5F1FE",
                "hover_border": "#B9DCFD",
                "accent": "#1E5DB4"
            },
            "amber": {
                "bg": "#FFFDF0",
                "border": "#FDEEB3",
                "hover_bg": "#FEF9DC",
                "hover_border": "#FCD97A",
                "accent": "#B45309"
            },
            "rose": {
                "bg": "#FFF5F5",
                "border": "#FED7D7",
                "hover_bg": "#FEE8E8",
                "hover_border": "#FEB2B2",
                "accent": "#BE123C"
            },
        }
        cfg = palettes.get(card_type, palettes["blue"])

        super().__init__(
            parent,
            bg_color=cfg["bg"],
            border_color=cfg["border"],
            hover_bg=cfg["hover_bg"],
            hover_border=cfg["hover_border"],
            radius=16,
            pad_shadow=6,
            padx=14,
            pady=12,
            height=95,
            **kwargs
        )

        self.accent_color = cfg["accent"]

        # Card layout
        row = tk.Frame(self.inner, bg=cfg["bg"])
        row.pack(fill=tk.BOTH, expand=True)

        # 2D Circular Icon Badge
        self.badge = CircleBadge(
            row, icon=icon, size=46,
            bg_color="#FFFFFF", border_color=cfg["border"],
            fg_color=cfg["accent"], font_size=15
        )
        self.badge.pack(side=tk.LEFT, padx=(0, 12))

        # Metric Value & Label
        text_box = tk.Frame(row, bg=cfg["bg"])
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_val = tk.Label(
            text_box, text=value, font=("Segoe UI", 18, "bold"),
            fg="#0C2340", bg=cfg["bg"]
        )
        self.lbl_val.pack(anchor=tk.W)

        self.lbl_title = tk.Label(
            text_box, text=title, font=("Segoe UI", 9, "bold"),
            fg="#64748B", bg=cfg["bg"]
        )
        self.lbl_title.pack(anchor=tk.W)

        if sub_text:
            self.lbl_sub = tk.Label(
                text_box, text=sub_text, font=("Segoe UI", 7),
                fg=cfg["accent"], bg=cfg["bg"]
            )
            self.lbl_sub.pack(anchor=tk.W)

        self.value_label = self.lbl_val
        self.sub_label = getattr(self, "lbl_sub", None)

    def update_value(self, new_val: str, new_sub: Optional[str] = None):
        self.lbl_val.config(text=new_val)
        if new_sub and hasattr(self, "lbl_sub"):
            self.lbl_sub.config(text=new_sub)

    def config(self, **kwargs):
        if "text" in kwargs:
            self.lbl_val.config(text=kwargs.pop("text"))
        if kwargs:
            super().config(**kwargs)

    configure = config


class SpecialistChipCard(RoundedCard):
    """
    Light-colored, Semi-Transparent 2D Specialist Card with Hover Elevation:
    - Cardiologist (Light Rose), Neurologist (Light Amber), Radiologist (Light Blue), Pediatrician (Light Lavender)
    """

    def __init__(self, parent, title: str, subtitle: str, icon: str = "🩺",
                 chip_type: str = "blue", on_click: Optional[Callable] = None, **kwargs):
        palettes = {
            "blue": ("#F0F7FF", "#D6E8FC", "#E5F1FE", "#1E5DB4"),
            "amber": ("#FFFDF0", "#FDEEB3", "#FEF9DC", "#B45309"),
            "rose": ("#FFF5F5", "#FED7D7", "#FEE8E8", "#BE123C"),
            "purple": ("#FAF5FF", "#E9D8FD", "#F3E8FF", "#7C3AED"),
        }
        bg, border, h_bg, accent = palettes.get(chip_type, palettes["blue"])

        super().__init__(
            parent,
            bg_color=bg,
            border_color=border,
            hover_bg=h_bg,
            hover_border=border,
            radius=14,
            pad_shadow=5,
            padx=12,
            pady=10,
            height=70,
            cursor="hand2" if on_click else "arrow",
            **kwargs
        )
        self.on_click = on_click

        row = tk.Frame(self.inner, bg=bg)
        row.pack(fill=tk.BOTH, expand=True)

        # 2D Icon Badge
        badge = CircleBadge(
            row, icon=icon, size=40,
            bg_color="#FFFFFF", border_color=border,
            fg_color=accent, font_size=13
        )
        badge.pack(side=tk.LEFT, padx=(0, 10))

        # Title & Subtitle
        text_box = tk.Frame(row, bg=bg)
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        lbl_t = tk.Label(text_box, text=title, font=("Segoe UI", 10, "bold"), fg="#0C2340", bg=bg)
        lbl_t.pack(anchor=tk.W)

        lbl_s = tk.Label(text_box, text=subtitle, font=("Segoe UI", 8), fg="#64748B", bg=bg)
        lbl_s.pack(anchor=tk.W)

        # Right arrow
        arrow = tk.Label(row, text="›", font=("Segoe UI", 14, "bold"), fg=accent, bg=bg)
        arrow.pack(side=tk.RIGHT, padx=4)

        if on_click:
            self.bind("<Button-1>", lambda e: on_click())
            row.bind("<Button-1>", lambda e: on_click())
            text_box.bind("<Button-1>", lambda e: on_click())
            lbl_t.bind("<Button-1>", lambda e: on_click())
            lbl_s.bind("<Button-1>", lambda e: on_click())


class EmergencyBannerCard(RoundedCard):
    """
    Light-colored, Semi-Transparent Emergency Alert Card with 2D Emergency Shield & Instant Token Button.
    No 3D characters. Soft rose palette with clean red accents and soft drop shadow.
    """

    def __init__(self, parent, on_emergency_action: Optional[Callable] = None, **kwargs):
        super().__init__(
            parent,
            bg_color="#FFF1F2",
            border_color="#FECDD3",
            hover_bg="#FFE4E6",
            hover_border="#FDA4AF",
            radius=18,
            pad_shadow=6,
            padx=16,
            pady=14,
            height=140,
            **kwargs
        )
        self.on_emergency_action = on_emergency_action

        row = tk.Frame(self.inner, bg="#FFF1F2")
        row.pack(fill=tk.BOTH, expand=True)

        # Left Info & Action
        left = tk.Frame(row, bg="#FFF1F2")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        head_row = tk.Frame(left, bg="#FFF1F2")
        head_row.pack(anchor=tk.W)

        tk.Label(
            head_row, text="🚨 Emergency Triage Desk",
            font=("Segoe UI", 12, "bold"), fg="#9F1239", bg="#FFF1F2"
        ).pack(side=tk.LEFT)

        tk.Label(
            left, text="Instant Code Red Emergency Token & Priority Bed Allocation",
            font=("Segoe UI", 8), fg="#BE123C", bg="#FFF1F2"
        ).pack(anchor=tk.W, pady=(2, 8))

        # Clean white pill button with red text & soft hover
        btn = PillButton(
            left, text="🚨 Issue Emergency Token →", font_size=8,
            bg_color="#FFFFFF", fg_color="#BE123C",
            hover_color="#FFF1F2", padx=10, pady=5,
            command=self.on_emergency_action
        )
        btn._keep_own_bg = True
        btn.pack(anchor=tk.W)

        # Right 2D Emergency Shield Badge
        badge_box = tk.Frame(row, bg="#FFF1F2")
        badge_box.pack(side=tk.RIGHT, padx=(6, 0))

        CircleBadge(
            badge_box, icon="⚡", size=52,
            bg_color="#FFFFFF", border_color="#FECDD3",
            fg_color="#E11D48", font_size=18
        ).pack()


class WelcomeHeroBanner(RoundedCard):
    """
    Light-colored, Semi-Transparent Frosted Welcome Hero Banner.
    Uses 2D Medical Iconography, Soft Azure Tint, Telemetry Pills, and Gaussian Shadow.
    No 3D graphics. Clean, modern, and uncluttered.
    """

    def __init__(self, parent, staff_name: str = "Dr. Bhupinder Singh", role_title: str = "Hospital Admin", **kwargs):
        super().__init__(
            parent,
            bg_color="#F0F6FE",
            border_color="#D0E2FC",
            hover_bg="#E6F0FD",
            hover_border="#BDD7FB",
            radius=18,
            pad_shadow=6,
            padx=18,
            pady=14,
            height=125,
            **kwargs
        )

        row = tk.Frame(self.inner, bg="#F0F6FE")
        row.pack(fill=tk.BOTH, expand=True)

        # Left: Clean 2D Medical Cross Icon Badge
        left_badge = CircleBadge(
            row, icon="🩺", size=54,
            bg_color="#FFFFFF", border_color="#D0E2FC",
            fg_color="#1E5DB4", font_size=20
        )
        left_badge.pack(side=tk.LEFT, padx=(0, 16))

        # Middle: Greetings & Information
        mid = tk.Frame(row, bg="#F0F6FE")
        mid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            mid, text=f"👋 Welcome back, {staff_name}!",
            font=("Segoe UI", 14, "bold"), fg="#0C2340", bg="#F0F6FE"
        ).pack(anchor=tk.W)

        tk.Label(
            mid, text="MedCare Clinical Operations Command • TQM Quality Goal Q02: High Performance",
            font=("Segoe UI", 9), fg="#475569", bg="#F0F6FE"
        ).pack(anchor=tk.W, pady=(2, 6))

        # Semi-transparent 2D status pills
        pills_row = tk.Frame(mid, bg="#F0F6FE")
        pills_row.pack(anchor=tk.W)

        badges = [
            ("● LIVE OPD QUEUE", "#15803D", "#DCFCE7"),
            ("● SQLITE WAL ACTIVE", "#1E40AF", "#DBEAFE"),
            ("● SUB-100MS SEARCH", "#B45309", "#FEF3C7"),
            (f"● ROLE: {role_title.upper()}", "#6B21A8", "#F3E8FF"),
        ]

        for text, fg_c, bg_c in badges:
            lbl = tk.Label(
                pills_row, text=text, font=("Segoe UI", 7, "bold"),
                fg=fg_c, bg=bg_c, padx=8, pady=2
            )
            lbl._keep_own_bg = True
            lbl.pack(side=tk.LEFT, padx=(0, 6))


class ModernSearchBox(tk.Frame):
    """
    Modern pill-shaped search bar with leading 2D icon and clear button.
    """

    def __init__(self, parent, on_search_callback: Optional[Callable[[str], None]] = None,
                 placeholder: str = "Search patients, doctors, or tokens...", width: int = 34):
        super().__init__(parent, bg="#FFFFFF", highlightthickness=1,
                         highlightbackground="#CBD5E1", padx=10, pady=5)
        self.on_search_callback = on_search_callback
        self.search_var = tk.StringVar()

        tk.Label(self, text="🔍", font=("Segoe UI", 10), bg="#FFFFFF", fg="#64748B").pack(side=tk.LEFT, padx=(0, 6))

        self.entry = tk.Entry(
            self, textvariable=self.search_var, font=("Segoe UI", 9),
            bg="#FFFFFF", relief="flat", bd=0, width=width, insertbackground=THEME["primary"]
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.btn_clear = tk.Button(
            self, text="✕", font=("Segoe UI", 8), bg="#FFFFFF", fg="#94A3B8",
            relief="flat", cursor="hand2", bd=0, command=self.clear
        )
        self.btn_clear.pack(side=tk.RIGHT, padx=(4, 0))

        if on_search_callback:
            self.entry.bind("<KeyRelease>", lambda e: on_search_callback(self.search_var.get()))

    def get(self) -> str:
        return self.search_var.get()

    def clear(self):
        self.search_var.set("")
        if self.on_search_callback:
            self.on_search_callback("")


class PillButton(tk.Button):
    """
    Modern flat button with smooth hover animation and hand cursor.
    """

    def __init__(self, parent, text: str, command: Optional[Callable] = None,
                 bg_color: str = "#1E5DB4", fg_color: str = "white",
                 hover_color: str = "#0C2B59", font_size: int = 9,
                 padx: int = 14, pady: int = 6, **kwargs):
        super().__init__(
            parent, text=text, command=command,
            font=("Segoe UI", font_size, "bold"),
            bg=bg_color, fg=fg_color,
            activebackground=hover_color, activeforeground=fg_color,
            relief="flat", cursor="hand2", bd=0, padx=padx, pady=pady,
            **kwargs
        )
        self.default_bg = bg_color
        self.default_fg = fg_color
        self.hover_bg = hover_color
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        if self["state"] != tk.DISABLED:
            super().config(bg=self.hover_bg)

    def _on_leave(self, e):
        if self["state"] != tk.DISABLED:
            super().config(bg=self.default_bg)

    def config(self, **kwargs):
        if "state" in kwargs:
            st = kwargs["state"]
            if st == tk.DISABLED:
                super().config(bg="#E2E8F0", fg="#94A3B8", cursor="arrow", **kwargs)
                return
            elif st == tk.NORMAL:
                super().config(bg=self.default_bg, fg=self.default_fg, cursor="hand2", **kwargs)
                return
        super().config(**kwargs)

    configure = config


class ModernCard(RoundedCard):
    """Clean floating card container with soft Gaussian drop shadow and padding."""

    def __init__(self, parent, bg_color: str = "#FFFFFF", border_color: str = "#E2E8F0",
                 hover_bg: Optional[str] = None, hover_border: Optional[str] = None,
                 radius: int = 16, pad_shadow: int = 6, padx: int = 16, pady: int = 14, **kwargs):
        super().__init__(parent, bg_color=bg_color, border_color=border_color,
                         hover_bg=hover_bg or bg_color, hover_border=hover_border or border_color,
                         radius=radius, pad_shadow=pad_shadow, padx=padx, pady=pady, **kwargs)


class HeroMetricCard(PastelStatCard):
    """Backward-compatible alias for existing code referencing HeroMetricCard."""
    def __init__(self, parent, title: str, value: str, sub: str = "", icon: str = "📊",
                 bg_color: str = "#2563EB", **kwargs):
        ctype = "blue"
        if "amber" in bg_color.lower() or "0284c7" in bg_color.lower() or "sky" in bg_color.lower():
            ctype = "amber"
        elif "rose" in bg_color.lower() or "e11d48" in bg_color.lower() or "red" in bg_color.lower():
            ctype = "rose"
        super().__init__(parent, title=title, value=value, icon=icon, card_type=ctype, sub_text=sub)


class AccentLineStatCard(RoundedCard):
    """
    Polished Metric Card with Colored Vertical Left Accent Bar (Image 4 & 5).
    Features large bold number, title, and subtext on pure white background.
    """
    def __init__(self, parent, value: str, title: str, sub_text: str = "",
                 accent_color: str = "#2563EB", **kwargs):
        super().__init__(
            parent,
            bg_color="#FFFFFF",
            border_color="#E2E8F0",
            hover_bg="#FFFFFF",
            hover_border="#CBD5E1",
            radius=14,
            pad_shadow=5,
            padx=14,
            pady=12,
            **kwargs
        )
        self.accent_color = accent_color

        row = tk.Frame(self.inner, bg="#FFFFFF")
        row.pack(fill=tk.BOTH, expand=True)

        # Left vertical accent line
        self.accent_bar = tk.Frame(row, bg=accent_color, width=4)
        self.accent_bar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        # Text column
        col = tk.Frame(row, bg="#FFFFFF")
        col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_value = tk.Label(
            col, text=value, font=("Segoe UI", 20, "bold"),
            fg="#0F172A", bg="#FFFFFF"
        )
        self.lbl_value.pack(anchor=tk.W)

        self.lbl_title = tk.Label(
            col, text=title, font=("Segoe UI", 9, "bold"),
            fg="#0F172A", bg="#FFFFFF"
        )
        self.lbl_title.pack(anchor=tk.W, pady=(1, 2))

        if sub_text:
            self.lbl_sub = tk.Label(
                col, text=sub_text, font=("Segoe UI", 7),
                fg="#64748B", bg="#FFFFFF"
            )
            self.lbl_sub.pack(anchor=tk.W)

    def set_value(self, val: str):
        self.lbl_value.config(text=val)


class OverviewMetricCard(RoundedCard):
    """
    Dashboard Overview Card (Image 1 & Image 2).
    Features top-left rounded square badge with letter/icon, top-right indicator,
    large metric value, uppercase category title, and subtitle.
    """
    def __init__(self, parent, value: str, title: str, sub_text: str = "",
                 badge_text: str = "P", badge_bg: str = "#EFF6FF", badge_fg: str = "#2563EB",
                 dot_color: str = "#2563EB", **kwargs):
        super().__init__(
            parent,
            bg_color="#FFFFFF",
            border_color="#E2E8F0",
            hover_bg="#FFFFFF",
            hover_border="#CBD5E1",
            radius=16,
            pad_shadow=6,
            padx=16,
            pady=14,
            **kwargs
        )

        top_row = tk.Frame(self.inner, bg="#FFFFFF")
        top_row.pack(fill=tk.X, pady=(0, 10))

        # Square rounded badge
        badge = tk.Label(
            top_row, text=badge_text, font=("Segoe UI", 9, "bold"),
            bg=badge_bg, fg=badge_fg, width=3, height=1
        )
        badge.pack(side=tk.LEFT)

        if dot_color:
            dot = tk.Label(
                top_row, text="●", font=("Segoe UI", 7),
                fg=dot_color, bg="#FFFFFF"
            )
            dot.pack(side=tk.RIGHT)

        self.lbl_value = tk.Label(
            self.inner, text=value, font=("Segoe UI", 22, "bold"),
            fg="#0F172A", bg="#FFFFFF"
        )
        self.lbl_value.pack(anchor=tk.W)

        self.lbl_title = tk.Label(
            self.inner, text=title.upper(), font=("Segoe UI", 8, "bold"),
            fg="#0F172A", bg="#FFFFFF"
        )
        self.lbl_title.pack(anchor=tk.W, pady=(2, 2))

        self.lbl_sub = tk.Label(
            self.inner, text=sub_text, font=("Segoe UI", 7),
            fg="#64748B", bg="#FFFFFF"
        )
        self.lbl_sub.pack(anchor=tk.W)

    def set_value(self, val: str):
        self.lbl_value.config(text=val)


class DarkHeroBanner(RoundedCard):
    """
    Polished Dark Navy Welcome Hero Banner (Image 1 & Image 2).
    Deep dark navy background with clean typography and system status pill.
    """
    def __init__(self, parent, greeting: str = "Good day, Admin",
                 subtitle: str = "Here is your hospital's performance summary for today.",
                 **kwargs):
        super().__init__(
            parent,
            bg_color="#0F172A",
            border_color="#1E293B",
            hover_bg="#0F172A",
            hover_border="#334155",
            radius=16,
            pad_shadow=6,
            padx=20,
            pady=16,
            height=90,
            **kwargs
        )

        row = tk.Frame(self.inner, bg="#0F172A")
        row.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(row, bg="#0F172A")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            left, text=greeting, font=("Segoe UI", 15, "bold"),
            fg="#FFFFFF", bg="#0F172A"
        ).pack(anchor=tk.W)

        tk.Label(
            left, text=subtitle, font=("Segoe UI", 9),
            fg="#94A3B8", bg="#0F172A"
        ).pack(anchor=tk.W, pady=(4, 0))

        right = tk.Frame(row, bg="#0F172A")
        right.pack(side=tk.RIGHT)

        status_pill = tk.Label(
            right, text="● System Online", font=("Segoe UI", 8, "bold"),
            fg="#10B981", bg="#064E3B", padx=10, pady=4
        )
        status_pill.pack(anchor=tk.E)


class DarkWaitingCard(RoundedCard):
    """
    Dark Average Waiting Time Card (Image 1 & Image 2).
    """
    def __init__(self, parent, wait_time: str = "1 min 39 sec",
                 sub_text: str = "Measured from recorded check-in to consultation start.",
                 **kwargs):
        super().__init__(
            parent,
            bg_color="#0F172A",
            border_color="#1E293B",
            hover_bg="#0F172A",
            hover_border="#334155",
            radius=16,
            pad_shadow=6,
            padx=18,
            pady=16,
            **kwargs
        )

        top_row = tk.Frame(self.inner, bg="#0F172A")
        top_row.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            top_row, text="Average Waiting Time", font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF", bg="#0F172A"
        ).pack(side=tk.LEFT)

        q_badge = tk.Label(
            top_row, text="Q02", font=("Segoe UI", 7, "bold"),
            fg="#38BDF8", bg="#0C4A6E", padx=6, pady=2
        )
        q_badge.pack(side=tk.RIGHT)

        self.lbl_time = tk.Label(
            self.inner, text=wait_time, font=("Segoe UI", 20, "bold"),
            fg="#FFFFFF", bg="#0F172A"
        )
        self.lbl_time.pack(anchor=tk.W, pady=(4, 2))

        self.lbl_sub = tk.Label(
            self.inner, text=sub_text, font=("Segoe UI", 8),
            fg="#94A3B8", bg="#0F172A"
        )
        self.lbl_sub.pack(anchor=tk.W, pady=(0, 10))

        # Modern progress bar
        self.pbar_bg = tk.Frame(self.inner, bg="#1E293B", height=6)
        self.pbar_bg.pack(fill=tk.X)
        self.pbar_fill = tk.Frame(self.pbar_bg, bg="#2563EB", height=6, width=140)
        self.pbar_fill.pack(side=tk.LEFT)

    def set_time(self, t_str: str):
        self.lbl_time.config(text=t_str)

