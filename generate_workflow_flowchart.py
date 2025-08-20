#!/usr/bin/env python3
"""
Generate a comprehensive workflow flowchart for the Automatic Pentesting Framework
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.lines as mlines

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(20, 24))
ax.set_xlim(0, 10)
ax.set_ylim(0, 30)
ax.axis('off')

# Define colors for different phases
colors = {
    'start': '#2E7D32',      # Dark Green
    'input': '#1976D2',      # Blue
    'recon': '#7B1FA2',      # Purple
    'classify': '#C62828',   # Red
    'scan': '#F57C00',       # Orange
    'exploit': '#D32F2F',    # Dark Red
    'payload': '#5D4037',    # Brown
    'report': '#00796B',     # Teal
    'decision': '#FBC02D',   # Yellow/Gold
    'process': '#455A64',    # Blue Grey
    'ai': '#9C27B0',         # Deep Purple
    'end': '#388E3C'         # Green
}

def draw_box(ax, x, y, width, height, text, color, text_color='white', fontsize=10, style='round'):
    """Draw a box with text"""
    if style == 'round':
        box = FancyBboxPatch((x, y), width, height,
                            boxstyle="round,pad=0.05",
                            facecolor=color,
                            edgecolor='black',
                            linewidth=2)
    elif style == 'diamond':
        # Create diamond shape for decision nodes
        points = [(x + width/2, y),  # bottom
                 (x + width, y + height/2),  # right
                 (x + width/2, y + height),  # top
                 (x, y + height/2)]  # left
        box = mpatches.Polygon(points, closed=True, 
                              facecolor=color,
                              edgecolor='black',
                              linewidth=2)
    else:
        box = Rectangle((x, y), width, height,
                       facecolor=color,
                       edgecolor='black',
                       linewidth=2)
    
    ax.add_patch(box)
    
    # Add text
    ax.text(x + width/2, y + height/2, text,
           horizontalalignment='center',
           verticalalignment='center',
           fontsize=fontsize,
           color=text_color,
           weight='bold',
           wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='black', style='->'):
    """Draw an arrow between two points"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle=style,
                           color=color,
                           linewidth=2,
                           mutation_scale=20)
    ax.add_patch(arrow)
    
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(mid_x, mid_y, label,
               fontsize=8,
               color=color,
               weight='bold',
               ha='center',
               bbox=dict(boxstyle="round,pad=0.3", 
                        facecolor='white', 
                        edgecolor='none',
                        alpha=0.8))

# Title
ax.text(5, 29, 'Automatic Pentesting Framework Workflow', 
       fontsize=20, weight='bold', ha='center')
ax.text(5, 28.3, 'Complete Process Flow from Initialization to Reporting', 
       fontsize=12, ha='center', style='italic')

# Start Node
draw_box(ax, 4.25, 27, 1.5, 0.8, 'START', colors['start'])

# User Input & CLI
draw_box(ax, 3.5, 25.5, 3, 0.8, 'User Input\n(Target, Options, Mode)', colors['input'])
draw_arrow(ax, 5, 27, 5, 26.3)

# Configuration Check
draw_box(ax, 3.5, 24.2, 3, 0.8, 'Configuration Check\n(API Keys, Tools, Paths)', colors['process'])
draw_arrow(ax, 5, 25.5, 5, 25)

# Mode Selection Diamond
draw_box(ax, 3.75, 22.5, 2.5, 1.2, 'Mode\nSelection?', colors['decision'], style='diamond')
draw_arrow(ax, 5, 24.2, 5, 23.7)

# Three main branches
# 1. Manual Mode (Left)
draw_arrow(ax, 3.75, 23.1, 2, 22, 'Manual', 'black')
draw_box(ax, 0.5, 21, 3, 0.8, 'Traditional CLI\nPentesting', colors['process'])

# 2. Chatbot Mode (Middle)
draw_arrow(ax, 5, 22.5, 5, 21.8, 'Chatbot', 'black')
draw_box(ax, 3.5, 21, 3, 0.8, 'PentestGPT\nNatural Language', colors['ai'])

