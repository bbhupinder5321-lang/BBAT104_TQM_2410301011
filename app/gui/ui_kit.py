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
        self._page_animation_running = False
        self.after(80, self.play_page_reveal)

    def play_page_reveal(self):
        if self._page_animation_running or not self.winfo_exists():
            return
        self._page_animation_running = True

        overlay = ctk.CTkFrame(self, fg_color=self.PRIMARY, corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        label = ctk.CTkLabel(
            overlay,
            text="MEDICARE  •  LOADING",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        steps = 18

        def reveal(step=0):
            if not overlay.winfo_exists():
                self._page_animation_running = False
                return
            progress = step / steps
            if progress >= 1:
                overlay.destroy()
                self._page_animation_running = False
                return
            overlay.place(
                relx=progress,
                rely=0,
                relwidth=max(0.001, 1 - progress),
                relheight=1
            )
            self.after(16, lambda: reveal(step + 1))

        self.after(70, reveal)

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
