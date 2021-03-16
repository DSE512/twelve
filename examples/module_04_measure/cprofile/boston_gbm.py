from sklearn import datasets
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


def load_boston_data():
    boston = datasets.load_boston()
    return boston.data, boston.target


def build_model():
    hparams = {
        'n_estimators': 500,
        'max_depth': 4,
        'min_samples_split': 5,
        'learning_rate': 0.01,
        'loss': 'ls'
    }

    model = GradientBoostingRegressor(**hparams)

    return model


def main():
    data, target = load_boston_data()

    x_train, x_valid, y_train, y_valid = train_test_split(
        data, target, test_size=0.33, random_state=42
    )

    model = build_model()

    model.fit(x_train, y_train)
    preds = model.predict(x_valid)

    mse = mean_squared_error(y_valid, preds)
    print(f"The mean squared error (MSE) on test set: {mse:.4f}")


if __name__=="__main__":
    main()
