"""IDS core scenes, restyled to match the author's diagram styling.

Silent versions of the incremental-synthesis and backtracking scenes,
using the Google Slides look: Century Schoolbook serif (TeX Gyre Schola)
for titles/labels, pastel panel fills, thin dark outlines, gray captions.
Rocq code stays monospace (Menlo), as in the paper's Figure 2.
Manim CE v0.20.1, 16:9.
"""
from manim import *

BG = "#FFFFFF"
FG = "#212121"
DIM = "#666666"
STROKE = "#3C3C3C"
BLUE = "#1155CC"     # spec axioms
GREEN = "#38761D"    # proven / success
AMBER = "#BF9000"    # Admitted IOUs
RED = "#CC0000"      # failure
P_BLUE = "#CFE2F3"
P_YELLOW = "#FFF2CC"
P_GREEN = "#D9EAD3"
P_RED = "#F4CCCC"
SERIF = "TeX Gyre Schola"
MONO = "Menlo"


def txt(s, size=24, color=FG, weight=NORMAL):
    # 2x-render-then-scale: this serif's glyph advances collapse word
    # spaces below ~20pt (same workaround as the Jitski script).
    return Text(s, font=SERIF, font_size=size * 2, color=color,
                weight=weight).scale(0.5)


def code(s, size=16, color=FG):
    return Text(s, font=MONO, font_size=size, color=color)


def panel(title, fill_color, w, h):
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h,
                            stroke_color=STROKE, stroke_width=1.8,
                            fill_color=fill_color, fill_opacity=1)
    label = txt(title, size=20, weight=BOLD)
    label.next_to(rect, UP, buff=0.18)
    return rect, label


def code_lines(lines, rect, size=14, x_buff=0.22, y_start=0.32, spacing=0.36,
               start_row=0):
    """Left-aligned monospace lines laid out inside a panel rect.

    lines: list of (string, color) tuples. Leading spaces become a
    position offset (Pango strips whitespace). start_row places the
    first line at that row index within the panel.
    """
    out = []
    anchor = rect.get_corner(UL)
    char_w = Text("0" * 10, font=MONO, font_size=size).width / 10
    for i, (s, c) in enumerate(lines):
        lead = len(s) - len(s.lstrip(" "))
        t = code(s.lstrip(" "), size=size, color=c)
        t.move_to(anchor + RIGHT * (x_buff + lead * char_w)
                  + DOWN * (y_start + (start_row + i) * spacing),
                  aligned_edge=UL)
        out.append(t)
    return out


