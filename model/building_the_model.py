import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    roc_auc_score,
)
from os import path
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Input, PReLU, Normalization
from keras.optimizers import Adam
from keras.regularizers import l2


def _load_data(file_path: str) -> tuple:
    """
    Load data from a CSV file.

    Args:
    :argument: file_path (str): Path to the CSV file.

    Returns:
    :return: tuple: A tuple containing numpy arrays for features and target.

    Throws:
    :raise: FileNotFoundError
    """
    if not path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")
    dataset = np.loadtxt(file_path, delimiter=',')
    dataset_values = dataset[:, 0:13]
    dataset_win = dataset[:, 13]
    return dataset_values, dataset_win


class NeuralNetworkClassifier:
    def __init__(self, path_train: str, path_test: str, path_val: str) -> None:
        """
        Initialize the NeuralNetworkClassifier.

        Args:
        :argument: path_train (str): Path to the training dataset.
        :argument: path_test (str): Path to the testing dataset.
        :argument: path_val (str): Path to the validation dataset.

        Returns:
        :return: None
        """
        self.dataset_train_values, self.dataset_train_win = _load_data(path_train)
        self.dataset_test_values, self.dataset_test_win = _load_data(path_test)
        self.dataset_val_values, self.dataset_val_win = _load_data(path_val)

        self.model = None

    def build_model(self) -> None:
        """
        Build the neural network model.

        Returns:
        :return: None
        """
        input_layer = Input(shape=(13,))
        norm_layer = Normalization()
        norm_layer.adapt(self.dataset_train_values)

        model = Sequential()
        model.add(input_layer)
        model.add(norm_layer)
        model.add(Dense(64, input_shape=(13,), activation='elu', activity_regularizer=l2(0.002)))
        model.add(PReLU())
        model.add(Dense(32, activation='sigmoid', activity_regularizer=l2(0.0001)))
        model.add(Dense(16, activation='sigmoid', activity_regularizer=l2(0.0001)))
        model.add(Dense(1, activation='sigmoid', activity_regularizer=l2(0.0001)))

        new_learning_rate = 0.001
        optimizer = Adam(learning_rate=new_learning_rate)

        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model = model

    def build_the_model(self,use_PReLu: bool, first_neurons: int, first_activation: str, first_lambda: float,
                        second_neurons: int, second_activation: str, second_lambda: float, third_neurons: int,
                        third_activation: str, third_lambda: float, output_activation: str, output_lambda: float)\
            -> None:

        input_layer = Input(shape=(13,))
        norm_layer = Normalization()
        norm_layer.adapt(self.dataset_train_values)

        model = Sequential()
        model.add(input_layer)
        model.add(norm_layer)
        model.add(Dense(first_neurons, activation=first_activation, activity_regularizer=l2(first_lambda)))
        if use_PReLu:
            model.add(PReLU())
        model.add(Dense(second_neurons, activation=second_activation, activity_regularizer=l2(second_lambda)))
        model.add(Dense(third_neurons, activation=third_activation, activity_regularizer=l2(third_lambda)))
        model.add(Dense(1, activation=output_activation, activity_regularizer=l2(output_lambda)))

        new_learning_rate = 0.001
        optimizer = Adam(learning_rate=new_learning_rate)

        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model = model

    def train(self, epochs: int = 150, batch_size: int = 1024) -> None:
        """
        Train the neural network model.

        Args:
        :argument: epochs (int): Number of epochs for training.
        :argument: batch_size (int): Batch size for training.

        Returns:
        :return: None
        """
        if self.model is None:
            self.build_model()

        self.model.fit(x=self.dataset_train_values, y=self.dataset_train_win, epochs=epochs, batch_size=batch_size,
                       validation_data=(self.dataset_val_values, self.dataset_val_win), verbose=0)

    def predict(self) -> np.ndarray:
        """
        Make predictions using the trained model.

        Returns:
        :return: np.ndarray: Predicted values.
        """
        if self.model is None:
            raise ValueError("model has not been trained yet.")

        return self.model.predict(self.dataset_test_values)

    def evaluate(self, y_pred: np.ndarray) -> tuple:
        """
        Evaluate the performance of the model.

        Args:
        :argument: y_pred (np.ndarray): Predicted values.

        Returns:
        :return: tuple: Accuracy, precision, recall, F1-score, and confusion matrix.
        """
        accuracy = accuracy_score(self.dataset_test_win, y_pred.round())
        precision = precision_score(self.dataset_test_win, y_pred.round())
        recall = recall_score(self.dataset_test_win, y_pred.round())
        f1 = f1_score(self.dataset_test_win, y_pred.round())
        conf_matrix = confusion_matrix(self.dataset_test_win, y_pred.round())
        return accuracy, precision, recall, f1, conf_matrix

    def plot_roc_curve(self, y_pred: np.ndarray) -> None:
        """
        Plot the ROC curve.

        Args:
        :argument: y_pred (np.ndarray): Predicted values.

        Returns:
        :return: None
        """
        fpr, tpr, thresholds = roc_curve(self.dataset_test_win, y_pred)
        auc_score = roc_auc_score(self.dataset_test_win, y_pred)

        plt.figure().canvas.manager.set_window_title("ROC Curve")
        plt.plot(fpr, tpr, label='AUC-Score: ' + str(round(auc_score, 2)), color='#1260CC')
        plt.plot([0, 1], [0, 1], 'r--', label='Random: 0.5')
        plt.axis((0, 1, 0, 1))
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc='best')
        plt.savefig('Images/curve')
        plt.close()
