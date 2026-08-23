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

## 📊 Tableau Dashboard

The model outputs were translated into an interactive Tableau dashboard designed to support material planners in monitoring backorder risk and identifying the SKUs that require the most attention.

The dashboard includes:

- **Material Risk Command Center** — overall view of predicted backorder exposure and planner priorities
- **Risk Drivers** — analysis of the operational factors associated with backorder risk
- **Model Performance** — evaluation of the final classifier and prediction outcomes
- **SKU Detail** — material-level consultation including inventory, demand, supply conditions, and planner recommendation

The dashboard converts predicted probabilities into operational risk categories and planner priorities, allowing users to move from model performance to material-level decision support.

### 🔗 Live Dashboard

[View the interactive Tableau dashboard](https://public.tableau.com/views/BackorderPredictionMaterialRiskPlanning/MaterialRiskCommandCenter_?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

## 📦 Material Risk Planner — Streamlit App

As an additional operational layer, I developed a Streamlit application that allows planners to interact directly with the model outputs.

The application provides two decision-support tools:

### 🔎 SKU Consultation

Users can search for an individual SKU and review:

- Backorder probability
- Risk level
- Planner priority
- Current inventory and in-transit quantities
- Local backorder quantity
- Demand forecasts
- Supplier lead time and performance
- Past-due quantities
- Current backorder status
- Automated planner recommendation

### 🏭 BOM / Production Material Risk Check

Users can enter multiple SKUs required for a production plan or Bill of Materials (BOM).

The application then:

- Checks whether the required materials are available in the dataset
- Identifies High, Elevated, Moderate, and Low risk materials
- Evaluates overall production readiness
- Prioritizes the most critical SKUs
- Provides recommended planner actions for materials requiring attention


### 🔗 Live Application

[Open the Material Risk Planner](https://material-risk-planner.streamlit.app/)

> **Demo note:** The deployed application uses a curated sample of 18,821 SKUs from the final model output to provide a lightweight interactive demonstration. The sample preserves all High-risk SKUs and representative observations from the remaining risk levels. The complete dataset was used for model development and evaluation.

---

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **Scikit-learn**
- **Imbalanced-learn / SMOTE**
- **Matplotlib**
- **Jupyter Notebook**
- **Tableau**
- **Streamlit**
- **Git & GitHub**
