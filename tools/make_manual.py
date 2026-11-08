#!/usr/bin/env python3
# Builds docs/UNIT110-Manual.pdf (needs: pip install reportlab).
#   python3 tools/make_manual.py
# Pictures: docs/panel.png and docs/pcb.png (editor snapshots written by the plug-in test).
import os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = re.search(r"project\(UNIT110 VERSION ([0-9.]+)\)", open(os.path.join(ROOT, "CMakeLists.txt")).read()).group(1)
OUT = os.path.join(ROOT, "docs", "UNIT110-Manual.pdf")

INK = colors.HexColor("#1e1f21")
BLUE = colors.HexColor("#3f7f9e")
GREY = colors.HexColor("#6b6e6a")
LIGHT = colors.HexColor("#eef1ea")

body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6)
small = ParagraphStyle("small", parent=body, fontSize=8.6, leading=11.6, spaceAfter=0)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=10, spaceAfter=7, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=BLUE, spaceBefore=9, spaceAfter=4, keepWithNext=1)
title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=34, leading=38, textColor=INK)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=11, leading=15, textColor=GREY, spaceAfter=14)
cell = ParagraphStyle("cell", parent=small)
cellb = ParagraphStyle("cellb", parent=small, fontName="Helvetica-Bold")


def table(rows, widths):
    data = [[Paragraph(str(c), cellb if i == 0 or j == 0 else cell) for j, c in enumerate(r)] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BLUE),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#cfd3cb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def P(t): return Paragraph(t, body)


def footer(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 8)
    canv.setFillColor(GREY)
    canv.drawString(18 * mm, 10 * mm, f"UNIT 110 {VERSION}  ·  Transistor Labs")
    canv.drawRightString(A4[0] - 18 * mm, 10 * mm, str(doc.page))
    canv.setStrokeColor(BLUE); canv.setLineWidth(0.6)
    canv.line(18 * mm, 13.5 * mm, A4[0] - 18 * mm, 13.5 * mm)
    canv.restoreState()


W = A4[0] - 36 * mm
s = []
s += [Spacer(1, 14 * mm), Paragraph('UNIT <font color="#3f7f9e">110</font>', title),
      Paragraph(f"Transistor Labs rhythm composer  ·  Owner's manual  ·  version {VERSION}", sub)]
img = os.path.join(ROOT, "docs", "panel.png")
if os.path.exists(img):
    s += [Image(img, width=W, height=W * 922 / 1502), Spacer(1, 8)]
s += [P("UNIT 110 is a drum machine you play like the hardware: press its keys, turn its knobs, read its LCD, and open the "
        "case to reach the trimmers inside. Six analog-style voices - bass drum, snare, hand clap, closed hat, open hat "
        "and cymbal - a global accent, and a 16-step sequencer with 32 patterns and a song mode. It runs as an Audio Unit, "
        "VST3 or LV2 plug-in and as a standalone app on macOS, Windows and Linux.")]

s += [PageBreak(), Paragraph("1  System requirements", h1)]
s += [table([
    ["System", "Needs"],
    ["macOS", "<b>Minimum: macOS 10.13 High Sierra on Intel, macOS 11 Big Sur on Apple silicon</b> (universal build; runs on macOS 12 "
              "Monterey and every later version). A host for AU or VST3 (Ableton Live, Logic Pro, GarageBand, Bitwig, Reaper...), or the standalone app."],
    ["Windows", "<b>Minimum: Windows 10, 64-bit</b> (Windows 11 too). A VST3 host, or the standalone app."],
    ["Linux", "<b>Minimum: x86_64</b> with X11, FreeType and ALSA or JACK. A VST3 or LV2 host (Bitwig, Reaper, Ardour...), or the standalone app."],
    ["Screen", "The window opens at 1126 x 691 and can be resized from 50 % to 120 %."],
    ["CPU / memory", "Light: one instance uses a few percent of one core; about 30 MB of memory."],
], [28 * mm, W - 28 * mm])]

