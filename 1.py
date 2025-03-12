import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt

df=pd.DataFrame(
    np.random.randn(10,20), 
    columns=("col %d" % i for i in range(20))
)

st.dataframe(df.style.highlight_max(axis=0))

data=pd.DataFrame(
    np.random.randn(20,3),
    columns=["a","b","c"]
)
st.line_chart(data)