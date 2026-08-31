"""IDS explainer — Inductive Deductive Synthesis (arXiv 2605.23109).

Six scenes, timed to pre-measured ElevenLabs narration (see plan.md).
Manim CE v0.20.1, 16:9.
"""
from manim import *

BG = "#0D1117"
FG = "#E6EDF3"
DIM = "#8B949E"
BLUE = "#58A6FF"     # spec
PURPLE = "#BC8CFF"   # impl
GREEN = "#3FB950"    # proof / success
YELLOW = "#D29922"   # Admitted IOUs
RED = "#F85149"      # failure
MONO = "Menlo"


def txt(s, size=28, color=FG, weight=NORMAL):
    return Text(s, font=MONO, font_size=size, color=color, weight=weight)


def fill(scene, seg, used):
    """Wait out the remainder of a narration segment."""
    scene.wait(max(seg - used, 0.15))


def panel(title, accent, w, h):
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h,
                            stroke_color=accent, stroke_width=2.5,
                            fill_color=BG, fill_opacity=0.6)
    label = txt(title, size=24, color=accent, weight=BOLD)
    label.next_to(rect, UP, buff=0.18)
    return rect, label


def code_lines(lines, rect, size=16, x_buff=0.22, y_start=0.32, spacing=0.34,
               start_row=0):
    """Left-aligned Text lines laid out inside a panel rect.

    lines: list of (string, color) tuples. Returns list of Text mobjects.
    Leading spaces become a position offset (Pango strips whitespace).
    start_row places the first line at that row index within the panel.
    """
    out = []
    anchor = rect.get_corner(UL)
    char_w = Text("0" * 10, font=MONO, font_size=size).width / 10
    for i, (s, c) in enumerate(lines):
        lead = len(s) - len(s.lstrip(" "))
        t = txt(s.lstrip(" "), size=size, color=c)
        t.move_to(anchor + RIGHT * (x_buff + lead * char_w)
                  + DOWN * (y_start + (start_row + i) * spacing),
                  aligned_edge=UL)
        out.append(t)
    return out


