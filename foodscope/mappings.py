alpha = "α"
beta = "β"
gamma = "γ"
delta = "δ"
epsilon = "ε"

greek = {
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "delta": delta,
    "epsilon": epsilon,
}


def expand_greeks(word, delimiter="-"):
    """Return list of all permutations of word with
    greek letters substituted or not
    """
    parts = word.split(delimiter)
    result = [parts]
    for i, token in enumerate(parts):
        temp = []
        for r in result:
            r = r.copy()
            if token in greek:
                r[i] = greek[token]
                temp.append(r)
        result.extend(temp)

    return [delimiter.join(r) for r in result]


# TODO: map "alpha" to alpha and use in search automatically

vitamin_a = ["Retinol"] + expand_greeks("beta-Carotene")
