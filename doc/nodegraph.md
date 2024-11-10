flowchart TD
    A[Player node 1] <-->|Creates game 1| B(Matchmaker)
    B -->|finds game 1| C[Player node 3]
    B -->|finds game 1| D[P4]
    B -->|finds game 1| E[P5]
    C -->|connects| A
    D -->|connects| A
    E -->|connects| A

    CC[Player 1 has word] <--> DD[P4 guesses]
    CC <--> EE[P5 guesses]
    CC <--> FF[P6 guesses]
    DD <--> FF
    DD <--> EE
    EE <--> FF