class Scene1_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG
        seg = [6.97, 7.34, 6.87]

        # Seg 0: agents write code, run tests, fix mistakes
        self.add_subcaption("AI coding agents are getting remarkably good. "
                            "They write code, run the tests, and fix their "
                            "own mistakes.", duration=seg[0])
        title = txt("AI agents write code", size=40, weight=BOLD).to_edge(UP, buff=0.8)
        win, win_label = panel("agent.py", DIM, 5.6, 3.2)
        win.move_to(ORIGIN + DOWN * 0.5)
        win_label.next_to(win, UP, buff=0.18)
        lines = code_lines([("def handle(req):", FG),
                            ("    key = req.key", FG),
                            ("    return store[key]", FG)],
                           win, size=20, y_start=0.45, spacing=0.5)
        checks = Group(txt("tests: ", size=22, color=DIM),
                       txt("PASS", size=22, color=GREEN, weight=BOLD))
        checks.arrange(RIGHT, buff=0.15).next_to(win, DOWN, buff=0.35)
        self.play(Write(title), run_time=1.0)
        self.play(Create(win), FadeIn(win_label), run_time=1.0)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(checks), run_time=0.6)
        fill(self, seg[0], 4.1)

        # Seg 1: tested is not proven
        self.add_subcaption("But some software has to be more than "
                            "well-tested. It has to be provably correct. "
                            "On every input, every time.", duration=seg[1])
        tested = txt("well-tested", size=34, color=DIM)
        arrow = txt("→", size=34, color=DIM)
        proven = txt("provably correct", size=34, color=GREEN, weight=BOLD)
        row = Group(tested, arrow, proven).arrange(RIGHT, buff=0.4)
        row.move_to(UP * 0.3)
        every = txt("on every input, every time", size=24, color=FG)
        every.next_to(row, DOWN, buff=0.5)
        self.play(FadeOut(Group(win, win_label, *lines, checks)),
                  title.animate.set_opacity(0.3), run_time=0.8)
        self.play(FadeIn(tested), run_time=0.7)
        self.play(FadeIn(arrow), FadeIn(proven, scale=1.15), run_time=1.0)
        self.play(FadeIn(every, shift=UP * 0.2), run_time=0.8)
        fill(self, seg[1], 3.3)

        # Seg 2: distributed systems, rare interleavings
        self.add_subcaption("Think distributed systems, where bugs hide in "
                            "rare interleavings of messages that no test "
                            "suite will ever reach.", duration=seg[2])
        self.play(FadeOut(Group(title, row, every)), run_time=0.6)
        nodes = [Circle(radius=0.42, stroke_color=BLUE, stroke_width=3,
                        fill_color=BG, fill_opacity=1).move_to(p)
                 for p in [LEFT * 4 + UP * 1.2, RIGHT * 4 + UP * 1.2, DOWN * 1.8]]
        node_labels = [txt(n, size=20, color=BLUE).move_to(c.get_center())
                       for n, c in zip(["A", "B", "C"], nodes)]
        msgs = []
        for i in range(3):
            for j in range(3):
                if i != j:
                    msgs.append(Arrow(nodes[i].get_center(), nodes[j].get_center(),
                                      buff=0.55, stroke_width=2, color=DIM,
                                      tip_length=0.15).set_opacity(0.4))
        self.play(*[Create(n) for n in nodes],
                  *[FadeIn(l) for l in node_labels], run_time=1.0)
        self.play(*[Create(m) for m in msgs], run_time=1.2)
        bad = Arrow(nodes[0].get_center(), nodes[2].get_center(), buff=0.55,
                    stroke_width=5, color=RED, tip_length=0.2)
        bad_label = txt("the interleaving your tests never see",
                        size=20, color=RED).to_edge(DOWN, buff=0.7)
        self.play(Create(bad), FadeIn(bad_label), run_time=1.0)
        self.play(ShowPassingFlash(bad.copy().set_color(RED), time_width=0.5),
                  run_time=1.0)
        fill(self, seg[2], 4.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)


