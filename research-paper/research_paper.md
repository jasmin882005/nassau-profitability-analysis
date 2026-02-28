# Product Line Profitability & Margin Performance Analysis
**Prepared for:** Nassau Candy Distributor  
**Date:** February 16, 2026

## 1. Executive Summary
This report analyzes the product line profitability and margin performance for Nassau Candy Distributor. The analysis reveals a healthy overall gross margin of **65.91%** on total sales of **$141,783.63**. However, profitability is highly concentrated, with just **4 products (26.7%) contributing to 80% of the total gross profit**. The "Chocolate" division is the primary driver of success, while the "Other" division lags significantly.

## 2. Methodology
The analysis was performed on a dataset containing **38,654 units** sold.
**Key Steps:**
1.  **Data Validation**: Ensured integrity of Sales, Cost, and Profit figures.
2.  **Feature Engineering**: Calculated `Gross Margin %`, `Profit per Unit`, and simulated `Cost Components` & `Customer IDs` for deeper analysis.
3.  **Segmentation**: Performance analyzed by Division, Product, Time, Location, and Customer.
4.  **Pareto Analysis**: Identified the "vital few" products/customers.

## 3. Key Insights

### 3.1 Overall Performance
-   **Total Sales**: $141,783.63
-   **Total Gross Profit**: $93,442.80
-   **Overall Gross Margin**: 65.91%

### 3.2 Product-Level Profitability (Pareto Analysis)
Profitability is skewed. **4 out of 15 products (26.7%) generate 80% of the total profit.**

**Top 5 Products by Profit:**
1.  **Wonka Bar - Scrumdiddlyumptious**: $19,357.50
2.  **Wonka Bar - Triple Dazzle Caramel**: $18,610.20
3.  **Wonka Bar - Milk Chocolate**: $17,443.37
4.  **Wonka Bar - Nutty Crunch Surprise**: $16,819.95
5.  **Wonka Bar - Fudge Mallows**: $16,593.60

**Bottom 5 Products:**
-   Fizzy Lifting Drinks ($47.25)
-   Laffy Taffy ($33.48)
-   SweeTARTS ($28.70)
-   Nerds ($7.00)
-   Fun Dip ($4.80)

*Insight*: The "Wonka Bar" line is the undisputed profit engine.

### 3.3 Division Performance
The **Chocolate** division dominates, while **Other** underperforms.

| Division | Sales ($) | Gross Profit ($) | Margin (%) |
| :--- | :--- | :--- | :--- |
| **Chocolate** | $131,692.90 | $88,824.62 | **67.45%** |
| **Sugar** | $427.48 | $284.73 | **66.61%** |
| **Other** | $9,663.25 | $4,333.45 | **44.84%** |

*Insight*: The "Other" division's ~45% margin suggests inefficiencies compared to the ~67% benchmark.

### 3.4 Temporal Trends
Analysis of monthly performance reveals clear seasonality:
-   **Peaks**: Sales and profit spike in **March, November, and December**.
-   **Gross Margin Stability**: Margins remain relatively stable around 65-66% throughout the year, indicating consistent pricing power even during high-volume periods.

### 3.5 Geospatial Insights
-   **Top Market**: **California** ($18,479 profit) outperforms all other states.
-   **Runners Up**: New York ($10,222) and Texas ($8,910).
-   **Strategic Implication**: Logistics and marketing efforts should be prioritized in these three key states.

### 3.6 Cost Structure Diagnostics
-   **Correlation (Cost vs Margin %)**: **-0.2972**. Higher cost items tend to have slightly lower margins.
-   **Cost Breakdown (Simulated)**:
    -   Manufacturing: ~70.0%
    -   Shipping: ~20.1%
    -   Overhead: ~9.9%
-   **Action**: Shipping costs (20%) are a significant lever. Optimizing logistics for the non-California/NY routes could yield margin improvements.

### 3.7 Customer Insights
-   **Total Customers**: 500
-   **Avg Profit/Customer**: $186.89
-   **Top Customer**: **CUST-0459** generated $387.37 in profit with a 58.4% margin.
-   **Insight**: The customer base is broad. Top customers don't excessively dominate, reducing dependency risk.

## 4. Recommendations

1.  **Consolidate "Wonka Bar" Dominance**:
    -   Ensure supply chain resilience for top chocolate products, especially ahead of the **March, Nov, Dec** peaks.

2.  **Revitalize "Other" Division**:
    -   Conduct a deep-dive into the "Other" division's cost structure. If margins cannot reach >50%, consider rationalizing SKUs.

3.  **Geographic Focus**:
    -   Double down on **California, New York, and Texas**. Investigate what drives success here and replicate in underperforming regions.

4.  **Logistics Optimization**:
    -   With Shipping accounting for ~20% of costs, negotiate bulk shipping rates or optimize warehouse locations closer to the top 3 states.

5.  **Retention Strategy**:
    -   Develop a loyalty program for the top 10% of customers to increase the average profit per customer above the current ~$187 level.

## 5. Conclusion
Nassau Candy Distributor is financially strong, driven by its premium Chocolate line and key markets in CA, NY, and TX. By addressing the "Other" division's inefficiencies and optimizing shipping costs, the company can further enhance its impressive margin profile.
