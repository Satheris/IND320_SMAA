import streamlit as st
import plotly.express as px

# import iris dataset 
iris_df = px.data.iris()

# display iris dataset 
st.subheader('Iris Dataset')
st.dataframe(iris_df)

# create scatter plot using plotly express
basic_scatter_fig = px.scatter(iris_df, x='sepal_width', y='sepal_length', color='species', size='petal_length', symbol='species',
                               hover_data=['petal_width'])

# display the figure in streamlit 
st.subheader('Iris Dataset: Basic Scatter Plot')
st.plotly_chart(basic_scatter_fig)



st.subheader('Iris Dataset: Bubble Chart with Selectable axes')

# user axis selection 
x_axis = st.selectbox('Choose a variable for the x-axis', iris_df.columns, index=0)
y_axis = st.selectbox('Choose a variable for the y-axis', iris_df.columns, index=1)

# create bubble chart with color, different symbols, and hover data
colored_bubble_fig = px.scatter(iris_df, x=x_axis, y=y_axis, color='species', size='petal_length',
                                hover_data=['species', 'petal_length', 'petal_width', 'sepal_length', 'sepal_width'])

colored_bubble_fig.update_layout(
    font_family='Courier New',
    title='Iris Dataset Bubble Chart',
    xaxis_title=x_axis,
    yaxis_title=y_axis,
    legend_title='Species'
)

# display the figure in streamlit 
st.plotly_chart(colored_bubble_fig)





chart_type = st.radio('Select chart type:', ('Scatter Plot', 'Line Chart', 'Bar Chart', 'Histogram', 'Box Plot',
                                             'Pie Chart', '3D Scatter Plot'))

# visualize the relationship between sepal length and sepal width, colored by species
if chart_type == 'Scatter Plot':
    fig = px.scatter(iris_df, x='sepal_length', y='sepal_width', color='species', title='Iris Scatter Plot')
    st.plotly_chart(fig)

# since line charts typically require time-series data,
# let's simulate a line chart using the iris dataset index as a faux time-axis
elif chart_type == 'Line Chart':
    iris_df_sorted = iris_df.sort_values(by='sepal_length').reset_index()
    fig = px.line(iris_df_sorted, x=iris_df_sorted.index, y='sepal_length', color='species', title='Iris Sepal Length Line Chart')
    st.plotly_chart(fig)

# display the average sepal length of each species using a bar chart 
elif chart_type == 'Bar Chart':
    avg_sepal_length = iris_df.groupby('species')['sepal_length'].mean().reset_index()
    fig = px.bar(avg_sepal_length, x='species', y='sepal_length', title='Average Sepal Length of Iris Species')
    st.plotly_chart(fig)

# show the distribution of sepal lengths across all species 
elif chart_type == 'Histogram':
    fig = px.histogram(iris_df, x='sepal_length', title='Sepal Length Distribution')
    st.plotly_chart(fig)

# visualize the distribution of sepal lengths for each species using a box plot 
elif chart_type == 'Box Plot':
    fig = px.box(iris_df, x='species', y='sepal_length', title='Sepal Length by Species')
    st.plotly_chart(fig)

# display the distribution of species in the dataset
elif chart_type == 'Pie Chart':
    species_count = iris_df['species'].value_counts().reset_index()
    fig = px.pie(species_count, values='count', names='species', title='Iris Species Distribution')
    st.plotly_chart(fig)

# create a 3D scatter plot showing the sepal length, sepal width and petal length, colored by species
elif chart_type == '3D Scatter Plot':
    fig = px.scatter_3d(iris_df, x='sepal_length', y='sepal_width', z='petal_length', 
                        color='species', title='3D Scatter Plot of Iris Dataset')
    st.plotly_chart(fig)






import plotly.graph_objects as go
import pandas as pd

# claculate a correlation matrix 
corr = iris_df.iloc[:, :4].corr()

# create a heatmap 
fig = go.Figure(data=go.Heatmap(
                z=corr,
                x=corr.columns,
                y=corr.columns))
fig.update_layout(title='Heatmap of Iris Features Correlation')
st.plotly_chart(fig)