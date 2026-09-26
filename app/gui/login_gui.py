import customtkinter as ctk
from tkinter import messagebox

from app.services.auth_service import AuthService
from app.database.database import initialize_database


class LoginWindow(ctk.CTk):

    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    BORDER = "#E5EAF2"
    TEXT = "#0F172A"
    MUTED = "#64748B"
    BLUE = "#2563EB"
    BLUE_HOVER = "#1D4ED8"
    GREEN = "#10B981"
    GREEN_SOFT = "#ECFDF5"
    BLUE_SOFT = "#EFF6FF"
    RED = "#DC2626"

    def __init__(self):
        super().__init__()

        initialize_database()
        self.auth_service = AuthService()

        self.title("MediCare Hospital Management System")
        self.geometry("1180x720")
        self.minsize(1050, 650)
        self.configure(fg_color=self.BG)

        self.selected_role = "admin"
        self.create_login_ui()
        self.bind("<Return>", lambda event: self.login())
        self.after(100, self.username_entry.focus)

    def create_login_ui(self):
        # Left branding/healthcare panel
        self.brand_panel = ctk.CTkFrame(
            self,
            width=430,
            corner_radius=0,
            fg_color="#111827"
        )
        self.brand_panel.pack(side="left", fill="y")
        self.brand_panel.pack_propagate(False)

        brand_inner = ctk.CTkFrame(self.brand_panel, fg_color="transparent")
        brand_inner.pack(fill="both", expand=True, padx=48, pady=48)

        icon = ctk.CTkFrame(
            brand_inner,
            width=62,
            height=62,
            corner_radius=18,
            fg_color=self.BLUE
        )
        icon.pack_propagate(False)
        icon.pack(anchor="w")

        ctk.CTkLabel(
            icon,
            text="+",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=38, weight="bold")
        ).pack(expand=True)

        ctk.CTkLabel(
            brand_inner,
            text="MediCare",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=34, weight="bold")
        ).pack(anchor="w", pady=(28, 3))

        ctk.CTkLabel(
            brand_inner,
            text="Hospital Management System",
            text_color="#CBD5E1",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_inner,
            text="TQM • Q02 IMPROVE PERFORMANCE",
            text_color="#93C5FD",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", pady=(25, 0))

        feature_box = ctk.CTkFrame(
            brand_inner,
            fg_color="#182234",
            corner_radius=18,
            border_width=1,
            border_color="#26344B"
        )
        feature_box.pack(fill="x", pady=(35, 0))

        features = [
            ("01", "Patient records", "Fast and organized patient workflows"),
            ("02", "Appointments", "Scheduling and waiting-time tracking"),
            ("03", "Quality", "TQM analysis and Q02 performance")
        ]

        for number, title, subtitle in features:
            row = ctk.CTkFrame(feature_box, fg_color="transparent")
            row.pack(fill="x", padx=18, pady=13)

            ctk.CTkLabel(
                row,
                text=number,
                text_color="#60A5FA",
                font=ctk.CTkFont(size=10, weight="bold")
            ).pack(side="left", padx=(0, 13))

            text_area = ctk.CTkFrame(row, fg_color="transparent")
            text_area.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                text_area,
                text=title,
                text_color="#F8FAFC",
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                text_area,
                text=subtitle,
                text_color="#94A3B8",
                font=ctk.CTkFont(size=9)
            ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            brand_inner,
            text="Secure role-based access • SQLite • Python",
            text_color="#64748B",
            font=ctk.CTkFont(size=9)
        ).pack(side="bottom", anchor="w")

        # Right login workspace
        workspace = ctk.CTkFrame(self, fg_color=self.BG, corner_radius=0)
        workspace.pack(side="right", fill="both", expand=True)

        card = ctk.CTkFrame(
            workspace,
            fg_color=self.CARD,
            corner_radius=24,
            border_width=1,
            border_color=self.BORDER
        )
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.82, relheight=0.86)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=42, pady=(35, 0))

        ctk.CTkLabel(
            top,
            text="WELCOME BACK",
            text_color=self.BLUE,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            top,
            text="Sign in to MediCare",
            text_color=self.TEXT,
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", pady=(4, 2))

        ctk.CTkLabel(
            top,
            text="Choose your workspace and continue.",
            text_color=self.MUTED,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w")

        # Role selector
        role_section = ctk.CTkFrame(card, fg_color="transparent")
        role_section.pack(fill="x", padx=42, pady=(25, 0))

        ctk.CTkLabel(
            role_section,
            text="WORKSPACE",
            text_color=self.MUTED,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w", pady=(0, 8))

        roles = ctk.CTkFrame(role_section, fg_color="transparent")
        roles.pack(fill="x")

        roles.grid_columnconfigure(0, weight=1)
        roles.grid_columnconfigure(1, weight=1)

        self.admin_role_button = self.create_role_button(
            roles, 0, "admin", "ADMIN", "Full management access", self.BLUE
        )
        self.staff_role_button = self.create_role_button(
            roles, 1, "staff", "STAFF", "Daily operations access", self.GREEN
        )

        # Credentials
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=42, pady=(22, 0))

        ctk.CTkLabel(
            form,
            text="USERNAME",
            text_color=self.MUTED,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w")

        self.username_entry = ctk.CTkEntry(
            form,
            height=44,
            corner_radius=11,
            border_width=1,
            border_color=self.BORDER,
            fg_color="#FFFFFF",
            text_color=self.TEXT,
            placeholder_text="Enter username"
        )
        self.username_entry.pack(fill="x", pady=(7, 15))

        ctk.CTkLabel(
            form,
            text="PASSWORD",
            text_color=self.MUTED,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w")

        self.password_entry = ctk.CTkEntry(
            form,
            height=44,
            corner_radius=11,
            border_width=1,
            border_color=self.BORDER,
            fg_color="#FFFFFF",
            text_color=self.TEXT,
            placeholder_text="Enter password",
            show="*"
        )
        self.password_entry.pack(fill="x", pady=(7, 10))

        self.status_label = ctk.CTkLabel(
            form,
            text="",
            text_color=self.RED,
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(anchor="w")

        self.login_button = ctk.CTkButton(
            card,
            text="Sign In  →",
            height=46,
            corner_radius=11,
            fg_color=self.BLUE,
            hover_color=self.BLUE_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.login
        )
        self.login_button.pack(fill="x", padx=42, pady=(10, 12))

        self.demo_label = ctk.CTkLabel(
            card,
            text="",
            text_color=self.MUTED,
            font=ctk.CTkFont(size=9)
        )
        self.demo_label.pack(pady=(0, 20))

        self.update_role_ui()

    def create_role_button(self, parent, column, role, title, subtitle, accent):
        button = ctk.CTkButton(
            parent,
            text=f"  {title}\n{subtitle}",
            height=62,
            corner_radius=12,
            fg_color=self.BLUE_SOFT if role == "admin" else "#F0FDF4",
            hover_color="#DBEAFE" if role == "admin" else "#DCFCE7",
            text_color=accent,
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda selected=role: self.select_role(selected)
        )
        button.grid(row=0, column=column, padx=4, sticky="ew")
        return button

    def select_role(self, role):
        self.selected_role = role
        self.update_role_ui()
        self.username_entry.focus()

    def update_role_ui(self):
        if self.selected_role == "admin":
            self.admin_role_button.configure(
                border_width=2,
                border_color=self.BLUE,
                fg_color="#DBEAFE"
            )
            self.staff_role_button.configure(
                border_width=1,
                border_color=self.BORDER,
                fg_color="#F0FDF4"
            )
            self.login_button.configure(
                fg_color=self.BLUE,
                hover_color=self.BLUE_HOVER
            )
            self.demo_label.configure(
                text="Demo admin account:  admin  /  admin123"
            )
        else:
            self.staff_role_button.configure(
                border_width=2,
                border_color=self.GREEN,
                fg_color=self.GREEN_SOFT
            )
            self.admin_role_button.configure(
                border_width=1,
                border_color=self.BORDER,
                fg_color=self.BLUE_SOFT
            )
            self.login_button.configure(
                fg_color=self.GREEN,
                hover_color="#059669"
            )
            self.demo_label.configure(
                text="Demo staff account:  staff  /  staff123"
            )

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.configure(
                text="Please enter username and password.",
                text_color=self.RED
            )
            return

        self.login_button.configure(
            state="disabled",
            text="Signing in..."
        )
        self.update_idletasks()

        try:
            user = self.auth_service.login(username, password)

            if user["role"] != self.selected_role:
                raise ValueError(
                    f"This is a {user['role'].title()} account. "
                    f"Select the {user['role'].title()} workspace."
                )

            self.status_label.configure(
                text=f"Signed in as {user['role'].title()}",
                text_color=self.GREEN
            )

            self.open_main_application(user)

        except ValueError as error:
            self.status_label.configure(
                text=str(error),
                text_color=self.RED
            )
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
            self.login_button.configure(
                state="normal",
                text="Sign In  →"
            )

        except Exception as error:
            self.status_label.configure(
                text="Unable to sign in. Please try again.",
                text_color=self.RED
            )
            messagebox.showerror(
                "Login Error",
                f"An unexpected error occurred.\n\n{error}"
            )
            self.login_button.configure(
                state="normal",
                text="Sign In  →"
            )

    def open_main_application(self, user):
        try:
            from app.gui.main_app import MainApplication

            self.destroy()

            application = MainApplication(user)
            application.mainloop()

        except Exception as error:
            messagebox.showerror(
                "Application Error",
                f"Unable to open the hospital application.\n\n{error}"
            )

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = LoginWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