class Scene2_Problem(Scene):
    def construct(self):
        self.camera.background_color = BG
        seg = [8.73, 5.34, 8.41, 10.17]

        # Seg 0: the verification triangle
        self.add_subcaption("The gold standard is formal verification. You "
                            "write a specification, an implementation, and a "
                            "machine-checked proof that they always agree.",
                            duration=seg[0])
        spec = txt("SPEC", size=30, color=BLUE, weight=BOLD).move_to(UP * 2.2)
        impl = txt("IMPL", size=30, color=PURPLE, weight=BOLD).move_to(DL * 1.8 + LEFT * 1.4)
        proof = txt("PROOF", size=30, color=GREEN, weight=BOLD).move_to(DR * 1.8 + RIGHT * 1.4)
        e1 = Line(impl.get_top() + UP * 0.1, spec.get_bottom() + DOWN * 0.1,
                  color=DIM, stroke_width=2)
        e2 = Line(proof.get_top() + UP * 0.1, spec.get_bottom() + DOWN * 0.1,
                  color=DIM, stroke_width=2)
        e3 = Line(impl.get_right() + RIGHT * 0.1, proof.get_left() + LEFT * 0.1,
                  color=DIM, stroke_width=2)
        agree = txt("proof: impl satisfies spec, always", size=20, color=DIM)
        agree.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(spec, scale=1.2), run_time=0.8)
        self.play(FadeIn(impl, scale=1.2), run_time=0.8)
        self.play(FadeIn(proof, scale=1.2), run_time=0.8)
        self.play(Create(e1), Create(e2), Create(e3), FadeIn(agree), run_time=1.2)
        fill(self, seg[0], 3.6)

        # Seg 1: months to years
        self.add_subcaption("The catch: doing this by hand takes experts "
                            "months, sometimes years, per system.",
                            duration=seg[1])
        cost = txt("months → years of expert effort", size=30, color=YELLOW,
                   weight=BOLD).to_edge(UP, buff=0.7)
        self.play(FadeIn(cost, shift=DOWN * 0.3), run_time=1.0)
        self.play(Indicate(proof, color=YELLOW, scale_factor=1.15), run_time=1.2)
        fill(self, seg[1], 2.2)

        # Seg 2: SOTA agents 2/7
        self.add_subcaption("So can today's coding agents just do it for us? "
                            "Not really. Given seven key-value store "
                            "specifications, state of the art agents "
                            "verified only two.", duration=seg[2])
        self.play(FadeOut(Group(spec, impl, proof, e1, e2, e3, agree, cost)),
                  run_time=0.7)
        score_title = txt("7 key-value store specs, same budget", size=26,
                          color=FG).to_edge(UP, buff=0.9)
        rows = []
        for i, (name, n, color) in enumerate([("Codex", 2, RED),
                                              ("Claude Code", 2, RED)]):
            label = txt(name, size=24, color=FG)
            cells = Group(*[Square(0.45, stroke_color=DIM, stroke_width=1.5,
                                   fill_color=(color if k < n else BG),
                                   fill_opacity=(0.9 if k < n else 0.2))
                            for k in range(7)]).arrange(RIGHT, buff=0.12)
            count = txt(f"{n}/7", size=24, color=color, weight=BOLD)
            row = Group(label, cells, count).arrange(RIGHT, buff=0.5)
            rows.append(row)
        table = Group(*rows).arrange(DOWN, buff=0.6, aligned_edge=RIGHT)
        table.move_to(DOWN * 0.4)
        self.play(FadeIn(score_title), run_time=0.8)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=1.0)
        fill(self, seg[2], 2.8)

        # Seg 3: code first, then a proof cliff
        self.add_subcaption("And the failure mode is structural. They write "
                            "all the code first, then face the entire proof "
                            "at once. A sheer cliff, with no feedback along "
                            "the way.", duration=seg[3])
        self.play(FadeOut(Group(score_title, table)), run_time=0.6)
        steps = Group(*[Square(0.4, stroke_color=PURPLE, stroke_width=2,
                               fill_color=PURPLE, fill_opacity=0.5)
                        for _ in range(6)]).arrange(RIGHT, buff=0.25)
        steps.move_to(LEFT * 3.2 + DOWN * 1.6)
        steps_label = txt("write ALL the code", size=20, color=PURPLE)
        steps_label.next_to(steps, DOWN, buff=0.3)
        wall = Rectangle(width=2.6, height=4.4, stroke_color=GREEN,
                         stroke_width=3, fill_color=GREEN, fill_opacity=0.15)
        wall.move_to(RIGHT * 3.6 + UP * 0.4)
        wall_label = txt("THE ENTIRE\nPROOF", size=26, color=GREEN,
                         weight=BOLD).move_to(wall.get_center())
        nofb = txt("no feedback until the very end", size=20, color=RED)
        nofb.to_edge(DOWN, buff=0.55)
        for sq in steps:
            self.play(FadeIn(sq), run_time=0.25)
        self.play(FadeIn(steps_label), run_time=0.6)
        self.play(Create(wall), FadeIn(wall_label), run_time=1.4)
        self.play(FadeIn(nofb), Flash(wall.get_left(), color=RED,
                                      flash_radius=0.6), run_time=1.0)
        fill(self, seg[3], 5.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)


