"""Light-theme render of the two core scenes, no audio.

Overrides the dark palette in script.py (GitHub-light-inspired colors),
then re-exports the scenes so manim can render them from this file.
"""
import script as s

s.BG = "#FFFFFF"
s.FG = "#1F2328"      # near-black text
s.DIM = "#57606A"     # muted gray
s.BLUE = "#0969DA"    # spec
s.PURPLE = "#8250DF"  # impl
s.GREEN = "#1A7F37"   # proof / success
s.YELLOW = "#9A6700"  # Admitted IOUs (amber, readable on white)
s.RED = "#CF222E"     # failure

class Scene3_Insight(s.Scene3_Insight):
    pass


class Scene4_Backtrack(s.Scene4_Backtrack):
    pass
