---
categories: data
description: From Personal notes on working with data
featured_image: covers/pandas-1.png
author: Anders
title: Data Cleaning with pandas
finished: true
date: "2018-11-22"
layout: post
tags: ['pandas', 'python']
---

## Clean data

Pandas is a data library. I dont actually mean those cute bears.

This post is based on a pull from my personal notes when learning to work with 
data in python with pandas (So it might not be perfect, but hey - Im trying). 
These are some of the essentials tools/skills I picked up about cleaning data.

Data scientists actually spend the majority of their time wrangling and cleaning
data, as it is a time consuming and complex process - kind of a grind. It 
is, however, a very essential part of working with data, which is hard to
avoid - and because of this, its worth looking into getting efficient at it.

The conventions in pandas is that pandas is imported as `pd` and dataframes are
called `df`. Im sticking to that convention in my notes.

## Pandas Core utilities

These are some of the essential functions for exploring data with pandas

### Extracting some samples:
{{< highlight python >}}
df.head()  # Gets first 5 rows
df.tail()  # Gets last 5 rows
{{< /highlight >}}

### Getting some df metadata:
{{< highlight python >}}
df.info()  # Gets essential info on dataframe
df.dtypes  # Datatypes
df.columns # get/set
df.describe()  # Some statistical values on the df
df['column'].value_counts()  # counts of unique values on the column (Series method)
{{< /highlight >}}

### Some quick visualization
{{< highlight python >}}
df.column.plot('hist')  # For histogram
df.plot(kind='scatter', x='col', y='col') # Scatter
{{< /highlight >}}

may need to `import matplotlib.pyplot as plt` and run `plt.show()` below

## Data cleaning
### Normalized data:
These are the allmighty laws of normalized data
- Rows form observations
- Columns form variables
- Datasets form observational units

### Melting and pivoting data:
**Meltings** turns columns into rows

{{< highlight python >}}
pd.melt(frame=df, id_vars='fixed_column', value_vars=['columns', 'to', 'melt'],
        var_name='variable col name', value_name='value column name')
{{< /highlight >}}

This will reslt in the `fixed_column` column to be untouched, just broadcasted
down, while the `value_vars` columns will be turned into a variable and value
name column

{{< highlight python >}}
>>> df
   A  B  C
0  a  1  2
1  b  3  4
2  c  5  6

>>> pd.melt(df, id_vars=['A'], value_vars=['B', 'C'],
...         var_name='myVarname', value_name='myValname')
   A myVarname  myValname
0  a         B          1
1  b         B          3
2  c         B          5
3  a         C          2
4  b         C          4
5  c         C          6
{{< /highlight >}}

**Pivoting** takes unique vals from columns and alter the dataset by creating new
columns:

{{< highlight python >}}
df.pivot(index='foo', columns='bar', values='baz')
{{< /highlight >}}

This will result in the 'foo' column becoming the new index, the 'columns'
column becoming the columns and 'baz' column becoming the actual values of the
dataframe.

{{< highlight python >}}
>>> df
    foo   bar  baz
0   one   A    1
1   one   B    2
2   one   C    3
3   two   A    4
4   two   B    5
5   two   C    6

>>> df.pivot(index='foo', columns='bar', values='baz')

bar  A   B   C
foo
one  1   2   3
two  4   5   6

{{< /highlight >}}

Melting and pivoting can be very useful when cleaning data and making it normalized (see criteria on
normalized data above)

As we also can see, melting and pivoting are opposites

## Data Combining:
### Grouping data:
Pandas allows us to group data together:
{{< highlight python >}}
df.groupby('column')
{{< /highlight >}}
This will make pandas group the data by the unique values.  Basically it looks
through the column and groups together the indexes of the different values. It
returns a special group object which we can iterate on and get attributes on to
look at the different groups. Each group in the grouped object is basically
a dataframe for the given group.

[Tutorialspoint](https://www.tutorialspoint.com/python_pandas/python_pandas_groupby.htm)
has a tutorial on this that I found very useful.

### Globbing:
Globbing is useful when retreiving files in a directory, see sample use below:
{{< highlight python >}}
glob.glob(./*.csv) # gets all csv files in current dir
{{< /highlight >}}

### Concatenating data:
Basically, concatenating frames together just glues together multiple frames.
{{< highlight python >}}
pd.concat([df1, df2, ...][, ignore_index=True, axis=1 ])
{{< /highlight >}}
pandas [docs](https://pandas.pydata.org/pandas-docs/stable/merging.html) 
has a nice guide on this.

### Merging data:
Well mergining is merging. Pandas looks at the `on` keys and 

{{< highlight python >}}
pd.merge(left=dfl, right=dfr, [left_on='left column', right_on='right column', on='shared column'])
{{< /highlight >}}
provide either `on=..` if same column name or `left_on/right_on` if differnt name
columns

Returned will be the merged dataset. So for example with a users df with `id`
column merged with visit df with `user_id` column will give us a df with visits
and user info provided, which is nice.

## Cleaning data:
### Datatype Altering:
The more I learn about programming and CS, the more I learn that there are
basically two important things: datatypes and algorithms. Lets work with some
pandas datatype altering.
{{< highlight python >}}
# turn a column of strings to numeric column
df['numbers_as_strings'] = pd.to_numeric(df['numbers_as_strings'])
# turn a column of categories (feks: ['M', 'F']) to categories
df['col'].astype('category')
{{< /highlight >}}
These are very handy, and good clean data should have appropriate datatypes.
If all columns are `object` the df is going to have low performance and be more
difficult to work with.

### Regex:

Regexes are hugely useful when working with strings. Im not going to cover here
how regexes work or how Series.str works, just some basic use of these on a df.

{{< highlight python >}}
# Compiling a basic regex
pattern = re.compile('\d+') # matches 1 or many numbers
pattern.match('w0rd') # False
pattern.match('123') # True

# Using on df
df['column'].str.replace('\d+', 'replacement', regex=True)
df['column'].str.extract('\d+', expand=True)  # Pulls out the first full number
df[df['col'].str.contains('\d+', regex=True)]  # Get rows w/ number in 'col'
{{< /highlight >}}

### Functions to clean data:

One can write python functions or lambdas for doing operations on the data.
This isnt just important when cleaning, its a general important data utility.

{{< highlight python >}}
def myfunc(row):
    return np.sum(row)

def mycolfunc(value):
    return value + 1
{{< /highlight >}}

And applying the function to the datasets:

{{< highlight python >}}
df['myfunc_results'] = df.apply(myfunc, axis=1) # Run row-wise function
df['numplus1'] = df['num'].apply(myfunc) # run func on every val in 'num' column
{{< /highlight >}}

Basically what to remember is that running `axis=1` causes the function to handle
rows, and `axis=0` (default) runs the function cell-wise (even when not
specifying columns to run on)

### Dropping duplicates, filling missed:
Some handy utils when you clean data.
{{< highlight python >}}
df.drop_duplicates() # Only unique rows remain
df.dropna()  # Rows with NaNs are removed
df['col'].fillna(value)  # NaNs are replaces with value
{{< /highlight >}}

### Testing:
To ensure that the datacleaning was successful, it can be very helpful to set
up some tests at the end of the program. Below are some useful samples.
{{< highlight python >}}
# Test that the data is clean
assert(condition)
# Checking if no values in df is NaN
pd.notnull(df).all().all()
# Checking that all df values are larger or equal to zero
(df >= 0).all().all()
{{< /highlight >}}
