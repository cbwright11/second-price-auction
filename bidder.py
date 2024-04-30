import numpy as np

class Bidder():
    """This class creates bidders equipped with knowledge of the number of users in the auction and the number 
    of auction rounds to be played"""
    
    def __init__(self, num_users, num_rounds, bidder_id = None, bidder_type = "smart", alpha = 0.1, aggressiveness = 0.85, under_cut = 0):
        # third entry is the estimated clicking likelihood of the user
        self.prob_estimates = {i:[0,0,0] for i in range(num_users)}
        self.current_user = 0 
        self.alpha = alpha
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.under_cut = under_cut
        self.current_round = 0
        self.aggressiveness = aggressiveness
        self.bidder_type = bidder_type
        self.bidder_id = bidder_id
    
    def bid(self, user_id):
        """Returns a non-negative amount of money. If you don't wish to bid anything on a given user, this should 
        return 0.
        My strategy is to explore for the first `alpha` percent of the game with a bid of `aggressiveness` dollars.
        Then I enter the exploit phase and bid `under_cut` dollars below my estimate of the user's likelihood of 
        clicking."""
        self.current_user = user_id

        if self.bidder_type == "smart":
            if self.current_round / self.num_rounds < self.alpha: # for the first `alpha` percent of the game
                self.current_round += 1
                return self.aggressiveness # simply bid `aggressiveness` = 0.6
            else: # for the rest of the game
                self.current_round += 1
                return self.prob_estimates[user_id][2] - self.under_cut # base the bid on the estimated clicking likelihood of the user
        elif self.bidder_type == "random":
            return np.random.uniform()
        else:
            return 0
        
    
    def notify(self, auction_winner, price, clicked=None):
        """Used to send info about what happened in a round back to the bidder. auction_winner will be a boolean:
        True if the bidder won a given round, False otherwise. price will be the amount of the second bid, only the
        winner pays this. clicked will only take on a value if auction_winner is True (if the bidder won that given
        round) in which case it will take on a boolean value: True if the user clicked on the ad and False 
        otherwise"""
        if auction_winner:        # If the bidder won the auction
            if clicked:           # Additionally, if the user clicked
                # update the prob_estimates dictionary for the current user
                self.prob_estimates[self.current_user][0] += 1
                self.prob_estimates[self.current_user][1] += 1
                self.prob_estimates[self.current_user][2] = self.prob_estimates[self.current_user][0] / self.prob_estimates[self.current_user][1]
            else:  # if the user didn't click
                # update the prob_estimates dictionary for the current user
                self.prob_estimates[self.current_user][1] += 1
                self.prob_estimates[self.current_user][2] = self.prob_estimates[self.current_user][0] / self.prob_estimates[self.current_user][1]


