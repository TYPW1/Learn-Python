import streamlit as st
import sys
import os
from cb import predict_json

from testa.convert import calc

st.text(calc(2,3))