class Scene3_Insight(Scene):
    """FLAGSHIP: spec complete from the start; impl and proof grow together."""

    def construct(self):
        self.camera.background_color = BG
        seg = [10.45, 7.62, 13.70, 11.42, 9.61]
        PW, PH = 4.15, 4.7

        # Seg 0: title, then panels appear
        self.add_subcaption("This paper's idea is called Inductive Deductive "
                            "Synthesis, or IDS. The key insight: don't build "
                            "the proof after the code. Grow them together, "
                            "incrementally.", duration=seg[0])
        big = txt("Inductive Deductive Synthesis", size=40, color=FG,
                  weight=BOLD)
        sub = txt("grow the code and its proof together", size=26, color=DIM)
        sub.next_to(big, DOWN, buff=0.4)
        self.play(Write(big), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        header = txt("IDS: grow code and proof together", size=26, color=FG,
                     weight=BOLD).to_edge(UP, buff=0.35)
        spec_rect, spec_label = panel("SPEC", BLUE, PW, PH)
        impl_rect, impl_label = panel("IMPL", PURPLE, PW, PH)
        proof_rect, proof_label = panel("PROOF", GREEN, PW, PH)
        for rect, label, x in [(spec_rect, spec_label, -4.55),
                               (impl_rect, impl_label, 0.0),
                               (proof_rect, proof_label, 4.55)]:
            rect.move_to(RIGHT * x + DOWN * 0.55)
            label.next_to(rect, UP, buff=0.18)
        self.play(FadeOut(big), FadeOut(sub), FadeIn(header), run_time=0.8)
        self.play(Create(spec_rect), FadeIn(spec_label),
                  Create(impl_rect), FadeIn(impl_label),
                  Create(proof_rect), FadeIn(proof_label), run_time=1.4)
        fill(self, seg[0], 6.6)

        # Seg 1: full spec appears; impl and proof are empty
        self.add_subcaption("You start with the full specification, every "
                            "property the system must satisfy, an empty "
                            "implementation, and an empty proof.",
                            duration=seg[1])
        spec_src = [("Parameter t : Type.", FG),
                    ("Parameter init : t.", FG),
                    ("Parameter inc : t -> t.", FG),
                    ("Parameter read : t -> nat.", FG),
                    ("", FG),
                    ("Axiom read_init :", BLUE),
                    ("  read init = 0.", BLUE),
                    ("Axiom read_inc :", BLUE),
                    ("  read (inc s) = S (read s).", BLUE)]
        spec_code = code_lines(spec_src, spec_rect, size=14, spacing=0.36)
        empty_i = txt("(empty)", size=18, color=DIM).move_to(impl_rect)
        empty_p = txt("(empty)", size=18, color=DIM).move_to(proof_rect)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15)
                                for l in spec_code if l.text], lag_ratio=0.12),
                  run_time=2.4)
        self.play(FadeIn(empty_i), FadeIn(empty_p), run_time=0.8)
        fill(self, seg[1], 3.2)

        # Rocq badge, used from seg 2 on
        badge = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.62,
                                 stroke_color=FG, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
        badge.to_edge(DOWN, buff=0.28)
        badge_text = txt("Rocq type-checker", size=17, color=FG)
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

        # Seg 2: first joint step; Admitted IOUs appear
        self.add_subcaption("The agent takes a small step: define one piece "
                            "of the implementation, and prove one small "
                            "property about it. Anything unfinished is "
                            "marked with an explicit placeholder. An I O U, "
                            "called Admitted.", duration=seg[2])
        impl_src = [("Definition t := list unit.", FG),
                    ("Definition init := nil.", FG),
                    ("Definition read s := length s.", FG),
                    ("Definition inc (s : t) : t.", FG),
                    ("Admitted.", YELLOW)]
        proof_src = [("Theorem read_init :", FG),
                     ("  read init = 0.", FG),
                     ("Proof. reflexivity. Qed.", GREEN),
                     ("", FG),
                     ("Theorem read_inc :", FG),
                     ("  read (inc s) = S (read s).", FG),
                     ("Admitted.", YELLOW)]
        impl_code = code_lines(impl_src, impl_rect, size=14, spacing=0.36)
        proof_code = code_lines(proof_src, proof_rect, size=14, spacing=0.36)
        used = 0.0
        self.play(FadeOut(empty_i), FadeOut(empty_p), FadeIn(rocq),
                  run_time=0.6)
        used += 0.6
        # step 1: representation
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15)
                                for l in impl_code[0:2]], lag_ratio=0.15),
                  run_time=1.2)
        used += 1.2 + grade()
        # step 2: read + its first proof; proven axiom pulses in the spec
        self.play(FadeIn(impl_code[2], shift=RIGHT * 0.15), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15)
                                for l in proof_code[0:3]], lag_ratio=0.15),
                  run_time=1.2)
        used += 2.1 + grade(extra=[Indicate(Group(spec_code[5], spec_code[6]),
                                            color=BLUE, scale_factor=1.08)])
        # IOUs: inc deferred, read_inc deferred
        iou1 = SurroundingRectangle(Group(*impl_code[3:5]), color=YELLOW,
                                    stroke_width=2, buff=0.08)
        iou2 = SurroundingRectangle(Group(*proof_code[4:7]), color=YELLOW,
                                    stroke_width=2, buff=0.08)
        self.play(LaggedStart(*[FadeIn(l) for l in impl_code[3:5]],
                              *[FadeIn(l) for l in proof_code[4:7]],
                              lag_ratio=0.1), run_time=1.5)
        iou_tag = txt("Admitted = an IOU", size=20, color=YELLOW, weight=BOLD)
        iou_tag.next_to(badge, LEFT, buff=0.6)
        self.play(Create(iou1), Create(iou2), FadeIn(iou_tag), run_time=1.0)
        used += 2.5 + grade()
        fill(self, seg[2], used)

        # Seg 3: the checker grades every partial state
        self.add_subcaption("And here's the trick. The Rocq proof assistant "
                            "grades every partial state. If the file "
                            "type-checks, the design is still viable, so the "
                            "agent banks the progress and takes another "
                            "step.", duration=seg[3])
        self.play(FadeOut(iou_tag), run_time=0.4)
        spotlight = SurroundingRectangle(badge, color=GREEN, stroke_width=3,
                                         buff=0.12)
        verdict = txt("type-checks → design still viable", size=20,
                      color=GREEN)
        verdict.next_to(badge, LEFT, buff=0.5)
        self.play(Create(spotlight), run_time=0.8)
        self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.8)
        beams = [DashedLine(badge.get_top(), r.get_bottom(), color=GREEN,
                            stroke_width=2).set_opacity(0.6)
                 for r in [impl_rect, proof_rect]]
        self.play(*[Create(b) for b in beams], run_time=0.9)
        self.play(*[ShowPassingFlash(b.copy().set_color(GREEN),
                                     time_width=0.4) for b in beams],
                  run_time=1.2)
        banked = txt("progress banked ✓", size=20, color=DIM)
        banked.next_to(badge, RIGHT, buff=0.5)
        self.play(FadeIn(banked), run_time=0.7)
        fill(self, seg[3], 4.8)

        # Seg 4: IOUs get paid off; fully implemented and proven
        self.add_subcaption("A bit more implementation. A bit more proof. "
                            "Step by step the I O Us get paid off, until the "
                            "specification is fully implemented, and fully "
                            "proven.", duration=seg[4])
        self.play(FadeOut(Group(spotlight, verdict, banked, *beams)),
                  run_time=0.5)
        inc_fill = code_lines([("Definition inc (s : t) := tt::s.", GREEN)],
                              impl_rect, size=14, spacing=0.36, start_row=3)
        proof_fill = code_lines([("Proof. intros s. simpl.", GREEN),
                                 ("  reflexivity. Qed.", GREEN)],
                                proof_rect, size=14, spacing=0.36, start_row=6)
        iou1_paid = SurroundingRectangle(inc_fill[0], color=GREEN,
                                         stroke_width=2, buff=0.08)
        iou2_paid = SurroundingRectangle(Group(*proof_code[4:6], *proof_fill),
                                         color=GREEN, stroke_width=2,
                                         buff=0.08)
        used = 0.5
        self.play(FadeOut(impl_code[3]), FadeOut(impl_code[4]),
                  FadeIn(inc_fill[0]),
                  Transform(iou1, iou1_paid), run_time=1.0)
        used += 1.0 + grade()
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
            color=GREEN, stroke_width=3, buff=0.25, corner_radius=0.2)
        self.play(FadeOut(iou1), FadeOut(iou2), Create(glow), FadeIn(done),
                  run_time=1.4)
        used += 1.4
        fill(self, seg[4], used)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)


