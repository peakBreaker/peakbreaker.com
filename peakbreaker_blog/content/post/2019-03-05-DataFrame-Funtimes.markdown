---
category: data
subtitle: From Personal notes on working with data
img: covers/pandas-1.png
author: Anders
title: More data manipulation with pandas
finished: true
date: "2019-03-05"
layout: post
tags: ['pandas,', 'python']
---

## Data Exploration

Working with data is a lot of fun. In this day and age, there is a lot of data,
but a lack of data stories.  Exploring data is about uncovering the stories
that the data may hold - whether it is anomalies or powerful insights.

### Beyond the basics

My [first](http://peakbreaker.com/data-cleaning-with-pandas/) post on working
with data using pandas goes into the basics of cleaning data and some core
utilities, I would recommend starting there. In this post I will be exploring
some further tools to manipulating data and uncovering data stories.

### Data insight

Say we start out with a [dataset](https://www.theguardian.com/sport/datablog/2012/jun/25/olympic-medal-winner-list-data) provided by The Guardian on olympic medals won throughout the years.

```
n [1]: medals.head()
... 
Out[1]: 
     City  Edition     Sport Discipline             Athlete  NOC Gender Event                       Event_gender   Medal
0  Athens     1896  Aquatics   Swimming       HAJOS, Alfred  HUN    Men 100m freestyle                         M    Gold
1  Athens     1896  Aquatics   Swimming    HERSCHMANN, Otto  AUT    Men 100m freestyle                         M  Silver
2  Athens     1896  Aquatics   Swimming   DRIVAS, Dimitrios  GRE    Men  100m freestyle for sailors            M  Bronze
3  Athens     1896  Aquatics   Swimming  MALOKINIS, Ioannis  GRE    Men  100m freestyle for sailors            M    Gold
4  Athens     1896  Aquatics   Swimming  CHASAPIS, Spiridon  GRE    Men  100m freestyle for sailors            M  Silver
```

#### Nice utils

These are nice pandas utils that should be quite straight forward. Nice to use

- nunique

```python
grouped = medals.groupby('NOC') #  Group by country
grouped['Sport'].nunique().sort_values(ascending=False) #  Gives num unique sports per country
```

- isin

```python
is_usa_urs = medals['NOC'].isin(['USA', 'URS']) #  Get boolean series
medals.loc[is_usa_urs] #  Get all rows won by either usa or urs
```

- idxmax & idxmin

```python
# Create the pivot table: medals_won_by_country
medals_won_by_country = medals.pivot_table(index='Edition', columns='NOC',
values='Athlete', aggfunc='count')
# Slice medals_won_by_country: cold_war_usa_urs_medals
cold_war_usa_urs_medals = medals_won_by_country.loc[1952:1988, ['USA','URS']]
# Create most_medals 
most_medals = cold_war_usa_urs_medals.idxmax(axis='columns')
# Who won the most medals between ussa and urs during the cold war?
print(most_medals.value_counts())
```

#### value_counts

We can get the number of medals won per country by using
[value_counts](http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html):

```python
# Count the number of medals won by each country: medal_counts
medal_counts = country_names.value_counts()

# Print top 15 countries ranked by medals
print(medal_counts.head())
```

outputs:
```
 USA    4335
 URS    2049
 GBR    1594
 FRA    1314
 ITA    1228
```

#### pivot_table

We can count the values by type using
[pivot_table](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html)

```python
counted = medals.pivot_table(
            index='NOC', # Country as index
            values='Athlete', # Values we will run the aggfunc on
            columns='Medals', # Columns
            aggfunc='count' # How we aggregate the values
            )

counted['totals'] = counted.sum(axis='columns')
counted.sort_values('totals', ascending=False)
```

#### grouping

Grouping is taking common values and creating sets of dataframes underneath.
Thats how I think about it anyway.  Grouping by multiple columns will give
a multi-index df.

```python
medals.groupby(['Event_gender', 'Gender'])
```

outputs:
```
                          City  Edition  Sport  Discipline  Athlete    NOC Event  Medal
    Event_gender Gender                                                                 
    M            Men     20067    20067  20067       20067    20067  20067 20067  20067
    W            Men         1        1      1           1        1      1      1      1
                 Women    7277     7277   7277        7277     7277   7277 7277   7277
    X            Men      1653     1653   1653        1653     1653   1653 1653   1653
                 Women     218      218    218         218      218    218  218    218
```

#### boolean selection

Using boolean operations, we can select values from dfs very nicely:

```python
medals[(medals['Gender'] == 'Men') & (medals['Event_gender'] == 'W')]
```

This returns one row?

#### Stack/unstack

Ehm, Todo.

#### Finally some visualization

Attractive graphs are nice. Lets make some.  Area plots and violin plots are my
favorite.

```python
# Redefine 'Medal' as an ordered categorical
medals.Medal = pd.Categorical(values=medals['Medal'], categories=['Bronze',
'Silver', 'Gold'], ordered=True)

# Create the DataFrame: usa
usa = medals[medals.NOC == 'USA']

# Group usa by 'Edition', 'Medal', and 'Athlete'
usa_medals_by_year = usa.groupby(['Edition', 'Medal'])['Athlete'].count()

# Reshape usa_medals_by_year by unstacking
usa_medals_by_year = usa_medals_by_year.unstack(level='Medal')

# Create an area plot of usa_medals_by_year
usa_medals_by_year.plot.area()
plt.show()
```

![medals](/assets/img/blog/data/medals.svg)
