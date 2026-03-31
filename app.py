"""
CampusFuel — Nutrition & Fitness MVP for College Students
=========================================================
A single-file Streamlit app that lets students track dining-hall meals,
hit macro targets, and get AI-style nutrition insights.

Run with:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
import math

# ─────────────────────────────────────────────────────────────────────────────
# 1.  PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampusFuel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
/* ── Import premium fonts ───────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CSS variables ──────────────────────────────────────────────────────── */
:root {
    --bg-primary:    #0A0A0A;
    --bg-card:       #111111;
    --bg-card-hover: #1A1A1A;
    --accent:        #00FF88;
    --accent-dim:    #00CC6A;
    --accent-dark:   #0F3D2E;
    --text-primary:  #FFFFFF;
    --text-secondary:#B0B0B0;
    --text-muted:    #666666;
    --danger:        #FF4D6A;
    --warning:       #FFB84D;
    --border:        #1E1E1E;
}

/* ── Global overrides ───────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D0D 0%, #0A0A0A 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
}

/* ── Headings ───────────────────────────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
}
h1 { font-weight: 800 !important; letter-spacing: -0.03em; }
h2 { font-weight: 700 !important; letter-spacing: -0.02em; }
h3 { font-weight: 600 !important; }

/* ── Card container ─────────────────────────────────────────────────────── */
.cf-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s ease;
}
.cf-card:hover {
    border-color: #2A2A2A;
}

/* ── Metric card (mini) ─────────────────────────────────────────────────── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.metric-card .metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
}
.metric-card .metric-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.35rem;
}

/* ── Progress bars ──────────────────────────────────────────────────────── */
.progress-outer {
    background: #1A1A1A;
    border-radius: 8px;
    height: 14px;
    overflow: hidden;
    margin: 0.3rem 0 0.2rem 0;
}
.progress-inner {
    height: 100%;
    border-radius: 8px;
    transition: width 0.6s cubic-bezier(.22,1,.36,1);
}

/* ── Insight box ────────────────────────────────────────────────────────── */
.insight-box {
    background: linear-gradient(135deg, #0F3D2E 0%, #112211 100%);
    border: 1px solid #1B5E3C;
    border-radius: 14px;
    padding: 1.35rem 1.5rem;
    margin-top: 0.5rem;
    line-height: 1.7;
    color: #D0FFE8;
    font-size: 0.95rem;
}
.insight-box strong {
    color: var(--accent);
}

/* ── Food table ─────────────────────────────────────────────────────────── */
.food-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 0.5rem 0;
}
.food-table th {
    text-align: left;
    padding: 0.6rem 0.75rem;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border);
}
.food-table td {
    padding: 0.55rem 0.75rem;
    font-size: 0.92rem;
    color: var(--text-secondary);
    border-bottom: 1px solid #151515;
}
.food-table tr:last-child td { border-bottom: none; }
.food-table .food-name { color: var(--text-primary); font-weight: 500; }
.food-table .accent-val { color: var(--accent); font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 0.88rem; }

/* ── Meal tray ──────────────────────────────────────────────────────────── */
.tray-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid #181818;
    font-size: 0.92rem;
}
.tray-item:last-child { border-bottom: none; }
.tray-item .tray-name { color: var(--text-primary); font-weight: 500; }
.tray-item .tray-qty  { color: var(--accent); font-family: 'JetBrains Mono', monospace; }

/* ── Badge pill ─────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    background: var(--accent-dark);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Hero title ─────────────────────────────────────────────────────────── */
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.15rem;
}
.hero-title .accent { color: var(--accent); }
.hero-sub {
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 1.5rem;
}

/* ── Misc polish ────────────────────────────────────────────────────────── */
.stMultiSelect [data-baseweb="tag"] {
    background-color: var(--accent-dark) !important;
    color: var(--accent) !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] {
    font-family: 'Outfit', sans-serif !important;
}
.stNumberInput input {
    font-family: 'JetBrains Mono', monospace !important;
}

/* hide default streamlit metric styling (we use custom cards) */
[data-testid="stMetric"] { display: none; }

/* divider */
.cf-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2.  MOCK DINING-HALL MENU DATA  (per serving)
# ─────────────────────────────────────────────────────────────────────────────
MENU: list[dict] = [
    {"name": "Grilled Chicken",  "cal": 220, "protein": 35, "carbs":  0, "fat":  8, "emoji": "🍗"},
    {"name": "Rice",             "cal": 210, "protein":  4, "carbs": 46, "fat":  1, "emoji": "🍚"},
    {"name": "Pasta",            "cal": 320, "protein": 11, "carbs": 58, "fat":  5, "emoji": "🍝"},
    {"name": "Salad",            "cal":  80, "protein":  3, "carbs": 10, "fat":  3, "emoji": "🥗"},
    {"name": "Eggs (2 large)",   "cal": 155, "protein": 13, "carbs":  1, "fat": 11, "emoji": "🥚"},
    {"name": "Oatmeal",          "cal": 150, "protein":  5, "carbs": 27, "fat":  3, "emoji": "🥣"},
    {"name": "Greek Yogurt",     "cal": 130, "protein": 17, "carbs":  6, "fat":  4, "emoji": "🍦"},
    {"name": "Burrito Bowl",     "cal": 510, "protein": 28, "carbs": 52, "fat": 18, "emoji": "🌯"},
    {"name": "Stir Fry",         "cal": 340, "protein": 22, "carbs": 30, "fat": 14, "emoji": "🥘"},
    {"name": "Turkey Sandwich",  "cal": 380, "protein": 26, "carbs": 36, "fat": 12, "emoji": "🥪"},
]


# ─────────────────────────────────────────────────────────────────────────────
# 3.  DAILY TARGET CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────
def compute_targets(weight_lbs: float, goal: str, activity: str, day_type: str) -> dict:
    """
    Simple but logical calorie / macro estimator.

    Base calories  = body-weight (lbs) × 15  (rough TDEE proxy)
    Activity mult  = low 0.90 | medium 1.00 | high 1.15
    Day-type adj   = rest −200 | gym +100 | running +150
    Goal adj       = lose −400 | maintain 0 | gain +350

    Macros derived from goal-specific percentage splits.
    """
    base = weight_lbs * 15.0

    # Activity multiplier
    act_mult = {"Low": 0.90, "Medium": 1.00, "High": 1.15}[activity]
    base *= act_mult

    # Day-type adjustment
    day_adj = {"Rest day": -200, "Gym / lifting": 100, "Running / cardio": 150}[day_type]
    base += day_adj

    # Goal adjustment
    goal_adj = {"Lose weight": -400, "Maintain weight": 0, "Gain muscle": 350}[goal]
    cal_target = max(1200, round(base + goal_adj))

    # Macro splits (% of calories → grams)
    splits = {
        "Lose weight":     (0.40, 0.30, 0.30),   # high protein
        "Maintain weight":  (0.30, 0.40, 0.30),
        "Gain muscle":      (0.30, 0.45, 0.25),   # high carbs
    }
    p_pct, c_pct, f_pct = splits[goal]

    protein_g = round(cal_target * p_pct / 4)
    carbs_g   = round(cal_target * c_pct / 4)
    fat_g     = round(cal_target * f_pct / 9)

    return {
        "calories": cal_target,
        "protein":  protein_g,
        "carbs":    carbs_g,
        "fat":      fat_g,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4.  AI-STYLE INSIGHT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
def generate_insights(consumed: dict, targets: dict, goal: str) -> list[str]:
    """Return a list of plain-English coaching tips."""
    tips: list[str] = []
    cal_pct  = consumed["calories"] / max(targets["calories"], 1)
    pro_pct  = consumed["protein"]  / max(targets["protein"], 1)
    carb_pct = consumed["carbs"]    / max(targets["carbs"], 1)
    fat_pct  = consumed["fat"]      / max(targets["fat"], 1)

    # ── Calorie insights ────────────────────────────────────────────────────
    if cal_pct < 0.25:
        tips.append("You've barely eaten today — make sure you're fueling up enough to stay focused in class.")
    elif cal_pct < 0.70:
        tips.append("You're under your calorie target. You still have room for a solid meal.")
    elif cal_pct < 0.95:
        tips.append("Nice — you're closing in on your calorie goal for the day.")
    elif cal_pct <= 1.05:
        tips.append("🎯 You've hit your calorie target almost perfectly. Well done!")
    else:
        over = round(consumed["calories"] - targets["calories"])
        tips.append(f"You're about {over} cal over your target. Not the end of the world — just keep it in mind.")

    # ── Protein insights ────────────────────────────────────────────────────
    if pro_pct < 0.60:
        tips.append("⚠️ You're well below your protein target. Add grilled chicken, eggs, or Greek yogurt.")
    elif pro_pct < 0.90:
        tips.append("Protein is a bit low — a quick Greek yogurt or some eggs would close the gap.")
    elif pro_pct >= 0.90:
        tips.append("✅ Protein intake is on track. Keep it up!")

    # ── Carb insights ───────────────────────────────────────────────────────
    if goal == "Lose weight" and carb_pct > 1.15:
        tips.append("Your carbs are running high for a cut. Consider swapping pasta for salad or extra protein.")
    elif goal == "Gain muscle" and carb_pct < 0.60:
        tips.append("Carbs are low for a bulk day. Add rice or oatmeal to fuel your workout recovery.")

    # ── Fat insights ────────────────────────────────────────────────────────
    if fat_pct > 1.20:
        tips.append("Fat intake is above target. Try grilled over fried options next meal.")

    # ── Bonus motivational nudge ────────────────────────────────────────────
    if consumed["calories"] == 0:
        tips = ["👋 Start logging your meals below — select items and set servings to see your dashboard light up!"]

    return tips


# ─────────────────────────────────────────────────────────────────────────────
# 5.  HELPER: RENDER A PROGRESS BAR
# ─────────────────────────────────────────────────────────────────────────────
def progress_bar_html(consumed: float, target: float, color: str = "#00FF88") -> str:
    """Return styled HTML for a single progress bar."""
    pct = min(consumed / max(target, 1) * 100, 100)
    overflow = consumed > target
    bar_color = "#FF4D6A" if overflow else color
    return (
        f'<div class="progress-outer">'
        f'  <div class="progress-inner" style="width:{pct:.1f}%;background:{bar_color};"></div>'
        f'</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# 6.  SIDEBAR — USER PROFILE
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p style="font-size:1.4rem;font-weight:800;letter-spacing:-0.03em;">'
        '⚡ <span style="color:#00FF88;">Campus</span>Fuel</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#666;font-size:0.82rem;margin-top:-0.6rem;">Your campus nutrition co-pilot</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="cf-divider">', unsafe_allow_html=True)

    st.markdown("##### 👤 Your Profile")
    weight = st.number_input("Body weight (lbs)", min_value=80, max_value=400, value=160, step=5)
    goal = st.selectbox("Goal", ["Lose weight", "Maintain weight", "Gain muscle"])
    activity = st.selectbox("Activity level", ["Low", "Medium", "High"])
    day_type = st.selectbox("Today's activity", ["Rest day", "Gym / lifting", "Running / cardio"])

    st.markdown('<hr class="cf-divider">', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#444;font-size:0.72rem;text-align:center;">v1.0 MVP · Built for students</p>',
        unsafe_allow_html=True,
    )


# Compute daily targets from profile
targets = compute_targets(weight, goal, activity, day_type)


# ─────────────────────────────────────────────────────────────────────────────
# 7.  MAIN AREA — HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero-title"><span class="accent">Campus</span>Fuel ⚡</div>'
    '<div class="hero-sub">Track your dining-hall meals. Hit your macros. Stay fueled.</div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# 8.  DAILY TARGETS (top metric cards)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🎯 Your Daily Targets")
t1, t2, t3, t4 = st.columns(4)

for col, (label, value, unit) in zip(
    [t1, t2, t3, t4],
    [
        ("Calories",  targets["calories"], "kcal"),
        ("Protein",   targets["protein"],  "g"),
        ("Carbs",     targets["carbs"],    "g"),
        ("Fat",       targets["fat"],      "g"),
    ],
):
    col.markdown(
        f'<div class="metric-card">'
        f'  <div class="metric-value">{value:,}</div>'
        f'  <div class="metric-label">{label} · {unit}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

goal_badge = {"Lose weight": "CUT", "Maintain weight": "MAINTAIN", "Gain muscle": "BULK"}[goal]
st.markdown(
    f'<div style="margin-top:0.5rem;">'
    f'  <span class="badge">{goal_badge}</span>  '
    f'  <span class="badge">{activity} activity</span>  '
    f'  <span class="badge">{day_type}</span>'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown('<hr class="cf-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 9.  DINING HALL MENU TABLE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🍽️ Dining Hall Menu")
st.markdown(
    '<p style="color:#666;font-size:0.85rem;margin-top:-0.5rem;">Nutritional values per single serving</p>',
    unsafe_allow_html=True,
)

rows_html = ""
for item in MENU:
    rows_html += (
        f'<tr>'
        f'  <td class="food-name">{item["emoji"]} {item["name"]}</td>'
        f'  <td class="accent-val">{item["cal"]}</td>'
        f'  <td>{item["protein"]}g</td>'
        f'  <td>{item["carbs"]}g</td>'
        f'  <td>{item["fat"]}g</td>'
        f'</tr>'
    )

st.markdown(
    f'<div class="cf-card">'
    f'<table class="food-table">'
    f'  <thead><tr>'
    f'    <th>Item</th><th>Calories</th><th>Protein</th><th>Carbs</th><th>Fat</th>'
    f'  </tr></thead>'
    f'  <tbody>{rows_html}</tbody>'
    f'</table></div>',
    unsafe_allow_html=True,
)

st.markdown('<hr class="cf-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 10.  MEAL BUILDER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🛠️ Meal Builder")
st.markdown(
    '<p style="color:#666;font-size:0.85rem;margin-top:-0.5rem;">Select items, set servings, and watch your macros update live</p>',
    unsafe_allow_html=True,
)

food_names = [f'{item["emoji"]} {item["name"]}' for item in MENU]
selected = st.multiselect("Choose dining hall items", food_names, placeholder="Search or pick foods…")

# Map display names back to data
name_to_item = {f'{item["emoji"]} {item["name"]}': item for item in MENU}

# Session state for servings
if "servings" not in st.session_state:
    st.session_state.servings = {}

# Build servings inputs & compute totals
consumed = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
tray_items: list[dict] = []

if selected:
    st.markdown('<div class="cf-card">', unsafe_allow_html=True)
    cols = st.columns(min(len(selected), 4))
    for idx, disp_name in enumerate(selected):
        item = name_to_item[disp_name]
        with cols[idx % len(cols)]:
            qty = st.number_input(
                f"{item['emoji']} {item['name']}",
                min_value=0.5,
                max_value=10.0,
                value=1.0,
                step=0.5,
                key=f"qty_{item['name']}",
            )
        consumed["calories"] += round(item["cal"]  * qty)
        consumed["protein"]  += round(item["protein"] * qty)
        consumed["carbs"]    += round(item["carbs"] * qty)
        consumed["fat"]      += round(item["fat"]  * qty)
        tray_items.append({"name": item["name"], "emoji": item["emoji"], "qty": qty,
                           "cal": round(item["cal"] * qty)})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Meal tray summary ───────────────────────────────────────────────────
    st.markdown("#### 🧾 Your Tray")
    tray_html = ""
    for t in tray_items:
        tray_html += (
            f'<div class="tray-item">'
            f'  <span class="tray-name">{t["emoji"]} {t["name"]}</span>'
            f'  <span class="tray-qty">×{t["qty"]:.1f}  —  {t["cal"]} cal</span>'
            f'</div>'
        )
    st.markdown(f'<div class="cf-card">{tray_html}</div>', unsafe_allow_html=True)

    # ── Totals row ──────────────────────────────────────────────────────────
    tc1, tc2, tc3, tc4 = st.columns(4)
    for col, (label, val) in zip(
        [tc1, tc2, tc3, tc4],
        [("Calories", consumed["calories"]),
         ("Protein",  consumed["protein"]),
         ("Carbs",    consumed["carbs"]),
         ("Fat",      consumed["fat"])],
    ):
        col.markdown(
            f'<div class="metric-card">'
            f'  <div class="metric-value" style="font-size:1.6rem;">{val:,}</div>'
            f'  <div class="metric-label">{label} consumed</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        '<div class="cf-card" style="text-align:center;padding:2.5rem;color:#555;">'
        '🍽️ Pick items above to start building your meal</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="cf-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 11.  DASHBOARD — CONSUMED vs. TARGET
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📊 Dashboard")

macro_colors = {
    "Calories": "#00FF88",
    "Protein":  "#00CCFF",
    "Carbs":    "#FFB84D",
    "Fat":      "#FF4D6A",
}

d1, d2 = st.columns(2)
pairs = [
    ("Calories", consumed["calories"], targets["calories"], "kcal"),
    ("Protein",  consumed["protein"],  targets["protein"],  "g"),
    ("Carbs",    consumed["carbs"],    targets["carbs"],    "g"),
    ("Fat",      consumed["fat"],      targets["fat"],      "g"),
]

for idx, (label, con, tar, unit) in enumerate(pairs):
    col = d1 if idx < 2 else d2
    pct = min(con / max(tar, 1) * 100, 100)
    status = "over" if con > tar else "on track" if pct >= 90 else "remaining"
    color = macro_colors[label]
    col.markdown(
        f'<div class="cf-card">'
        f'  <div style="display:flex;justify-content:space-between;align-items:baseline;">'
        f'    <span style="font-weight:600;font-size:1rem;">{label}</span>'
        f'    <span style="color:{color};font-family:JetBrains Mono,monospace;font-size:0.95rem;font-weight:600;">'
        f'      {con:,} <span style="color:#666;font-weight:400;">/ {tar:,} {unit}</span>'
        f'    </span>'
        f'  </div>'
        f'  {progress_bar_html(con, tar, color)}'
        f'  <div style="text-align:right;font-size:0.72rem;color:#666;margin-top:2px;">{pct:.0f}%</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="cf-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 12.  AI-STYLE INSIGHT BOX
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 💡 Smart Insights")
tips = generate_insights(consumed, targets, goal)
tips_html = "".join(f"<div style='margin-bottom:0.45rem;'>• {tip}</div>" for tip in tips)
st.markdown(f'<div class="insight-box">{tips_html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 13.  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;margin-top:3rem;padding:1.5rem 0;border-top:1px solid #1E1E1E;">'
    '  <span style="font-weight:700;font-size:1rem;">⚡ <span style="color:#00FF88;">Campus</span>Fuel</span><br>'
    '  <span style="color:#444;font-size:0.78rem;">Built for students who take their fuel seriously.</span>'
    '</div>',
    unsafe_allow_html=True,
)
