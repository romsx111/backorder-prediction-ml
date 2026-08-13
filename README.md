# Smart Material Planning: Backorder Prediction with Machine Learning

## 🔎 Project Overview

Material availability is essential for maintaining operational continuity and meeting customer demand. Unexpected backorders can result in production disruptions, expedited purchasing costs, delayed deliveries, and reduced service levels.

In this individual project, I aim to develop an end-to-end Machine Learning solution capable of identifying materials at risk of going on backorder before shortages negatively impact business operations.

Using inventory levels, supplier lead times, demand forecasts, historical sales, supplier performance, and procurement-related variables, the project compares multiple classification approaches and evaluates different strategies for handling the strong class imbalance present in the dataset.

The final solution goes beyond binary prediction by using predicted backorder probabilities to create operational risk levels and planner priorities. This allows model outputs to be translated into an early-warning tool that can help materials planners identify and prioritize potentially risky SKUs for further review.

---

## 🎯 Main Objective

Develop an end-to-end Machine Learning solution capable of predicting material backorders and supporting data-driven inventory planning and procurement decisions before shortages impact business operations.

---

## ❓ Business Questions

### Primary Question

**Can Machine Learning identify materials at risk of going on backorder before inventory shortages impact business operations?**

### Secondary Questions

- Which variables have the greatest influence on backorder risk?
- Can inventory, demand, supplier, and procurement information predict future backorders?
- How do inventory levels, supplier lead times, demand forecasts, and historical sales influence backorder risk?
- Which SKUs should materials planners prioritize based on their predicted probability of going on backorder?
- Are there identifiable patterns in backorder behavior across SKU groups?
- How can model predictions be translated into actionable inventory planning and procurement priorities?

---

## 📊 Dataset

The project uses the **Back Order Prediction Dataset**, which contains operational records related to inventory planning and material availability.

### Dataset characteristics

- Approximately 1.7 million training records
- Separate training and testing datasets
- 23 variables
- Binary classification problem
- Target variable: `went_on_backorder`

The dataset includes:

- Current inventory levels
- Inventory in transit
- Supplier lead times
- Demand forecasts
- Historical sales
- Minimum recommended stock
- Past-due quantities
- Supplier performance indicators
- Procurement and operational risk indicators
- Existing backorder quantities

> The dataset files are not included in this repository due to their size. They must be downloaded separately and stored inside `data/raw/`.

### Source

[Back Order Prediction Dataset — Kaggle](https://www.kaggle.com/datasets/gowthammiryala/back-order-prediction-dataset?resource=download)

---
## 🤖 Machine Learning Approach

Several classification approaches were evaluated to determine which model provided the most useful balance between identifying actual backorders and limiting false alerts.

The modeling process included:

- Logistic Regression
- Decision Tree
- Random Forest
- Undersampling experiments
- SMOTE oversampling
- Hyperparameter tuning
- Threshold optimization
- Validation and final evaluation on an untouched test set

Undersampling provided a useful high-recall reference, but generated a larger number of false positive predictions.

SMOTE provided a stronger overall precision-recall trade-off and was therefore used in the final Random Forest modeling workflow.

---

## 🌲 Final Model

The selected solution is a **Random Forest classifier trained using SMOTE-balanced training data**.

Instead of relying exclusively on the default classification threshold of `0.50`, different probability thresholds were evaluated on the validation set.

A final threshold of **0.40** was selected based on the best observed F1-score and then applied to the untouched test set.

### Final test performance

| Metric | Final Test |
|---|---:|
| Precision | 0.3499 |
| Recall | 0.4782 |
| F1-score | 0.4041 |
| ROC-AUC | 0.9469 |
| PR-AUC | 0.3024 |

The close performance between the validation and untouched test sets indicates that the final model generalizes consistently to unseen observations.

---

