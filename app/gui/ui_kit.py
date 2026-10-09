import tkinter as tk
from tkinter import ttk

import customtkinter as ctk


class HospitalFrame(ctk.CTkFrame):
    """Shared visual language and small UI primitives for hospital screens."""

    BACKGROUND = "#F6F8FC"
    CARD = "#FFFFFF"
    CARD_SOFT = "#F8FAFD"
    BORDER = "#E6EAF0"
    TEXT_DARK = "#0F172A"
    SECONDARY = "#64748B"
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    PURPLE = "#7C3AED"
    TABLE_HEADER = "#F1F5F9"
    TABLE_SELECTED = "#DBEAFE"
    TABLE_SELECTED_TEXT = "#1E3A8A"

    ICONS = {
        "dashboard": "⌂",
        "patients": "♙",
        "doctors": "⚕",
        "appointments": "◷",
        "billing": "▣",
        "import": "⇧",
        "reports": "▤",
        "performance": "⌁",
        "tqm": "✓",
        "search": "⌕",
        "refresh": "↻",
        "add": "+",
        "edit": "✎",
        "delete": "×",
        "save": "✓",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_table_styles()

    # ---------------------------------------------------------
    # SHARED TABLE DESIGN
    # ---------------------------------------------------------

    def configure_table_styles(self):
        """Keep native Tk tables consistent across all modules."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=self.CARD,
            foreground=self.TEXT_DARK,
            fieldbackground=self.CARD,
            rowheight=36,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.TABLE_HEADER,
            foreground="#334155",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(10, 9),
        )
        style.map(
            "Treeview",
            background=[("selected", self.TABLE_SELECTED)],
            foreground=[("selected", self.TABLE_SELECTED_TEXT)],
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#E2E8F0")],
        )
        style.configure(
            "Hospital.Treeview",
            background=self.CARD,
            foreground=self.TEXT_DARK,
            fieldbackground=self.CARD,
            rowheight=36,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Hospital.Treeview.Heading",
            background=self.TABLE_HEADER,
            foreground="#334155",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(10, 9),
        )
        style.map(
            "Hospital.Treeview",
            background=[("selected", self.TABLE_SELECTED)],
            foreground=[("selected", self.TABLE_SELECTED_TEXT)],
        )
        style.configure(
            "Hospital.TNotebook",
            background=self.BACKGROUND,
            borderwidth=0,
            tabmargins=(2, 8, 2, 0),
        )
        style.configure(
            "Hospital.TNotebook.Tab",
            background="#E8EEF7",
            foreground="#475569",
            padding=(16, 10),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Hospital.TNotebook.Tab",
            background=[("selected", self.CARD), ("active", "#DBEAFE")],
            foreground=[("selected", self.PRIMARY), ("active", "#1D4ED8")],
        )

    def style_treeview(self, tree, headings=None, widths=None):
        """Apply shared table styling and optional column definitions."""
        tree.configure(style="Hospital.Treeview")
        if headings:
            for column, label in headings.items():
                tree.heading(column, text=label)
        if widths:
            for column, options in widths.items():
                if isinstance(options, dict):
                    tree.column(column, **options)
                else:
                    tree.column(column, width=options)

    # ---------------------------------------------------------
    # SHARED PAGE COMPONENTS
    # ---------------------------------------------------------

    def page_header(self, parent, title, subtitle, icon="dashboard", accent=None):
        """Create a consistent compact header for a module page."""
        accent = accent or self.PRIMARY
        header = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER,
        )
        header.pack(fill="x", padx=28, pady=(22, 14))

        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=17)

        self.icon_badge(content, icon, 44, accent, font_size=19).pack(side="left")
        text_area = ctk.CTkFrame(content, fg_color="transparent")
        text_area.pack(side="left", fill="x", expand=True, padx=(13, 12))

        ctk.CTkLabel(
            text_area,
            text=title,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=23, weight="bold"),
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            text_area,
            text=subtitle,
            text_color=self.SECONDARY,
            font=ctk.CTkFont(size=11),
            anchor="w",
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))
        return header

    def section_card(self, parent, title, subtitle=None, icon="dashboard", accent=None):
        accent = accent or self.PRIMARY
        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER,
        )
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(16, 10))
        self.icon_badge(header, icon, 36, accent, font_size=16).pack(side="left")
        area = ctk.CTkFrame(header, fg_color="transparent")
        area.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(
            area,
            text=title,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(
                area,
                text=subtitle,
                text_color=self.SECONDARY,
                font=ctk.CTkFont(size=9),
            ).pack(anchor="w", pady=(2, 0))
        return card

    def metric_card(self, parent, label, value, icon="dashboard", accent=None, suffix=""):
        accent = accent or self.PRIMARY
        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER,
        )
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(14, 5))
        self.icon_badge(top, icon, 34, accent, font_size=15).pack(side="left")
        ctk.CTkLabel(
            top,
            text=label.upper(),
            text_color=self.SECONDARY,
            font=ctk.CTkFont(size=8, weight="bold"),
        ).pack(side="left", padx=(9, 0))
        value_label = ctk.CTkLabel(
            card,
            text=f"{value}{suffix}",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=23, weight="bold"),
        )
        value_label.pack(anchor="w", padx=15, pady=(2, 14))
        return card, value_label

    def status_pill(self, parent, text, status="info"):
        colors = {
            "success": ("#ECFDF5", "#047857"),
            "warning": ("#FFFBEB", "#B45309"),
            "danger": ("#FEF2F2", "#B91C1C"),
            "info": ("#EFF6FF", "#1D4ED8"),
        }
        bg, fg = colors.get(status, colors["info"])
        return ctk.CTkLabel(
            parent,
            text=f"  {text}  ",
            fg_color=bg,
            text_color=fg,
            corner_radius=8,
            font=ctk.CTkFont(size=8, weight="bold"),
        )

    def show_toast(self, text, kind="success"):
        if getattr(self, "_toast", None) is not None:
            try:
                self._toast.destroy()
            except Exception:
                pass
        accent = {
            "success": self.SUCCESS,
            "warning": self.WARNING,
            "danger": self.DANGER,
        }.get(kind, self.PRIMARY)
        self._toast = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color=accent,
        )
        self._toast.place(relx=0.98, rely=0.04, anchor="ne")
        ctk.CTkLabel(
            self._toast,
            text="●",
            text_color=accent,
            font=ctk.CTkFont(size=11, weight="bold"),
        ).pack(side="left", padx=(12, 5), pady=10)
        ctk.CTkLabel(
            self._toast,
            text=text,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=9, weight="bold"),
        ).pack(side="left", padx=(0, 12), pady=10)

        toast = self._toast
        self.after(
            2200,
            lambda: toast.destroy() if toast.winfo_exists() else None,
        )

    def bind_shortcut(self, sequence, command):
        self.bind_all(sequence, lambda _event: command(), add="+")

    def icon_badge(self, parent, icon, size=44, bg=None, fg="#FFFFFF", font_size=20):
        badge = ctk.CTkFrame(
            parent,
            width=size,
            height=size,
            corner_radius=int(size * 0.30),
            fg_color=bg or self.PRIMARY,
        )
        badge.pack_propagate(False)
        label = ctk.CTkLabel(
            badge,
            text=self.ICONS.get(icon, icon),
            text_color=fg,
            font=ctk.CTkFont(size=font_size, weight="bold"),
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        return badge

    def animated_button(self, parent, text, command, width=120):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=38,
            corner_radius=10,
            fg_color=self.PRIMARY,
            hover_color=self.PRIMARY_HOVER,
        )

        def enter(_event):
            button.configure(height=40)

        def leave(_event):
            button.configure(height=38)

        button.bind("<Enter>", enter)
        button.bind("<Leave>", leave)
        return button