# 3. Autonomous Mode (Right)
draw_arrow(ax, 6.25, 23.1, 8, 22, 'Autonomous', 'black')
draw_box(ax, 6.5, 21, 3, 0.8, 'AI-Driven\nAutonomous Testing', colors['ai'])

# Merge point for all modes
draw_arrow(ax, 2, 21, 2, 19.8)
draw_arrow(ax, 5, 21, 5, 19.8)
draw_arrow(ax, 8, 21, 8, 19.8)

# Phase 1: Reconnaissance
ax.text(0.5, 19.3, 'PHASE 1: RECONNAISSANCE', fontsize=12, weight='bold', color=colors['recon'])
draw_box(ax, 3.5, 18.2, 3, 0.8, 'Target Classification\n(Web, Network, Mixed)', colors['classify'])
draw_arrow(ax, 5, 19.5, 5, 19)

# Reconnaissance Activities (Parallel)
recon_y = 16.8
draw_box(ax, 0.5, recon_y, 2, 0.7, 'DNS Enumeration\n(Amass, DNS)', colors['recon'], fontsize=9)
draw_box(ax, 2.7, recon_y, 2, 0.7, 'Port Scanning\n(Nmap, SYN)', colors['recon'], fontsize=9)
draw_box(ax, 4.9, recon_y, 2, 0.7, 'OSINT Gathering\n(theHarvester)', colors['recon'], fontsize=9)
draw_box(ax, 7.1, recon_y, 2, 0.7, 'Shodan Search\n(Passive Recon)', colors['recon'], fontsize=9)

# Arrows from classification to recon activities
draw_arrow(ax, 4.2, 18.2, 1.5, 17.5, '', 'gray', '->')
draw_arrow(ax, 4.7, 18.2, 3.7, 17.5, '', 'gray', '->')
draw_arrow(ax, 5.3, 18.2, 5.9, 17.5, '', 'gray', '->')
draw_arrow(ax, 5.8, 18.2, 8.1, 17.5, '', 'gray', '->')

# Service Analysis
draw_box(ax, 3.5, 15.2, 3, 0.8, 'Service Analysis\n(Identify Running Services)', colors['process'])
draw_arrow(ax, 1.5, 16.8, 4, 16)
draw_arrow(ax, 3.7, 16.8, 4.5, 16)
draw_arrow(ax, 5.9, 16.8, 5.5, 16)
draw_arrow(ax, 8.1, 16.8, 6, 16)

# Phase 2: Vulnerability Scanning
ax.text(0.5, 14.3, 'PHASE 2: VULNERABILITY SCANNING', fontsize=12, weight='bold', color=colors['scan'])
draw_arrow(ax, 5, 15.2, 5, 14.5)

# Vulnerability Scanning Tools (Parallel)
vuln_y = 13
draw_box(ax, 0.3, vuln_y, 1.8, 0.7, 'Nuclei\n(Templates)', colors['scan'], fontsize=9)
draw_box(ax, 2.3, vuln_y, 1.8, 0.7, 'Nikto\n(Web Server)', colors['scan'], fontsize=9)
draw_box(ax, 4.3, vuln_y, 1.8, 0.7, 'SQLMap\n(SQL Injection)', colors['scan'], fontsize=9)
draw_box(ax, 6.3, vuln_y, 1.8, 0.7, 'Custom Checks\n(Scripts)', colors['scan'], fontsize=9)
draw_box(ax, 8.3, vuln_y, 1.6, 0.7, 'API Testing\n(REST/GraphQL)', colors['scan'], fontsize=9)

# Arrows to scanning tools
draw_arrow(ax, 3.8, 14.2, 1.2, 13.7, '', 'gray', '->')
draw_arrow(ax, 4.3, 14.2, 3.2, 13.7, '', 'gray', '->')
draw_arrow(ax, 5, 14.2, 5.2, 13.7, '', 'gray', '->')
draw_arrow(ax, 5.7, 14.2, 7.2, 13.7, '', 'gray', '->')
draw_arrow(ax, 6.2, 14.2, 9.1, 13.7, '', 'gray', '->')

