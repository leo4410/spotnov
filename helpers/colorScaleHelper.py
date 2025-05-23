def calculateColorScale(norm):
    r = int(255 * norm)
    g = int(255 * (1 - norm))
    return [r, g, 0]