s += [Paragraph("2  Installing", h1)]
s += [table([
    ["System", "File", "What it installs"],
    ["macOS", f"UNIT110-{VERSION}-macOS.pkg", "Audio Unit, VST3 and the standalone app. Click Customize to skip any of them."],
    ["Windows", f"UNIT110-{VERSION}-Windows-Setup.exe", "VST3 (Common Files\\VST3) and the standalone app."],
    ["Linux", f"UNIT110-{VERSION}-Linux-x86_64.tar.gz", "Unpack and run ./install.sh: VST3 to ~/.vst3, LV2 to ~/.lv2, app to ~/.local/bin."],
], [22 * mm, 66 * mm, W - 88 * mm])]
s += [Paragraph("2.1  macOS security warning", h2),
      P("The macOS installer is <b>not notarised</b> by Apple, so the first time you open it macOS says it \"cannot be opened "
        "because it is from an unidentified developer\" (or that Apple could not check it for malicious software). To install:"),
      P("1. Double-click the .pkg once and close the warning.<br/>"
        "2. Open <b>System Settings > Privacy &amp; Security</b>, scroll down to the message about UNIT110 and click <b>Open Anyway</b>.<br/>"
        "3. Confirm with your password and run the installer.<br/>"
        "Alternative: right-click (Control-click) the .pkg in Finder, choose <b>Open</b>, then <b>Open</b> again."),
      P("On Windows, SmartScreen may warn about the installer: click <b>More info > Run anyway</b>."),
      P("<b>Ableton Live:</b> Settings > Plug-Ins: turn on \"Use Audio Units v2\" (Mac) and/or VST3, then Rescan. UNIT 110 is under "
        "Plug-Ins > Audio Units (or VST3) > Transistor Labs. Drop it on a MIDI track.")]

s += [Paragraph("3  The front panel", h1),
      P("Everything works with the mouse, just like the real keys. Resize the window from its bottom-right corner. "
        "Click the TRANSISTOR LABS logo for the About window.")]
s += [Paragraph("3.0  Opening the case", h2),
      P("Click either <b>screw in the bottom corners</b> or the <b>ON-OFF POWER</b> lettering to open the unit (section 5). "
        "Inside, click one of the <b>screws</b> or one of the <b>three big black chips</b> to close it again (or press Esc).")]
s += [Paragraph("3.1  Knobs and switch", h2)]
s += [table([
    ["Control", "What it does"],
    ["SWING", "From STRAIGHT (50 %) to SHUFFLE (75 %): every second 16th note comes later. Around 62 % is the classic swing; fully right is a "
              "hard, dotted shuffle. The LCD shows the amount (SW) in the TEMPO box. MIDI export swings too."],
    ["BALANCE", "Drums against metal. Turn left and the hats and cymbal fade; turn right and the bass drum, snare and clap fade. Centre = both full."],
    ["ACCENT", "How hard accented steps hit: a short swell on the whole machine that also drives it into grit."],
    ["VOLUME", "Main output level (5 = -14 dB, 10 = +6 dB)."],
    ["POWER", "Click the switch on the top edge. Off = the LCD goes dark and UNIT 110 is silent."],
    ["Knobs", "Drag up/down. The value shows while you drag; double-click resets."],
    ["Tempo", "UNIT 110 always follows the tempo of your DAW. In the standalone app, drag up/down on the TEMPO box of the LCD to set it "
              "(40-250 BPM); double-click it for 120."],
], [26 * mm, W - 26 * mm])]
s += [Paragraph("3.2  Keys", h2)]
s += [table([
    ["Key", "What it does"],
    ["SHIFT", "Click it, then the next key does its upper (printed) function. Holding the computer's Shift key while clicking works too. "
              "<b>Double-click</b> SHIFT to switch the LCD to the P-LOCK screen (section 4.1); double-click again to go back."],
    ["A|B|C|D", "Steps through the 4 banks of 8 patterns (A1-D8). With SHIFT, or in WRITE STEP: I-II, switches between steps 1-8 and 9-16."],
    ["1 - 8", "Selects pattern 1-8 of the current bank. While playing, the new pattern starts at the next step 1 (the LCD shows NEXT). "
              "<b>Cmd-click</b> (Mac) / <b>Ctrl-click</b> (Windows, Linux) builds a PATTERN CHAIN of up to 8 patterns (section 4.3)."],
    ["START / STOP", "Runs and stops the sequencer while the DAW is stopped, at the DAW's tempo. When the DAW plays, UNIT 110 follows it."],
    ["Drum keys", "Play the drum. ACCENT arms an accent for the next drum you hit (the key stays down)."],
    ["SHIFT + drum", "<b>Mute</b> the drum on/off. Its row on the LCD shows M, the name blinks and its steps go faint."],
    ["Option + drum", "<b>Solo</b> the drum on/off (Alt on Windows / Linux). Its row shows S and the other drums go faint. Several drums can be soloed."],
    ["Right-click drum", "<b>Own output</b> (plug-in only): sends the drum to its own output instead of the main mix (section 6)."],
], [26 * mm, W - 26 * mm])]
s += [Paragraph("3.3  SHIFT functions", h2)]
s += [table([
    ["SHIFT +", "Function", "What it does"],
    ["1", "PLAY SONG", "Plays the song (the list of patterns built in WRITE SONG), one pattern per bar, locked to the song position."],
    ["2", "PLAY PATTERN", "Plays the selected pattern over and over (the default)."],
    ["3", "WRITE SONG", "Number keys add patterns of the current bank to the end of the song. O.HIHAT (ENTER) adds the playing pattern; "
                       "C.HIHAT (D.C.) takes back the last measure. Up to 32 measures."],
    ["4", "WRITE STEP", "Press ACCENT or a drum key to choose the row (marked on the LCD), then number keys 1-8 switch its steps on and off. "
                       "A|B|C|D (I-II) switches to steps 9-16."],
    ["5", "WRITE TAP", "Record live: drum keys and MIDI notes played while the sequencer runs go into the nearest step. "
                      "ACCENT before a hit, or velocity above 100, also sets the accent."],
    ["6", "12 / 16", "Pattern length 12 (shuffle, triplets) or 16 steps."],
    ["7", "PATTERN CLEAR", "Clears the selected pattern."],
    ["8", "MEASURE RESET", "Clears the song."],
    ["drum key", "MUTE", "Mutes / unmutes that drum (see 3.2)."],
], [16 * mm, 32 * mm, W - 48 * mm])]

