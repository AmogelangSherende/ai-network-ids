import numpy as np


def perturb(X, strength, seed=0):
    """Randomly rescale attacker-controllable features by up to +/- strength."""
    rng = np.random.default_rng(seed)
    n = len(X)
    f_size, f_cnt, f_time = (
        rng.uniform(1 - strength, 1 + strength, n).astype("float32") for _ in range(3)
    )
    Xp = X.copy()

    # Move 1: pad or trim packets (size features move together)
    for col in ["Max Packet Length", "Packet Length Std", "Average Packet Size", "Subflow Fwd Bytes"]:
        Xp[col] = Xp[col] * f_size
    Xp["Packet Length Variance"] = Xp["Packet Length Std"] ** 2

    # Move 2: send more or fewer packets
    for col in ["Total Fwd Packets", "Subflow Fwd Packets"]:
        Xp[col] = Xp[col] * f_cnt

    # Move 3: slow down or speed up
    for col in ["Flow Duration", "Fwd IAT Max"]:
        Xp[col] = Xp[col] * f_time
    return Xp