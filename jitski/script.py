"""Jitski pipeline animation (arXiv 2605.24096), light theme, silent.

Styled to match the author's Google Slides diagrams (see
reference_images/styling.png): Century Schoolbook serif (TeX Gyre Schola
clone), thin dark box outlines, pastel fills, gray captions.
Manim CE v0.20.1, 16:9.
"""
from manim import *

BG = "#FFFFFF"
FG = "#212121"       # near-black text
DIM = "#666666"      # captions
STROKE = "#3C3C3C"   # uniform thin box outline
BLUE = "#1155CC"     # accents / pulse
GREEN = "#38761D"
RED = "#CC0000"
# Google Slides pastel fills
P_BLUE = "#CFE2F3"
P_GREEN = "#D9EAD3"
P_YELLOW = "#FFF2CC"
P_CYAN = "#D0E0E3"
P_RED = "#F4CCCC"
P_ORANGE = "#FCE5CD"
P_GRAY = "#F3F3F3"
BAR_GRAY = "#B7B7B7"
BAR_GREEN = "#93C47D"
SERIF = "TeX Gyre Schola"


def txt(s, size=24, color=FG, weight=NORMAL, slant=NORMAL):
    # Render at 2x and scale down: this font's glyph advances get
    # quantized badly below ~20pt, collapsing/inserting word spaces.
    return Text(s, font=SERIF, font_size=size * 2, color=color, weight=weight,
                slant=slant).scale(0.5)


def cap(s, size=14, color=DIM):
    """Small gray caption, like the reference diagram's annotations."""
    return txt(s, size=size, color=color)


def box(w, h, fill, radius=0.1, stroke=STROKE, sw=1.8, opacity=1.0):
    return RoundedRectangle(corner_radius=radius, width=w, height=h,
                            stroke_color=stroke, stroke_width=sw,
                            fill_color=fill, fill_opacity=opacity)


def agent_box(name, num, fill="#FFFFFF", title_color=FG, w=2.2, h=0.95):
    rect = box(w, h, fill, radius=0.12)
    label = txt(name, size=20, color=title_color, weight=BOLD).move_to(rect)
    chip = Circle(radius=0.16, stroke_color=STROKE, stroke_width=1.5,
                  fill_color=BG, fill_opacity=1)
    chip.move_to(rect.get_corner(UL))
    chip_num = txt(str(num), size=15, color=FG, weight=BOLD).move_to(chip)
    return Group(rect, label, chip, chip_num)


def flow(a, b, color=DIM, **kw):
    return Arrow(a, b, buff=0.15, stroke_width=2.2, color=color,
                 tip_length=0.16, **kw)


class JitskitPipeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Title, then compact header
        big = txt("Jitski: Just-in-Time System Synthesis", size=36,
                  weight=BOLD)
        sub = cap("synthesize the whole system from a spec", size=22)
        sub.next_to(big, DOWN, buff=0.35)
        self.play(Write(big), run_time=1.4)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
        self.wait(1.2)
        header = txt("Jitski Synthesis Pipeline", size=26, weight=BOLD)
        header.to_edge(UP, buff=0.3)
        self.play(FadeOut(sub), FadeOut(big), FadeIn(header), run_time=0.8)

        # Specification: three pastel cards in a gray panel
        spec_rect = box(2.5, 2.6, P_GRAY, radius=0.15)
        spec_rect.move_to(LEFT * 5.65 + UP * 1.0)
        spec_label = txt("Specification", size=19, weight=BOLD)
        spec_label.next_to(spec_rect, UP, buff=0.15)
        cards = []
        for i, (name, fill) in enumerate([("Requirement", P_BLUE),
                                          ("Environment", P_ORANGE),
                                          ("Workload", P_GREEN)]):
            card = box(2.2, 0.7, fill, radius=0.08, sw=1.4)
            card.move_to(spec_rect.get_center() + UP * (0.75 - i * 0.78))
            cards.append(Group(card, txt(name, size=16).move_to(card)))
        builder = cap("System Builder", size=15)
        builder.next_to(spec_rect, DOWN, buff=0.25)
        self.play(Create(spec_rect), FadeIn(spec_label), FadeIn(builder),
                  run_time=0.9)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cards],
                              lag_ratio=0.25), run_time=1.3)
        self.wait(0.4)

        # Planner and Coder: white boxes, thin outline
        planner = agent_box("Planner", 1).move_to(LEFT * 2.55 + UP * 1.7)
        coder = agent_box("Coder", 2).move_to(RIGHT * 0.4 + UP * 1.7)
        a_spec = flow(spec_rect.get_right() + UP * 0.7,
                      planner[0].get_left())
        a_design = flow(planner[0].get_right(), coder[0].get_left())
        design_l = cap("design")
        design_l.next_to(a_design, DOWN, buff=0.12)
        self.play(FadeIn(planner, scale=1.1), Create(a_spec), run_time=0.9)
        self.play(FadeIn(coder, scale=1.1), Create(a_design),
                  FadeIn(design_l), run_time=0.9)
        self.wait(0.4)

        # Evaluation panel: lavender correctness + green performance
        eval_rect = box(4.3, 3.0, P_GRAY, radius=0.15)
        eval_rect.move_to(RIGHT * 4.4 + UP * 1.0)
        eval_label = txt("Evaluation", size=19, weight=BOLD)
        eval_label.next_to(eval_rect, UP, buff=0.15)
        corr = box(3.7, 1.05, P_CYAN, sw=1.4)
        corr.move_to(eval_rect.get_center() + UP * 0.72)
        corr_t = txt("Correctness Check", size=16, weight=BOLD)
        corr_t.move_to(corr.get_center() + UP * 0.22)
        corr_s = cap("API semantics · invariants", size=13)
        corr_s.move_to(corr.get_center() + DOWN * 0.24)
        corr_chip3 = Circle(radius=0.16, stroke_color=STROKE,
                            stroke_width=1.5, fill_color=BG, fill_opacity=1)
        corr_chip3.move_to(corr.get_corner(UL))
        corr_n3 = txt("3", size=15, weight=BOLD).move_to(corr_chip3)
        perf = box(3.7, 1.35, P_GREEN, sw=1.4)
        perf.move_to(eval_rect.get_center() + DOWN * 0.62)
        perf_t = txt("Performance Eval", size=16, weight=BOLD)
        perf_t.move_to(perf.get_left() + RIGHT * 1.35 + UP * 0.34)
        perf_s = cap("tput · p99 · hits", size=13)
        perf_s.move_to(perf_t.get_center() + DOWN * 0.42)
        perf_chip4 = Circle(radius=0.16, stroke_color=STROKE,
                            stroke_width=1.5, fill_color=BG, fill_opacity=1)
        perf_chip4.move_to(perf.get_corner(UL))
        perf_n4 = txt("4", size=15, weight=BOLD).move_to(perf_chip4)
        a_code = flow(coder[0].get_right(), eval_rect.get_left() + UP * 0.7)
        code_l = cap("code").next_to(a_code, UP, buff=0.1)
        self.play(Create(eval_rect), FadeIn(eval_label), Create(a_code),
                  FadeIn(code_l), run_time=0.9)
        self.play(FadeIn(Group(corr, corr_t, corr_s, corr_chip3, corr_n3)),
                  FadeIn(Group(perf, perf_t, perf_s, perf_chip4, perf_n4)),
                  run_time=0.9)
        self.wait(0.4)

        # Critic: the main feedback loop
        critic = agent_box("Critic", 5).move_to(RIGHT * 0.1 + DOWN * 1.4)
        a_to_critic = flow(eval_rect.get_bottom() + LEFT * 0.9,
                           critic[0].get_right())
        results_l = cap("code + eval results")
        results_l.move_to(a_to_critic.get_center() + DOWN * 0.36 + RIGHT * 0.3)
        a_feedback = flow(critic[0].get_left(),
                          planner[0].get_bottom() + DOWN * 0.05)
        feedback_l = cap("feedback")
        feedback_l.next_to(a_feedback, LEFT, buff=0.12)
        self.play(FadeIn(critic, scale=1.1), Create(a_to_critic),
                  FadeIn(results_l), run_time=0.9)
        self.play(Create(a_feedback), FadeIn(feedback_l), run_time=0.9)
        self.wait(0.5)

        # Iteration counter and perf bars
        it_label = cap("iteration", size=16)
        it_num = txt("1", size=22, weight=BOLD)
        it = Group(it_label, it_num).arrange(RIGHT, buff=0.25)
        it.move_to(LEFT * 5.4 + DOWN * 2.6)
        self.play(FadeIn(it), run_time=0.5)

        bar_base = perf.get_corner(DL) + RIGHT * 1.8 + UP * 0.12
        bar_xs = [0.0, 0.45, 0.9, 1.35]

        def bar(i, h, fill, stroke):
            r = Rectangle(width=0.32, height=h, stroke_color=stroke,
                          stroke_width=1.2, fill_color=fill,
                          fill_opacity=0.9)
            r.move_to(bar_base + RIGHT * bar_xs[i], aligned_edge=DOWN)
            return r

        loop_arrows = [a_spec, a_design, a_code, a_to_critic, a_feedback]

        def pulse_loop(rt=2.6):
            self.play(LaggedStart(
                *[ShowPassingFlash(a.copy().set_color(BLUE).set_stroke(width=5).set_z_index(10),
                                   time_width=0.6) for a in loop_arrows],
                lag_ratio=0.22), run_time=rt)

        def set_iter(n):
            new = txt(str(n), size=22, weight=BOLD).move_to(it_num)
            self.play(Transform(it_num, new), run_time=0.3)

        # Iteration 1: first candidate, modest bar
        pulse_loop()
        ok1 = txt("✓", size=22, color=GREEN, weight=BOLD)
        ok1.move_to(corr.get_right() + LEFT * 0.35)
        b1 = bar(0, 0.30, BAR_GRAY, STROKE)
        self.play(FadeIn(ok1, scale=1.3), FadeIn(b1), run_time=0.7)
        self.wait(0.3)

        # Iteration 2: feedback pays off
        set_iter(2)
        pulse_loop(rt=2.2)
        b2 = bar(1, 0.55, BAR_GRAY, STROKE)
        self.play(FadeIn(b2), Indicate(ok1, color=GREEN), run_time=0.7)
        self.wait(0.3)

        # Iteration 3: a suspicious 6x jump
        set_iter(3)
        pulse_loop(rt=2.2)
        b3 = bar(2, 0.85, P_RED, RED)
        jump = txt("6×?!", size=14, color=RED, weight=BOLD)
        jump.next_to(b3, UP, buff=0.05)
        self.play(FadeIn(b3), FadeIn(jump, scale=1.4), run_time=0.8)
        self.wait(0.5)

        # Auditor wakes up, catches the reward hack, extends the gate
        auditor = agent_box("Auditor", 6, fill=P_RED, title_color=RED)
        auditor.move_to(RIGHT * 4.4 + DOWN * 2.0)
        a_audit_in = DashedLine(eval_rect.get_bottom() + RIGHT * 0.9,
                                auditor[0].get_top(), color=DIM,
                                stroke_width=1.8)
        everyn = cap("every N iters", size=13)
        everyn.next_to(a_audit_in, RIGHT, buff=0.12)
        self.play(FadeIn(auditor, scale=1.1), Create(a_audit_in),
                  FadeIn(everyn), run_time=0.9)
        hack = txt("reward hack!", size=16, color=RED, weight=BOLD)
        hack.next_to(auditor[0], DOWN, buff=0.18)
        self.play(FadeIn(hack, scale=1.2),
                  Indicate(auditor[0], color=RED), run_time=0.9)
        # a new LLM-written test flies into the correctness gate
        test_chip = box(1.5, 0.46, BG, radius=0.06, sw=1.4)
        test_t = txt("new test", size=13, weight=BOLD)
        test = Group(test_chip, test_t.move_to(test_chip))
        test.move_to(auditor[0].get_top() + UP * 0.3)
        self.play(FadeIn(test, scale=0.8), run_time=0.5)
        self.play(test.animate.move_to(corr.get_center() + DOWN * 0.22),
                  run_time=1.0)
        self.play(FadeOut(corr_s), run_time=0.3)
        # the hacked candidate now fails the gate
        x3 = txt("✗", size=22, color=RED, weight=BOLD).move_to(b3)
        self.play(b3.animate.set_opacity(0.25), FadeOut(jump),
                  FadeIn(x3, scale=1.4), run_time=0.8)
        self.wait(0.4)

        # Iteration 4: a real design wins
        set_iter(4)
        pulse_loop(rt=2.2)
        b4 = bar(3, 0.78, BAR_GREEN, GREEN)
        best = txt("best", size=14, color=GREEN, weight=BOLD)
        best.next_to(b4, UP, buff=0.08)
        self.play(FadeIn(b4), FadeIn(best), Indicate(ok1, color=GREEN),
                  run_time=0.8)
        self.wait(0.5)

        # Closing banner
        banner = txt("18/18 specs · up to 4.6× over the best baseline",
                     size=22, weight=BOLD)
        banner.to_edge(DOWN, buff=0.35)
        cite = cap("arXiv 2605.24096", size=15)
        cite.next_to(banner, UP, buff=0.18)
        self.play(FadeIn(banner, shift=UP * 0.2), FadeIn(cite), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.wait(0.3)