# ---- the LCD, screen by screen: pictures taken from the plug-in (docs/lcd/*.png, written by the test) with numbered callouts
from PIL import Image as PILImage, ImageDraw as PILDraw, ImageFont as PILFont
LCD_DIR = os.path.join(ROOT, "docs", "lcd")
CALL_DIR = os.path.join(ROOT, "docs", "lcd", "callouts")
os.makedirs(CALL_DIR, exist_ok=True)


def callouts(name, marks):
    """Draws numbered circles on an LCD picture; marks = [(x, y), ...] in the picture's pixels."""
    im = PILImage.open(os.path.join(LCD_DIR, f"lcd_{name}.png")).convert("RGB")
    d = PILDraw.Draw(im)
    try: f = PILFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except Exception: f = PILFont.load_default()
    for i, (x, y) in enumerate(marks, 1):
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(214, 64, 40), outline=(255, 255, 255), width=3)
        d.text((x, y), str(i), font=f, fill=(255, 255, 255), anchor="mm")
    out = os.path.join(CALL_DIR, f"{name}.png")
    im.save(out)
    return out, im.size


def screen(title, name, marks, legend, intro=None):
    path, (w, h) = callouts(name, marks)
    iw = W * 0.74
    items = [Paragraph(title, h2)]
    if intro: items.append(P(intro))
    items.append(Image(path, width=iw, height=iw * h / w))
    items.append(Spacer(1, 3))
    items.append(table([["", "What it shows"]] + [[str(i), t] for i, t in enumerate(legend, 1)], [10 * mm, W - 10 * mm]))
    return KeepTogether(items)


s += [PageBreak(), Paragraph("4  The LCD", h1),
      P("The LCD is UNIT 110's control centre. Everything on it is live: click steps to edit, click the boxes to change things, "
        "<b>right-click</b> for the menu. These are its screens, taken straight from the plug-in.")]
s += [screen("4.1  The pattern screen (PLAY PATTERN)", "pattern",
             [(140, 34), (148, 170), (448, 123), (292, 352), (480, 398), (735, 398), (975, 398), (985, 600)],
             ["Step numbers. The playing step is shown reversed. Steps beyond the length (12-step patterns) are greyed out.",
              "The 7 rows: ACCENT and the six drums.",
              "Steps: <b>click</b> to switch one on or off, <b>drag</b> along a row to paint. A small dot in a step = it has parameter locks.",
              "The playing step's column is shaded.",
              "MODE: the current mode, or a short message after an action.",
              "PATTERN: bank letter + number (A1-D8). While playing, a newly chosen pattern blinks as NEXT until the bar ends.",
              "TEMPO: the tempo in BPM (in the standalone app, drag it up/down; double-click = 120).",
              "Length (12 / 16 STEPS), swing (SW), and HOST (the DAW is playing) or RUN (UNIT 110 runs on its own)."])]
