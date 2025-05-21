# 📊 Data Science with Python

This project contains two machine learning tasks implemented in Python:

1. **Linear Regression Analysis** on a medical expenses dataset using Jupyter Notebook  
2. **Implementation of a Nearest Neighbors in Radius (NNR) Classifier** from scratch using PyCharm

---

## 🧪 Task 1: Linear Regression with Medical Insurance Dataset

In this task, we perform data exploration and apply linear regression to predict individuals' medical expenses based on various features (age, sex, BMI, number of children, smoking status, and region). 

### Features:
- Uses `pandas`, `numpy`, `seaborn`, and `sklearn` for data handling, visualization, and modeling.
- Trains a linear regression model to predict continuous expense values.
- Evaluates the model's performance and answers analytical questions in the notebook.

### File:
- `assignment3_task1.ipynb`

---

## 🤖 Task 2: Nearest Neighbors in Radius (NNR) Classifier

This task implements a custom version of the Nearest Neighbors in Radius (NNR) classifier, a variation of KNN. The classifier labels a new data point by checking all training points within a given radius and applying a majority vote on their labels.

### Features:
- Written entirely from scratch (without using `sklearn`'s built-in `RadiusNeighborsClassifier`).
- Works on any compatible dataset structure with no hardcoded assumptions.
- Uses validation data to find the optimal radius.
- Evaluates test accuracy on unseen datasets.
- Optimized to run in under 3 minutes.

### File:
- `main.py`

---

## 🛠 Technologies Used

- Python 3
- NumPy
- Pandas
- Scikit-learn
- statsmodels
- Jupyter Notebook
- PyCharm

---

## 📈 Results

| Dataset               | Task       | Accuracy (%) |
|-----------------------|------------|--------------|
| Spotify Album Genre   | NNR        | ~46%         |
| Body Performance      | NNR        | ~57%         |
| Medical Insurance     | Regression | Evaluated with MSE / R² |

> The NNR classifier was evaluated on two datasets and achieved good performance. The code is designed to generalize to other datasets as well.

---

## ✅ How to Run

### Task 1 (Jupyter):
1. Open `assignment3_task1.ipynb` in Jupyter.
2. Run all cells after restarting the kernel and clearing outputs.

### Task 2 (NNR Classifier):
1. Make sure your dataset paths are configured in `config.json`.
2. Run `main.py` in PyCharm or from the command line.

---

## 📌 Notes

- The code is fully modular and generalized for unseen datasets.
- No hardcoded feature names or class labels.
- Designed for efficiency and clarity.
- Make sure all columns but the last are features, the last column (class) is labels.

---

## 🧑‍💻 Authors

- Ofri Kuperberg
- Adi Karif 

---
