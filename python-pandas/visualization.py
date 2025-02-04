import marimo

__generated_with = "0.7.0"
app = marimo.App()


@app.cell
def __():
    import numpy as np 
    import pandas as pd 
    import marimo as mo

    # There are some fake data csv files 
    # you can read in as dataframes 
    df1 = pd.read_csv('df1', index_col=0) 
    df2 = pd.read_csv('df2')
    return df1, df2, mo, np, pd


@app.cell
def __(df1):
    df1['A'].hist()
    return


@app.cell
def __(df1):
    import matplotlib.pyplot as plt 

    plt.style.use('ggplot') 

    df1['A'].hist()
    return plt,


@app.cell
def __(df1, plt):
    plt.style.use('bmh') 
    df1['A'].hist()
    return


@app.cell
def __(mo):
    text_input = mo.ui.text()
    mo.md(f"Enter some text: {text_input}")
    return text_input,


@app.cell
def __(mo, plt):
    plt.plot([1, 2])
    axis = plt.gca()
    mo.md(f"Here's a plot: {mo.as_html(axis)}")
    return axis,


@app.cell
def __(mo):
    mo.md(
        r"""
        The exponential function $f(x) = e^x$ can be represented as

        \[
            f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
        \]
        """
    )
    return


@app.cell
def __(df2):
    df2.plot.area(alpha=0.4) 
    return


@app.cell
def __(df2):
    df2.head(1) 

    return


@app.cell
def __(df2):
    df2.plot.bar() 

    return


@app.cell
def __(df2):
    df2.plot.bar(stacked=True)
    return


@app.cell
def __(df1):
    df1
    return


@app.cell
def __(df1):
    df1.plot.scatter(x='A', y='B') 
    return


@app.cell
def __(df1):
    df1.plot.scatter(x ='A', y ='B', c ='C', cmap ='coolwarm') 
    return


@app.cell
def __(df2):
    df2.plot.box()
    return


@app.cell
def __(df2):
    df2['a'].plot.kde()
    return


if __name__ == "__main__":
    app.run()