s += [screen("4.2  Writing steps (WRITE STEP)", "step",
             [(148, 168), (60, 34), (480, 398), (480, 604)],
             ["The arrow marks the row the number keys edit: press ACCENT or a drum key to choose it.",
              "The underline shows which half the number keys edit: steps 1-8 or 9-16 (switch with the A|B|C|D key).",
              "Mode (SHIFT + 4).",
              "What you're editing: the row and the half."],
             "SHIFT + 4, then a drum key, then number keys 1-8 to switch its steps.")]
s += [screen("4.3  Pattern chain", "chain",
             [(480, 398), (330, 487), (735, 398), (720, 606), (480, 604)],
             ["PATTERN CHAIN: a chain is playing.",
              "The chain in order (up to 8 patterns). The playing one is reversed; they loop, one per bar.",
              "The pattern playing now.",
              "Its place in the chain (2nd of 4).",
              "How full the chain is. A normal click on a number key ends the chain."],
             "<b>Cmd-click</b> (Mac) or <b>Ctrl-click</b> (Windows / Linux) number keys to build a chain: Cmd-click 1, 2, 2, 4 plays "
             "A1 → A2 → A2 → A4 → A1 ... Change bank with A|B|C|D between clicks. A ninth click shows CHAIN FULL. "
             "The chain is saved with the project.")]
s += [screen("4.4  Song (WRITE SONG / PLAY SONG)", "writesong",
             [(480, 398), (480, 604)],
             ["WRITE SONG (SHIFT + 3): number keys add patterns to the end of the song, O.HIHAT (ENTER) adds the playing one, "
              "C.HIHAT (DC) takes the last one back.",
              "How many measures the song has (up to 32)."])]
s += [screen("", "playsong",
             [(480, 398), (480, 604), (735, 398)],
             ["PLAY SONG (SHIFT + 1): the song plays, one pattern per bar, locked to the DAW's position.",
              "Song length and the measure playing now.",
              "The pattern of that measure."])]
s += [screen("4.5  Mute and solo", "mutesolo",
             [(240, 168), (240, 258), (500, 123)],
             ["S = soloed (Option / Alt + drum key). Several drums can be soloed.",
              "M = muted (SHIFT + drum key). A muted name blinks.",
              "Drums that are silent (muted, or not soloed while others are) are shown faint."])]
s += [screen("4.6  P-LOCK screen", "plock",
             [(140, 62), (140, 330), (140, 200), (440, 90), (880, 215), (500, 378), (310, 398), (630, 398), (975, 398)],
             ["P-LOCK: the lock screen is showing (double-click SHIFT; again to go back).",
              "The top and bottom of the scale.",
              "The drum and the setting being locked.",
              "A lock: the bar's height is the step's own value. <b>Click or drag</b> to set, <b>double-click</b> to remove.",
              "TUNE is centred on 0: bars go up (higher) or down (lower).",
              "A mark under a step = the drum plays there.",
              "DRUM: click to change (or press a drum key).",
              "SETTING: click to step through TUNE, DECAY, LEVEL and the drum's extra.",
              "VALUE: the last step you touched and its value (KNOB = no lock, the trimmer decides)."])]
s += [screen("4.7  Messages", "message",
             [(480, 398)],
             ["After an action the MODE box confirms it for a moment: COPIED A1, PASTED TO A4, PATTERN CLEARED, SONG CLEARED, "
              "12 STEPS, STEPS 9-16, SNARE MUTED, CHAIN FULL, HOST IS PLAYING..."])]
s += [screen("4.8  Swing and running on its own", "swing",
             [(990, 565)],
             ["SW 62 = SWING at 62 %. RUN = UNIT 110 plays on its own (START with the DAW stopped); HOST = the DAW is playing."])]
s += [screen("4.9  Power off", "off",
             [(507, 322)],
             ["With POWER off the LCD is blank and UNIT 110 is silent. The knobs and trimmers still move."])]
s += [Paragraph("4.10  The right-click menu", h2),
      P("Right-click the LCD for: <b>Export</b> this pattern, all patterns in a row, every pattern as its own file, or the song as MIDI "
        "(16th notes on channel 10, accents at velocity 127, swing included); <b>Copy pattern</b> / <b>Paste pattern</b> (steps and locks); "
        "<b>Copy pattern to</b> a slot of bank A, B, C or D; <b>Clear</b> the pattern or the song; on the P-LOCK screen also clear the "
        "locks of a lane, of a drum or of the whole pattern.")]
