# visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def auto_visualize(df: pd.DataFrame, return_figs: bool = True):
    """
    Automatically generate visualizations for a given DataFrame.
    Returns a list of matplotlib Figures if return_figs=True.
    """

    figs = []

    if df.empty:
        print("DataFrame is empty, cannot visualize.")
        return [] if return_figs else None

    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns
    datetime_cols = df.select_dtypes(include='datetime64[ns]').columns

    # --- Pie Charts for categorical (<= 10 unique values)
    for col in categorical_cols:
        if df[col].nunique() <= 10:
            fig, ax = plt.subplots(figsize=(6, 6))
            df[col].value_counts().plot.pie(
                autopct='%1.1f%%', startangle=90, colormap='tab20', ax=ax
            )
            ax.set_title(f'Pie Chart of {col}')
            ax.set_ylabel('')
            figs.append(fig)

    # --- Bar Charts for numeric (<= 10 unique values)
    for col in numeric_cols:
        if df[col].nunique() <= 10:
            fig, ax = plt.subplots(figsize=(8, 5))
            df[col].value_counts().plot.bar(color='skyblue', ax=ax)
            ax.set_title(f'Bar Chart of {col}')
            ax.set_ylabel('Count')
            figs.append(fig)

    # --- Histograms for numeric (> 10 unique values)
    for col in numeric_cols:
        if df[col].nunique() > 10:
            fig, ax = plt.subplots(figsize=(8, 5))
            df[col].plot.hist(bins=15, color='lightgreen', edgecolor='black', ax=ax)
            ax.set_title(f'Histogram of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            figs.append(fig)

    # --- Pairplot for multiple numeric columns
    if len(numeric_cols) >= 2:
        pairplot_fig = sns.pairplot(df[numeric_cols])
        pairplot_fig.fig.suptitle("Scatter Plot Matrix", y=1.02)
        figs.append(pairplot_fig.fig)

    # --- Line charts for datetime vs numeric
    for dt_col in datetime_cols:
        for num_col in numeric_cols:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df[dt_col], df[num_col], marker='o')
            ax.set_title(f"{num_col} over {dt_col}")
            ax.set_xlabel(dt_col)
            ax.set_ylabel(num_col)
            ax.grid(True)
            figs.append(fig)

    return figs if return_figs else None
