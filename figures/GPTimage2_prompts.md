# Figure 2 & 3 — Image Generation Prompts for GPTimage2

## FIGURE 2: Stakeholder Information Interaction and Game Flow
======================================================================

Create a clean professional academic block diagram on a pure white background.
Style: flat corporate, light gray boxes, black text, no shadows, no gradients.
Aspect ratio: 16:9 landscape.

LAYOUT — Three columns, two rows of rounded rectangular blocks:

TOP ROW (left to right):
1. [DASHED BORDER BOX] "Exogenous API Supply" (bold title)
   subtitle in smaller gray text: "token capacity, API cost, reliability inputs"
   x=0.10, y=0.65, width=0.22, height=0.22

2. [SOLID BORDER BOX] "Stage 1: Platform" (bold title)
   subtitle: "wholesale price w_t; anticipates responses"
   x=0.38, y=0.65, width=0.22, height=0.22

3. [SOLID BORDER BOX] "Stage 2: API Brokers" (bold title)
   subtitle: "retail price p_jt; allocate capacity g_jt"
   x=0.66, y=0.65, width=0.22, height=0.22

BOTTOM ROW (left to right):
4. [DASHED BORDER BOX] "Objective Diagnostics" (bold title)
   subtitle: "platform / broker / system payoff; user value"
   x=0.10, y=0.22, width=0.22, height=0.22

5. [SOLID BORDER BOX] "QoS Monitor" (bold title)
   subtitle: "u_jt, q_jt; served demand D_jt·q_jt"
   x=0.38, y=0.22, width=0.22, height=0.22

6. [SOLID BORDER BOX] "Stage 3: Users" (bold title)
   subtitle: "broker × period choice; cross-period migration"
   x=0.66, y=0.22, width=0.22, height=0.22

ARROWS (solid dark gray lines with arrowheads):
- Box 1 right edge → Box 2 left edge (horizontal)
- Box 2 right edge → Box 3 left edge (horizontal)
- Box 3 bottom edge → Box 6 top edge (vertical down)
- Box 6 left edge → Box 5 right edge (horizontal)
- Box 5 left edge → Box 4 right edge (horizontal)

FEEDBACK ARROW (dashed gray line with arrowhead, curved):
- From Box 4 top edge, curving up and right, to Box 2 bottom edge

SECTION LABELS (small uppercase gray text, centered above each column):
- Above column 1 (x=0.21): "Exogenous Input"
- Above column 2 (x=0.49): "Upper Layer (Platform)"  
- Above column 3 (x=0.77): "Middle Layer (Brokers)"
- Label at right of bottom row: "Lower Layer (Users)"
- Label near Boxes 4-5: "QoS & Diagnostics"

TEXT on feedback arrow: "feedback loop" in small italic gray

COLORS:
- Background: pure white #FFF
- Box fill: very light gray #F5F5F8
- Box borders: medium gray #6B6B6B
- Dashed box borders: lighter gray #999999
- Title text: black #000000 bold 12pt
- Subtitle text: dark gray #555555 9pt
- Arrows: dark gray #555555, arrowheads, 1.5pt
- Feedback arrow: gray #888888, dashed, 1.2pt
- Section labels: medium gray #777777, 8pt, uppercase

FONT: clean sans-serif (Helvetica/Arial style)
======================================================================


## FIGURE 3: API Market Topology with Direct Channel Outside Option
======================================================================

Create a clean professional academic block diagram on a pure white background.
Style: flat corporate, light gray boxes, black text, no shadows, no gradients.
Aspect ratio: 4:3.

LAYOUT — Top-down hierarchical flow with branching:

TOP:
1. [DASHED BORDER BOX, wider] "Exogenous Model API Supply"
   subtitle: "DeepSeek / Claude / GPT / Gemini, Qwen and other API inputs"
   Centered at top, full width (x=0.15-0.85, y=0.78-0.95)

UPPER-MIDDLE:
2. [SOLID BORDER BOX] "Platform Wholesale Layer"
   subtitle: "sets wholesale price w_t; observes settlement and QoS"
   Centered below supply (x=0.28-0.72, y=0.55-0.72)

MIDDLE ROW — Two boxes side by side:
3. [SOLID BORDER BOX, left] "Brokered Retail APIs"
   subtitle (3 lines): "Broker 1: p_1t, g_1t | Broker 2: p_2t, g_2t | Broker 3: p_3t, g_3t"
   Sub-label: "OpenRouter-like aggregator model"
   x=0.08-0.42, y=0.25-0.48

4. [SOLID BORDER BOX, right] "Direct API Channel (j = 0)"
   subtitle: "outside option: p^D_t, g^D_t"
   Sub-label: "platform self-operated, SLA-guaranteed reserve capacity"
   x=0.58-0.92, y=0.25-0.48

BOTTOM:
5. [SOLID BORDER BOX, narrow] "User Classes & Time Slots"
   subtitle: "choose broker / direct channel / shift across periods"
   Centered below both middle boxes (x=0.28-0.72, y=0.08-0.18)

ARROWS (solid dark gray with arrowheads):
- Box 1 bottom center → Box 2 top center (vertical down)
- Box 2 bottom-left → Box 3 top center (diagonal left-down)
- Box 2 bottom-right → Box 4 top center (diagonal right-down)
- Box 3 bottom center → Box 5 top-left (diagonal down-right)
- Box 4 bottom center → Box 5 top-right (diagonal down-left)

LABELS:
- Near the left diagonal arrow: "Brokered path" in small gray
- Near the right diagonal arrow: "Outside option" in small gray

SEPARATOR LINES (very thin light gray horizontal lines between layers):
- Between Supply and Platform layers
- Between Platform and Retail layers
- Between Retail and User layers

COLORS: same as Figure 2
FONT: same as Figure 2
======================================================================
