# -*- coding: utf-8 -*-

# -- Sheet --

import pathlib

pathlib.Path.cwd()


os.listdir()

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Any results you write to the current directory are saved as output.

# Import the required modules and set some parameters

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white",color_codes=True)
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")
plt.rcParams['figure.figsize'] = (15,9.27)

# # 1.relationship between strokes and the frequency of us


# import data with pandas
df = pd.read_csv('hanziDB.csv')
# View basic information of the data
df

df.info()
df.describe()

df["stroke_count"]

print("Value of row 804")
display(df.iloc[804])

# This stroke data was incorrectly entered as "8 9" and needs to be corrected.
df.loc[804,'stroke_count'] = 8

# Convert data types to integers
df.frequency_rank = df.frequency_rank.astype(int)
df.stroke_count = df.stroke_count.astype(int)

df.stroke_count.describe()

# ### Boxplot graph showing stroke count and frequency of use


sns.boxenplot(df.stroke_count, df.frequency_rank)

# We can find that the more strokes of Chinese characters, the lower the frequency of use.


# # Zipf's Law 
# 
# Zipf's Law is an empirical law formulated using mathematical statistics that refers to the fact that for many types of data studied in the physical and social sciences, the rank-frequency distribution is an inverse relation. 
# 
# In probability, this asserts that the frequencies ***f*** of certain events are inversely proportional to their rank ***r***. The law was originally proposed by American linguist George Kingsley Zipf (1902–50) for the frequency of usage of different words in the English language; this frequency is given approximately by $ f(r) \cong \frac{0.1}{r}$. Thus, the most common word (rank 1) in English, which is "the", occurs about one-tenth of the time in a typical text; the next most common word (rank 2), which is "of", occurs about one-twentieth of the time; and so forth.
# 
# Another way of looking at this is that a rank ***r*** word occurs ***1/r*** times as often as the most frequent word, so the rank 2 word occurs half as often as the rank 1 word, the rank 3 word one-third as often, the rank 4 word one-fourth as often, and so forth. Beyond about rank 1,000, the law completely breaks down.
# 
# The law is similar in concept, though not identical in distribution, to Benford's law. 
# 
# References:
# 
# - 1 - https://en.wikipedia.org/wiki/Zipf%27s_law 
# - 2 - https://www.britannica.com/topic/Zipfs-law 


# The data from http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO allows us to analyze the frequency of a total of 9,933 Chinese characters and their frequency rankings, which can be used to verify the applicability of Zipf's law in Chinese.



hanzi = pd.read_excel('hanzi_freq.xlsx')
hanzi.head(10)

hanzi.info()
hanzi.describe()

# From the hanzi dataset we can see that based how many times a character haas been used ("freq" column), it has an associated frequency percentage (freq_percent). This is then summed up within all of the characters present in the dataset ("cum_freq_percent") to analyze its distribution over a graph.


px.line(hanzi, x="rank", y="cum_freq_percent", )

# Zipf's law is most easily observed by plotting the data on a log-log graph, with the axes being the logarithm of rank order, and logarithm of frequency. It is also possible to plot reciprocal rank against frequency or reciprocal frequency or interword interval against rank. Assuming Zipf's Law to be true, there will be a linear relationship between these two variables of inverse polarity aka the higher the log, the lower the rank. 


hanzi['log_rank'] = np.log10(hanzi['rank'])
hanzi['log_freq'] = np.log10(hanzi['freq'])
hanzi['log_cum_freq'] = np.log10(hanzi['cum_freq_percent'])
hanzi.head(10)

fig = px.scatter(hanzi, x="log_rank", y="log_freq", trendline= "ols") 

results = px.get_trendline_results(fig)
print(results)

results.px_fit_results.iloc[0].summary()

fig

# We can find that the application of zipf's law in Chinese characters is not ideal. One possible reason is that Chinese uses more two-syllable or multi-syllable words to express meaning than a single Chinese character. But it could also be associated with the decaying effect of the Zipf's Law after the 1000th values. We can use linear regression to analyze the relationship between the two. First, let's define a helper function whics use the statsmodels library for linear regression.


def reg(y,*args):
    import statsmodels.api as sm
    x = np.vstack((args)).T
    mat_x = sm.add_constant(x)
    res = sm.OLS(y,mat_x).fit()
    print(res.summary())

reg(hanzi.log_freq,hanzi.log_rank)

# Let's then use only the first 1000 characters in rank to have an idea of


sns.regplot(hanzi.log_rank[:1000],hanzi.log_freq[:1000])
x = np.linspace(0,3)
y = -x + 7
plt.plot(x,y,'r--')
plt.text(0.75,6.8,r'',fontsize=20)
plt.xlim(0,2.5)
plt.ylim(5.3,7)

