greek = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ε",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "omicron": "ο",
    "pi": "π",
    "rho": "ρ",
    "sigma": "σ",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "φ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
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


vitamin_a = ["Retinol"] + expand_greeks("beta-Carotene")
vitamin_c = ["ascorbic acid"]
