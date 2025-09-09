

import pandas as pd
import numpy as np
from io import StringIO
import plotly.graph_objects as go
from IPython.display import display, Markdown

########################################
# Code from plot_1.py
########################################

import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("Ecommerce_Delivery_Analytics_New.csv")

# Normalize 'Yes'/'No' in 'Delivery Delay' and 'Refund Requested' columns
df["Delivery Delay"] = df["Delivery Delay"].str.strip().str.lower()
df["Refund Requested"] = df["Refund Requested"].str.strip().str.lower()

# Group by platform and calculate delay and refund rates (percentages)
performance_metrics = df.groupby("Platform").agg(
    Delay_Rate=("Delivery Delay", lambda x: (x == "yes").mean() * 100),
    Refund_Rate=("Refund Requested", lambda x: (x == "yes").mean() * 100)
).reset_index()

# Melt dataframe for easier plotting with Plotly Express
perf_melted = performance_metrics.melt(id_vars='Platform', 
                                      var_name='Service Metric', 
                                      value_name='Rate (%)')

# Plot with data labels
fig = px.bar(
    perf_melted,
    x='Service Metric',
    y='Rate (%)',
    color='Platform',
    barmode='group',
    title='Platform Service Quality Rates',
    labels={'Rate (%)': 'Rate (%)', 'Service Metric': 'Service Metrics'}
)

# Add data labels on bars
fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')

fig.update_layout(
    yaxis=dict(range=[0, perf_melted['Rate (%)'].max() + 10]),
    template='plotly_white',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

fig.show()


########################################
# Code from plot_6.py
########################################

import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("Ecommerce_Delivery_Analytics_New.csv")

# Group by Platform and calculate averages
avg_df = df.groupby("Platform").agg({
    "Order Value (INR)": "mean",
    "Service Rating": "mean",
    "Delivery Time (Minutes)": "mean"
}).reset_index()

# Rename columns for clarity
avg_df.columns = ["Platform", "Avg Order Value", "Avg Rating", "Avg Delivery Time"]
print(avg_df)

fig = px.scatter(
    avg_df,
    x="Avg Order Value",
    y="Avg Rating",
    size="Avg Delivery Time",
    color="Platform",
    color_discrete_map={
        "JioMart": "#1FB8CD",
        "Blinkit": "#DB4545",
        "Swiggy Instamart": "#FDBE34"
    },
    text="Platform",
    title="Platform Comparison (Averages)"
)

fig.update_traces(textposition="top center")

fig.update_layout(
    xaxis_title="Avg Order Value ₹",
    yaxis_title="Avg Service Rating",
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=1.05, 
        xanchor="center", 
        x=0.5
    )
)

fig.show()


########################################
# Code from plot_2.py
########################################

# Group by Product Category and calculate average order value
avg_order_value = df.groupby("Product Category")["Order Value (INR)"].mean().reset_index()

# Sort for better visualization (optional)
avg_order_value = avg_order_value.sort_values(by="Order Value (INR)", ascending=False)

# Rename columns (optional)
avg_order_value.columns = ["Product Category", "Average Order Value (INR)"]

# Show table
print(avg_order_value)

# Plot the bar chart
fig = px.bar(
    avg_order_value,
    x="Product Category",
    y="Average Order Value (INR)",
    color="Product Category",
    title="Average Order Value by Product Category",
    text_auto=".2s"
)

fig.update_layout(
    xaxis_title="Product Category",
    yaxis_title="Avg Order Value (INR)",
    showlegend=False
)

fig.show()


########################################
# Code from plot_3.py
########################################

from plotly.subplots import make_subplots
# Normalize Yes/No values
df["Delivery Delay"] = df["Delivery Delay"].str.strip().str.lower()
df["Refund Requested"] = df["Refund Requested"].str.strip().str.lower()

# Create aggregated performance overview
performance_summary = df.groupby("Platform").agg({
    "Delivery Time (Minutes)": "mean",
    "Service Rating": "mean",
    "Delivery Delay": lambda x: (x == "yes").sum(),
    "Refund Requested": lambda x: (x == "yes").sum()
}).reset_index()

# Rename for readability
performance_summary.columns = [
    "Platform",
    "Avg Delivery Time (min)",
    "Avg Service Rating",
    "Total Delays",
    "Total Refunds"
]

# Show summary table
print(performance_summary)

# ---------------------------
# Code from plot_4.py
# ---------------------------

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Avg Delivery Time", "Avg Service Rating", "Delivery Delays", "Refund Requests"),
    vertical_spacing=0.2
)

# Bar chart for Avg Delivery Time
fig.add_trace(
    go.Bar(x=performance_summary["Platform"], y=performance_summary["Avg Delivery Time (min)"],
           marker_color='steelblue', name="Avg Delivery Time"),
    row=1, col=1
)

# Bar chart for Avg Service Rating
fig.add_trace(
    go.Bar(x=performance_summary["Platform"], y=performance_summary["Avg Service Rating"],
           marker_color='orange', name="Avg Rating"),
    row=1, col=2
)

# Bar chart for Delivery Delays
fig.add_trace(
    go.Bar(x=performance_summary["Platform"], y=performance_summary["Total Delays"],
           marker_color='crimson', name="Delays"),
    row=2, col=1
)

# Bar chart for Refund Requests
fig.add_trace(
    go.Bar(x=performance_summary["Platform"], y=performance_summary["Total Refunds"],
           marker_color='darkgreen', name="Refunds"),
    row=2, col=2
)

fig.update_layout(
    height=700,
    title_text="Order Performance Issue Overview by Platform",
    showlegend=False
)

fig.show()


########################################
# Code from plot_5.py
########################################

import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("Ecommerce_Delivery_Analytics_New.csv")

# Normalize Yes/No columns
df["Delivery Delay"] = df["Delivery Delay"].str.strip().str.lower()
df["Refund Requested"] = df["Refund Requested"].str.strip().str.lower()

# Thresholds
low_rating_threshold = 3
high_value_threshold = df["Order Value (INR)"].quantile(0.75)

# Calculate counts
total_orders = len(df)
delivery_delays = (df["Delivery Delay"] == "yes").sum()
refund_requests = (df["Refund Requested"] == "yes").sum()
low_ratings = (df["Service Rating"] <= low_rating_threshold).sum()
high_value_orders = (df["Order Value (INR)"] >= high_value_threshold).sum()

# Prepare dataframe for plotting
data = {
    "Metric": ["Total Orders", "Delivery Delays", "Refund Requests", "Low Ratings", "High Value"],
    "Count": [total_orders, delivery_delays, refund_requests, low_ratings, high_value_orders],
}
overview_df = pd.DataFrame(data)
overview_df["Percent"] = overview_df["Count"] / total_orders * 100

# Plot with Plotly Express
fig = px.bar(
    overview_df,
    x="Count",
    y="Metric",
    orientation='h',
    text=overview_df["Percent"].apply(lambda x: f"{x:.1f}%"),
    color="Metric",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Order Performance Issues Overview"
)

fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis_title="Count",
    yaxis_title="Metrics",
    yaxis=dict(categoryorder='total ascending'),
    uniformtext_minsize=12,
    uniformtext_mode='hide',
    template='plotly_white',
    showlegend=False,
    margin=dict(l=150, r=20, t=60, b=40)
)

fig.show()


