# from bidder_wright import Bidder
import numpy as np
import matplotlib.pyplot as plt

class User():
    """This class creates users that are to be shown ads"""
    
    def __init__(self):
        self.__probability = np.random.uniform(0, 1)
    
    def show_ad(self):
        """Returns a boolean: True if the user clicks on the add, False otherwise. Remember that the user's 
        likelihood of clicking is not influenced at all by who the specific bidder is that shows the ad. All that
        matters is the user's secret probability of clicking"""
        
        ad_id = np.random.uniform(0, 1)
        if ad_id <= self.__probability:
            return True
        else:
            return False
    
    # this method is just for development purposes, I might remove
    def get_prob(self):
        return round(self.__probability, 2)


class Auction():
    """This class creates Auction objects. So a given auction object will have info on the number of bidders
    and the number of users in the game. You can call the .execute_rounds() method as many times as you want rounds  
    in your auction. 
    Attributes are:
    bidders
    users
    balances
    winning_prices
    wins_by_bidder
    bids_by_user
    winning_price_by_user
    num_rounds
    balances_by_round"""
    
    def __init__(self, users, bidders, auction_id=None):
        self.bidders = bidders
        self.users = users
        self.balances = {bidder:0 for bidder in self.bidders} # finances will be completely handled in Auction class
        self.winning_prices = []
        self.wins_successes_by_bidder = {bidder:[0,0] for bidder in self.bidders} # keep track of how many wins each bidder has
        self.bids_by_user = {i:[0,0] for i in range(len(users))} # keep track of the average of EVERY bid by user
        self.winning_price_by_user = {i:[0,0] for i in range(len(users))} # keep track of the average of WINNING PRICE by user
        self.num_rounds = 0
        self.balances_by_round = {bidder:[0] for bidder in self.bidders}
        self.secret_probs = [user.get_prob() for user in users]
        self.rounds = {}
        self.auction_id = auction_id
    
    def execute_round(self):
        """This should execute all the steps within a single round of the game"""
        
        # choose a user at random
        user = np.random.randint(0, len(self.users)) 
        
        bids = {} # store the bids in a dictionary --> bidder is the key, their bid is the value
        # call bid for each bidder using the id of the chosen user
        for bidder in self.bidders:
            bid = bidder.bid(user)
            bids[bidder] = bid
        
        max_bid = 0            # only for the purpose of determining winning_bidder and winning price
        second_highest_bid = 0 # starts at zero
        winning_bidders = []
        for bidder,bid in bids.items():
            if bid > max_bid:
                second_highest_bid = max_bid
                max_bid = bid
                winning_bidders.clear()
                winning_bidders.append(bidder) 
            elif bid == max_bid:
                winning_bidders.append(bidder)
                second_highest_bid = bid
            elif bid > second_highest_bid:
                second_highest_bid = bid
        winning_bidder = np.random.choice(winning_bidders)
            
        # show the ad to the user
        ad_outcome = self.users[user].show_ad()
        
        # loop through the bidders to notify each of them of the outcome of the auction round
        # also adjust their balances accordingly
        for bidder in self.bidders:
            # the winner also gets to find out the result of showing the add to the user
            if bidder == winning_bidder:
                bidder.notify(True, second_highest_bid, ad_outcome) 
                self.balances[bidder] -= second_highest_bid
#                 bidder.balances -= second_highest_bid
                if ad_outcome:
                    self.balances[bidder] += 1
