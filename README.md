# Second Price Auction: Architecture and Strategy

## Overview
In this project, I create the infrastructure to execute a second price sealed-bid auction and analyze the relative success of different bidding strategies. The infrastucture is implemented via an object oriented paradigm. 

## Motivation
The primary reason for undertaking this project was to practice object oriented programming in Python. However, elements of data analysis and data visualization became pivotal as I moved from infrastructure design to assessment of bidding strategy. This project also contributes to the multi-armed bandit literature, shedding light on how to effectively leverage the explore/exploit approach in a landscape of strategic competitors. 

## What is a second-price auction? And why build one? 
A second price sealed-bid auction is an auction in which an item is offered for sale to a group of potential buyers (or "bidders"). Each bidder submits a single monetary bid (unseen by the other bidders, hence "sealed"). The item is awarded to the bidder who submits the highest bid, and the price paid for the item is the second highest bid submitted (hence "secnd price"). 

In my implementation, the item up for auction is the opportunity to show an advertisement to a user (think of a pop-up ad on a web page). The auction therefore involves a set of **users** and a set of **bidders**. The auction proceeds in a series of rounds; in each round, a user is selected at random and each bidder submits their bid for the opportunity to show an ad to this user. The winning bidder pays the second highest bid and earns 1 dollar if the user clicks on their ad (they earn nothing if the user does not click). Each user has an underlying probability of clicking on an ad and this probability remains constant throughout the entire auction and regardless of which bidder shows them an ad. At the beginning of the auction, the bidders have no knowledge of each user's underlying clicking probability. However, the winning bidder in each round is informed as to whether or not the user clicked on their ad. Each bidder begins with a balance of 0 dollars and their singular objective is to finish the auction with as high a balance as possible (it is okay for a bidder's balance to become negative). 
