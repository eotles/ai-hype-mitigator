#!/usr/bin/env python3
"""Generate patent figures as PNG images for embedding in the PDF."""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

os.makedirs('docs/patent/figures', exist_ok=True)


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
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 9); ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    ax.text(4.5, 5.7, 'FIG. 1 — System Architecture (100)',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Boxes  (x, y, w, h, label, sublabel, color)
    boxes = [
        (4.5, 4.8, 3.2, 0.7, 'Social Media Platform Interface (110)', None, '#cce5ff'),
        (1.8, 3.2, 2.6, 0.7, 'AI Content Analyzer (120)', None, '#d4edda'),
        (4.5, 1.8, 2.2, 0.7, 'Challenge Generator (130)', None, '#fff3cd'),
        (4.5, 0.8, 1.6, 0.5, 'Problem Bank (131)', None, '#ffeeba'),
        (7.2, 3.2, 2.2, 0.7, 'Response Evaluator (140)', None, '#f8d7da'),
        (4.5, 3.2, 2.2, 0.7, 'Post Disposition\nModule (150)', None, '#e2d9f3'),
        (4.5, 4.0, 2.6, 0.55, 'User Interface Manager (160)', None, '#d1ecf1'),
    ]
    for bx, by, bw, bh, bl, bsl, bc in boxes:
        draw_box(ax, bx, by, bw, bh, bl, bsl, bc)

    # Problem Bank is inside Challenge Generator – dashed border
    rect = plt.Rectangle((4.5 - 1.3, 0.55), 2.6, 1.8,
                          linewidth=1, edgecolor='#888', facecolor='none',
                          linestyle='--', zorder=2)
    ax.add_patch(rect)

    # Arrows
    arrow(ax, 4.5, 4.45, 1.8, 3.55, 'post text')         # SMPI -> ACA
    arrow(ax, 1.8, 2.85, 4.5, 2.15, 'trigger')            # ACA -> CG
    arrow(ax, 4.5, 1.45, 4.5, 0.95)                        # CG -> PB
    arrow(ax, 4.5, 1.05, 4.5, 1.45)                        # PB -> CG (return)
    arrow(ax, 5.6, 1.8, 4.5, 3.55, 'challenge')           # CG -> UIM  (right side out)
    arrow(ax, 5.6, 4.0, 7.2, 3.55, 'user response')       # UIM -> RE
    arrow(ax, 7.2, 2.85, 4.5, 3.55)  # wait, fix paths
    arrow(ax, 6.1, 3.2, 5.6, 3.2, 'correctness')          # RE -> PDM
    arrow(ax, 4.5, 2.85, 4.5, 2.15)                        # PDM -> CG? no
    arrow(ax, 3.4, 3.2, 1.8, 3.55)                         # PDM -> ACA score
    arrow(ax, 4.5, 3.48, 4.5, 3.73, 'publish/block')       # PDM -> UIM
    arrow(ax, 4.5, 4.28, 4.5, 4.45, 'result')             # UIM -> SMPI

    plt.tight_layout(pad=0.5)
    plt.savefig('docs/patent/figures/fig1.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig1.png')


# ── FIG. 2  Method Flowchart ─────────────────────────────────────────────────
def fig2():
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.set_xlim(0, 7); ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(3.5, 9.7, 'FIG. 2 — Method Flowchart',
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

    # Nodes (top→bottom)
    pill(3.5, 9.2, 'START')
    box(3.5, 8.3, 3.2, 0.65, 'Step 210: Receive social media post')
    box(3.5, 7.4, 3.2, 0.65, 'Step 220: Analyze text for AI content')
    diamond(3.5, 6.4, 3.0, 0.8, 'Step 230: AI score ≥ threshold?')
    # YES branch (left)
    box(1.5, 5.2, 2.4, 0.65, 'Step 240: Generate &\npresent challenge', '#fff3cd')
    box(1.5, 4.2, 2.4, 0.65, 'Step 250: Receive &\nevaluate response', '#fff3cd')
    diamond(1.5, 3.1, 2.4, 0.8, 'Correct?')
    box(0.8, 1.9, 2.0, 0.85, 'Step 260: Publish post\n+ Expert badge\n+ Success UI', '#d4edda')
    box(2.6, 1.7, 2.0, 1.1, 'Step 270: Prevent pub.\nSave as draft\n+ Failure UI\n+ Educ. resources', '#f8d7da')
    # NO branch (right)
    box(5.5, 5.2, 2.0, 0.65, 'Step 260a:\nPublish post\n(no challenge)', '#d4edda')

    pill(0.8, 0.6, 'END')
    pill(2.6, 0.6, 'END')
    pill(5.5, 0.6, 'END')

    # Arrows
    arrow(ax, 3.5, 9.0, 3.5, 8.65)
    arrow(ax, 3.5, 7.97, 3.5, 7.72)
    arrow(ax, 3.5, 7.07, 3.5, 6.8)
    # YES left
    arrow(ax, 2.0, 6.4, 1.5, 5.52)
    ax.text(1.6, 6.1, 'YES', fontsize=7.5, color='#444')
    arrow(ax, 1.5, 4.87, 1.5, 4.52)
    arrow(ax, 1.5, 3.87, 1.5, 3.5)
    # CORRECT
    arrow(ax, 0.9, 3.1, 0.8, 2.32)
    ax.text(0.35, 2.9, 'CORRECT', fontsize=7, color='#444')
    arrow(ax, 2.1, 3.1, 2.6, 2.25)
    ax.text(2.15, 2.7, 'INCORRECT', fontsize=7, color='#444')
    # END arrows
    arrow(ax, 0.8, 1.47, 0.8, 0.85)
    arrow(ax, 2.6, 1.15, 2.6, 0.85)
    # NO right
    arrow(ax, 5.0, 6.4, 5.5, 5.52)
    ax.text(5.0, 6.1, 'NO', fontsize=7.5, color='#444')
    arrow(ax, 5.5, 4.87, 5.5, 0.85)

    plt.tight_layout(pad=0.3)
    plt.savefig('docs/patent/figures/fig2.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig2.png')


# ── FIG. 3  Challenge Generator Subsystem ────────────────────────────────────
def fig3():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 8); ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(4.0, 4.75, 'FIG. 3 — Challenge Generator Subsystem (130)',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Outer dashed border for subsystem 130
    rect = plt.Rectangle((0.3, 0.3), 7.4, 4.1,
                          linewidth=1.5, edgecolor='#555', facecolor='#fffdf0',
                          linestyle='--', zorder=1)
    ax.add_patch(rect)
    ax.text(0.5, 4.25, 'Challenge Generator (130)',
            fontsize=8, color='#555', style='italic')

    draw_box(ax, 2.0, 3.4, 2.4, 0.7, 'Category Selector (132)', color='#d4edda')
    draw_box(ax, 2.0, 2.2, 2.4, 0.7, 'Difficulty Adjuster (133)', color='#cce5ff')
    draw_box(ax, 5.5, 2.8, 2.2, 1.4, 'Problem Bank (131)\n\n[linear algebra]\n[ML theory]\n[AI programming]',
             color='#ffeeba', fontsize=8)
    draw_box(ax, 2.0, 1.0, 2.4, 0.7, 'Problem Formatter (134)', color='#e2d9f3')

    # External I/O labels
    ax.text(0.1, 3.4, 'AI topics\n(from Analyzer)', ha='right', va='center', fontsize=7.5)
    ax.text(0.1, 2.2, 'Expertise\nprofile (opt.)', ha='right', va='center', fontsize=7.5)
    ax.text(7.95, 1.0, 'Formatted\nchallenge →\n(to UI Mgr)', ha='left', va='center', fontsize=7.5)

    # Arrows inside
    arrow(ax, 0.5, 3.4, 0.8, 3.4)       # input -> CatSel
    arrow(ax, 0.5, 2.2, 0.8, 2.2)       # input -> DiffAdj
    arrow(ax, 3.2, 3.4, 4.4, 3.0)       # CatSel -> ProbBank
    arrow(ax, 3.2, 2.2, 4.4, 2.6)       # DiffAdj -> ProbBank
    arrow(ax, 4.4, 2.8, 3.2, 1.2)       # ProbBank -> Formatter
    arrow(ax, 3.2, 1.0, 7.5, 1.0)       # Formatter -> output

    plt.tight_layout(pad=0.3)
    plt.savefig('docs/patent/figures/fig3.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig3.png')


# ── FIG. 4  User Interface State Diagram ─────────────────────────────────────
def fig4():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5.0, 5.75, 'FIG. 4 — User Interface State Diagram',
            ha='center', va='center', fontsize=11, fontweight='bold')

    states = [
        (1.1, 3.0, 1.6, 1.8, '(A)\nComposition\nState',
         'Text area\nCharacter counter\nPost button', '#cce5ff'),
        (3.2, 3.0, 1.6, 1.8, '(B)\nAnalysis\nState',
         'Post preview\nScan animation\nKeyword chips\nSpinner', '#d4edda'),
        (5.5, 3.0, 1.6, 1.8, '(C)\nChallenge\nState',
         'Amber banner\nKeyword tags\nProblem card\nSubmit/Alt buttons', '#fff3cd'),
        (7.8, 4.1, 1.6, 1.8, '(D)\nSuccess\nState',
         'Green banner\nPublished post\nExpert badge\nExplanation box', '#d4edda'),
        (7.8, 1.9, 1.6, 1.8, '(E)\nFailure\nState',
         'Purple banner\nDraft saved\nAnswer reveal\nEduc. resources', '#f8d7da'),
    ]

    for sx, sy, sw, sh, sl, desc, sc in states:
        draw_box(ax, sx, sy, sw, sh, sl, color=sc, fontsize=8)
        ax.text(sx, sy - sh*0.25, desc, ha='center', va='top', fontsize=6.5,
                color='#333', zorder=5)

    # Transitions
    arrow(ax, 1.9, 3.0, 2.4, 3.0)   # A -> B  (user posts)
    ax.text(2.15, 3.08, 'Post', fontsize=7, ha='center')

    arrow(ax, 4.0, 3.0, 4.7, 3.0)   # B -> C  (AI detected)
    ax.text(4.35, 3.08, 'AI\ndetected', fontsize=7, ha='center')

    # B -> A  (no AI content, arc above)
    ax.annotate('', xy=(1.9, 3.3), xytext=(4.0, 3.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2,
                                connectionstyle='arc3,rad=-0.3'), zorder=5)
    ax.text(2.95, 4.0, 'No AI content\n(publish)', fontsize=7, ha='center', color='#555')

    arrow(ax, 6.3, 3.5, 6.95, 4.1)   # C -> D  (correct)
    ax.text(6.5, 3.9, 'Correct', fontsize=7, ha='center')

    arrow(ax, 6.3, 2.5, 6.95, 1.9)   # C -> E  (incorrect)
    ax.text(6.5, 2.1, 'Incorrect', fontsize=7, ha='center')

    # D -> A  (compose another)
    ax.annotate('', xy=(1.1, 3.9), xytext=(6.95, 4.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2,
                                connectionstyle='arc3,rad=0.15'), zorder=5)
    ax.text(4.0, 5.2, 'Compose Another', fontsize=7, ha='center', color='#555')

    # E -> C  (try again / different problem)
    ax.annotate('', xy=(6.3, 2.5), xytext=(6.95, 1.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2,
                                connectionstyle='arc3,rad=0.3'), zorder=5)
    ax.text(6.15, 1.7, 'Try Again', fontsize=7, ha='right', color='#555')

    plt.tight_layout(pad=0.3)
    plt.savefig('docs/patent/figures/fig4.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('Saved fig4.png')


if __name__ == '__main__':
    fig1()
    fig2()
    fig3()
    fig4()
    print('All figures saved to docs/patent/figures/')
