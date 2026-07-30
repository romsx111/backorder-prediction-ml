# Smart Material Planning: Backorder Prediction with Machine Learning

## 🔎 Project Overview

Material availability is essential for maintaining operational continuity and meeting customer demand. Unexpected backorders can result in production disruptions, expedited purchasing costs, delayed deliveries, and reduced service levels.

In this individual project, I aim to develop an end-to-end Machine Learning solution capable of identifying materials at risk of going on backorder before shortages negatively impact business operations.

Using inventory levels, supplier lead times, demand forecasts, historical sales, supplier performance, and procurement-related variables, I will compare several classification models and investigate the main operational factors associated with backorder risk.

Rather than focusing only on predictive performance, I also aim to translate the analytical results into practical recommendations that can support materials planners in prioritizing replenishment and inventory management decisions.

---

## 🎯 Main Objective

Develop an end-to-end Machine Learning solution capable of predicting material backorders and supporting data-driven inventory planning and procurement decisions before shortages impact business operations.

---

## ❓ Business Questions

### Primary Question

**Can I build a Machine Learning model capable of identifying materials at risk of going on backorder before inventory shortages impact business operations?**

### Secondary Questions

- Which variables have the greatest influence on backorder risk?
- Can inventory, demand, supplier, and procurement information accurately predict future backorders?
- How do inventory levels, supplier lead times, demand forecasts, and historical sales influence backorder risk?
- Which SKUs should materials planners prioritize based on their predicted probability of going on backorder?
- Which operational patterns are most commonly associated with backorders?
- How can Explainable Machine Learning help planners understand why a material is considered high risk?
- How can I translate model predictions into actionable inventory planning and procurement recommendations?

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

Back Order Prediction Dataset — Kaggle
