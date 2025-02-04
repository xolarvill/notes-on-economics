import marimo

__generated_with = "0.7.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo 
    import pandas as pd
    import numpy as np
    return mo, np, pd


@app.cell
def __(mo):
    mo.md(
        r"""
        # creating DataFrame

        pandas use `read_csv`, `read_stata`, `read_xlsx` and so on to read data
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        DataFrame is used to capture a table.
        **note: pay attention to the text denotetor'**
        """
    )
    return


@app.cell
def __(pd):
    df_a = pd.DataFrame(
        [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ],
        index=['A','B','C'],
        columns=['X','Y','Z']
    )
    df_a
    return df_a,


@app.cell
def __(mo):
    mo.md(r"another way to create DataFrame is to read existed files. (Because mostly all functions return DataFrame so uniformity)")
    return


@app.cell
def __(pd):
    df_b = pd.read_csv('df2')
    df_b
    return df_b,


@app.cell
def __(mo):
    mo.md(r"# change layout")
    return


@app.cell
def __(mo):
    mo.md(r"合并列")
    return


@app.cell
def __(df_a, pd):
    pd.melt(df_a)
    return


@app.cell
def __(mo):
    mo.md(r"拆列")
    return


@app.cell
def __():
    # df_a.pivot()
    return


@app.cell
def __(mo):
    mo.md(r"列合并表")
    return


@app.cell
def __(df_a, df_b, pd):
    pd.concat([df_a,df_b])
    return


@app.cell
def __(mo):
    mo.md(r"排序，默认升序")
    return


@app.cell
def __(df_a):
    df_a.sort_values('X',ascending=False)
    return


@app.cell
def __(df_a):
    df_a.sort_index()
    return


@app.cell
def __(df_a):
    df_a.rename(columns={'X':'Xavier','Y':'Yandex','Z':'Zebra'})
    return


@app.cell
def __(df_a):
    df_a.drop(columns=['Y','Z'])
    return


@app.cell
def __(mo):
    mo.md(r"# observation")
    return


@app.cell
def __(df_a):
    df_a.head()
    return


@app.cell
def __(df_a):
    df_a.tail()
    return


@app.cell
def __(mo):
    mo.md(r"randomly select = sampling")
    return


@app.cell
def __(df_a):
    df_a.sample(frac=0.5)
    return


@app.cell
def __(df_a):
    df_a.sample(n=2)
    return


@app.cell
def __(mo):
    mo.md(r"n largest and smallest")
    return


@app.cell
def __(df_a):
    df_a.nlargest(n=1,columns='X') # or df_a.nlargest(1,columns='X')
    return


@app.cell
def __(df_a):
    df_a.filter(like='',regex='')
    return


@app.cell
def __(df_a):
    df_a[['X','Y']]
    return


@app.cell
def __(df_a):
    df_a.X
    return


@app.cell
def __(df_a):
    df_a['X'] # df_a['X','Y'] is wrong, for multiple columns try use [['X','Y']]
    return


@app.cell
def __(mo):
    mo.md(r"# query")
    return


@app.cell
def __(df_a):
    df_a.query('X > 7') # df_a.query(X > 7) is not available
    return


@app.cell
def __(df_a):
    df_a.query('X > 7 and Y < 3')
    return


@app.cell
def __(df_a):
    df_a.query('X>7' and 'Y<3') # notice the difference
    return


@app.cell
def __(df_a):
    df_a.iloc[0:2] # starting from 0 but not ending at 2. it ends before 2, which is at 1.
    return


@app.cell
def __(df_a):
    df_a.loc[df_a.X>5]
    return


@app.cell
def __(mo):
    mo.md(r"`df_a.iat[]` and `df_a.at[]` are similiar tools for specific values")
    return


@app.cell
def __(mo):
    mo.md(r"# summarize data")
    return


@app.cell
def __(df_a):
    df_a.shape # notice df_a.shape() is not available
    return


@app.cell
def __(df_a):
    len(df_a)
    return


@app.cell
def __(df_a):
    df_a['X'].value_counts()
    return


@app.cell
def __(df_a):
    df_a['X'].nunique()
    return


@app.cell
def __(df_b):
    df_b
    return


@app.cell
def __(df_b):
    df_b.describe()
    return


@app.cell
def __(df_b):
    df_b.sum()
    return


@app.cell
def __(df_b):
    df_b.count()
    return


@app.cell
def __(df_b):
    df_b.median()
    return


@app.cell
def __(df_b):
    df_b.mean()
    return


@app.cell
def __(df_b):
    df_b.quantile([0.25,0.75]) # inside the bracet must be a [n1,n2]
    return


