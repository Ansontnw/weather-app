import matplotlib.pyplot as plt
import streamlit as st

# Generate your plot using Matplotlib
# ... (your plotting code here)
plt.savefig("plot.png")

# Display the plot image in Streamlit
st.image("plot.png")
