import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Loaded cleaned data
product_df = pd.read_csv('product_category_name.csv')
revenue_df = pd.read_csv('revenue_by_day.csv')

# Mengubah 'order_approved_at' ke tipe data 'datetime'
revenue_df['order_approved_at'] = pd.to_datetime(
    revenue_df['order_approved_at'])

# Filter date
min_date = revenue_df['order_approved_at'].min()
max_date = revenue_df['order_approved_at'].max()

with st.sidebar:
    # Mengambil 'start_date' & 'end_date' dari 'date_input'
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = revenue_df[(revenue_df["order_approved_at"] >= str(start_date)) &
                     (revenue_df["order_approved_at"] <= str(end_date))]

# Plot number of daily orders
st.header('E-Commerce Collection :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.total_order.sum()
    st.metric('Total Orders', value=total_orders)

with col2:
    total_revenue = format_currency(
        main_df.total_revenue.sum(), "BRL ", locale='ES_CO'
    )
    st.metric('Total Revenue', value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    revenue_df['order_approved_at'],
    revenue_df['total_order'],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# product performance
st.subheader("Best & Worst Performing Product\'s")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


sns.barplot(x='total_order', y='product_category_name_english',
            data=product_df.groupby('product_category_name_english')
            .total_order
            .nunique()
            .sort_values(ascending=False)
            .reset_index()
            .head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x='total_order', y='product_category_name_english',
            data=product_df.groupby('product_category_name_english')
            .total_order
            .nunique()
            .sort_values(ascending=True)
            .reset_index()
            .head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)
