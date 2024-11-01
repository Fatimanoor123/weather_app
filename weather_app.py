# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import streamlit as st  # For creating a web application interface
import seaborn as sns  # For advanced data visualization
import matplotlib.pyplot as plt  # For general plotting

# Set the Seaborn theme for consistent styling of plots
sns.set_theme(style="darkgrid")

# Title of the Streamlit web app
st.title('Advanced Weather Data Analyzer')

# File uploader widget for CSV files
file = st.file_uploader("Upload a CSV file", type="csv")

# Check if a file has been uploaded
if file is not None:
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(file)

    # Add a synthetic 'Date' column if it's not already present in the DataFrame
    if 'Date' not in df.columns:
        df['Date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
    
    # Convert the 'Date' column to a datetime object for time-based analysis
    df['Date'] = pd.to_datetime(df['Date'])

    # Display the first few rows of the DataFrame for preview
    st.subheader("Data Preview")
    st.write(df.head())

    # Section for data cleaning options
    st.subheader("Data Cleaning Options")
    # Option to drop duplicate rows
    if st.checkbox("Drop duplicates"):
        df = df.drop_duplicates()
        st.write("Duplicates dropped!")
    
    # Option to drop rows with missing values
    if st.checkbox("Drop missing values"):
        df = df.dropna()
        st.write("Missing values dropped!")

    # Choose columns for plotting (numerical columns only)
    x_col = 'Date'  # Fixed x-axis as the Date column
    y_col = st.selectbox("Select Value Column (e.g., Temperature, Rainfall)", df.select_dtypes(include=['float64', 'int64']).columns)

    # Date range slider for filtering data
    st.subheader("Filter by Date Range")
    min_date = df[x_col].min().date()  # Get the minimum date in the DataFrame
    max_date = df[x_col].max().date()  # Get the maximum date in the DataFrame
    # Slider widget for selecting a date range
    start_date, end_date = st.slider(
        "Select date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # Filter the DataFrame based on the selected date range
    filtered_df = df[(df[x_col] >= pd.to_datetime(start_date)) & (df[x_col] <= pd.to_datetime(end_date))]

    # Display summary statistics for the filtered data
    st.subheader("Summary Statistics")
    st.write(filtered_df.describe())

    # Section for plot type selection
    st.subheader("Choose Plot Type")
    plot_type = st.radio("Select plot type", ["Line Plot", "Scatter Plot", "Bar Plot", "Multiple Columns Comparison"])

    # Create and display the selected plot
    plt.figure(figsize=(12, 6))  # Set the figure size for the plot
    if plot_type == "Line Plot":
        sns.lineplot(x=filtered_df[x_col], y=filtered_df[y_col], data=filtered_df)
        plt.title(f"{y_col} Over Time")
    elif plot_type == "Scatter Plot":
        sns.scatterplot(x=filtered_df[x_col], y=filtered_df[y_col], data=filtered_df)
        plt.title(f"{y_col} Scatter Plot")
    elif plot_type == "Bar Plot":
        sns.barplot(x=filtered_df[x_col].dt.strftime('%Y-%m-%d'), y=filtered_df[y_col], data=filtered_df)
        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        plt.title(f"{y_col} Bar Plot")
    elif plot_type == "Multiple Columns Comparison":
        # Allow selection of multiple columns for comparison
        selected_cols = st.multiselect("Select multiple columns to compare", df.select_dtypes(include=['float64', 'int64']).columns)
        if selected_cols:
            for col in selected_cols:
                sns.lineplot(x=filtered_df[x_col], y=filtered_df[col], label=col)
            plt.title("Comparison of Multiple Columns Over Time")
            plt.legend()  # Display the legend

    # Set labels for the x and y axes
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    st.pyplot(plt)  # Render the plot in the Streamlit app

    # Section for displaying the correlation matrix
    st.subheader("Correlation Matrix")
    if st.checkbox("Show correlation matrix"):
        # Select only numeric columns for the correlation matrix
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        
        # Check if there are any numeric columns to display
        if not numeric_df.empty:
            # Calculate the correlation matrix
            corr = numeric_df.corr()
            # Create and display the heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
            plt.title("Correlation Matrix")
            st.pyplot(plt)
        else:
            st.warning("No numeric columns available for correlation matrix.")
else:
    # Display a message prompting the user to upload a CSV file
    st.info("Please upload a CSV file.")
