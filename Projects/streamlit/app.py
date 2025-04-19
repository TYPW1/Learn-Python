import streamlit as st
import pandas as pd
import numpy as np
import time

st.code("import pandas")

with st.echo():
    import pandas as pd
    import numpy as np

st.badge("This is a badge")

my_bar = st.progress(0)
with st.spinner():
    time.sleep(1)
    my_bar.success("Done!")

for p in range(100):
    time.sleep(0.001)
    my_bar.progress(p + 1)

df= pd.DataFrame(
    np.random.randn(100, 2),
    columns=["a", "b"]
)
st.dataframe(df)