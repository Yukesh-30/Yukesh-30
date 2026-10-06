import os
import json
import xml.sax.saxutils as xml_escape

def get_target_ascii_art():
    """Exact ASCII portrait with 'NOT MY CUP OF TEA' embedded."""
    lines = [
        "              `.-:::///+++++//:.              ",
        "           .///:-...---://+OOSSYYHDHS+-       ",
        "        :Y+.`````````..--:/+OSYYYYHHHO.       ",
        "      /D-``                 ` -:+SYSYM:       ",
        "     DM.`                       -//MH:-.`     ",
        "     DNMO.                        :HDOHMNNNMYO-",
        "     DMNNNDS/-`                -/SYS/-.``-:+OYHMMS.",
        "     HMMNNNNNNMDHYSSOOOOOsssss+:`.`..+`````..:/+S+",
        "     HMMNNMMMMMDDHYYS0+/:--.....`...+`        :0/:/",
        "     HMMNNMMMMMDDHHYS0++/:-......--/          -S0---0",
        "     YMMNMMMMMMDDHHYS0+/::--......--/          .YYO--0",
        "     YMMMMMMMMMDDH    +/::--......--/          /YYS---0",
        "     SMMMMMMMMMDDH NOT +/::--......--/          /SYYO-0",
        "     OMMMMMMMMMDDH MY  ++/::----...--:          ./+YSS:0",
        "     +MMMMMMMMMDDH CUP ++/::-------...:      .:++SSYO:0",
        "     +MMMMMMMMMDDH OF  0+/::-------...:-./++OOSSS+-0",
        "     +MMMMMMMMMDDH TEA 0+//:::-------:-////++00/-`0",
        "     /MMMMMMMMMDDH     0+//:::-------::`.-:///-.0",
        "     /MMMMMMMMMDDDHHYYS0++///:::-----::/`.-.,`",
        "     .DMMMMMMMMDDDHHYYS0++//::::::--:::/",
        "      -DMMMMMMMDDDHHYYS0++//:::::::::::",
        "       `ODMMMMMDDDHHYYS0++//:::::::::-",
        "         :SDMDDDDHHYYSS00+//:::--.",
        "           ./OSHHHYYSS000+/:--.",
        "                ......."
    ]
    return lines

