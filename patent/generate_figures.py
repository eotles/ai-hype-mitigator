#!/usr/bin/env python3
"""Generate patent figures as PNG images for embedding in the PDF."""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

os.makedirs('figures', exist_ok=True)


def draw_box(ax, x, y, w, h, label, sublabel=None, color='#ddeeff', fontsize=9):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.02", linewidth=1.2,
                         edgecolor='#333', facecolor=color, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x, y + h*0.12, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', zorder=4)
        ax.text(x, y - h*0.2, sublabel, ha='center', va='center',
                fontsize=fontsize - 1, style='italic', zorder=4)
    else:
        ax.text(x, y, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', zorder=4)


def arrow(ax, x1, y1, x2, y2, label=None):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5), zorder=5)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.03, my, label, fontsize=7.5, color='#444', zorder=6)


# ── FIG. 1  System Architecture ─────────────────────────────────────────────
def fig1():
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.set_xlim(0, 11); ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    ax.text(5.5, 8.7, 'FIG. 1 — System Architecture (100)',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Component positions chosen so arrows don't need to cross any box.
    # Layout (top→bottom):
    #   Row 1: SMPI (top centre)
    #   Row 2: UIM (centre)
    #   Row 3: ACA (left)  |  PDM (centre)  |  RE (right)
    #   Row 4: CG + PB (centre, in dashed subsystem border)
    boxes = [
        (5.5, 8.05, 3.6, 0.70, 'Social Media Platform Interface (110)', None, '#cce5ff'),
        (5.5, 6.85, 2.8, 0.65, 'User Interface Manager (160)',          None, '#d1ecf1'),
        (1.8, 5.10, 2.8, 0.70, 'AI Content Analyzer (120)',             None, '#d4edda'),
        (5.5, 5.10, 2.8, 0.70, 'Post Disposition\nModule (150)',         None, '#e2d9f3'),
        (9.2, 5.10, 2.4, 0.70, 'Response Evaluator (140)',              None, '#f8d7da'),
        (5.5, 3.00, 2.6, 0.70, 'Challenge Generator (130)',             None, '#fff3cd'),
        (5.5, 1.70, 1.8, 0.55, 'Problem Bank (131)',                    None, '#ffeeba'),
    ]
    for bx, by, bw, bh, bl, bsl, bc in boxes:
        draw_box(ax, bx, by, bw, bh, bl, bsl, bc)

    # Box edges for reference:
    #   SMPI: x[3.70,7.30] y[7.70,8.40]
    #   UIM:  x[4.10,6.90] y[6.525,7.175]
    #   ACA:  x[0.40,3.20] y[4.75,5.45]
    #   PDM:  x[4.10,6.90] y[4.75,5.45]
    #   RE:   x[8.00,10.40] y[4.75,5.45]
    #   CG:   x[4.20,6.80] y[2.65,3.35]
    #   PB:   x[4.60,6.40] y[1.425,1.975]

    # Dashed subsystem border around CG + PB
    rect = plt.Rectangle((3.9, 1.30), 3.2, 2.35,
                          linewidth=1.2, edgecolor='#888', facecolor='none',
                          linestyle='--', zorder=2)
    ax.add_patch(rect)

    # ── Arrows ──

    # SMPI ↔ UIM  (short vertical pair, offset left/right of centre)
    arrow(ax, 5.3, 7.70, 5.3, 7.175)
    ax.text(4.85, 7.43, 'post', fontsize=7.5, color='#444')
    arrow(ax, 5.7, 7.175, 5.7, 7.70)
    ax.text(5.75, 7.43, 'result', fontsize=7.5, color='#444')

    # UIM → ACA  (left-side of UIM diagonally down-left to ACA top)
    # x=4.10 is the left edge of UIM; ACA top-right is (3.20, 5.45)
    arrow(ax, 4.10, 6.525, 3.20, 5.45)
    ax.text(3.30, 6.10, 'post\ntext', fontsize=7.5, color='#444')

    # ACA → PDM  (AI score, horizontal right, same y level)
    arrow(ax, 3.20, 5.10, 4.10, 5.10)
    ax.text(3.55, 5.22, 'AI score', fontsize=7.5, color='#444')

    # ACA → CG  (trigger)
    # From ACA bottom (1.8, 4.75) to CG left edge (4.20, 3.00).
    # Straight line stays below PDM y-range [4.75, 5.45] for all x > 3.20. Safe.
    arrow(ax, 1.80, 4.75, 4.20, 3.00)
    ax.text(2.55, 3.75, 'trigger', fontsize=7.5, color='#444')

    # CG ↔ PB  (internal, vertical pair)
    arrow(ax, 5.30, 2.65, 5.30, 1.975)
    arrow(ax, 5.70, 1.975, 5.70, 2.65)

    # CG → UIM  (challenge)
    # Route LEFT of PDM: vertical segment at x=3.60, well clear of PDM (left edge 4.10)
    # Segment: CG left-top corner → left waypoint → UIM bottom-left corner
    ax.plot([4.20, 3.60, 3.60, 4.10], [3.35, 3.35, 6.525, 6.525],
            '-', color='#333', lw=1.5, zorder=5)
    ax.annotate('', xy=(4.10, 6.525), xytext=(3.60, 6.525),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5), zorder=5)
    ax.text(3.00, 4.90, 'challenge', fontsize=7.5, color='#444',
            ha='center', va='center', rotation=90)

    # UIM → RE  (user response, right diagonal)
    arrow(ax, 6.90, 6.85, 8.00, 5.45)
    ax.text(7.75, 6.30, 'user\nresponse', fontsize=7.5, color='#444')

    # RE → PDM  (correctness, horizontal left)
    arrow(ax, 8.00, 5.10, 6.90, 5.10)
    ax.text(7.30, 5.22, 'correctness', fontsize=7.5, color='#444')

    # PDM → UIM  (publish/block, vertical up)
    arrow(ax, 5.50, 5.45, 5.50, 6.525)
    ax.text(5.60, 5.95, 'publish/\nblock', fontsize=7.5, color='#444')

    plt.tight_layout(pad=0.5)
    plt.savefig('figures/fig1.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig1.png')


