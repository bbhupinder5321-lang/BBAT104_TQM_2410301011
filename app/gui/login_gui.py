import customtkinter as ctk
from tkinter import messagebox

from app.services.auth_service import AuthService


class LoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()

        self.title("Hospital Management System - Login")
        self.geometry("500x600")
        self.resizable(False, False)

        self.configure(fg_color="#F4F7FB")

        self.create_login_ui()

    def create_login_ui(self):

        # Main container
        self.login_card = ctk.CTkFrame(
            self,
            width=400,
            height=480,
            corner_radius=20,
            fg_color="white"
        )

        self.login_card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Hospital icon/title
        self.title_label = ctk.CTkLabel(
            self.login_card,
            text="Hospital Management",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color="#1F2937"
        )

        self.title_label.pack(pady=(45, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.login_card,
            text="TQM Performance Management System",
            font=ctk.CTkFont(size=13),
            text_color="#6B7280"
        )

        self.subtitle_label.pack(pady=(0, 35))

        # Username
        self.username_label = ctk.CTkLabel(
            self.login_card,
            text="Username",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        )

        self.username_label.pack(
            anchor="w",
            padx=50
        )

        self.username_entry = ctk.CTkEntry(
            self.login_card,
            width=300,
            height=42,
            placeholder_text="Enter username",
            corner_radius=10
        )

        self.username_entry.pack(pady=(8, 20))

        # Password
        self.password_label = ctk.CTkLabel(
            self.login_card,
            text="Password",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        )

        self.password_label.pack(
            anchor="w",
            padx=50
        )

        self.password_entry = ctk.CTkEntry(
            self.login_card,
            width=300,
            height=42,
            placeholder_text="Enter password",
            show="*",
            corner_radius=10
        )

        self.password_entry.pack(pady=(8, 25))

        # Login button
        self.login_button = ctk.CTkButton(
            self.login_card,
            text="Login",
            width=300,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.login
        )

        self.login_button.pack(pady=(0, 15))

        # Status
        self.status_label = ctk.CTkLabel(
            self.login_card,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#DC2626"
        )

        self.status_label.pack()

        # Development credentials
        self.demo_label = ctk.CTkLabel(
            self.login_card,
            text="Development login: admin / admin123",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF"
        )

        self.demo_label.pack(
            side="bottom",
            pady=25
        )

        # Enter key
        self.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus()

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:

            self.status_label.configure(
                text="Please enter username and password.",
                text_color="#DC2626"
            )

            return

        self.login_button.configure(
            state="disabled",
            text="Signing in..."
        )

        self.update_idletasks()

        try:

            user = self.auth_service.login(
                username,
                password
            )

            self.status_label.configure(
                text=f"Login successful - {user['role'].title()}",
                text_color="#16A34A"
            )

            self.open_main_application(
                user
            )

        except ValueError as error:

            self.status_label.configure(
                text=str(error),
                text_color="#DC2626"
            )

            self.password_entry.delete(
                0,
                "end"
            )

            self.password_entry.focus()

            self.login_button.configure(
                state="normal",
                text="Login"
            )

        except Exception as error:

            self.status_label.configure(
                text="Unable to sign in. Please try again.",
                text_color="#DC2626"
            )

            messagebox.showerror(
                "Login Error",
                f"An unexpected error occurred.\n\n{error}"
            )

            self.login_button.configure(
                state="normal",
                text="Login"
            )

    def open_main_application(
        self,
        user
    ):

        try:

            from app.gui.main_app import MainApplication

            self.destroy()

            application = MainApplication(
                user
            )

            application.mainloop()

        except Exception as error:

            messagebox.showerror(
                "Application Error",
                f"Unable to open the hospital application.\n\n{error}"
            )

            try:
                self.login_button.configure(
                    state="normal",
                    text="Login"
                )
            except Exception:
                pass


if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = LoginWindow()
    app.mainloop()
