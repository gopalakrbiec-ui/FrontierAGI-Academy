# Screenshot scaling for computer use, after the pattern in Anthropic's computer use tool docs
# (earlier-model limits: long edge 1,568 px, about 1.15 megapixels). Standard library only.
import math

def scale_factor(w, h, long_edge=1568, max_pixels=1_150_000):
    return min(1.0, long_edge / max(w, h), math.sqrt(max_pixels / (w * h)))

for name, (w, h) in {"MacBook 1512x982": (1512, 982), "Full HD 1920x1080": (1920, 1080), "4K 3840x2160": (3840, 2160)}.items():
    s = scale_factor(w, h)
    sw, sh = int(w * s), int(h * s)
    # the model answers in scaled coordinates; map a click back to the real screen
    cx, cy = 600, 400
    print(f"{name}: send {sw}x{sh} (scale {s:.3f}); model click ({cx},{cy}) -> screen ({round(cx / s)},{round(cy / s)})")
