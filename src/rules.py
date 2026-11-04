def rule_based_predict(X):
    """Hand-written detection rules, chosen using training data only."""
    r1 = X["Destination Port"].isin([21, 22])
    r2 = (X["Flow Duration"] > 1_000_000) & (X["Total Fwd Packets"] >= 3)
    return (r1 | r2).astype("int8")