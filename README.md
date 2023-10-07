# Connect Four AI

Play Connect Four against MiniMax and MCTS AIs.

## Run

```
poetry install
cd src; uvicorn connect_four.app:app
```

## TODO

- Add selector to choose between MiniMax or MCTS
- Configure AI (depth, duration)
- Show which player's turn it is
- Show when there is a tie
- Choose first player (human/ai)
- Fix human win message
