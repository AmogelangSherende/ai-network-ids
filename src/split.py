from sklearn.model_selection import train_test_split

from src.load_data import load_all

NON_FEATURES = ["Label", "Day", "is_attack"]


def get_split(test_size=0.3, seed=42):
    df = load_all()
    features = [c for c in df.columns if c not in NON_FEATURES]

    train, test = train_test_split(
        df, test_size=test_size, random_state=seed, stratify=df["Label"]
    )
    return (train[features], test[features],
            train["is_attack"], test["is_attack"],
            train["Label"], test["Label"])