#                     bidder.balances += 1
                #     self.wins_successes_by_bidder[bidder][1] += 1 # just for diagnostics, not crucial
                # self.wins_successes_by_bidder[bidder][0] += 1 # just for diagnostics, not crucial
            else:
                bidder.notify(False, second_highest_bid, None)
        
        # following four blocks are just for diagnostics, not crucial
        bids_mean = np.mean([bid for bid in bids.values()]) # take the average of the bids for this round
        # and update the instance attribute bids_by_user to update the average bid for them
        self.bids_by_user[user][0] = (self.bids_by_user[user][0] + bids_mean)/(self.bids_by_user[user][1] + 1)
        self.bids_by_user[user][1] += 1 # increment the number of rounds that they've been selected by 1
        
        # update the average of the winning prices for each user
        self.winning_price_by_user[user][0] = (self.winning_price_by_user[user][0] + second_highest_bid)/(self.winning_price_by_user[user][1] + 1)
        self.winning_price_by_user[user][1] += 1 # increment the number of rounds they've been selected by 1
        
        # update balances by round to see the history of the bidders balances over the course of the game
        for bidder in self.bidders: 
            self.balances_by_round[bidder].append(self.balances[bidder])
        
        # update num_rounds
        self.num_rounds += 1
        
        self.rounds[self.num_rounds] = [user, self.secret_probs[user], ad_outcome]
        
        self.winning_prices.append(second_highest_bid)
                
                
    # optional
    def plot_history(self, info_type="balance_history"):
        """Create a visual representation of how the auction has proceeded. 
        info_type parameter determines what type of graph you are shown. Options are:
        balance_history
        wins_by_bidder
        winning_prices
        bids_by_user
        winning_price_by_user
        summary_by_round
        """
        
        if info_type == "balance_history":
            x = np.arange(self.num_rounds + 1)
            # create several lists, each representing the history of each bidder's balance over the course of the game
            y = [[balance for balance in self.balances_by_round[bidder]] for bidder in self.bidders]
            for bidder in y:
                plt.plot(x,bidder)
            # plt.legend(["bidder" + str(i) for i in range(len(y))])
            legend = ["bidder" + str(i) + " | alpha: " + str(self.bidders[i].alpha) + ", agg: " + str(self.bidders[i].aggressiveness) for i in range(len(self.bidders))]
            legend[0] = "bidder0 | bids only $0"
            legend[-1] = "bidder" + str(len(legend) - 1) + " | bids randomly"
            plt.legend(legend, bbox_to_anchor=(1.05, 1.0))
            plt.xlabel("round")
            plt.ylabel("balance")
            plt.title("history of balances by bidder over the rounds")
            plt.show()
        
        elif info_type == "wins_by_bidder":
            x = ["bidder" + str(i) for i in range(len(self.bidders))]
            num_wins = [self.wins_successes_by_bidder[bidder][0] for bidder in self.bidders]
            num_successes = [self.wins_successes_by_bidder[bidder][1] for bidder in self.bidders]
            
            w = 0.4
            bar1 = np.arange(len(x))
            bar2 = [i+w for i in bar1]
            
            plt.bar(bar1, num_wins, w, label="number of wins")
            plt.bar(bar2, num_successes, w, label="number of successes")
            
            plt.xticks(bar1+w/2, x)
            plt.xlabel("bidder")
            plt.ylabel("wins and successes")
            plt.legend()
            plt.title("Number of wins and successes by bidder")
            plt.show()
            
        elif info_type == "winning_prices":
            x = np.arange(1, self.num_rounds+1)
            y = [winning_price for winning_price in self.winning_prices]
            plt.scatter(x,y)
            plt.xlabel("round number")
            plt.ylabel("price")
            plt.title("winning prices by rounds")
            plt.show()
            
        elif info_type == "bids_by_user":
            x = np.arange(len(self.users))
            y = [pair[0] for pair in self.bids_by_user.values()]
            z = [prob for prob in self.secret_probs]
            
            w = 0.4
            bar1 = np.arange(len(x))
            bar2 = [i+w for i in bar1]
            
            plt.bar(bar1, y, w, label="average of bids")
            plt.bar(bar2, z, w, label="secret probabilities")
            
            plt.xticks(bar1+w/2, x)
            
            plt.xlabel("user_id")
            plt.ylabel("bid amount and secret probability")
            plt.title("comparison of bidders attempts per user vs users' actual clicking likelihoods")
            plt.legend()
            plt.show()
            
        elif info_type == "winning_price_by_user":
            x = np.arange(len(self.users))
            y = [pair[0] for pair in self.winning_price_by_user.values()]
            plt.bar(x,y)
            plt.xlabel("user_id")
            plt.ylabel("bid amount")
            plt.title("average of the winning bids in each round by user")
            plt.show()
            
        elif info_type == "summary_by_round":
            # I want to know which user was selected
            # I want to know their clicking likelihood
            # I want to know whether they clicked
            # I want to know which bidder won **
            # I want to know the winning price
            return self.rounds
            
            
            
            

