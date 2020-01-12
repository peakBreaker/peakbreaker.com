---
categories: big data
description: Ensuring scalability through splitting up our data into chunks - paritioning!
featured_image: covers/database-1.jpg
author: Anders
title: Understanding Database Partitioning
date: "2020-01-12"
draft: true
layout: post
tags: ['database', 'concept', 'scalability']
---

## Understanding parititons

First off, partitioning - in the context of databases - is the process of splitting data into smaller parts to achieve certain benefits.

### Why partitioning? When is it applicable?

There are many different flavors of databases these days, perhaps more than there are socks in my sock drawer, and many of them have partitioning build into their DNA. Partitioning is a core concept in ensuring scalability once data becomes too large or cumbersome to deal with it, or if requirements specify that the data needs to be distributed, which is often the case.

The most, perhaps, cliché reason for splitting data into parts may be just because the data is of a too large volume to fit in memory or on the disk of a single node (i.e. computer holding the database), but it may aswell be because those who read or write the data are doing so too often for a single node to handle. In addition it may because the data is too important to be lost, which means we need to build in some sort of redundancy, so that we dont loose all our precious data if one node blows up for some reason (which one should expect).

I remember being vaguely first introduced to the concept in the form of RAID, or Redundant Array of Inexpensive Disks, at school. The RAID technology is a storage virtualization technology which takes your data and splits it up over more than one disk in order to ensure performance and/or reliability for a nice price. This was very applicable during the 90s when disks were less reliable, much slower and smaller in storage than today. This isnt strictly database partitioning though (because RAID is concerned with disks, not databases), it just entails many of the same concepts (i.e. splitting data).

## Exploring the definitions

Database partitioning may mean splitting the data over multiple disks on one node too. The term has a wide implication and multiple subdefinitions which we will dig into here.

### Partitioning

 A (database) partition is a part of the data in the database. Though I am constraining myself to databases here, the concept is wider and may also apply to other data technologies. For example distributed message broker systems, such as Kafka, are message brokers - not databases - but often use the same partition concepts as databases do.

Paritioning may be done using different techniques, though the underlying concept is splitting our data. For example, say we have 100 rows of data, and we want to partition this data over four partitions. We could take the first 25 rows on partition one, the next 25 on partition two, and so on.  This would be an range based way of partioning.  There are of course others methods. I wont get too much into the exact methods used here, just the main ideas.

### Vertical partitions

In vertical partitions we split the table of data on the columnar level. This is similar to normalization (youre familiar with normalization, right?) in that we create multiple tables we can join by some key - however the goal here isn't to keep things DRY, its to gain the benefits of partitioning.  So given a table:

```
r | a   |   b   |  c  |   d
---------------------------
1 | data | data | data | data
2 | data | data | data | data
3 | data | data | data | data
```

We could split it like 

```
r |  a   |   b    - r |   c  |   d
----------------- - ---------------
 1 | data | data  - 1 |  data | data
 2 | data | data  - 2 |  data | data
 3 | data | data  - 3 |  data | data

```

And then just join them by the row index when we need all the data. Pretty
straight forward

![vertical partitioning animation](/images/posts/partitioning/vertical.gif)

Now we could, for example, put these tables now on different disks on our node to scale our system.

For the eager observer, one might see that what we are doing here is akin to database normalization.  Indeed that is true, though vertical partitioning would be doing it for performance reasons and can go further than normalization - in partitioning the database even further if it is normalized.

### Horizontal Partitions

So if vertical partitioning is to partition based on the columns, horizontal
partitioning is to partitiong based on the rows. The classic example of this
is is to take ranges of zip codes and partition based on that. Say you take the
range 0-1000 into one table, and 1001-2000 in another table.

Of course there are many other techniques for doing this horizontal partitioning, but the main idea is to use some technique for selecing the data and partiton based on that.

![Horizontal partitioning animation](/images/posts/partitioning/horizontal.gif)

^ Shows one table being split into multiple tables based on rows.

### What is a shard?

 So continuing from the above on horizontal partitions.  If we now put the different tables / partitions on seperate machines, we would be sharding the data, possibly granting us multiple scalability benefits.  We could, for example, create copies of the horizontally partitioned data to ensure that we have the data even if one of our computers were to break.

So at this point I asked myself why its a shard if we do put horizontal partitions on seperate nodes, but it is not sharded if we do the same with vertical paritions. The reason, I believe, is because doing this with horizontal partitions guarantees scalability. Aslong as we add nodes to our clusters, we will never run out of room for the data; while doing it with vertical partitions does not provide us with the same guarantee.

## Final thoughts

 Partitioning is a central theme in data engineering, and builds on the fundamental concepts of how to structure data for databases, i.e. row based on column based.

Further its important to note here that I have been writing through the scope of SQL or relational databases, which are known to be difficult to scale in this way due to JOINS, and scaling databases like this are often more common in NoSQL databases. More often with RDBMS is to use master/slave relationships - by creating multiple databases which are duplicates, where one master is written to and the data is propagated to the slaved, which are read - to ensure fault tolerance.

This SQL vs NoSQL is a subject large enough to be explored in its own post. As is the master / follower relationships for RDBMS

## Thanks for reading

So I hope you enjoyed this blogpost! If so, feel free to leave a comment below or [sign up to my newsletter!](https://sub.peakbreaker.com/subscribe)
