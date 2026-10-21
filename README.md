# Message Ordering Simulator

An educational Python implementation of the CS3551 Distributed Computing project: FIFO, causal, and total message ordering.

## Features

- **FIFO ordering:** preserves sequence numbers for each sender.
- **Causal ordering:** uses explicit message dependencies and rejects unknown dependencies or cycles.
- **Total ordering:** sorts by `(logical timestamp, sender ID, message ID)` to produce a deterministic common sequence.
- Demo mode, small interactive menu, and unit tests.

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Run

```bash
python simulator.py
```

Run the interactive menu:

```bash
python simulator.py --interactive
```

Run tests:

```bash
python -m unittest -v
```

## Example

```text
=== MESSAGE ORDERING SIMULATOR ===
Processes: P1 P2 P3 P4
Messages: M1, M2, M3, M4

FIFO
Delivery: M1 -> M2 -> M3 -> M4

CAUSAL
Dependencies: {'M1': [], 'M2': ['M1'], 'M3': [], 'M4': ['M3']}
Delivery: M1 -> M2 -> M3 -> M4

TOTAL
Order key: (timestamp, sender, message ID)
Delivery: M1 -> M3 -> M2 -> M4
```

Exact FIFO display order across different senders is only a deterministic presentation choice: FIFO itself guarantees per-sender order, not a global sequence.

## Important scope note

This is a local educational simulator, not a real distributed networking implementation. The total-order policy uses a deterministic sorting key; it does not implement consensus or a sequencer protocol. Causal dependencies are explicitly supplied with each message.

## Suggested repository structure

```text
message-ordering-simulator/
├── simulator.py
├── test_simulator.py
├── README.md
└── .gitignore
```

## Upload to GitHub

1. Sign in at https://github.com/new and create a repository named `message-ordering-simulator`.
2. Do not initialize it with a README if you plan to push this project as-is.
3. Download and extract this project ZIP.
4. Open a terminal in the extracted folder and run:

```bash
git init
git add .
git commit -m "Implement message ordering simulator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/message-ordering-simulator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub may prompt you to authenticate through a browser or token; never share your password or token in chat.

## Share the repository with your course coordinator (CC)

- **Public repository:** open the repository on GitHub and copy its URL, such as `https://github.com/YOUR-USERNAME/message-ordering-simulator`. Send that link to your CC.
- **Private repository:** open the repository → **Settings** → **Collaborators** (sometimes under **Collaborators and teams**) → **Add people**. Search for your CC's GitHub username or email and send the invitation. They must accept it. Then share the repository URL.
- For a college submission, check whether your CC expects a public link or a private repository invitation.
