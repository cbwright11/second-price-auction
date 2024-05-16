# Second Price Auction: Architecture and Strategy

## Overview
In this project, I create the infrastructure to execute a second price sealed-bid auction and analyze the relative success of different bidding strategies. The infrastucture is implemented via an object oriented paradigm. 

## Motivation
The primary reason for undertaking this project was to practice object oriented programming in Python. However, elements of data analysis and data visualization became pivotal as I moved from infrastructure design to assessment of bidding strategy. This project also contributes to the multi-armed bandit literature, shedding light on how to effectively leverage the explore/exploit approach in a landscape of strategic competition. 

## What is a second price auction? And why build one? 
A second price sealed-bid auction is an auction in which an item is offered for sale to a group of potential buyers (or "bidders"). Each bidder submits a single monetary bid (unseen by the other bidders, hence "sealed"). The item is awarded to the bidder who submits the highest bid, and the price paid for the item is the second highest bid submitted (hence "second price"). 

In my implementation, the item up for auction is the opportunity to show an advertisement to a user (think of a pop-up ad on a web page). The auction therefore involves a set of **users** and a set of **bidders**. The auction proceeds in a series of rounds; in each round, a user is selected at random and each bidder submits their bid for the opportunity to show an ad to this user. The winning bidder pays the second highest bid and earns 1 dollar if the user clicks on their ad (they earn nothing if the user does not click). Each user has an underlying probability of clicking on an ad and this probability remains constant throughout the entire auction and regardless of which bidder shows them an ad. At the beginning of the auction, the bidders have no knowledge of each user's underlying clicking probability. However, the winning bidder in each round is informed as to whether or not the user clicked on their ad. Each bidder begins with a balance of 0 dollars and their singular objective is to finish the auction with as high a balance as possible (balances are allowed to become negative). 

## OOP Implementation

In order to create all the functionality necessary to administer such an auction, I created three classes: a `User()` class, a `Bidder()` class, and an `Auction()` class. Objects created from the `User()` class are initialized with a randomly chosen clicking probability. `Bidder()` objects contain the logic necessary to strategically bid in the auction. Lastly, objects created from the `Auction()` class must be initialized with a set of `User()` objects and a set of `Bidder()` objects. `Auction()` objects have the ability to execute rounds of the auction, keeping track of the bidders' balances along the way. 

## Bidding Logic
The central reasoning that should govern a bidder's behavior in this auction is to bid high for users with high clicking probabilities and bid low for users with low clicking probabilities. However, as mentioned above, bidders begin an auction without any knowledge of the users' clicking probabilities; the only way to approximate these probabilities is to repeatedly win auction rounds and observe the clicking tendencies of the users. Such bevavior invariably loses a bidder money in the short term, but serves as an investment into information that can be used to bid more intelligently in later rounds.  

*insert image of balances by round here*

Therefore, bidding can serve two purposes: (1.) to gain information about the users' clicking probabilities and (2.) to make the bidder money. When a bidder pursues the former objective they are said to be "exploring" and when they pursue the latter they are "exploiting". At least three questions arise for a bidder attempting to leverage an explore/exploit approach to strategic bidding:
1. For how many rounds should I explore before using the information I've gained to exploit?
2. How aggressively should I bid during the exploration stage?
3. How should I use the information gained through exploration to craft the most profitable bids during exploitation? 

The approach that I took to answering these question was to create three numeric variables which take on specific values for a given `Bidder()` object. The variable `alpha` indicates the fraction of the auction for which the bidder will explore; for example, in an auction with $1000$ rounds, an `alpha` value of $0.2$ means that the bidder will explore for $200$ rounds and exploit for $800$ rounds. The `aggressiveness` variable indicates the fixed bid that a bidder will submit during their exploration stage; to continue with the previous example, if this bidder has an `aggressiveness` value of $0.9$, then they will bid \$0.90 for each of the first $200$ rounds. Lastly, to answer the third question, I rely on the assumption that bidding at or near the best estimate of a user's clicking probability is the most effective way to bid during the exploitation stage. The only deviation from this theory was to create a variable called `undercut` which serves to submit bids slightly lower than a given user's estimated clicking probability. For example, if a bidder has an `undercut` value of $0.15$, and - through the information gained during exploration - they estimate that a given user's clicking probability is $0.56$, then they will submit a bid of \$0.41. The task of devising the optimal bidding strategy thus simplifies to finding the values of `alpha`, `aggressiveness`, and `undercut` that maximize a bidder's closing balance. 

It's important to note that this is just one approach to devising bidding logic in a second price sealed-bid auction. More sophisticated approaches abound, but are beyond the scope of what I hoped to gain from this project. For instance, one opportunity that I completely neglect is to incorporate the winning price in each round into bidding logic. While only the winning bidder in a given round can observe the user's clicking behavior, *every* bidder gets to observe the winning price. The reasoning here being that - at least during exploitation - the winning price is likely a good reflection of the given user's clicking probability. This phenomenon sheds light on the fundamentally game theoretical nature of the auction: the suspician that other bidders might incorporate your bids into their estimates of the users' clicking probabilities offers the opportunity to intentionally mislead those bidders. I chose not to engage with this complex opportunity space. 

## Experiment design

## Conclusions
