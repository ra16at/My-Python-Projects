import os
import numpy as np
from tensorflow import keras
from keras import layers
import tkinter as tk
from PIL import Image, ImageDraw, ImageOps, ImageChops

import pickle
import random
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping

MODEL_PATH = "mnist_digit_model.keras"
DATA_PATH = "my_digits.pkl"
N_CLASSES = 11  # 0-9 digits + 1 for 'Not a Number'

# ---------------------------
# Model loading/training
# ---------------------------
def train_or_load_model():
    """
    Loads a trained model if available, otherwise trains on MNIST and saves it.
    """
    keras_model_path = "mnist_digit_model.keras"
    if os.path.exists(keras_model_path):
        print("Loading trained model (.keras format)...")
        model = keras.models.load_model(keras_model_path)
    else:
        print("Training model on MNIST...")
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train = x_train.astype("float32") / 255.0
        x_test = x_test.astype("float32") / 255.0
        x_train = x_train.reshape(-1, 28*28)
        x_test = x_test.reshape(-1, 28*28)

        model = keras.Sequential([
            layers.Input(shape=(784,)),
            layers.Dense(128, activation="relu"),
            layers.Dense(10, activation="softmax")
        ])
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)
        model.save(keras_model_path)
        print("Model trained and saved as .keras.")
    return model

# ---------------------------
# Data augmentation for better accuracy
# ---------------------------
def augment_image(img_arr):
    """
    Applies random rotation, shift, and noise to an image array.
    """
    img = Image.fromarray((img_arr * 255).astype(np.uint8))
    # Random rotation
    angle = random.uniform(-15, 15)
    img = img.rotate(angle)
    # Random shift
    dx = random.randint(-2, 2)
    dy = random.randint(-2, 2)
    img = ImageChops.offset(img, dx, dy)
    # Add random noise
    arr = np.array(img).astype(np.float32) / 255.0
    arr += np.random.normal(0, 0.02, arr.shape)
    arr = np.clip(arr, 0, 1)
    return arr