class Scene4_Backtrack(Scene):
    def construct(self):
        self.camera.background_color = BG
        seg = [10.54, 11.98]

        # Seg 0: a failing step is a signal, caught early
        self.add_subcaption("What if a step fails? That's not wasted work. "
                            "It's signal. A partial proof that gets stuck "
                            "rules out a dead-end design before more effort "
                            "is piled on top.", duration=seg[0])
        header = txt("failed steps are signal", size=30, color=FG,
                     weight=BOLD).to_edge(UP, buff=0.6)
        root = Circle(radius=0.28, stroke_color=FG, stroke_width=2.5,
                      fill_color=BG, fill_opacity=1).move_to(UP * 1.6)
        n1 = root.copy().set_stroke(GREEN).move_to(UP * 0.3 + LEFT * 1.2)
        n2 = root.copy().set_stroke(GREEN).move_to(DOWN * 1.0 + LEFT * 2.0)
        bad = root.copy().set_stroke(RED).move_to(DOWN * 1.0 + LEFT * 0.2)
        e1 = Line(root.get_bottom(), n1.get_top(), color=DIM, stroke_width=2)
        e2 = Line(n1.get_bottom(), n2.get_top(), color=DIM, stroke_width=2)
        e3 = Line(n1.get_bottom(), bad.get_top(), color=DIM, stroke_width=2)
        cross = txt("✗", size=34, color=RED, weight=BOLD).move_to(bad)
        early = txt("dead end — found early, cheaply", size=22, color=RED)
        early.next_to(bad, RIGHT, buff=0.6)
        self.play(FadeIn(header), Create(root), run_time=1.0)
        self.play(Create(e1), Create(n1), run_time=0.8)
        self.play(Create(e2), Create(n2), run_time=0.8)
        self.play(Create(e3), Create(bad), run_time=0.8)
        self.play(FadeIn(cross, scale=1.5), FadeIn(early), run_time=0.9)
        fill(self, seg[0], 4.3)

        # Seg 1: backtrack and pivot — split per key
        self.add_subcaption("IDS backtracks to the last good state and "
                            "pivots. When one big monolithic store made the "
                            "proof intractable, it split the data per key, "
                            "and the proof fell apart into small, easy "
                            "cases.", duration=seg[1])
        self.play(FadeOut(Group(cross, early)),
                  bad.animate.set_opacity(0.25), e3.animate.set_opacity(0.25),
                  Indicate(n1, color=YELLOW), run_time=1.2)
        alt = Circle(radius=0.28, stroke_color=GREEN, stroke_width=2.5,
                     fill_color=BG, fill_opacity=1).move_to(DOWN * 1.0 + RIGHT * 1.2)
        e4 = Line(n1.get_bottom(), alt.get_top(), color=GREEN, stroke_width=2)
        self.play(Create(e4), Create(alt), run_time=0.9)
        mono = Rectangle(width=2.2, height=1.5, stroke_color=RED,
                         stroke_width=2.5, fill_opacity=0.1, fill_color=RED)
        mono.move_to(RIGHT * 3.9 + UP * 1.2)
        mono_label = txt("one big store", size=18, color=RED)
        mono_label.next_to(mono, UP, buff=0.2)
        self.play(Create(mono), FadeIn(mono_label), run_time=0.9)
        keys = VGroup(*[Square(0.7, stroke_color=GREEN, stroke_width=2,
                               fill_color=GREEN, fill_opacity=0.12)
                        for _ in range(3)]).arrange(RIGHT, buff=0.3)
        keys.move_to(RIGHT * 3.9 + DOWN * 1.3)
        key_labels = Group(*[txt(k, size=16, color=GREEN).move_to(sq)
                             for k, sq in zip(["k1 ✓", "k2 ✓", "k3 ✓"], keys)])
        keys_label = txt("split per key → small, easy cases", size=18,
                         color=GREEN).next_to(keys, DOWN, buff=0.25)
        self.play(ReplacementTransform(mono.copy(), keys),
                  FadeIn(key_labels), run_time=1.4)
        self.play(FadeIn(keys_label), run_time=0.8)
        fill(self, seg[1], 5.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)