# ── FIG. 2  Method Flowchart ─────────────────────────────────────────────────
def fig2():
    fig, ax = plt.subplots(figsize=(8, 13))
    ax.set_xlim(0, 8); ax.set_ylim(0, 13)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(4.0, 12.7, 'FIG. 2 — Method Flowchart',
            ha='center', va='center', fontsize=11, fontweight='bold')

    def box(x, y, w, h, txt, color='#ddeeff'):
        draw_box(ax, x, y, w, h, txt, color=color, fontsize=8.5)

    def diamond(x, y, w, h, txt):
        pts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
        poly = plt.Polygon(pts, closed=True, facecolor='#fff3cd',
                           edgecolor='#333', linewidth=1.2, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, txt, ha='center', va='center', fontsize=8.5,
                fontweight='bold', zorder=4)

    def pill(x, y, txt, color='#e8f5e9'):
        ellipse = mpatches.Ellipse((x, y), 1.4, 0.5, facecolor=color,
                                   edgecolor='#333', linewidth=1.2, zorder=3)
        ax.add_patch(ellipse)
        ax.text(x, y, txt, ha='center', va='center', fontsize=8.5,
                fontweight='bold', zorder=4)

    # ── Nodes (top→bottom, with extra vertical room in the lower half) ──
    pill(4.0, 12.2, 'START')
    box(4.0, 11.2, 3.4, 0.70, 'Step 210: Receive social media post')
    box(4.0, 10.2, 3.4, 0.70, 'Step 220: Analyze text for AI content')
    diamond(4.0, 9.1, 3.2, 0.90, 'Step 230: AI score ≥ threshold?')

    # YES branch (left column x=2.0)
    box(2.0, 7.8, 2.6, 0.70, 'Step 240: Generate &\npresent challenge', '#fff3cd')
    box(2.0, 6.6, 2.6, 0.70, 'Step 250: Receive &\nevaluate response', '#fff3cd')
    diamond(2.0, 5.4, 2.6, 0.90, 'Correct?')

    # Extra vertical space here so 260/270 don't crowd the diamond
    box(1.0, 3.7, 2.2, 1.00, 'Step 260: Publish post\n+ Expert badge\n+ Success UI', '#d4edda')
    box(3.2, 3.6, 2.2, 1.20, 'Step 270: Prevent pub.\nSave as draft\n+ Failure UI\n+ Educ. resources', '#f8d7da')

    # NO branch (right column x=6.2)
    box(6.2, 7.8, 2.2, 0.90, 'Step 260a:\nPublish post\n(no challenge)', '#d4edda')

    pill(1.0, 1.8, 'END')
    pill(3.2, 1.8, 'END')
    pill(6.2, 1.8, 'END')

    # ── Arrows ──
    arrow(ax, 4.0, 11.95, 4.0, 11.55)
    arrow(ax, 4.0, 10.85, 4.0, 10.55)
    arrow(ax, 4.0, 9.85, 4.0, 9.55)

    # YES left
    arrow(ax, 2.4, 9.1, 2.0, 8.15)
    ax.text(1.85, 8.75, 'YES', fontsize=7.5, color='#444')
    arrow(ax, 2.0, 7.45, 2.0, 6.95)
    arrow(ax, 2.0, 6.25, 2.0, 5.85)

    # CORRECT / INCORRECT from diamond
    arrow(ax, 1.2, 5.4, 1.0, 4.20)
    ax.text(0.30, 5.0, 'CORRECT', fontsize=7, color='#444')
    arrow(ax, 2.8, 5.4, 3.2, 4.20)
    ax.text(3.05, 4.95, 'INCORRECT', fontsize=7, color='#444')

    # END arrows
    arrow(ax, 1.0, 3.20, 1.0, 2.05)
    arrow(ax, 3.2, 3.00, 3.2, 2.05)

    # NO right
    arrow(ax, 5.6, 9.1, 6.2, 8.25)
    ax.text(5.85, 8.85, 'NO', fontsize=7.5, color='#444')
    arrow(ax, 6.2, 7.35, 6.2, 2.05)

    plt.tight_layout(pad=0.3)
    plt.savefig('figures/fig2.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig2.png')