# Vulnerability Prioritization
draw_box(ax, 3.5, 11.5, 3, 0.8, 'Exploit Prioritization\n(CVSS, Impact Analysis)', colors['process'])
draw_arrow(ax, 1.2, 13, 4, 12.3)
draw_arrow(ax, 3.2, 13, 4.5, 12.3)
draw_arrow(ax, 5.2, 13, 5, 12.3)
draw_arrow(ax, 7.2, 13, 5.5, 12.3)
draw_arrow(ax, 9.1, 13, 6, 12.3)

# Decision: Exploitable vulnerabilities found?
draw_box(ax, 3.75, 10, 2.5, 1, 'Exploitable\nVulns Found?', colors['decision'], style='diamond')
draw_arrow(ax, 5, 11.5, 5, 11)

# Phase 3: Exploitation (if vulnerabilities found)
ax.text(0.5, 9, 'PHASE 3: EXPLOITATION & PAYLOAD GENERATION', fontsize=12, weight='bold', color=colors['exploit'])
draw_arrow(ax, 6.25, 10.5, 7.5, 10.5, 'Yes', 'black')

# Exploitation Branch
draw_box(ax, 7, 9.8, 2.5, 0.8, 'Payload Generation\n(Metasploit, Custom)', colors['payload'])
draw_arrow(ax, 8.25, 9.8, 8.25, 9)

# Payload Types
pay_y = 8.2
draw_box(ax, 6, pay_y, 1.5, 0.6, 'Reverse\nShells', colors['payload'], fontsize=8)
draw_box(ax, 7.7, pay_y, 1.5, 0.6, 'Web\nShells', colors['payload'], fontsize=8)
draw_box(ax, 9.4, pay_y, 0.5, 0.6, '...', colors['payload'], fontsize=8)

draw_arrow(ax, 7.5, 9, 6.75, 8.8, '', 'gray', '->')
draw_arrow(ax, 8.25, 9, 8.45, 8.8, '', 'gray', '->')
draw_arrow(ax, 9, 9, 9.65, 8.8, '', 'gray', '->')

# Exploitation Attempt
draw_box(ax, 7, 7, 2.5, 0.8, 'Exploitation Attempt\n(Safe Mode)', colors['exploit'])
draw_arrow(ax, 6.75, 8.2, 7.5, 7.8)
draw_arrow(ax, 8.45, 8.2, 8.25, 7.8)
draw_arrow(ax, 9.65, 8.2, 8.75, 7.8)

# Post-Exploitation
draw_box(ax, 7, 5.8, 2.5, 0.8, 'Post-Exploitation\n(Evidence Collection)', colors['process'])
draw_arrow(ax, 8.25, 7, 8.25, 6.6)

# No vulnerabilities branch
draw_arrow(ax, 3.75, 10.5, 2, 10.5, 'No', 'black')
draw_box(ax, 0.5, 10, 3, 0.8, 'Document Findings\n(No Critical Vulns)', colors['process'])

# Merge exploitation paths
draw_arrow(ax, 2, 10, 2, 5.5)
draw_arrow(ax, 8.25, 5.8, 8.25, 5.5)

# AI/ML Components (if enabled)
ax.text(0.5, 4.8, 'AI/ML ENHANCEMENT (Optional)', fontsize=12, weight='bold', color=colors['ai'])
draw_box(ax, 0.5, 3.8, 2, 0.7, 'Continuous\nLearning', colors['ai'], fontsize=9)
draw_box(ax, 2.7, 3.8, 2, 0.7, 'Self-Healing\nSystem', colors['ai'], fontsize=9)
draw_box(ax, 4.9, 3.8, 2, 0.7, 'Pattern\nRecognition', colors['ai'], fontsize=9)
draw_box(ax, 7.1, 3.8, 2, 0.7, 'Threat\nPrediction', colors['ai'], fontsize=9)

