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

# Modern SaaS Healthcare UI Theme Palette (Matching Image 1 & Reference Design)
THEME = {
    "primary": "#0284C7",         # Vibrant Cyan-Blue
    "primary_dark": "#0369A1",    # Deep Blue
    "primary_light": "#DDF2FD",   # Soft Sky-Blue Active Pill (Image 1)
    "secondary": "#06B6D4",       # Medical Cyan
    "topbar_bg": "#003E5C",       # Deep Prussian / Teal Navy (Image 1 Header)
    "topbar_text": "#FFFFFF",
    "sidebar_bg": "#FFFFFF",      # Pure White Sidebar (Image 1)
    "sidebar_border": "#E2E8F0",  # Soft Slate Border
    "sidebar_hover": "#F0F9FF",   # Soft Light Blue Hover
    "sidebar_active": "#DDF2FD",  # Soft Cyan-Blue Active Pill (Image 1)
    "sidebar_text": "#334155",    # Dark Slate Menu Text
    "sidebar_text_active": "#0284C7", # Active Cyan-Blue Text (Image 1)
    "hero_navy": "#003E5C",       # Header Navy
    "emergency_coral": "#EF4444", # Vibrant Alert Red
    "pastel_blue": "#EFF6FF",     # Pastel Stat Card 1
    "pastel_blue_border": "#DBEAFE",
    "pastel_blue_hover": "#E0E7FF",
    "pastel_amber": "#FFFBEB",    # Pastel Stat Card 2
    "pastel_amber_border": "#FDE68A",
    "pastel_amber_hover": "#FEF3C7",
    "pastel_rose": "#FEF2F2",     # Pastel Stat Card 3
    "pastel_rose_border": "#FECACA",
    "pastel_rose_hover": "#FEE2E2",
    "pastel_purple": "#FAF5FF",   # Pastel Specialist Card
    "pastel_purple_border": "#E9D8FD",
    "pastel_purple_hover": "#F3E8FF",
    "success": "#10B981",         # Emerald Green
    "success_light": "#ECFDF5",
    "warning": "#F59E0B",         # Amber Alert
    "warning_light": "#FFFBEB",
    "danger": "#EF4444",          # Rose Red
    "danger_light": "#FEF2F2",
    "purple": "#8B5CF6",          # Violet Accent
    "purple_light": "#F5F3FF",
    "background": "#F0F6FA",      # Soft Light Cool Gray-Blue (Image 1 Canvas)
    "surface": "#FFFFFF",         # Pure White Card
    "border": "#E2E8F0",          # Soft Border
    "text": "#0F172A",            # High Contrast Heading Navy
    "text_muted": "#64748B",      # Slate Gray Body
    "font_family": "Segoe UI",
}

# Application Metadata
APP_NAME = "High-Performance Hospital Management System"
COURSE_CODE = "BBAT104"
STUDENT_NAME = "Bhupinder Singh"
STUDENT_ROLL = "2410301011"
QUALITY_GOAL = "Q02 - Improve Performance"
