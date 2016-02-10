from random import shuffle

def printAll():
	print "\nPrinting all hands:"
	print ("K:", king)
	print ("Q:", queen)
	print ("M:", mid)
	print ("L:", low)
	print "\n"


def makeDeck():
	deck = []
	# 2 is the highest value with value 15
	for value in range(3, 16):
		# suits have numeric value to help compare
		for suit in range(1,5):
			deck.append(value*10 + suit)
	return deck

def dealPlacementHand(deck):
	global king, queen, mid, low
	shuffle(deck)
	king = deck[0 : 13]
	queen = deck[13 : 26]
	mid = deck[26 : 39]
	low = deck[39 : 52]
	sortAll()

def dealHand(deck):
	global king, queen, mid, low
	shuffle(deck)
	king = deck[0 : 12]
	queen = deck[12 : 25]
	mid = deck[25 : 38]
	low = deck[38 : 52]
	sortAll()

def sortAll():
	global king, queen, mid, low
	king.sort()
	queen.sort()
	mid.sort()
	low.sort()

def isValidPlay(card, player):
	global prevCard
	if (len(card) < 1 or len(card) > 4):
		return False
	for i in card:
		if (i not in player):
			return False
	
	print len(card)
	print len(prevCard)
	if ((len(card) != len(prevCard) and len(prevCard) != 0) and len(card) != 4):
		return False

	# here I need to check if all the cards have same value
	temp = card[0] / 10
	for i in card[1:]:
		if (i / 10 != temp):
			return False

	if (len(prevCard) == 0):
		return True
	elif (len(card) == 4 and len(prevCard) != 4):
		return True
	else:
		return card[0] > prevCard[0]
		
def trade():
	global king, queen, mid, low
	print("Lows full hand", low)
	handSeen = []
	kingSuitFree = set(x / 10 for x in king)

	for i in kingSuitFree:
		for j in low:
			if (i == j / 10):
				handSeen.append(j)
	print("Hand displayed", handSeen)

	takeCards = raw_input("pick 3 cards to take")
	takeCards = takeCards.split()
	takeCards = [int(x) for x in takeCards]

	giveCards = raw_input("pick 3 cards to give")
	giveCards = giveCards.split()
	giveCards = [int(x) for x in giveCards]

	print (takeCards, giveCards, low)
	
	for i in takeCards:
		del low[low.index(i)]
		king.append(i)

	for i in giveCards:
		del king[king.index(i)]
		low.append(i)
	
	sortAll()
	printAll()

def updateScore():
	pass

def playCard(player):
	global thisPass, prevCard

	thisPass = False
	selection = raw_input("pick cards or (p)ass (actual value)")
	if (selection == "p"):
		thisPass = True
		return player
	else:
		selection = selection.split()
		selection = [int(x) for x in selection]

	# selecting a valid card		
	while (not isValidPlay(selection, player)):
		print ("failed, try again")
		print player
		selection = raw_input("pick card or (p)ass (actual value...)")
		if (selection == "p"):
			thisPass = True
			return player
		else:
			selection = selection.split()
			selection = [int(x) for x in selection]
	
	print ("card played: ", selection)
	# only keeps track of value of card not suit
	prevCard = selection
	for i in selection:
		del player[player.index(i)] 
	return player

# plays a hand, which consists of multiple "tricks"
def playHand():
	global king, queen, mid, low
	global passCount
	global thisPass

	kPass = False
	qPass = False
	mPass = False
	lPass = False
	handWin = False
	
	trade()
	

	while (not handWin):
		if (not kPass):
			print "King's turn"
			king = playCard(king)
			kPass = thisPass
		else:
			print "King passed"
		if (not qPass):
			print "Queen's turn"
			queen = playCard(queen)
			qPass = thisPass
		else:
			print "Queen passed"
		if (not mPass):
			print "Mid's turn"
			mid = playCard(mid)
			mPass = thisPass
		else:
			print "Mid passed"
		if (not mPass):
			print "Low's turn"
			low = playCard(low)
			lPass = thisPass
		else:
			print "low passed"

	updateScore()	

king = []
queen = []
mid = []
low =[]

thisPass = False
passCount = 0
prevCard = []

gameWin = False
deck = makeDeck()

# placement round
dealPlacementHand(deck)
printAll()
playHand()
printAll()