@app.cell
def __(df_b):
    df_b.var()
    df_b.std()
    df_b.min()
    df_b.max()
    # and so on
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # handling missing data

        we start by creating a DataFrame with missing data, using numpy's 'np.nan'.
        """
    )
    return


@app.cell
def __(np, pd):
    df = pd.DataFrame(
        [
            [1,88,44],
            [np.nan,np.nan,4],
            [2,5,6]
        ],
        index=['index1','index2','index3'],
        columns=['column1','column2','column3']
                     )
    df
    return df,


@app.cell
def __(df):
    df.dropna()
    return


@app.cell
def __(df):
    df.fillna(0)
    return


@app.cell
def __(df):
    df.fillna('ofc')
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # join tables
        let's design two tables
        """
    )
    return


@app.cell
def __(pd):
    left = pd.DataFrame(
        [[1,9],
        [2,9],
        [3,9]],
        index=['a','b','c'],
        columns=['omega','epsilon']
                       )
    right = pd.DataFrame(
        [[1,8],
        [2,8],
        [4,8]],
        index=['a','b','d'],
        columns=['omega','epsilon']
                       )

    left
    return left, right


@app.cell
def __(left, pd, right):
    pd.merge(left,right,how='left',on='omega')
    return


@app.cell
def __(left, pd, right):
    pd.merge(left,right,how='left',on='epsilon')
    return


@app.cell
def __(left, pd, right):
    pd.merge(left,right,how='right',on='omega')
    return


@app.cell
def __(left, pd, right):
    pd.merge(left,right,how='inner',on='omega')
    return


@app.cell
def __(left, pd, right):
    pd.merge(left,right,how='outer',on='omega')
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # group

        a shit thing is that by is col, and level is index
        """
    )
    return


@app.cell
def __(df):
    df.groupby(by='column1')
    return


@app.cell
def __(mo):
    mo.md(r"# plot")
    return


@app.cell
def __(df_b):
    df_b.plot.hist()
    return


@app.cell
def __(df_b):
    df_b.plot.scatter(x='a',y='b')
    return


@app.cell
def __(mo):
    mo.md(r"# more complicated stuff")
    return


@app.cell
def __(pd):
    nba = pd.read_csv('nba.csv')
    nba
    return nba,


@app.cell
def __(nba):
    nba.groupby('Team').head()
    return


@app.cell
def __(nba):
    nba.groupby('Team').first()
    return


@app.cell
def __(nba):
    nba.groupby('Team').get_group('Brooklyn Nets') # nba.get_group('Brooklyn Nets') is impossible
    return


@app.cell
def __(nba):
    nba.groupby(['Team','Position']).first() # always remember for more than one use ['x','y','z']. nba.groupby('Team','Position') is a wrong case.
    return


@app.cell
def __(nba):
    nba.groupby(['Position']).Salary.sum().head() # after groupby column-picking is still available
    return


@app.cell
def __(nba):
    nba['Height'] = nba['Height'].str.replace('-', '.', regex=True).astype(float)
    nba.groupby('Team')['Height'].mean().head()
    return


@app.cell
def __(np):
    a = np.array(
        [
            [1,2,3,4],
            [7,8,9,10],
            [5,3,5,7]
        ]
    )

    b = np.array(
        [
            [69,58,65],
            [77,81,70],
            [8,42,8],
            [91,98,92]
        ]
    )

    a@b
    return a, b


@app.cell
def __(np):
    c = [
        [i*j for j in range(4,7)]
        for i in range(6,9)
    ]

    np.array(c)
    return c,


@app.cell
def __(a, np):
    np.transpose(a)
    return


@app.cell
def __(a, b, np):
    np.linalg.det(a@b)
    return


@app.cell
def __(dad, mom):
    class Orphan:
        def __init__(self, dad, mom): # define initial parameters
            self.dad = dad # use self.arg to pass parameters
            self.mom = mom

        def family(self): # define method
            assert self.dad
            if self.dad == '' and self.mom == '':
                return 'whole'
            elif self.dad == '' or self.mom == '':
                return 'single'
            else:
                return 'orphan'

    class Superhero(Orphan):
        def __init__(self, alias):
            super().__init__(dad, mom)
            self.alias = alias

    class Villain(Orphan):
        def __init__(self, dad, mom, alias):
            super().__init__(dad, mom)
            self.alias = alias

    oliver = Superhero('','alive','green arrow')
    oliver.family()
    return Orphan, Superhero, Villain, oliver


if __name__ == "__main__":
    app.run()