class Scene5_Results(Scene):
    def construct(self):
        self.camera.background_color = BG
        seg = [8.59, 8.82, 8.27]

        # Seg 0: 7/7 vs 2/7
        self.add_subcaption("The results: IDS verified all seven "
                            "specifications. Seven out of seven, where the "
                            "best coding agents managed two.", duration=seg[0])
        title = txt("7 key-value store specs", size=28, color=FG,
                    weight=BOLD).to_edge(UP, buff=0.6)
        rows = []
        for name, n, color in [("Codex", 2, DIM), ("Claude Code", 2, DIM),
                               ("IDS", 7, GREEN)]:
            label = txt(name, size=24,
                        color=FG if color == GREEN else DIM)
            cells = Group(*[Square(0.5, stroke_color=DIM, stroke_width=1.5,
                                   fill_color=(color if k < n else BG),
                                   fill_opacity=(0.9 if k < n else 0.15))
                            for k in range(7)]).arrange(RIGHT, buff=0.14)
            count = txt(f"{n}/7", size=26, color=color, weight=BOLD)
            rows.append(Group(label, cells, count).arrange(RIGHT, buff=0.5))
        table = Group(*rows).arrange(DOWN, buff=0.55, aligned_edge=RIGHT)
        table.move_to(DOWN * 0.3)
        self.play(FadeIn(title), run_time=0.7)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.3), run_time=0.8)
        self.play(Indicate(rows[2], color=GREEN, scale_factor=1.06),
                  run_time=1.0)
        fill(self, seg[0], 4.1)

        # Seg 1: hours and dollars vs months
        self.add_subcaption("On average, six point eight hours and about a "
                            "hundred dollars per system. Against months of "
                            "expert effort, that's roughly two hundred times "
                            "faster.", duration=seg[1])
        self.play(FadeOut(Group(title, table)), run_time=0.6)
        stats = Group(txt("6.8 hours", size=44, color=GREEN, weight=BOLD),
                      txt("$106", size=44, color=GREEN, weight=BOLD))
        stats.arrange(RIGHT, buff=1.6).move_to(UP * 0.8)
        per = txt("per verified system", size=22, color=DIM)
        per.next_to(stats, DOWN, buff=0.35)
        vs = txt("vs months of expert effort  →  ~200× faster", size=26,
                 color=FG).move_to(DOWN * 1.3)
        self.play(FadeIn(stats[0], scale=1.2), run_time=0.8)
        self.play(FadeIn(stats[1], scale=1.2), run_time=0.8)
        self.play(FadeIn(per), run_time=0.6)
        self.play(FadeIn(vs, shift=UP * 0.2), run_time=1.0)
        fill(self, seg[1], 3.8)

        # Seg 2: up to 3x throughput
        self.add_subcaption("And because IDS benchmarks candidates as it "
                            "goes, its verified implementations run up to "
                            "three times faster than published, hand-written "
                            "ones.", duration=seg[2])
        self.play(FadeOut(Group(stats, per, vs)), run_time=0.6)
        base = Rectangle(width=1.4, height=1.2, stroke_color=DIM,
                         stroke_width=2, fill_color=DIM, fill_opacity=0.4)
        fast = Rectangle(width=1.4, height=3.6, stroke_color=GREEN,
                         stroke_width=2, fill_color=GREEN, fill_opacity=0.5)
        base.move_to(LEFT * 1.6 + DOWN * 1.0, aligned_edge=DOWN)
        fast.move_to(RIGHT * 1.6 + DOWN * 1.0, aligned_edge=DOWN)
        base_l = txt("hand-written\nreference", size=18, color=DIM)
        base_l.next_to(base, DOWN, buff=0.3)
        fast_l = txt("IDS", size=20, color=GREEN, weight=BOLD)
        fast_l.next_to(fast, DOWN, buff=0.3)
        x3 = txt("up to 3× throughput", size=28, color=GREEN, weight=BOLD)
        x3.to_edge(UP, buff=0.8)
        self.play(FadeIn(base), FadeIn(base_l), run_time=0.8)
        self.play(GrowFromEdge(fast, DOWN), FadeIn(fast_l), run_time=1.2)
        self.play(FadeIn(x3, shift=DOWN * 0.2), run_time=0.8)
        fill(self, seg[2], 3.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)


