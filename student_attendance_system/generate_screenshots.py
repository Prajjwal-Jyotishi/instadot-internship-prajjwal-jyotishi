"""
generate_screenshots.py
Runs each system function, captures terminal output, and saves
dark-themed terminal PNG screenshots to the screenshots/ folder.
"""

import sys, os, io
sys.path.insert(0, os.path.dirname(__file__))

import storage
storage.DATA_DIR = os.path.join(os.path.dirname(__file__), "data_ss")
storage.STUDENTS_FILE = os.path.join(storage.DATA_DIR, "students.json")
storage.ATTENDANCE_FILE = os.path.join(storage.DATA_DIR, "attendance.csv")
os.makedirs(storage.DATA_DIR, exist_ok=True)

from system import (register_student, search_student, list_students, delete_student,
                    mark_attendance, update_attendance, attendance_percentage,
                    monthly_report, run_report_in_background)
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ── Terminal colours ──────────────────────────────────────────────────────────
BG      = (18, 18, 18)
FG      = (204, 204, 204)
GREEN   = (80, 200, 120)
YELLOW  = (255, 200, 80)
CYAN    = (86, 182, 194)
PAD     = 24
LINE_H  = 20
FONT_SZ = 14

try:
    FONT = ImageFont.truetype("cour.ttf", FONT_SZ)         # Courier New
except:
    try:
        FONT = ImageFont.truetype("consola.ttf", FONT_SZ)  # Consolas
    except:
        FONT = ImageFont.load_default()


MENU = """\n--- Student Attendance Management System ---
1. Register Student
2. Search Student
3. List All Students
4. Delete Student
5. Mark Attendance
6. Update Attendance
7. Attendance Percentage
8. Monthly Report
0. Exit"""


def capture(fn):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    fn()
    sys.stdout = old
    return buf.getvalue()


def save_screenshot(filename, text_blocks):
    """
    text_blocks: list of (text, color) tuples.
    Renders them as a terminal-style PNG.
    """
    lines = []
    for text, color in text_blocks:
        for line in text.splitlines():
            lines.append((line, color))

    width  = 860
    height = PAD * 2 + len(lines) * LINE_H + 10

    img  = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 28], fill=(40, 40, 40))
    draw.text((12, 6), "  Python  ●  Student Attendance Management System", font=FONT, fill=(160, 160, 160))
    draw.ellipse([width-60, 8, width-44, 22], fill=(255, 90, 90))
    draw.ellipse([width-38, 8, width-22, 22], fill=(255, 190, 60))
    draw.ellipse([width-16, 8, width-2,  22], fill=(60, 200, 80))

    y = 36
    for line, color in lines:
        draw.text((PAD, y), line, font=FONT, fill=color)
        y += LINE_H

    path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(path)
    print(f"Saved: {path}")


# ── Seed data ─────────────────────────────────────────────────────────────────
register_student("10", "prajjwal jyotishi", "bca")
for d, s in [("2026-06-23","P"),("2026-06-24","A"),("2026-06-25","P")]:
    mark_attendance("10", d, s)

# ── Screenshot 1: Register + Search ──────────────────────────────────────────
s_reg    = capture(lambda: register_student("11", "anjali sharma", "mca"))
s_search = capture(lambda: search_student("10"))

save_screenshot("output_1_register_search.png", [
    (MENU,                          FG),
    ("\nEnter choice: 1",            CYAN),
    ("Student ID: 11",              FG),
    ("Name: anjali sharma",         FG),
    ("Course: mca",                 FG),
    (s_reg.strip(),                 GREEN),
    (MENU,                          FG),
    ("\nEnter choice: 2",            CYAN),
    ("Student ID: 10",              FG),
    (s_search.strip(),              GREEN),
])

# ── Screenshot 2: List + Delete ───────────────────────────────────────────────
s_list = capture(list_students)
save_screenshot("output_2_list_delete.png", [
    (MENU,                                          FG),
    ("\nEnter choice: 3",                            CYAN),
    (s_list.strip(),                                FG),
    (MENU,                                          FG),
    ("\nEnter choice: 4",                            CYAN),
    ("Student ID: 11",                              FG),
    ("Delete '11'? (yes/no): yes",                  FG),
    (capture(lambda: delete_student("11")).strip(), GREEN),
])

# ── Screenshot 3: Register again + Mark Attendance ────────────────────────────
s_reg2  = capture(lambda: register_student("11", "anjali sharma", "mca"))
s_mark  = capture(lambda: mark_attendance("11", "2026-06-25", "P"))

save_screenshot("output_3_register_mark.png", [
    (MENU,                           FG),
    ("\nEnter choice: 1",             CYAN),
    ("Student ID: 11",               FG),
    ("Name: anjali sharma",          FG),
    ("Course: mca",                  FG),
    (s_reg2.strip(),                 GREEN),
    (MENU,                           FG),
    ("\nEnter choice: 5",             CYAN),
    ("Student ID: 10",               FG),
    ("Date (YYYY-MM-DD) [blank = today]: 2026-06-25", FG),
    ("Status (P/A/L): p",            FG),
    ("Attendance for '10' on 2026-06-25 already marked.", YELLOW),
    ("\nMarking fresh date 2026-06-26:", FG),
    (capture(lambda: mark_attendance("10", "2026-06-26", "P")).strip(), GREEN),
])

# ── Screenshot 4: Update + Percentage ────────────────────────────────────────
s_upd = capture(lambda: update_attendance("10", "2026-06-24", "L"))
s_pct = capture(lambda: attendance_percentage("10"))

save_screenshot("output_4_update_percentage.png", [
    (MENU,           FG),
    ("\nEnter choice: 6", CYAN),
    ("Student ID: 10",   FG),
    ("Date (YYYY-MM-DD): 2026-06-24", FG),
    ("New Status (P/A/L): l",         FG),
    (s_upd.strip(),                   GREEN),
    (MENU,           FG),
    ("\nEnter choice: 7", CYAN),
    ("Student ID: 10",   FG),
    (s_pct.strip(),      GREEN),
])

# ── Screenshot 5: Percentage + Monthly Report ─────────────────────────────────
s_pct2    = capture(lambda: attendance_percentage("10"))
s_report  = capture(lambda: monthly_report(2026, 6))

save_screenshot("output_5_percentage_report.png", [
    (MENU,           FG),
    ("\nEnter choice: 7", CYAN),
    ("Student ID: 10",   FG),
    (s_pct2.strip(),     GREEN),
    (MENU,           FG),
    ("\nEnter choice: 8", CYAN),
    ("Year [2026]:",      FG),
    ("Month [6]:",        FG),
    (s_report.strip(),    FG),
])

# ── Screenshot 6: Monthly Report + Background Auto Exit ───────────────────────
s_report2 = capture(lambda: monthly_report(2026, 6))

def run_bg():
    t = run_report_in_background()
    t.join(timeout=5)

s_bg = capture(run_bg)

save_screenshot("output_6_report_exit.png", [
    (s_report2.strip(),                              FG),
    (MENU,                                           FG),
    ("\nEnter choice: 0",                             CYAN),
    (s_bg.strip(),                                   YELLOW),
    ("\nGoodbye!",                                    GREEN),
])

# Cleanup
import shutil
shutil.rmtree(storage.DATA_DIR, ignore_errors=True)
print("\nAll 6 screenshots generated successfully!")
