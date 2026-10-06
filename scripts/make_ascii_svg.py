import os
import sys
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

def create_ascii_svg(ascii_lines, output_file="avi-ascii.svg"):
    num_rows = len(ascii_lines)
    num_cols = max(len(l) for l in ascii_lines)
    
    width = 420
    height = 520
    
    font_size = 10.5
    line_height = 16.5
    
    padding_x = 22
    padding_y = 62
    
    total_duration = 5.5
    row_delay = total_duration / max(1, num_rows)
    row_duration = 0.45

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #21262d; stroke-width: 1px; }')
    svg.append('  .title-bar { fill: #161b22; }')
    svg.append('  .dot-red { fill: #ff5f56; } .dot-yellow { fill: #ffbd2e; } .dot-green { fill: #27c93f; }')
    svg.append('  .title-text { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 600; }')
    svg.append('  .ascii-text { fill: #d27d2d; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10.5px; font-weight: 600; white-space: pre; }')
    svg.append('  .cup-text-highlight { fill: #fbbf24; font-weight: 800; }')
    svg.append('  .prompt-text { fill: #7d8590; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; font-weight: 500; }')
    svg.append('  .user-text { fill: #ffffff; font-weight: bold; }')
    svg.append('</style>')

    # Clip paths for row-by-row SMIL animation (Slow & Eased)
    svg.append('<defs>')
    for i in range(num_rows):
        clip_id = f"art-clip-{i}"
        begin_time = f"{i * row_delay:.2f}s"
        svg.append(f'  <clipPath id="{clip_id}">')
        svg.append(f'    <rect x="{padding_x}" y="{padding_y + i * line_height - 4}" width="0" height="{line_height + 4}">')
        svg.append(f'      <animate attributeName="width" from="0" to="{width - padding_x}" dur="{row_duration:.2f}s" begin="{begin_time}" calcMode="spline" keySplines="0.25 0.1 0.25 1.0" fill="freeze" />')
        svg.append('    </rect>')
        svg.append('  </clipPath>')
    svg.append('</defs>')

    # Window background
    svg.append(f'<rect width="{width}" height="{height}" class="bg" />')
    
    # Title bar
    svg.append(f'<path d="M 0 8 A 8 8 0 0 1 8 0 L {width-8} 0 A 8 8 0 0 1 {width} 8 L {width} 36 L 0 36 Z" class="title-bar" />')
    svg.append('<circle cx="16" cy="18" r="5" class="dot-red" />')
    svg.append('<circle cx="32" cy="18" r="5" class="dot-yellow" />')
    svg.append('<circle cx="48" cy="18" r="5" class="dot-green" />')
    svg.append(f'<text x="65" y="22" class="title-text">yukesh@github: ~ $ ./portrait.sh</text>')

    # ASCII Content with staggered clip wipe animations
    for i, line in enumerate(ascii_lines):
        escaped_line = xml_escape.escape(line)
        # Highlight NOT, MY, CUP, OF, TEA
        for kw in ["NOT", "MY", "CUP", "OF", "TEA"]:
            if f" {kw} " in escaped_line:
                escaped_line = escaped_line.replace(f" {kw} ", f' <tspan class="cup-text-highlight">{kw}</tspan> ')
        
        y_pos = padding_y + (i + 1) * line_height - 4
        clip_id = f"art-clip-{i}"
        svg.append(f'<g clip-path="url(#{clip_id})">')
        svg.append(f'  <text x="{padding_x}" y="{y_pos}" class="ascii-text">{escaped_line}</text>')
        svg.append('</g>')

    # Bottom status bar inside window
    bottom_y = height - 16
    svg.append(f'<text x="20" y="{bottom_y}" class="prompt-text">yukesh@github:~$ whoami <tspan class="user-text">Yukesh D</tspan></text>')

    svg.append('</svg>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print(f"Generated ASCII SVG: {output_file}")

def main():
    lines = get_target_ascii_art()
    create_ascii_svg(lines, "avi-ascii.svg")

if __name__ == "__main__":
    main()