class Scene3_Insight(Scene):
    """FLAGSHIP: spec complete from the start; impl and proof grow together."""

    def construct(self):
        self.camera.background_color = BG
        PW, PH = 4.15, 4.7

        # Beat 0: title, then panels appear
        big = txt("Inductive Deductive Synthesis", size=40, weight=BOLD)
        sub = txt("grow the code and its proof together", size=26, color=DIM)
        sub.next_to(big, DOWN, buff=0.4)
        self.play(Write(big), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        header = txt("IDS: grow code and proof together", size=26,
                     weight=BOLD).to_edge(UP, buff=0.35)
        spec_rect, spec_label = panel("Specification", P_BLUE, PW, PH)
        impl_rect, impl_label = panel("Implementation", P_YELLOW, PW, PH)
        proof_rect, proof_label = panel("Proof", P_GREEN, PW, PH)
        for rect, label, x in [(spec_rect, spec_label, -4.55),
                               (impl_rect, impl_label, 0.0),
                               (proof_rect, proof_label, 4.55)]:
            rect.move_to(RIGHT * x + DOWN * 0.3)
            label.next_to(rect, UP, buff=0.18)
        self.play(FadeOut(big), FadeOut(sub), FadeIn(header), run_time=0.8)
        self.play(Create(spec_rect), FadeIn(spec_label),
                  Create(impl_rect), FadeIn(impl_label),
                  Create(proof_rect), FadeIn(proof_label), run_time=1.4)
        self.wait(0.8)

        # Beat 1: full spec appears; impl and proof are empty
        spec_src = [("Parameter t : Type.", FG),
                    ("Parameter init : t.", FG),
                    ("Parameter inc : t -> t.", FG),
                    ("Parameter read : t -> nat.", FG),
                    ("", FG),
                    ("Axiom read_init :", BLUE),
                    ("  read init = 0.", BLUE),
                    ("Axiom read_inc :", BLUE),
                    ("  read (inc s) = S (read s).", BLUE)]
        spec_code = code_lines(spec_src, spec_rect)
        empty_i = txt("(empty)", size=18, color=DIM).move_to(impl_rect)
        empty_p = txt("(empty)", size=18, color=DIM).move_to(proof_rect)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15)
                                for l in spec_code if l.text], lag_ratio=0.12),
                  run_time=2.4)
        self.play(FadeIn(empty_i), FadeIn(empty_p), run_time=0.8)
        self.wait(1.0)

        # Rocq badge, used from beat 2 on
        badge = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.62,
                                 stroke_color=STROKE, stroke_width=1.8,
                                 fill_color=BG, fill_opacity=1)
        badge.to_edge(DOWN, buff=0.28)
        badge_text = txt("Rocq type-checker", size=16, weight=BOLD)
        badge_text.move_to(badge.get_center())
        rocq = Group(badge, badge_text)

        def grade(extra=None, ok=True):
            mark = txt("✓" if ok else "✗", size=30,
                       color=GREEN if ok else RED, weight=BOLD)
            mark.next_to(badge, RIGHT, buff=0.25)
            anims = [FadeIn(mark, scale=1.4),
                     Indicate(badge, color=GREEN if ok else RED,
                              scale_factor=1.05)]
            if extra:
                anims += extra
            self.play(*anims, run_time=0.9)
            self.play(FadeOut(mark), run_time=0.3)
            return 1.2

        # Iteration counter, bottom-right
        it_label = txt("iteration", size=16, color=DIM)
        it_num = txt("1", size=22, weight=BOLD)
        it = Group(it_label, it_num).arrange(RIGHT, buff=0.25)
        it.move_to(RIGHT * 5.6 + DOWN * 3.3)

        def set_iter(n):
            new = txt(str(n), size=22, weight=BOLD).move_to(it_num)
            self.play(Transform(it_num, new), run_time=0.3)
            return 0.3

        # Beat 2: first joint step; Admitted IOUs appear
        impl_src = [("Definition t := list unit.", FG),
                    ("Definition init := nil.", FG),
                    ("Definition read s := length s.", FG),
                    ("Definition inc (s : t) : t.", FG),
                    ("Admitted.", AMBER)]
        proof_src = [("Theorem read_init :", FG),
                     ("  read init = 0.", FG),
                     ("Proof. reflexivity. Qed.", GREEN),
                     ("", FG),
                     ("Theorem read_inc :", FG),
                     ("  read (inc s) = S (read s).", FG),
                     ("Admitted.", AMBER)]
        impl_code = code_lines(impl_src, impl_rect)
        proof_code = code_lines(proof_src, proof_rect)
        used = 0.0
        self.play(FadeOut(empty_i), FadeOut(empty_p), FadeIn(rocq),
                  FadeIn(it), run_time=0.6)
        used += 0.6
        # step 1: representation
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15)
                                for l in impl_code[0:2]], lag_ratio=0.15),
                  run_time=1.2)
        used += 1.2 + grade()
        # step 2: read + its first proof; proven axiom pulses in the spec
        used += set_iter(2)
        self.play(FadeIn(impl_code[2], shift=RIGHT * 0.15), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15)
                                for l in proof_code[0:3]], lag_ratio=0.15),
                  run_time=1.2)
        used += 2.1 + grade(extra=[Indicate(Group(spec_code[5], spec_code[6]),
                                            color=BLUE, scale_factor=1.08)])
        # IOUs: inc deferred, read_inc deferred
        iou1 = SurroundingRectangle(Group(*impl_code[3:5]), color=AMBER,
                                    stroke_width=2, buff=0.08)
        iou2 = SurroundingRectangle(Group(*proof_code[4:7]), color=AMBER,
                                    stroke_width=2, buff=0.08)
        self.play(LaggedStart(*[FadeIn(l) for l in impl_code[3:5]],
                              *[FadeIn(l) for l in proof_code[4:7]],
                              lag_ratio=0.1), run_time=1.5)
        iou_tag = txt("Admitted = an IOU", size=20, color=AMBER, weight=BOLD)
        iou_tag.next_to(badge, LEFT, buff=0.6)
        self.play(Create(iou1), Create(iou2), FadeIn(iou_tag), run_time=1.0)
        used += 2.5 + grade()
        self.wait(0.8)

        # Beat 3: the checker grades every partial state
        self.play(FadeOut(iou_tag), run_time=0.4)
        spotlight = SurroundingRectangle(badge, color=GREEN, stroke_width=2.5,
                                         buff=0.12)
        verdict = txt("type-checks → design still viable", size=20,
                      color=GREEN)
        verdict.next_to(badge, LEFT, buff=0.5)
        self.play(Create(spotlight), run_time=0.8)
        self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.8)
        beams = [DashedLine(badge.get_top(), r.get_bottom(), color=GREEN,
                            stroke_width=2).set_opacity(0.7)
                 for r in [impl_rect, proof_rect]]
        self.play(*[Create(b) for b in beams], run_time=0.9)
        self.play(*[ShowPassingFlash(b.copy().set_color(GREEN)
                                     .set_stroke(width=4).set_z_index(10),
                                     time_width=0.4) for b in beams],
                  run_time=1.2)
        banked = txt("progress banked ✓", size=20, color=DIM)
        banked.next_to(badge, RIGHT, buff=0.5)
        self.play(FadeIn(banked), run_time=0.7)
        self.wait(1.2)

        # Beat 4: IOUs get paid off; fully implemented and proven
        self.play(FadeOut(Group(spotlight, verdict, banked, *beams)),
                  run_time=0.5)
        inc_fill = code_lines([("Definition inc (s : t) := tt::s.", GREEN)],
                              impl_rect, start_row=3)
        proof_fill = code_lines([("Proof. intros s. simpl.", GREEN),
                                 ("  reflexivity. Qed.", GREEN)],
                                proof_rect, start_row=6)
        iou1_paid = SurroundingRectangle(inc_fill[0], color=GREEN,
                                         stroke_width=2, buff=0.08)
        iou2_paid = SurroundingRectangle(Group(*proof_code[4:6], *proof_fill),
                                         color=GREEN, stroke_width=2,
                                         buff=0.08)
        used = 0.5
        used += set_iter(3)
        self.play(FadeOut(impl_code[3]), FadeOut(impl_code[4]),
                  FadeIn(inc_fill[0]),
                  Transform(iou1, iou1_paid), run_time=1.0)
        used += 1.0 + grade()
        used += set_iter(4)
        self.play(FadeOut(proof_code[6]), FadeIn(proof_fill[0]),
                  FadeIn(proof_fill[1]),
                  Transform(iou2, iou2_paid), run_time=1.0)
        used += 1.0 + grade()
        done = txt("fully implemented · fully proven", size=20, color=GREEN,
                   weight=BOLD)
        done.next_to(badge, LEFT, buff=0.5)
        glow = SurroundingRectangle(
            Group(spec_rect, impl_rect, proof_rect,
                  spec_label, impl_label, proof_label),
            color=GREEN, stroke_width=2.5, buff=0.25, corner_radius=0.2)
        self.play(FadeOut(iou1), FadeOut(iou2), Create(glow), FadeIn(done),
                  run_time=1.4)
        used += 1.4
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)


