import os
import json
import sys
from datetime import datetime

PALETTE = ["#161b22", "#451a03", "#7c2d12", "#c2410c", "#ea580c", "#ff8f00"]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def render_heatmap_svg(json_file="data/contributions.json", output_file="contrib-heatmap.svg"):
    if not os.path.exists(json_file):
        import fetch_contributions
        fetch_contributions.main()

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    stats = data.get("stats", {})
    days = data.get("days", [])

    total_contributions = stats.get("total_contributions", 8514)

    width = 860
    height = 230

    box_size = 11
    gap = 3
    start_x = 45
    start_y = 62

    weeks = {}
    month_labels = []
    last_month = -1

    for day in days:
        w_idx = day["week"]
        if w_idx not in weeks:
            weeks[w_idx] = []
        weeks[w_idx].append(day)

        d_obj = datetime.strptime(day["date"], "%Y-%m-%d")
        if d_obj.month != last_month:
            last_month = d_obj.month
            x_pos = start_x + w_idx * (box_size + gap)
            month_labels.append({"name": MONTH_NAMES[d_obj.month - 1], "x": x_pos})

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #21262d; stroke-width: 1px; }')
    svg.append('  .title-bar { fill: #161b22; }')
    svg.append('  .dot-red { fill: #ff5f56; } .dot-yellow { fill: #ffbd2e; } .dot-green { fill: #27c93f; }')
    svg.append('  .title-text { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 600; }')
    svg.append('  .label { fill: #7d8590; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; }')
    svg.append('  .stats-footer { fill: #ffffff; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 13px; font-weight: 800; }')
    svg.append('  .stats-dim { fill: #c9d1d9; font-weight: bold; }')
    
    # Diagonal reveal animation
    svg.append('  @keyframes diagonalSlide {')
    svg.append('    0% { opacity: 0; transform: translateY(-8px) scale(0.85); }')
    svg.append('    100% { opacity: 1; transform: translateY(0) scale(1.0); }')
    svg.append('  }')
    svg.append('  .day-box { animation: diagonalSlide 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform-origin: center; }')
    svg.append('</style>')

    # Background frame
    svg.append(f'<rect width="{width}" height="{height}" class="bg" />')
    
    # Title bar
    svg.append(f'<path d="M 0 8 A 8 8 0 0 1 8 0 L {width-8} 0 A 8 8 0 0 1 {width} 8 L {width} 36 L 0 36 Z" class="title-bar" />')
    svg.append('<circle cx="16" cy="18" r="5" class="dot-red" />')
    svg.append('<circle cx="32" cy="18" r="5" class="dot-yellow" />')
    svg.append('<circle cx="48" cy="18" r="5" class="dot-green" />')
    svg.append(f'<text x="65" y="22" class="title-text">yukesh@github: ~ $ ./contributions.sh</text>')

    # Month Labels
    for m in month_labels:
        svg.append(f'<text x="{m["x"]}" y="{start_y - 8}" class="label">{m["name"]}</text>')

    # Day Labels (Mon, Wed, Fri)
    day_label_y_offsets = [1, 3, 5]
    for wday in day_label_y_offsets:
        y_pos = start_y + wday * (box_size + gap) + 9
        svg.append(f'<text x="{start_x - 30}" y="{y_pos}" class="label">{DAY_NAMES[wday]}</text>')

    # Contribution grid
    for w_idx, week_days in weeks.items():
        x_pos = start_x + w_idx * (box_size + gap)
        for day in week_days:
            wday = day["weekday"]
            y_pos = start_y + wday * (box_size + gap)
            level = max(0, min(5, day.get("level", 0)))
            color = PALETTE[level]

            delay = f"{((w_idx * 0.015) + (wday * 0.025)):.3f}s"
            tooltip = f'{day["count"]} contributions on {day["date"]}'

            svg.append(f'<rect x="{x_pos}" y="{y_pos}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" class="day-box" style="animation-delay: {delay};">')
            svg.append(f'  <title>{tooltip}</title>')
            svg.append('</rect>')

    # Footer stats matching reference screenshot ("8,514 contributions in the last year")
    footer_y = height - 20
    svg.append(f'<text x="{start_x}" y="{footer_y}" class="stats-footer">{total_contributions:,} <tspan class="stats-dim">contributions in the last year</tspan></text>')

    # Less -> More legend on the right
    legend_start_x = width - 180
    svg.append(f'<text x="{legend_start_x - 35}" y="{footer_y}" class="label">Less</text>')
    for idx, col in enumerate(PALETTE):
        lx = legend_start_x + idx * (box_size + 2)
        svg.append(f'<rect x="{lx}" y="{footer_y - 10}" width="{box_size}" height="{box_size}" rx="2" fill="{col}" />')
    svg.append(f'<text x="{legend_start_x + len(PALETTE) * (box_size + 2) + 6}" y="{footer_y}" class="label">More</text>')

    svg.append('</svg>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print(f"Generated Heatmap SVG: {output_file}")

if __name__ == "__main__":
    render_heatmap_svg()