s += [Paragraph("4.11  Parameter locks", h2),
      P("A parameter lock gives one step of one drum its own setting: a higher tuned snare on step 7, a longer open hat on the last step. "
        "A lock holds until that drum's next hit. Locks are saved with each pattern and copied with it.")]

s += [Paragraph("5  Inside the case", h1),
      P("Click either <b>screw in the bottom corners</b> of the front panel to open the unit. The circuit board has a service trimmer for "
        "every sound setting. Drag a trimmer up/down; double-click resets it. Click a corner screw on the board, right-click, or press Esc "
        "to close the case.")]
img = os.path.join(ROOT, "docs", "pcb.png")
if os.path.exists(img):
    s += [Image(img, width=W, height=W * 922 / 1502), Spacer(1, 6)]
s += [table([
    ["Trimmer", "What it does"],
    ["TUNE", "Pitch, ±12 semitones. On the hats and cymbal it moves the whole metallic cluster."],
    ["DECAY", "Length of the sound. Middle is the classic timing; fully left a quarter as long, fully right four times as long. "
              "On the bass drum it is the ring of its resonant filter; on the snare the length of the noise; on the clap the last burst "
              "and the room tail."],
    ["LEVEL", "The drum's level, -inf to +6 dB."],
    ["Defaults", "Bass drum TUNE -2.4 st, DECAY 21.4 %; snare DECAY 36.1 %; clap TUNE +2.6 st, DECAY 30 %, LEVEL +4.1 dB. "
                 "Double-click any trimmer to return to its default."],
    ["ACC: DRIVE", "How much an accent pushes the machine into grit."],
    ["ACC: DECAY", "How long the accent swell lasts."],
    ["ACC: LEVEL", "Accent amount (the same setting as the ACCENT knob on the front)."],
    ["ATTACK (BD)", "How far the kick's pitch drops at the start: 50 % = one octave (110 Hz down to 55 Hz), 0 % = no drop, 100 % = from three times the pitch."],
    ["SNAPPY (SD)", "Noise snap against the 235 Hz tone. 60 % is the original balance."],
    ["TONE (CY)", "Bright attack shimmer (right) against the darker ringing body (left)."],
    ["TAIL (CP)", "Level of the clap's room tail after the burst of hits. 15 % is the original."],
], [28 * mm, W - 28 * mm])]

s += [Paragraph("6  MIDI and outputs", h1)]
s += [table([
    ["Drum", "MIDI notes (C1 = 36)"],
    ["Bass drum", "35, 36"], ["Snare", "37, 38, 40"], ["Hand clap", "39"], ["Closed hat", "42, 44"], ["Open hat", "46"],
    ["Cymbal", "49, 51, 52, 53, 55, 57"],
], [40 * mm, W - 40 * mm])]
s += [Spacer(1, 4),
      P("Velocities up to 100 scale the level; above 100 also fires the accent."),
      P("<b>Outputs (plug-in):</b> main stereo plus one mono output per drum. Right-click a drum key and choose <b>Own output</b> to take "
        "that drum out of the main mix and send it to its own output (in Live: make an audio track, Audio From = the UNIT 110 track, "
        "pick the drum's output, Monitor In). The standalone app has only the main output, so there is no right-click menu there."),
      P("All 32 patterns, the song, the mode and every knob and trimmer are saved with your project.")]

s += [Paragraph("7  Specifications", h1)]
s += [table([
    ["", ""],
    ["Voices", "6: bass drum (55 Hz resonant filter with an octave pitch drop), snare (235 Hz tone + 3550 Hz noise), hand clap "
               "(3 + 1 noise bursts and a room tail at 1140 Hz), closed hat, open hat, cymbal; plus global accent"],
    ["Sequencer", "16 steps (12 or 16), 7 rows, 32 patterns (4 banks x 8), song of up to 32 measures, swing 50-75 %, parameter locks, "
                  "host sync, own clock, step and tap writing"],
    ["Outputs", "Main stereo + 6 mono drum outputs (plug-in)"],
    ["Formats", "AU, VST3 (macOS); VST3 (Windows); VST3, LV2 (Linux); standalone app on all three"],
    ["Sample rates", "Any host rate (44.1-192 kHz)"],
], [30 * mm, W - 30 * mm])]
s += [Spacer(1, 8), P("Store: <b>https://ticcoross.gumroad.com/</b>  ·  Questions and feedback: <b>ticcoross@gmail.com</b>")]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                        title=f"UNIT 110 Manual {VERSION}", author="Transistor Labs", subject="UNIT 110 owner's manual")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
