# Endpoint Server

## Lobby

- lobby/create

  - tipo: **POST**
  - richiesta: {"name": "player_name"}
  - risposta: {"player_id": "abcdefgh", "lobby_id": "abcdefghij"}
  - header: Opzionale {"player_id": "abcdefgh"}

- lobby/join
  - tipo: **POST**
  - richiesta: {"name": "player_name", "lobby_id": "abcdefghij"}
  - risposta: {"player_id": "abcdefgh"}
  - header: Opzionale {"player_id": "abcdefgh"}
- lobby/{lobby_id}/leave
  - tipo: **GET**
  - header: Opzionale {"player_id": "abcdefgh"}
- lobby/{lobby_id}/players
  - tipo: **GET**
  - risposta: [{"player_id": "abcdefgh", "player_name":"gino"}, {...}]

## Game (per ogni chiamata serve un header con player_id)

- game/{lobby_id}/ready
  - tipo: **POST**
  - richiesta: {"state": true}
- game/{lobby_id}/stats
  - tipo: **GET**
  - richiesta: statistiche, da definire
- game/{lobby_id}/player_state
  - tipo: **GET**
  - risposta: [{"player_id": "abcdefgh", "state":true}, {...}]
- game/{lobby_id}/cards
  - tipo: **GET**
  - risposta: {"cards": [{"suit": "1", "rank": "1"}, {"suit": "2", "rank": "2"}, {"suit": "3", "rank": "3"}]}
- game/{lobby_id}/play_card
  - tipo: **POST**
  - richiesta: {"card": {"suit": "1", "rank": "1"}}
  - risposta: None
- game/{lobby_id}/last_played_hand (**nota** ha senso dire che questa chiamata non è vincolata allo stato del game?)
  - tipo: **GET**
  - risposta: {"last_hand": {"winner_player_id": "abcdefgh", "winner_card":{"suit": "1", "rank": "1"}, "loser_card":{"suit": "2", "rank": "2"}}}
- game/{lobby_id}/cards_on_table
  - tipo: **GET**
  - risposta: {"card": {"suit": "1", "rank": "1"} ... }
- game/{lobby_id}/my_turn
  - tipo: **GET**
  - risposta: {"my_turn": true }
- game/{lobby_id}/my_score
  - tipo: **GET**
  - risposta: {"actual_score": "23" }
- game/{lobby_id}/briscola
  - tipo: **GET**
  - risposta: {"card": {"suit": "1", "rank": "1"}}
- game/{lobby_id}/deck_size
  - tipo: **GET**
  - risposta: {"size": 22}
- game/{lobby_id}/surrender
  - tipo: **POST**
  - richiesta: None
