from typing import Tuple

import colorsys

def rgb_to_hls (r : int, g : int, b : int) -> Tuple[float, float, float] :
	r, g, b = [x / 255.0 for x in [r, g, b]]
	h, l, s = colorsys.rgb_to_hls(r, g, b)
	h, l, s = [x * 255.0 for x in [h, l, s]]

	return h, l, s

def hls_to_rgb (h : float, l : float, s : float) -> Tuple[float, float, float] :
	h, l, s = [x / 255.0 for x in [h, l, s]]
	r, g, b = colorsys.hls_to_rgb(h, l, s)
	r, g, b = [x * 255.0 for x in [r, g, b]]

	return r, g, b

def rgb_to_l (r : int, g : int, b : int) -> float :
	if r > g :
		maxval = max(r, b)
		minval = min(g, b)
	else :
		maxval = max(g, b)
		minval = min(r, b)

	return (int(maxval) + int(minval)) / 2.0
