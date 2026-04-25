# 🛒 Superstore Sales & Customer Analytics Dashboard

An interactive sales analytics dashboard built with **Streamlit** and **Plotly**, using the Superstore Sales dataset. The dashboard enables dynamic filtering and visual exploration of sales performance across regions, product categories, customer segments, and time.

---

## 📊 Dashboard Features

- **KPI Metrics** — Total Sales, Average Order Value, Unique Customers, Total Orders
- **Sales by Category & Region** — Bar and pie charts for category and regional breakdown
- **Monthly Sales Trend** — Line chart showing sales over time
- **Sales Distribution** — Histogram of sales values by product category
- **Scatter Plot** — Sales by category and region with bubble sizing
- **Top 10 Customers** — Horizontal bar chart of highest-value customers
- **Sub-Category Breakdown** — Top 10 sub-categories by total sales
- **Correlation Heatmap** — Relationships between numerical features
- **Raw Data Viewer** — Filterable table with summary statistics

---

## 🔎 Sidebar Filters

All charts respond dynamically to the following filters:
- Region
- Product Category
- Customer Segment
- Year Range

---

## 🗂️ Repository Structure

```
superstore-dashboard/
├── app.py                      # Main Streamlit application
├── superstore_sales_data.csv   # Dataset (9,800 rows, 18 columns)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/your-username/superstore-dashboard.git
cd superstore-dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## ☁️ Live Demo

Deployed on **Streamlit Community Cloud**:
> 🔗 [your-app-url.streamlit.app](https://your-app-url.streamlit.app)

*(Replace this link with your actual deployment URL after deploying)*

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `pandas` | Data loading and manipulation |
| `plotly` | Interactive charts |
| `seaborn` | Correlation heatmap |
| `matplotlib` | Figure rendering backend |

---

## 📁 Dataset

The dataset contains **9,800 orders** with the following key fields:

| Column | Description |
|--------|-------------|
| `Order Date` | Date the order was placed |
| `Region` | Geographic region (East, West, Central, South) |
| `Product_Category` | Furniture, Office Supplies, Technology |
| `Sub-Category` | Product sub-category |
| `Segment` | Customer segment (Consumer, Corporate, Home Office) |
| `Total_Sales` | Revenue for the order line |

---

## 👩‍💻 Author

**Florence Owiti**  
MSc Data Science  
