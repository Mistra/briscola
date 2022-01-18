# Oggetti di modello

Gli oggetti di modello rappresentano i contenitori di dati. Sono entità di tipo "passivo" (non agiscono direttamente ma vengono manipolate), costituiscono inoltre il layer DTO con cui client e server si scambiano informazioni.

## Lobby

Una lobby è intesa come una "stanza" dove i giocatori possono sfidarsi in più partite consecutive.
Viene creata all'ingresso di un giocatore e rimane aperta fino a quando tutti i giocatori nella lobby hanno deciso di uscire o un meccanismo di svecchiamento (da definire) decide che la lobby è stantia.

```json
{
  "id": "abcdefghij",
  "player_ids": ["abcdefgh", "cbcdefgh"],
  "created_at": "2020-01-01T00:00:00Z",
  "last_activity_at": "2020-01-01T00:00:00Z"
}
```

## Game

Un game è una singola partita di briscola.
Ha tre possibili stati: iniziale, in corso e terminato.
Non possono essere presenti in una lobby più di un game iniziale/in-corso contemporaneamente.

```json
{
  "id": 1,
  "lobby_id": "abcdefghij",
  "created_at": "2020-01-01T00:00:00Z",
  "last_activity_at": "2020-01-01T00:00:00Z",
  "state": 0
}
```

## Card

La carta è l'unità di base del mazzo. Ci sono 40 carte in totale, ogni carta è contraddistinta da un seme (suit) e il valore (rank).

Il seme di una carta è un valore numerico compreso tra 1 e 4, qui rappesentati come:

    - HEART
    - SPADE
    - DIAMOND
    - CLUB

Il rank di una carta è un valore numerico compreso tra 1 e 10, seguono nome e punteggio:

    - DEUCE - 0 pts
    - FOUR  - 0 pts
    - FIVE  - 0 pts
    - SIX   - 0 pts
    - SEVEN - 0 pts
    - JACK  - 2 pts
    - QUEEN - 3 pts
    - KING  - 4 pts
    - THREE - 10 pts
    - ACE   - 11 pts

## Deck

Un deck è il mazzo messo a disposizione per una singola partita.
All'inizio del gioco viene creato e contiene 40 carte mescolate.
Al procedere dell'avanzamento del gioco il deck perde progressivamente carte fino a raggiungere la cardinalità di 0.

```json
{
  "id": 1,
  "game_id": 1,
  "cards": [
    { "suit": 1, "rank": 1 },
    { "suit": 2, "rank": 2 }
  ]
}
```

## Player

Il giocatore rappresenta l'entità giocante. Al momento è provvisto di un id univoco e di un nome.

```json
{
  "id": "abcdefgh",
  "name": "John Doe"
}
```

## PlayerHand

Ogni giocatore presente in un gioco iniziato possiede una mano di carte (3 o meno) giocabili quando il suo turno lo consente.

```json
{
  "id": 1,
  "game_id": 1,
  "player_id": "abcdefgh",
  "cards": [
    { "suit": 1, "rank": 1 },
    { "suit": 2, "rank": 2 },
    { "suit": 3, "rank": 3 }
  ]
}
```

## TableHand

La mano del tavolo contiene le carte attualmente in gioco, il numero è variabile tra 0 e 2.

```json
{
  "id": 1,
  "game_id": 1,
  "play": [
    { "player_id": "abcdefgh", "card": { "suit": 1, "rank": 1 } },
    { "player_id": "bbcdefgh", "card": { "suit": 2, "rank": 2 } }
  ]
}
```

## PlayerStack

Lo stack del giocatore è la pila di carte ottenuta dalla vincita delle mani. All'inizio della partita è sempre a 0 e aumenta con ogni vincita di mano.

```json
{
  "id": 1,
  "game_id": 1,
  "player_id": "abcdefgh",
  "cards": [
    { "suit": 1, "rank": 1 },
    { "suit": 2, "rank": 2 },
    { "suit": 3, "rank": 3 },
    { "suit": 4, "rank": 4 }
  ]
}
```