# Phase 4: Reporting
ax.text(0.5, 3, 'PHASE 4: REPORTING & DOCUMENTATION', fontsize=12, weight='bold', color=colors['report'])
draw_box(ax, 3.5, 2, 3, 0.8, 'Report Generation\n(HTML, MD, JSON, PDF)', colors['report'])
draw_arrow(ax, 2, 5.2, 3.5, 2.8)
draw_arrow(ax, 8.25, 5.2, 6.5, 2.8)

# Report Types
rep_y = 0.8
draw_box(ax, 0.5, rep_y, 1.8, 0.6, 'Executive\nSummary', colors['report'], fontsize=8)
draw_box(ax, 2.5, rep_y, 1.8, 0.6, 'Technical\nDetails', colors['report'], fontsize=8)
draw_box(ax, 4.5, rep_y, 1.8, 0.6, 'Remediation\nSteps', colors['report'], fontsize=8)
draw_box(ax, 6.5, rep_y, 1.8, 0.6, 'Risk\nAssessment', colors['report'], fontsize=8)
draw_box(ax, 8.5, rep_y, 1.3, 0.6, 'Evidence\nFiles', colors['report'], fontsize=8)

draw_arrow(ax, 3.8, 2, 1.4, 1.4, '', 'gray', '->')
draw_arrow(ax, 4.4, 2, 3.4, 1.4, '', 'gray', '->')
draw_arrow(ax, 5, 2, 5.4, 1.4, '', 'gray', '->')
draw_arrow(ax, 5.6, 2, 7.4, 1.4, '', 'gray', '->')
draw_arrow(ax, 6.2, 2, 9.15, 1.4, '', 'gray', '->')

# End Node
draw_box(ax, 4.25, -0.5, 1.5, 0.8, 'END', colors['end'])
draw_arrow(ax, 5, 0.8, 5, 0.3)

# Add Legend
legend_x = 0.2
legend_y = 21
legend_elements = [
    ('Start/End', colors['start']),
    ('User Input', colors['input']),
    ('Decision', colors['decision']),
    ('Reconnaissance', colors['recon']),
    ('Scanning', colors['scan']),
    ('Exploitation', colors['exploit']),
    ('AI/ML', colors['ai']),
    ('Reporting', colors['report']),
    ('Process', colors['process'])
]

ax.text(legend_x, legend_y + 1.5, 'Legend:', fontsize=10, weight='bold')
for i, (label, color) in enumerate(legend_elements):
    y_pos = legend_y - (i * 0.4)
    ax.add_patch(Rectangle((legend_x, y_pos), 0.3, 0.3, 
                          facecolor=color, edgecolor='black'))
    ax.text(legend_x + 0.4, y_pos + 0.15, label, fontsize=8, va='center')

# Add workflow notes
notes_x = 0.2
notes_y = 15
ax.text(notes_x, notes_y, 'Workflow Notes:', fontsize=10, weight='bold')
notes = [
    '• Autonomous mode uses AI for decision-making',
    '• All phases can be run independently',
    '• Self-healing recovers from errors',
    '• Continuous learning improves over time',
    '• Safe mode prevents destructive actions'
]
for i, note in enumerate(notes):
    ax.text(notes_x, notes_y - 0.4 - (i * 0.4), note, fontsize=8)

# Add title and save
plt.title('AutoPenTest Framework - Complete Workflow Diagram', fontsize=16, weight='bold', pad=20)
plt.tight_layout()

# Save the flowchart
output_file = 'workflow_flowchart.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"✅ Workflow flowchart saved as '{output_file}'")

# Also save as PDF for better quality
pdf_file = 'workflow_flowchart.pdf'
plt.savefig(pdf_file, format='pdf', bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"✅ Workflow flowchart also saved as '{pdf_file}'")

# Display the plot
plt.show()
