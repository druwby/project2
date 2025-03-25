def shufflecheck(deck, handSize):
    if len(deck) % handSize != 0:
        return False
    
    deck.sort()

    while deck:

        start = deck[0]

        for i in range(handSize):
            curr = start + i

            if curr not in deck:
                return False
            
            deck.remove(curr)

    #if the while loop exits, all of the cards must have been used successfully, and therefore we can..
    return True

if __name__ == "__main__":
    hand1 = [1, 2, 3, 6, 2, 3, 4, 7, 8]
    handSize1 = 3
    hand2 = [1, 2, 3, 3, 4, 5, 6, 7]
    handSize2 = 4
    print(shufflecheck(hand1, handSize1))
    print(shufflecheck(hand2,handSize2))
    

