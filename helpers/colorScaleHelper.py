def calculateColorScale(norm, gl_rh):
    if gl_rh:
        r = int(255 * norm)
        g = int(255 * (1 - norm))
    else:
        r = int(255 * norm)
        g = int(255 * (norm))
    return [r, g, 0]