class Scene6_Outro(Scene):
    def construct(self):
        self.camera.background_color = BG
        seg = [10.03, 7.34]

        # Seg 0: recap motif
        self.add_subcaption("Verified software used to be a human-labor "
                            "bottleneck. IDS turns it into a compute "
                            "problem. Grow the code and its proof together, "
                            "and let the checker keep score.", duration=seg[0])
        mini = []
        for name, color, x in [("SPEC", BLUE, -3.4), ("IMPL", PURPLE, 0.0),
                               ("PROOF", GREEN, 3.4)]:
            r = RoundedRectangle(corner_radius=0.12, width=2.4, height=1.5,
                                 stroke_color=color, stroke_width=2.5,
                                 fill_opacity=0.08, fill_color=color)
            r.move_to(RIGHT * x + UP * 0.9)
            t = txt(name, size=22, color=color, weight=BOLD).move_to(r)
            mini.append(Group(r, t))
        check = txt("✓", size=40, color=GREEN, weight=BOLD).move_to(DOWN * 1.0)
        line1 = txt("human-labor bottleneck  →  compute problem", size=26,
                    color=FG).move_to(DOWN * 2.2)
        self.play(LaggedStart(*[FadeIn(m, scale=1.1) for m in mini],
                              lag_ratio=0.25), run_time=1.6)
        self.play(FadeIn(check, scale=1.4), run_time=0.8)
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=1.0)
        fill(self, seg[0], 3.4)

        # Seg 1: title card
        self.add_subcaption("The paper is Inductive Deductive Synthesis: "
                            "Enabling AI to Generate Formally Verified "
                            "Systems. Check it out to learn more.",
                            duration=seg[1])
        self.play(FadeOut(Group(*mini, check, line1)), run_time=0.6)
        t1 = txt("Inductive Deductive Synthesis:", size=32, color=FG,
                 weight=BOLD)
        t2 = txt("Enabling AI to Generate", size=32, color=FG, weight=BOLD)
        t3 = txt("Formally Verified Systems", size=32, color=FG, weight=BOLD)
        card = Group(t1, t2, t3).arrange(DOWN, buff=0.3).move_to(UP * 0.6)
        arxiv = txt("arXiv 2605.23109", size=24, color=BLUE)
        arxiv.next_to(card, DOWN, buff=0.7)
        affil = txt("UC Berkeley · Google · UC Santa Cruz", size=20,
                    color=DIM).next_to(arxiv, DOWN, buff=0.4)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.2)
        self.play(FadeIn(arxiv), FadeIn(affil), run_time=0.8)
        fill(self, seg[1], 2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.wait(0.3)
