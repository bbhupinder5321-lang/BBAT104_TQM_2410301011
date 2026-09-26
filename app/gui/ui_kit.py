import customtkinter as ctk


class HospitalFrame(ctk.CTkFrame):
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
        "save": "✓"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def icon_badge(self, parent, icon, size=44, bg=None, fg="#FFFFFF", font_size=20):
        badge = ctk.CTkFrame(
            parent,
            width=size,
            height=size,
            corner_radius=int(size * 0.30),
            fg_color=bg or self.PRIMARY
        )
        badge.pack_propagate(False)
        label = ctk.CTkLabel(
            badge,
            text=self.ICONS.get(icon, icon),
            text_color=fg,
            font=ctk.CTkFont(size=font_size, weight="bold")
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
            hover_color=self.PRIMARY_HOVER
        )

        def enter(_event):
            button.configure(height=41)

        def leave(_event):
            button.configure(height=38)

        button.bind("<Enter>", enter)
        button.bind("<Leave>", leave)
        return button
