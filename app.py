import streamlit as st
import numpy as np
from scipy.stats import t
from statistics import stdev
from scipy import stats

st.title("Two Sample t-Test Calculator")

st.write("Enter two samples (comma separated values)")

# Inputs
sample1 = st.text_input("Sample 1", "10,12,14,15,18")
sample2 = st.text_input("Sample 2", "9,11,13,14,16")

alternative = st.selectbox(
    "Alternative Hypothesis",
    ["two-sided", "left", "right"]
)

if st.button("Calculate"):

    # convert input to list of floats
    a = list(map(float, sample1.split(",")))
    b = list(map(float, sample2.split(",")))

    xbar1 = np.mean(a)
    xbar2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    n1 = len(a)
    n2 = len(b)

    alpha = 0.05 / 2
    df = n1 + n2 - 2
    se = np.sqrt((sd1**2)/n1 + (sd2**2)/n2)

    tcal = ((xbar1 - xbar2)) / se

    # p-value calculation
    if alternative == "two-sided":
        p_value = 2 * (1 - t.cdf(abs(tcal), df))
    elif alternative == "left":
        p_value = t.cdf(tcal, df)
    else:
        p_value = 1 - t.cdf(tcal, df)

    st.subheader("Results")
    st.write(f"Mean 1: {xbar1:.3f}")
    st.write(f"Mean 2: {xbar2:.3f}")
    st.write(f"t-statistic: {tcal:.4f}")
    st.write(f"p-value: {p_value:.6f}")

    st.subheader("SciPy Verification")
    scipy_result = stats.ttest_ind(a, b, equal_var=False, alternative=alternative)
    st.write(scipy_result)