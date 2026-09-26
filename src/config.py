"""
Configuration and constants for Hospital Management System (HMS)
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
EXPORTS_DIR = BASE_DIR / "exports"

# Create directories if they do not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Database Settings
DB_PATH = DATA_DIR / "hms_database.db"
SCHEMA_PATH = DATA_DIR / "schema.sql"
SAMPLE_CSV_PATH = DATA_DIR / "sample_patients.csv"

# Quality Goal Q02 - Performance SLA Targets (in milliseconds / units)
SLA_TARGETS = {
    "SEARCH_MAX_MS": 100.0,       # Fast Search must respond in < 100ms
    "DASHBOARD_MAX_MS": 1000.0,   # Executive Dashboard must render in < 1.0s (1000ms)
    "REPORT_MAX_MS": 1500.0,      # Vectorized Reports must generate in < 1.5s
    "CSV_MIN_RPS": 500.0,         # Bulk CSV Ingestion must exceed 500 records/sec
}

# Modern KRL Healthcare UI Theme Palette (Inspired by Reference Image)
THEME = {
    "primary": "#1E5DB4",         # Royal Navy Blue
    "primary_dark": "#0C2B59",    # Deep Navy
    "primary_light": "#EBF3FD",   # Soft Pastel Sky Tint
    "secondary": "#0284C7",       # Sky Blue Accent
    "sidebar_bg": "#0A2346",      # Deep Royal Navy 950
    "sidebar_hover": "#143869",   # Navy Hover
    "sidebar_active": "#1C4E91",  # Active Nav Pill
    "sidebar_text": "#94A3B8",    # Muted Nav Text
    "sidebar_text_active": "#FFFFFF",
    "hero_navy": "#0A2756",       # Hero Welcome Banner Navy
    "emergency_coral": "#D93B58", # Rich Coral/Raspberry Emergency Card
    "pastel_blue": "#EBF3FD",     # Pastel Stat Card 1 (Patients)
    "pastel_blue_border": "#D2E4F9",
    "pastel_blue_hover": "#DCEAFB",
    "pastel_amber": "#FEF7DD",    # Pastel Stat Card 2 (Staff)
    "pastel_amber_border": "#F8E8B6",
    "pastel_amber_hover": "#FDF0C6",
    "pastel_rose": "#FCEEEA",     # Pastel Stat Card 3 (Doctors)
    "pastel_rose_border": "#F9D8D0",
    "pastel_rose_hover": "#F9DFD8",
    "pastel_purple": "#F3EEFA",   # Pastel Specialist Card
    "pastel_purple_border": "#E4D6F7",
    "pastel_purple_hover": "#EDE2FA",
    "success": "#10B981",         # Emerald Green
    "success_light": "#ECFDF5",
    "warning": "#F59E0B",         # Amber Alert
    "warning_light": "#FFFBEB",
    "danger": "#EF4444",          # Rose Red
    "danger_light": "#FEF2F2",
    "purple": "#8B5CF6",          # Violet Accent
    "purple_light": "#F5F3FF",
    "background": "#F0F4FA",      # Clean Slate Periwinkle Canvas
    "surface": "#FFFFFF",         # Pure White Card
    "border": "#E2E8F0",          # Soft Border
    "text": "#0C2340",            # High Contrast Heading Navy
    "text_muted": "#64748B",      # Slate Gray Body
    "font_family": "Segoe UI",
}

# Application Metadata
APP_NAME = "High-Performance Hospital Management System"
COURSE_CODE = "BBAT104"
STUDENT_NAME = "Bhupinder Singh"
STUDENT_ROLL = "2410301011"
QUALITY_GOAL = "Q02 - Improve Performance"