# ── FIG. 3  Challenge Generator Subsystem ────────────────────────────────────
def fig3():
    # Layout: inputs (left) → selectors → Problem Bank (centre) → Formatter (right) → output
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5.0, 4.75, 'FIG. 3 — Challenge Generator Subsystem (130)',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Outer dashed border for subsystem 130
    rect = plt.Rectangle((0.3, 0.3), 9.4, 4.1,
                          linewidth=1.5, edgecolor='#555', facecolor='#fffdf0',
                          linestyle='--', zorder=1)
    ax.add_patch(rect)
    ax.text(0.5, 4.25, 'Challenge Generator (130)',
            fontsize=8, color='#555', style='italic')

    # Column positions:
    #   x=2.0  Category Selector & Difficulty Adjuster  (left)
    #   x=5.0  Problem Bank                              (centre)
    #   x=8.0  Problem Formatter                         (right)
    draw_box(ax, 2.0, 3.4, 2.4, 0.70, 'Category Selector (132)',  color='#d4edda')
    draw_box(ax, 2.0, 2.1, 2.4, 0.70, 'Difficulty Adjuster (133)', color='#cce5ff')
    draw_box(ax, 5.0, 2.75, 2.4, 1.50,
             'Problem Bank (131)\n\n[linear algebra]\n[ML theory]\n[AI programming]',
             color='#ffeeba', fontsize=8)
    draw_box(ax, 8.0, 2.75, 2.0, 0.80, 'Problem\nFormatter (134)', color='#e2d9f3')

    # External I/O labels (outside dashed border)
    ax.text(0.20, 3.4, 'AI topics\n(from Analyzer)', ha='right', va='center', fontsize=7.5)
    ax.text(0.20, 2.1, 'Expertise\nprofile (opt.)', ha='right', va='center', fontsize=7.5)
    ax.text(9.85, 2.75, 'Formatted\nchallenge →\n(to UI Mgr)', ha='left', va='center', fontsize=7.5)

    # Arrows
    arrow(ax, 0.40, 3.4, 0.80, 3.4)      # input → CatSel
    arrow(ax, 0.40, 2.1, 0.80, 2.1)      # input → DiffAdj
    arrow(ax, 3.20, 3.4, 3.80, 3.10)     # CatSel  → ProbBank top
    arrow(ax, 3.20, 2.1, 3.80, 2.50)     # DiffAdj → ProbBank bottom
    arrow(ax, 6.20, 2.75, 7.00, 2.75)    # ProbBank → Formatter
    arrow(ax, 9.00, 2.75, 9.60, 2.75)    # Formatter → output

    plt.tight_layout(pad=0.3)
    plt.savefig('figures/fig3.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig3.png')


