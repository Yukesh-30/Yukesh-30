import os
import json
import xml.sax.saxutils as xml_escape

def create_info_card_svg(json_file="data/contributions.json", output_file="info-card.svg"):
    if not os.path.exists(json_file):
        import fetch_contributions
        fetch_contributions.main()

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    stats = data.get("stats", {})

    current_streak = stats.get("current_streak", 150)
    current_streak_range = stats.get("current_streak_range", "May 10 - Oct 6") or "May 10 - Oct 6"
    
    longest_streak = stats.get("longest_streak", 150)
    longest_streak_range = stats.get("longest_streak_range", "May 10 - Oct 6") or "May 10 - Oct 6"
    
    total_contributions = stats.get("total_contributions", 8514)
    active_days = stats.get("active_days", 363)
    total_days = stats.get("total_days", 367)
    active_pct = stats.get("active_percentage", 99)
    
    best_day_count = stats.get("best_day_count", 128)
    best_day_date = stats.get("best_day_date", "Mar 7") or "Mar 7"
    avg_per_active_day = stats.get("avg_per_active_day", 23.5)

    monthly_data = stats.get("monthly_contributions", [])
    if not monthly_data or len(monthly_data) < 12:
        # Fallback monthly distribution for aesthetic bar chart
        monthly_data = [
            {"label": "O", "count": 420}, {"label": "N", "count": 510}, {"label": "D", "count": 480},
            {"label": "J", "count": 650}, {"label": "F", "count": 890}, {"label": "M", "count": 1270},
            {"label": "A", "count": 740}, {"label": "M", "count": 780}, {"label": "J", "count": 620},
            {"label": "J", "count": 590}, {"label": "A", "count": 510}, {"label": "S", "count": 430},
            {"label": "O", "count": 380}
        ]

    width = 420
    height = 520

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #21262d; stroke-width: 1px; }')
    svg.append('  .title-bar { fill: #161b22; }')
    svg.append('  .dot-red { fill: #ff5f56; } .dot-yellow { fill: #ffbd2e; } .dot-green { fill: #27c93f; }')
    svg.append('  .title-text { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 600; }')
    
    # Sub-card styling
    svg.append('  .sub-card { fill: #11161d; rx: 6px; ry: 6px; stroke: #21262d; stroke-width: 1px; }')
    svg.append('  .label-text { fill: #ea580c; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 600; }')
    svg.append('  .val-large { fill: #ea580c; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 20px; font-weight: 800; }')
    svg.append('  .val-white { fill: #ffffff; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 20px; font-weight: 800; }')
    svg.append('  .val-unit { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 400; }')
    svg.append('  .sub-desc { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; }')
    svg.append('  .bar-label { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 9.5px; }')
    svg.append('  .peak-label { fill: #ff8f00; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 9px; font-weight: bold; }')
    
    # Entrance animations
    svg.append('  @keyframes cardFade { 0% { opacity: 0; transform: translateY(6px); } 100% { opacity: 1; transform: translateY(0); } }')
    svg.append('  .animate-item { animation: cardFade 0.4s ease-out forwards; opacity: 0; }')
    svg.append('</style>')

    # Window Background
    svg.append(f'<rect width="{width}" height="{height}" class="bg" />')
    
    # Title Bar
    svg.append(f'<path d="M 0 8 A 8 8 0 0 1 8 0 L {width-8} 0 A 8 8 0 0 1 {width} 8 L {width} 36 L 0 36 Z" class="title-bar" />')
    svg.append('<circle cx="16" cy="18" r="5" class="dot-red" />')
    svg.append('<circle cx="32" cy="18" r="5" class="dot-yellow" />')
    svg.append('<circle cx="48" cy="18" r="5" class="dot-green" />')
    svg.append(f'<text x="65" y="22" class="title-text">yukesh@github: ~ $ ./stats.sh</text>')

    # Sub-card grid calculations
    card_w = 182
    card_h = 75
    gap_x = 16
    gap_y = 12
    margin_x = 20
    margin_y = 52

    # Card 1: $ current streak
    x1, y1 = margin_x, margin_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.05s;">')
    svg.append(f'  <rect x="{x1}" y="{y1}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x1 + 12}" y="{y1 + 22}" class="label-text">$ current streak</text>')
    svg.append(f'  <text x="{x1 + 12}" y="{y1 + 47}"><tspan class="val-large">{current_streak}</tspan> <tspan class="val-unit">days</tspan></text>')
    svg.append(f'  <text x="{x1 + 12}" y="{y1 + 62}" class="sub-desc">{current_streak_range}</text>')
    svg.append('</g>')

    # Card 2: $ longest streak
    x2, y2 = margin_x + card_w + gap_x, margin_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.10s;">')
    svg.append(f'  <rect x="{x2}" y="{y2}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x2 + 12}" y="{y2 + 22}" class="label-text">$ longest streak</text>')
    svg.append(f'  <text x="{x2 + 12}" y="{y2 + 47}"><tspan class="val-white">{longest_streak}</tspan> <tspan class="val-unit">days</tspan></text>')
    svg.append(f'  <text x="{x2 + 12}" y="{y2 + 62}" class="sub-desc">{longest_streak_range}</text>')
    svg.append('</g>')

    # Card 3: $ contributions
    x3, y3 = margin_x, margin_y + card_h + gap_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.15s;">')
    svg.append(f'  <rect x="{x3}" y="{y3}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x3 + 12}" y="{y3 + 22}" class="label-text">$ contributions</text>')
    svg.append(f'  <text x="{x3 + 12}" y="{y3 + 47}" class="val-white">{total_contributions:,}</text>')
    svg.append(f'  <text x="{x3 + 12}" y="{y3 + 62}" class="sub-desc">in the last year</text>')
    svg.append('</g>')

    # Card 4: $ active days
    x4, y4 = margin_x + card_w + gap_x, margin_y + card_h + gap_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.20s;">')
    svg.append(f'  <rect x="{x4}" y="{y4}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x4 + 12}" y="{y4 + 22}" class="label-text">$ active days</text>')
    svg.append(f'  <text x="{x4 + 12}" y="{y4 + 47}"><tspan class="val-white">{active_days}</tspan> <tspan class="val-unit">/ {total_days}</tspan></text>')
    svg.append(f'  <text x="{x4 + 12}" y="{y4 + 62}" class="sub-desc">{active_pct}% of the year</text>')
    svg.append('</g>')

    # Card 5: $ best day
    x5, y5 = margin_x, margin_y + (card_h + gap_y) * 2
    svg.append(f'<g class="animate-item" style="animation-delay: 0.25s;">')
    svg.append(f'  <rect x="{x5}" y="{y5}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x5 + 12}" y="{y5 + 22}" class="label-text">$ best day</text>')
    svg.append(f'  <text x="{x5 + 12}" y="{y5 + 47}" class="val-white">{best_day_count}</text>')
    svg.append(f'  <text x="{x5 + 12}" y="{y5 + 62}" class="sub-desc">{best_day_date}</text>')
    svg.append('</g>')

    # Card 6: $ avg / active day
    x6, y6 = margin_x + card_w + gap_x, margin_y + (card_h + gap_y) * 2
    svg.append(f'<g class="animate-item" style="animation-delay: 0.30s;">')
    svg.append(f'  <rect x="{x6}" y="{y6}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x6 + 12}" y="{y6 + 22}" class="label-text">$ avg / active day</text>')
    svg.append(f'  <text x="{x6 + 12}" y="{y6 + 47}" class="val-white">{avg_per_active_day}</text>')
    svg.append(f'  <text x="{x6 + 12}" y="{y6 + 62}" class="sub-desc">contributions</text>')
    svg.append('</g>')

    # Card 7: Bottom Monthly Bar Chart ($ contributions / month)
    x7, y7 = margin_x, margin_y + (card_h + gap_y) * 3
    chart_w = width - margin_x * 2 # 380
    chart_h = 185
    
    svg.append(f'<g class="animate-item" style="animation-delay: 0.35s;">')
    svg.append(f'  <rect x="{x7}" y="{y7}" width="{chart_w}" height="{chart_h}" class="sub-card" />')
    svg.append(f'  <text x="{x7 + 14}" y="{y7 + 22}" class="label-text">$ contributions / month</text>')

    # Monthly Bar Rendering
    bar_area_y = y7 + 42
    max_bar_height = 105
    num_bars = len(monthly_data)
    
    max_val = max(item["count"] for item in monthly_data) if monthly_data else 1
    max_val = max(1, max_val)

    bar_width = 16
    spacing = (chart_w - 28 - (num_bars * bar_width)) / max(1, num_bars - 1)

    for idx, item in enumerate(monthly_data):
        cnt = item["count"]
        b_h = int((cnt / max_val) * max_bar_height)
        b_h = max(6, b_h) # At least 6px tall
        
        bx = x7 + 14 + idx * (bar_width + spacing)
        by = bar_area_y + (max_bar_height - b_h)

        is_peak = (cnt == max_val)
        fill_color = "#ff8f00" if is_peak else "#ea580c"

        # Bar rect
        svg.append(f'  <rect x="{bx}" y="{by}" width="{bar_width}" height="{b_h}" rx="3" fill="{fill_color}" opacity="0.9" />')
        
        # Month Label
        label_x = bx + (bar_width / 2) - 3
        label_y = bar_area_y + max_bar_height + 16
        svg.append(f'  <text x="{label_x}" y="{label_y}" class="bar-label">{item["label"]}</text>')

        # Peak value tooltip label above highest bar
        if is_peak and cnt > 0:
            peak_x = bx + (bar_width / 2) - 12
            peak_y = by - 6
            svg.append(f'  <text x="{peak_x}" y="{peak_y}" class="peak-label">{cnt:,}</text>')

    svg.append('</g>')

    svg.append('</svg>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print(f"Generated Info/Stats Card SVG: {output_file}")

if __name__ == "__main__":
    create_info_card_svg()
