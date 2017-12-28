#Blackjack Simulator, used for testing the payout of varying strategies over the inbetween side bet.
#can be easily modified for more robust betting strategy, currently uses defacto dealer betting strategy.
#table/dealer, deck, and player all abstracted to distinct objects.
import random


#def basic_strategyMat():

class Deck(object):
    deck = []
    numerical_deck = []
    currentdeck = []
    def __init__(self):
        self.deck = []
        self.currentdeck = []
        for j in range(0,6):
            for i in range(2,12):
                if i == 10:
                    self.deck.append("K")
                    self.deck.append("Q")
                    self.deck.append("J")
                elif i == 11:
                    self.deck.append("A")
                else:
                    self.deck.append(i)

        self.currentdeck = self.deck.copy()
    def draw(self):
        if len(self.currentdeck) == 0:
            self.currentdeck = self.deck.copy()
        card = self.currentdeck[random.randint(0,len(self.currentdeck))-1]
        self.currentdeck.remove(card)
        return card




class Player(object):

    def __init__(self,m,Dealer,b,bb):
        self.bankroll = m
        self.Dealer = Dealer
        self.standardinb = bb
        self.standardbj = b
        self.bjbet = self.standardbj
        self.inbbet = self.standardinb
        self.cardstack = []

    def getvalue(self,a,bet = "std"):
        if bet == "std":
            if type(a) == int:
                return a
            elif a == "A":
                return 11
            else:
                return 10
        elif bet == "inb":
            if type(a) == int:
                return a
            else:
                a_index = 0
                cards = ["J","Q","K","A"]
                for i in range(0,len(cards)):
                    if a == cards[i]:
                        return i + 11
    def sum_stack(self):
        total = 0
        for a in self.cardstack:
            total = total + self.getvalue(a,"std")
        return total
    def strategy(self):
        if self.sum_stack() < 17:
            self.Dealer.hit(self)
            return False
        else:
            return True
    def bet(self,x = 0,y = 0):
        if x == 0:
            x = self.standardbj
        if self.bankroll - x >= 0:
            self.bjtbet = x
            self.bankroll = self.bankroll - x
        else:
            self.bankroll = 0
            return "broke"
        if self.bankroll - y >=0:
            self.bankroll = self.bankroll - y
            self.inbbet = y
    def bust(self):
        return self.sum_stack()<22
    def won(self,bet = "bj",const = 0):
        if bet == "bj":
            self.bankroll = self.bankroll + 2*self.bjbet
        if bet == "inb":
            self.bankroll = self.bankroll + const*self.inbbet
    def reset(self):
        self.bjbet = self.standardbj
        self.inbbet = self.standardinb
        self.cardstack = []

class Dealer(object):
    players = []
    #D
    #deal
    def __init__(self,n,m = 1000, b = 15, bb = 5):
        for i in range(0,n):
            a = Player(m,self,b,bb)
            self.players.append(a)
            self.D = Deck()
        self.deal = Player(10000000000,self,0,0)
    def hit(self,p):
        p.cardstack.append(self.D.draw())
    def inbetween(self,p):
        cards = p.cardstack
        minn = 14
        maxx = 0
        for a in cards:
            y = p.getvalue(a,"inb")
            if y>maxx:
                maxx = y
        for a in cards:
            y = p.getvalue(a,"inb")
            if y < minn:
                minn = y
        if minn != maxx:
            x = range(minn + 1,maxx)
        else:
            x = range(minn,maxx)
        if (not self.deal.getvalue(self.deal.cardstack[0],"inb") in x):
            return -1
        else:
            spread = maxx - minn
            if spread == 0:
                return 30
            if spread == 2:
                return 12
            if spread == 3:
                return 6
            if spread >3:
                return 1
            else:
                return -1

    def play(self):
        ppl = self.players + [self.deal]
        for i in range(0,len(ppl)): #deals first card
            p = ppl[i]
            broke = p.bet(p.standardbj,p.standardinb)
            if broke == "broke":
                self.players.remove(p)
            p.cardstack.append(self.D.draw())
        for i in range(0,len(self.players)): #deals second card
            p = self.players[i]
            p.cardstack.append(self.D.draw())
        for i in range(0,len(self.players)):
            p = self.players[i]
            j = self.inbetween(p)+1
            t = self.deal.getvalue(self.deal.cardstack[0],"inb")
            p.won("inb",j)
            #print("inbetween",j,t,t in range(min(g),max(g)))
        for i in range(0,len(self.players)):
            p = self.players[i]
            b = False
            while(not b):
                if p.strategy():
                    b = True
        dd = False
        while(not dd):
            if self.deal.strategy():
                dd = True
        print("---Dealer Stack: ", self.deal.cardstack)
        for i in range(0,len(self.players)):
            p = self.players[i]
            if not p.bust() and ((p.sum_stack() > self.deal.sum_stack() or self.deal.bust())): #conditions for player winning
                p.won()
            #p.reset()
        #   for i in range(0,len(self.players)):
            print("Player " + str(i), p.bankroll, "cardstack: ", p.cardstack)
            p.reset()

        self.deal.reset()



global x


def start(k = 100,n = 3,m = 1000,b = 15,bb = 5):
    global x
    x = Dealer(n,m,b,bb)
    for i in range(0,k):
        print("----Round--- " + str(i))
        x.play()