def create_whoami_suite_svg(json_file="data/contributions.json", output_file="whoami-suite.svg"):
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
        monthly_data = [
            {"label": "O", "count": 420}, {"label": "N", "count": 510}, {"label": "D", "count": 480},
            {"label": "J", "count": 650}, {"label": "F", "count": 890}, {"label": "M", "count": 1270},
            {"label": "A", "count": 740}, {"label": "M", "count": 780}, {"label": "J", "count": 620},
            {"label": "J", "count": 590}, {"label": "A", "count": 510}, {"label": "S", "count": 430},
            {"label": "O", "count": 380}
        ]

    width = 860
    height = 530

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    # Master Container Outer Frame
    svg.append('  .master-bg { fill: #070a0f; rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1px; }')
    # Inner Window Frames
    svg.append('  .win-bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #21262d; stroke-width: 1px; }')
    svg.append('  .title-bar { fill: #161b22; }')
    svg.append('  .dot-red { fill: #ff5f56; } .dot-yellow { fill: #ffbd2e; } .dot-green { fill: #27c93f; }')
    svg.append('  .title-text { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 600; }')
    svg.append('  .ascii-text { fill: #d27d2d; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; font-weight: 600; white-space: pre; }')
    svg.append('  .cup-text-highlight { fill: #fbbf24; font-weight: 800; }')
    svg.append('  .prompt-text { fill: #7d8590; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 500; }')
    svg.append('  .user-text { fill: #ffffff; font-weight: bold; }')
    
    # Sub-card styling for Stats Window
    svg.append('  .sub-card { fill: #11161d; rx: 6px; ry: 6px; stroke: #21262d; stroke-width: 1px; }')
    svg.append('  .label-text { fill: #ea580c; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 600; }')
    svg.append('  .val-large { fill: #ea580c; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 19px; font-weight: 800; }')
    svg.append('  .val-white { fill: #ffffff; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 19px; font-weight: 800; }')
    svg.append('  .val-unit { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 400; }')
    svg.append('  .sub-desc { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; }')
    svg.append('  .bar-label { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 9.5px; }')
    svg.append('  .peak-label { fill: #ff8f00; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 9px; font-weight: bold; }')
    
    # Keyframe entrance animations
    svg.append('  @keyframes cardFade { 0% { opacity: 0; transform: translateY(6px); } 100% { opacity: 1; transform: translateY(0); } }')
    svg.append('  .animate-item { animation: cardFade 0.4s ease-out forwards; opacity: 0; }')
    svg.append('</style>')

    # ASCII clip paths (Slow & Eased typing animation)
    ascii_lines = get_target_ascii_art()
    num_rows = len(ascii_lines)
    total_duration = 5.5
    row_delay = total_duration / max(1, num_rows)
    row_duration = 0.45

    svg.append('<defs>')
    left_pad_x = 32
    left_pad_y = 66
    line_h = 16.0
    for i in range(num_rows):
        clip_id = f"suite-art-clip-{i}"
        begin_time = f"{i * row_delay:.2f}s"
        svg.append(f'  <clipPath id="{clip_id}">')
        svg.append(f'    <rect x="{left_pad_x}" y="{left_pad_y + i * line_h - 4}" width="0" height="{line_h + 4}">')
        svg.append(f'      <animate attributeName="width" from="0" to="380" dur="{row_duration:.2f}s" begin="{begin_time}" calcMode="spline" keySplines="0.25 0.1 0.25 1.0" fill="freeze" />')
        svg.append('    </rect>')
        svg.append('  </clipPath>')
    svg.append('</defs>')

    # Master Container Rect (Outer Dark Box with Border #30363d)
    svg.append(f'<rect width="{width}" height="{height}" class="master-bg" />')

    # ================= LEFT WINDOW: PORTRAIT =================
    win1_x, win1_y = 16, 16
    win1_w, win1_h = 404, 498
    svg.append(f'<rect x="{win1_x}" y="{win1_y}" width="{win1_w}" height="{win1_h}" class="win-bg" />')
    
    # Left Title bar
    svg.append(f'<path d="M {win1_x} {win1_y + 8} A 8 8 0 0 1 {win1_x + 8} {win1_y} L {win1_x + win1_w - 8} {win1_y} A 8 8 0 0 1 {win1_x + win1_w} {win1_y + 8} L {win1_x + win1_w} {win1_y + 36} L {win1_x} {win1_y + 36} Z" class="title-bar" />')
    svg.append(f'<circle cx="{win1_x + 16}" cy="{win1_y + 18}" r="5" class="dot-red" />')
    svg.append(f'<circle cx="{win1_x + 32}" cy="{win1_y + 18}" r="5" class="dot-yellow" />')
    svg.append(f'<circle cx="{win1_x + 48}" cy="{win1_y + 18}" r="5" class="dot-green" />')
    svg.append(f'<text x="{win1_x + 65}" y="{win1_y + 22}" class="title-text">yukesh@github: ~ $ ./portrait.sh</text>')

    # ASCII content inside left window
    for i, line in enumerate(ascii_lines):
        escaped_line = xml_escape.escape(line)
        for kw in ["NOT", "MY", "CUP", "OF", "TEA"]:
            if f" {kw} " in escaped_line:
                escaped_line = escaped_line.replace(f" {kw} ", f' <tspan class="cup-text-highlight">{kw}</tspan> ')
        
        y_pos = left_pad_y + (i + 1) * line_h - 4
        clip_id = f"suite-art-clip-{i}"
        svg.append(f'<g clip-path="url(#{clip_id})">')
        svg.append(f'  <text x="{left_pad_x}" y="{y_pos}" class="ascii-text">{escaped_line}</text>')
        svg.append('</g>')

    # Left bottom status prompt
    svg.append(f'<text x="{win1_x + 16}" y="{win1_y + win1_h - 16}" class="prompt-text">yukesh@github:~$ whoami <tspan class="user-text">Yukesh D</tspan></text>')


    # ================= RIGHT WINDOW: STATS =================
    win2_x, win2_y = 436, 16
    win2_w, win2_h = 408, 498
    svg.append(f'<rect x="{win2_x}" y="{win2_y}" width="{win2_w}" height="{win2_h}" class="win-bg" />')

    # Right Title bar
    svg.append(f'<path d="M {win2_x} {win2_y + 8} A 8 8 0 0 1 {win2_x + 8} {win2_y} L {win2_x + win2_w - 8} {win2_y} A 8 8 0 0 1 {win2_x + win2_w} {win2_y + 8} L {win2_x + win2_w} {win2_y + 36} L {win2_x} {win2_y + 36} Z" class="title-bar" />')
    svg.append(f'<circle cx="{win2_x + 16}" cy="{win2_y + 18}" r="5" class="dot-red" />')
    svg.append(f'<circle cx="{win2_x + 32}" cy="{win2_y + 18}" r="5" class="dot-yellow" />')
    svg.append(f'<circle cx="{win2_x + 48}" cy="{win2_y + 18}" r="5" class="dot-green" />')
    svg.append(f'<text x="{win2_x + 65}" y="{win2_y + 22}" class="title-text">yukesh@github: ~ $ ./stats.sh</text>')

    # Sub-cards inside right window
    card_w = 180
    card_h = 72
    gap_x = 14
    gap_y = 12
    margin_x = win2_x + 16
    margin_y = win2_y + 50

    # Card 1: $ current streak
    x1, y1 = margin_x, margin_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.05s;">')
    svg.append(f'  <rect x="{x1}" y="{y1}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x1 + 10}" y="{y1 + 20}" class="label-text">$ current streak</text>')
    svg.append(f'  <text x="{x1 + 10}" y="{y1 + 44}"><tspan class="val-large">{current_streak}</tspan> <tspan class="val-unit">days</tspan></text>')
    svg.append(f'  <text x="{x1 + 10}" y="{y1 + 59}" class="sub-desc">{current_streak_range}</text>')
    svg.append('</g>')

    # Card 2: $ longest streak
    x2, y2 = margin_x + card_w + gap_x, margin_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.10s;">')
    svg.append(f'  <rect x="{x2}" y="{y2}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x2 + 10}" y="{y2 + 20}" class="label-text">$ longest streak</text>')
    svg.append(f'  <text x="{x2 + 10}" y="{y2 + 44}"><tspan class="val-white">{longest_streak}</tspan> <tspan class="val-unit">days</tspan></text>')
    svg.append(f'  <text x="{x2 + 10}" y="{y2 + 59}" class="sub-desc">{longest_streak_range}</text>')
    svg.append('</g>')

    # Card 3: $ contributions
    x3, y3 = margin_x, margin_y + card_h + gap_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.15s;">')
    svg.append(f'  <rect x="{x3}" y="{y3}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x3 + 10}" y="{y3 + 20}" class="label-text">$ contributions</text>')
    svg.append(f'  <text x="{x3 + 10}" y="{y3 + 44}" class="val-white">{total_contributions:,}</text>')
    svg.append(f'  <text x="{x3 + 10}" y="{y3 + 59}" class="sub-desc">in the last year</text>')
    svg.append('</g>')

    # Card 4: $ active days
    x4, y4 = margin_x + card_w + gap_x, margin_y + card_h + gap_y
    svg.append(f'<g class="animate-item" style="animation-delay: 0.20s;">')
    svg.append(f'  <rect x="{x4}" y="{y4}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x4 + 10}" y="{y4 + 20}" class="label-text">$ active days</text>')
    svg.append(f'  <text x="{x4 + 10}" y="{y4 + 44}"><tspan class="val-white">{active_days}</tspan> <tspan class="val-unit">/ {total_days}</tspan></text>')
    svg.append(f'  <text x="{x4 + 10}" y="{y4 + 59}" class="sub-desc">{active_pct}% of the year</text>')
    svg.append('</g>')

    # Card 5: $ best day
    x5, y5 = margin_x, margin_y + (card_h + gap_y) * 2
    svg.append(f'<g class="animate-item" style="animation-delay: 0.25s;">')
    svg.append(f'  <rect x="{x5}" y="{y5}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x5 + 10}" y="{y5 + 20}" class="label-text">$ best day</text>')
    svg.append(f'  <text x="{x5 + 10}" y="{y5 + 44}" class="val-white">{best_day_count}</text>')
    svg.append(f'  <text x="{x5 + 10}" y="{y5 + 59}" class="sub-desc">{best_day_date}</text>')
    svg.append('</g>')

    # Card 6: $ avg / active day
    x6, y6 = margin_x + card_w + gap_x, margin_y + (card_h + gap_y) * 2
    svg.append(f'<g class="animate-item" style="animation-delay: 0.30s;">')
    svg.append(f'  <rect x="{x6}" y="{y6}" width="{card_w}" height="{card_h}" class="sub-card" />')
    svg.append(f'  <text x="{x6 + 10}" y="{y6 + 20}" class="label-text">$ avg / active day</text>')
    svg.append(f'  <text x="{x6 + 10}" y="{y6 + 44}" class="val-white">{avg_per_active_day}</text>')
    svg.append(f'  <text x="{x6 + 10}" y="{y6 + 59}" class="sub-desc">contributions</text>')
    svg.append('</g>')

    # Card 7: Bottom Monthly Bar Chart
    x7, y7 = margin_x, margin_y + (card_h + gap_y) * 3
    chart_w = win2_w - 32
    chart_h = 180
    
    svg.append(f'<g class="animate-item" style="animation-delay: 0.35s;">')
    svg.append(f'  <rect x="{x7}" y="{y7}" width="{chart_w}" height="{chart_h}" class="sub-card" />')
    svg.append(f'  <text x="{x7 + 12}" y="{y7 + 22}" class="label-text">$ contributions / month</text>')

    bar_area_y = y7 + 40
    max_bar_height = 102
    num_bars = len(monthly_data)
    max_val = max(item["count"] for item in monthly_data) if monthly_data else 1
    max_val = max(1, max_val)

    bar_width = 16
    spacing = (chart_w - 24 - (num_bars * bar_width)) / max(1, num_bars - 1)

    for idx, item in enumerate(monthly_data):
        cnt = item["count"]
        b_h = int((cnt / max_val) * max_bar_height)
        b_h = max(6, b_h)
        
        bx = x7 + 12 + idx * (bar_width + spacing)
        by = bar_area_y + (max_bar_height - b_h)

        is_peak = (cnt == max_val)
        fill_color = "#ff8f00" if is_peak else "#ea580c"

        svg.append(f'  <rect x="{bx}" y="{by}" width="{bar_width}" height="{b_h}" rx="3" fill="{fill_color}" opacity="0.9" />')
        
        label_x = bx + (bar_width / 2) - 3
        label_y = bar_area_y + max_bar_height + 16
        svg.append(f'  <text x="{label_x}" y="{label_y}" class="bar-label">{item["label"]}</text>')

        if is_peak and cnt > 0:
            peak_x = bx + (bar_width / 2) - 12
            peak_y = by - 6
            svg.append(f'  <text x="{peak_x}" y="{peak_y}" class="peak-label">{cnt:,}</text>')

    svg.append('</g>')

    svg.append('</svg>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print(f"Generated Combined Whoami Suite SVG: {output_file}")

if __name__ == "__main__":
    create_whoami_suite_svg()