# ── FIG. 4  User Interface State Diagram ─────────────────────────────────────
def fig4():
    # Wider/taller canvas gives arrows room to route around boxes.
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(6.5, 7.75, 'FIG. 4 — User Interface State Diagram',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # States arranged left→right with D/E offset vertically so loop-backs have room
    states = [
        (1.2,  4.0, 1.8, 2.0, '(A)\nComposition\nState',
         'Text area\nCharacter counter\nPost button', '#cce5ff'),
        (3.6,  4.0, 1.8, 2.0, '(B)\nAnalysis\nState',
         'Post preview\nScan animation\nKeyword chips\nSpinner', '#d4edda'),
        (6.0,  4.0, 1.8, 2.0, '(C)\nChallenge\nState',
         'Amber banner\nKeyword tags\nProblem card\nSubmit/Alt buttons', '#fff3cd'),
        (9.2,  5.5, 1.8, 2.0, '(D)\nSuccess\nState',
         'Green banner\nPublished post\nExpert badge\nExplanation box', '#d4edda'),
        (9.2,  2.5, 1.8, 2.0, '(E)\nFailure\nState',
         'Purple banner\nDraft saved\nAnswer reveal\nEduc. resources', '#f8d7da'),
    ]

    for sx, sy, sw, sh, sl, desc, sc in states:
        draw_box(ax, sx, sy, sw, sh, sl, color=sc, fontsize=8)
        ax.text(sx, sy - sh*0.28, desc, ha='center', va='top', fontsize=6.5,
                color='#333', zorder=5)

    # Box edges:
    #  A: x[0.30,2.10] y[3.0,5.0]
    #  B: x[2.70,4.50] y[3.0,5.0]
    #  C: x[5.10,6.90] y[3.0,5.0]
    #  D: x[8.30,10.10] y[4.5,6.5]
    #  E: x[8.30,10.10] y[1.5,3.5]

    # A → B  (Post)
    arrow(ax, 2.10, 4.0, 2.70, 4.0)
    ax.text(2.40, 4.15, 'Post', fontsize=7.5, ha='center')

    # B → C  (AI detected)
    arrow(ax, 4.50, 4.0, 5.10, 4.0)
    ax.text(4.80, 4.15, 'AI\ndetected', fontsize=7.5, ha='center')

    # B → A  (No AI content – arc below the row so it clears the boxes)
    ax.annotate('', xy=(2.10, 3.5), xytext=(4.50, 3.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2,
                                connectionstyle='arc3,rad=0.35'), zorder=5)
    ax.text(3.30, 2.10, 'No AI content\n(publish)', fontsize=7.5, ha='center', color='#555')

    # C → D  (Correct – diagonal up-right)
    arrow(ax, 6.90, 4.7, 8.30, 5.5)
    ax.text(7.50, 5.30, 'Correct', fontsize=7.5, ha='center')

    # C → E  (Incorrect – diagonal down-right)
    arrow(ax, 6.90, 3.3, 8.30, 2.5)
    ax.text(7.50, 2.70, 'Incorrect', fontsize=7.5, ha='center')

    # D → A  (Compose Another)
    # Route: over the top of all boxes via y=7.2 to avoid overlap
    ax.plot([9.20, 9.20, 1.20, 1.20], [6.50, 7.20, 7.20, 5.00],
            '-', color='#333', lw=1.2, zorder=5)
    ax.annotate('', xy=(1.20, 5.00), xytext=(1.20, 7.20),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2), zorder=5)
    ax.text(5.20, 7.45, 'Compose Another', fontsize=7.5, ha='center', color='#555')

    # E → C  (Try Again)
    # Route: below the boxes via y=0.8 to avoid overlap
    ax.plot([9.20, 9.20, 6.00, 6.00], [1.50, 0.80, 0.80, 3.00],
            '-', color='#333', lw=1.2, zorder=5)
    ax.annotate('', xy=(6.00, 3.00), xytext=(6.00, 0.80),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2), zorder=5)
    ax.text(7.60, 0.45, 'Try Again', fontsize=7.5, ha='center', color='#555')

    plt.tight_layout(pad=0.3)
    plt.savefig('figures/fig4.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig4.png')


if __name__ == '__main__':
    fig1()
    fig2()
    fig3()
    fig4()
    print('All figures saved to figures/')