class Scene4_Backtrack(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Beat 0: a failing step is a signal, caught early
        header = txt("failed steps are signal", size=30,
                     weight=BOLD).to_edge(UP, buff=0.6)
        root = Circle(radius=0.28, stroke_color=STROKE, stroke_width=2,
                      fill_color=BG, fill_opacity=1).move_to(UP * 1.6)
        n1 = root.copy().set_stroke(GREEN).set_fill(P_GREEN)
        n1.move_to(UP * 0.3 + LEFT * 1.2)
        n2 = root.copy().set_stroke(GREEN).set_fill(P_GREEN)
        n2.move_to(DOWN * 1.0 + LEFT * 2.0)
        bad = root.copy().set_stroke(RED).set_fill(P_RED)
        bad.move_to(DOWN * 1.0 + LEFT * 0.2)
        e1 = Line(root.get_bottom(), n1.get_top(), color=DIM, stroke_width=1.8)
        e2 = Line(n1.get_bottom(), n2.get_top(), color=DIM, stroke_width=1.8)
        e3 = Line(n1.get_bottom(), bad.get_top(), color=DIM, stroke_width=1.8)
        cross = txt("✗", size=34, color=RED, weight=BOLD).move_to(bad)
        early = txt("dead end — found early, cheaply", size=20, color=RED)
        early.next_to(bad, RIGHT, buff=0.6)
        self.play(FadeIn(header), Create(root), run_time=1.0)
        self.play(Create(e1), Create(n1), run_time=0.8)
        self.play(Create(e2), Create(n2), run_time=0.8)
        self.play(Create(e3), Create(bad), run_time=0.8)
        self.play(FadeIn(cross, scale=1.5), FadeIn(early), run_time=0.9)
        self.wait(1.2)

        # Beat 1: backtrack and pivot to a new branch
        self.play(FadeOut(Group(cross, early)),
                  bad.animate.set_opacity(0.3), e3.animate.set_opacity(0.3),
                  Indicate(n1, color=AMBER), run_time=1.2)
        alt = Circle(radius=0.28, stroke_color=GREEN, stroke_width=2,
                     fill_color=P_GREEN, fill_opacity=1)
        alt.move_to(DOWN * 1.0 + RIGHT * 1.2)
        e4 = Line(n1.get_bottom(), alt.get_top(), color=GREEN,
                  stroke_width=1.8)
        pivot_l = txt("backtrack, try a new design", size=20, color=GREEN)
        pivot_l.next_to(alt, RIGHT, buff=0.6)
        self.play(Create(e4), Create(alt), FadeIn(pivot_l), run_time=0.9)
        self.wait(1.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)
