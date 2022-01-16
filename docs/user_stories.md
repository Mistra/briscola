# 1 Interazioni su lobby

## Scenario 1.1: Il giocatore A entra e lascia

Giocatore A senza ID_giocatore ne ID_lobby richiede lobby.
Giocatore A lascia lobby.

## Scenario 1.2: Il giocatore A crea una lobby, lascia e passa alla lobby a B

Giocatore A senza ID_giocatore ne ID_lobby richiede lobby.
Giocatore A lascia lobby.
Giocatore A passa ID_lobby a Giocatore B.
Giocatore B richiede di entrare in lobby, il server lo permette (tiene/ricrea lobby?).

## Scenario 1.3: Il giocatore A vuole giocare ma B lascia anzitempo

Giocatore A senza ID_giocatore ne ID_lobby richiede lobby.
Giocatore A passa ID_lobby a Giocatore B.
Giocatore B entra nella lobby.
I giocatori conoscono i reciproci nomi.
Giocatore B lascia subito dopo.
Giocatore A resta nella lobby.

## Scenario 1.4: I giocatori A e B vogliono giocare

Ambo i giocatore sono in lobby e settano lo stato a ready.
Il gioco inizia

# 2 Interazioni su game

## Scenario 2.1: Interazione iniziale (lettura)

Ogni giocatore esegue i seguenti comandi una volta:

- Mostra la briscola

## Scenario 2.2: Interazione in caso di ripristino in seguito a crash/uscita (lettura)

Il giocatore esegue i seguenti comandi una volta:

- Mostra la briscola
- Mostra il numero di carte rimanenti nel mazzo
- Mostra il mio punteggio

## Scenario 2.3: Interazione ciclica di turno (lettura)

Il giocatore esegue i seguenti comandi (a ripetizione):

- Mostra le mie carte
- Richiesta turno (tocca a me?)
- Guarda le carte sul tavolo
- Mostra l'ultima giocata

## Scenario 2.4: Interazione attiva su turno (scrittura)

Il giocatore può scegliere di eseguire uno dei seguenti comandi:

- Gioca carta
- Arrenditi