def train_on_my_digits():
    """
    Trains a model on your own collected digits, with augmentation.
    """
    if not os.path.exists(DATA_PATH):
        print("No data found! Collect digits first.")
        return
    with open(DATA_PATH, "rb") as f:
        data = pickle.load(f)
    X = []
    y = []
    for arr, label in data:
        X.append(arr.flatten())
        y.append(label)
        # Augment each sample 4 times
        for _ in range(4):
            aug = augment_image(arr)
            X.append(aug.flatten())
            y.append(label)
    X = np.array(X)
    y = np.array(y)
    print(f"Training on {len(X)} samples (with augmentation)...")
    model = keras.Sequential([
        layers.Input(shape=(784,)),
        layers.Dense(256, activation="relu"),
        layers.Dense(128, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    # Use EarlyStopping to stop when validation loss doesn't improve for 10 epochs
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = model.fit(X, y, epochs=200, batch_size=16, validation_split=0.2, callbacks=[early_stop])
    keras_model_path = "mnist_digit_model.keras"
    model.save(keras_model_path)
    print("Model trained and saved on your digits as .keras!")
    plot_training_history(history)

def train_on_mnist_and_my_digits():
    """
    Trains a model on both MNIST and your own collected digits, with augmentation for your digits.
    """
    # Load MNIST
    (x_train, y_train), _ = keras.datasets.mnist.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_train = x_train.reshape(-1, 28*28)
    y_train = y_train.astype("int64")

    # Load your digits
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "rb") as f:
            data = pickle.load(f)
        X_my = []
        y_my = []
        for arr, label in data:
            X_my.append(arr.flatten())
            y_my.append(label)
            # Augment each sample 4 times
            for _ in range(4):
                aug = augment_image(arr)
                X_my.append(aug.flatten())
                y_my.append(label)
        X_my = np.array(X_my)
        y_my = np.array(y_my)
        # Combine
        X_all = np.concatenate([x_train, X_my], axis=0)
        y_all = np.concatenate([y_train, y_my], axis=0)
        print(f"Training on {len(X_all)} samples (MNIST + your digits with augmentation)...")
    else:
        X_all = x_train
        y_all = y_train
        print(f"Training on {len(X_all)} MNIST samples (no user digits found).")

    # Build and train model
    model = keras.Sequential([
        layers.Input(shape=(784,)),
        layers.Dense(256, activation="relu"),
        layers.Dense(128, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    # Use EarlyStopping to stop when validation loss doesn't improve for 5 epochs
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(X_all, y_all, epochs=100, batch_size=32, validation_split=0.1, callbacks=[early_stop])
    keras_model_path = "mnist_digit_model.keras"
    model.save(keras_model_path)
    print("Model trained and saved on MNIST + your digits as .keras!")
    plot_training_history(history)
def plot_training_history(history):
    """
    Plots training and validation accuracy and loss in a new window.
    """
    plt.figure(figsize=(12,5))
    # Plot accuracy
    plt.subplot(1,2,1)
    plt.plot(history.history.get('accuracy', []), label='Train Acc')
    plt.plot(history.history.get('val_accuracy', []), label='Val Acc')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    # Plot loss
    plt.subplot(1,2,2)
    plt.plot(history.history.get('loss', []), label='Train Loss')
    plt.plot(history.history.get('val_loss', []), label='Val Loss')
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.tight_layout()
    plt.show()

def train_on_custom_folder(folder_path):
    """
    Trains the model on a custom dataset in the given folder.
    The folder should have subfolders named 0-9, each containing images of that digit.
    """
    X = []
    y = []
    for digit in range(10):
        digit_folder = os.path.join(folder_path, str(digit))
        if not os.path.isdir(digit_folder):
            continue
        for fname in os.listdir(digit_folder):
            fpath = os.path.join(digit_folder, fname)
            try:
                img = Image.open(fpath).convert('L').resize((28, 28))
                arr = np.array(img).astype('float32') / 255.0
                X.append(arr.flatten())
                y.append(digit)
            except Exception as e:
                print(f"Skipping {fpath}: {e}")
    X = np.array(X)
    y = np.array(y)
    print(f"Loaded {len(X)} images from {folder_path}")
    if len(X) == 0:
        print("No images found!")
        return
    model = keras.Sequential([
        layers.Input(shape=(784,)),
        layers.Dense(256, activation="relu"),
        layers.Dense(128, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model.fit(X, y, epochs=100, batch_size=16, validation_split=0.2, callbacks=[early_stop])
    model.save(MODEL_PATH)
    print("Model trained and saved on your custom dataset!")

# ---------------------------
# Tkinter Drawing App
# ---------------------------
class App(tk.Tk):
    """
    Tkinter app for drawing, saving, and guessing digits.
    """
    def __init__(self, model=None, collect_mode=False):
        super().__init__()
        self.title("Draw a digit (0-9)")
        self.canvas = tk.Canvas(self, width=280, height=280, bg='white')
        self.canvas.pack()
        self.button = tk.Button(self, text="Guess", command=self.guess)
        self.button.pack()
        self.clear_btn = tk.Button(self, text="Clear", command=self.clear)
        self.clear_btn.pack()
        self.label = tk.Label(self, text="Draw a digit, then click Guess")
        self.label.pack()
        self.image = Image.new("L", (280, 280), 255)
        self.draw = ImageDraw.Draw(self.image)
        
        # For smooth drawing
        self.last_x, self.last_y = None, None
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_paint)

        self.model = model
        self.collect_mode = collect_mode

        if collect_mode:
            self.label.config(text="Draw a digit, enter label, then click Save")
            self.label_entry = tk.Entry(self)
            self.label_entry.pack()
            self.save_btn = tk.Button(self, text="Save", command=self.save_digit)
            self.save_btn.pack()
            self.data = []
            if os.path.exists(DATA_PATH):
                with open(DATA_PATH, "rb") as f:
                    self.data = pickle.load(f)
            self.button.config(state="disabled")
        else:
            self.label_entry = None
            self.save_btn = None

    def paint(self, event):
        """
        Draws on the canvas and updates the image with smooth lines.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                   width=16, fill='black',
                                   capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                           fill=0, width=16)
        self.last_x = event.x
        self.last_y = event.y

    def reset_paint(self, event):
        """
        Resets the last drawing position.
        """
        self.last_x, self.last_y = None, None

    def clear(self):
        """
        Clears the canvas and resets the image.
        """
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.reset_paint(None) # Reset drawing coordinates
        if self.collect_mode:
            self.label.config(text="Draw a digit, enter label, then click Save")
        else:
            self.label.config(text="Draw a digit, then click Guess")

    def guess(self):
        """
        Processes the drawing and predicts the digit using the model.
        """
        img = self.image.resize((28, 28))
        img = ImageOps.invert(img)
        arr = np.array(img).astype("float32")
        # Binarize
        arr = (arr > 50) * 255
        # Find bounding box of the digit
        coords = np.column_stack(np.where(arr > 0))
        if coords.size:
            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0)
            cropped = arr[y0:y1+1, x0:x1+1].astype(np.uint8)
            # Ensure cropped is at least 2x2
            if cropped.shape[0] < 2 or cropped.shape[1] < 2:
                cropped = np.pad(cropped, ((0, max(0, 2-cropped.shape[0])), (0, max(0, 2-cropped.shape[1]))), 'constant')
            cropped_img = Image.fromarray(cropped).resize((20, 20), Image.LANCZOS)
            # Paste into center of 28x28
            new_img = Image.new("L", (28, 28), 0)
            new_img.paste(cropped_img, ((28-20)//2, (28-20)//2))
            arr = np.array(new_img).astype("float32") / 255.0
        else:
            arr = arr / 255.0
        arr = arr.reshape(1, 28*28)
        pred = np.argmax(self.model.predict(arr), axis=1)[0]
        self.label.config(text=f"AI Guess: {pred}")

    def save_digit(self):
        """
        Saves the drawn digit and its label to the dataset.
        """
        label = self.label_entry.get()
        if not label.isdigit() or not (0 <= int(label) <= 9):
            self.label.config(text="Please enter a digit label (0-9)!")
            return
        img = self.image.resize((28, 28))
        img = ImageOps.invert(img)
        arr = np.array(img).astype("float32")
        arr = (arr > 50) * 255
        coords = np.column_stack(np.where(arr > 0))
        if coords.size:
            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0)
            cropped = arr[y0:y1+1, x0:x1+1].astype(np.uint8)
            # Ensure cropped is at least 2x2
            if cropped.shape[0] < 2 or cropped.shape[1] < 2:
                cropped = np.pad(cropped, ((0, max(0, 2-cropped.shape[0])), (0, max(0, 2-cropped.shape[1]))), 'constant')
            cropped_img = Image.fromarray(cropped).resize((20, 20), Image.LANCZOS)
            new_img = Image.new("L", (28, 28), 0)
            new_img.paste(cropped_img, ((28-20)//2, (28-20)//2))
            arr = np.array(new_img).astype("float32") / 255.0
        else:
            arr = arr / 255.0
        self.data.append((arr, int(label)))
        with open(DATA_PATH, "wb") as f:
            pickle.dump(self.data, f)
        self.label.config(text=f"Saved digit '{label}'. Draw another!")
        self.clear()
        self.label_entry.delete(0, tk.END)

# ---------------------------
# Main: Mode selection
# ---------------------------
if __name__ == "__main__":
    print("Choose mode:")
    print("1 - Collect digits (label and save your own digits)")
    print("2 - Train model on your digits")
    print("3 - Guess (use trained model to recognize digits)")
    print("4 - Train model on MNIST + your digits")
    print("5 - Train model on a custom image folder")
    mode = input("Enter 1, 2, 3, 4, or 5: ").strip()

    if mode == "1":
        print("Collect mode: Draw a digit, enter its label, and click Save.")
        app = App(collect_mode=True)
        app.mainloop()
    elif mode == "2":
        print("Training mode: Training model on your digits (with augmentation)...")
        train_on_my_digits()
    elif mode == "3":
        print("Guess mode: Draw a digit and click Guess.")
        model = train_or_load_model()
        app = App(model)
        app.mainloop()
    elif mode == "4":
        print("Training mode: Training model on MNIST + your digits (with augmentation)...")
        train_on_mnist_and_my_digits()
    elif mode == "5":
        folder = input("Enter the path to your custom dataset folder: ").strip()
        train_on_custom_folder(folder)
    else:
        print("Invalid mode. Please run the script again and choose 1, 2, 3, 4, or 5.")