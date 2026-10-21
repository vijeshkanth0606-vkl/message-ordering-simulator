"""Educational simulator for FIFO, causal, and total message ordering.

This models ordering decisions in one process; it does not implement real networking
or a distributed consensus protocol.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Message:
    mid: str
    sender: str
    receiver: str
    seq: int
    timestamp: int
    payload: str = ""
    dependencies: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.mid or not self.sender or not self.receiver:
            raise ValueError("Message ID, sender, and receiver must not be empty.")
        if self.seq < 1 or self.timestamp < 0:
            raise ValueError("Sequence must be >= 1 and timestamp must be >= 0.")


def _validate_unique_ids(messages: Iterable[Message]) -> list[Message]:
    items = list(messages)
    ids = [m.mid for m in items]
    if len(ids) != len(set(ids)):
        raise ValueError("Message IDs must be unique.")
    known = set(ids)
    for message in items:
        missing = set(message.dependencies) - known
        if missing:
            raise ValueError(
                f"{message.mid} depends on unknown message(s): {', '.join(sorted(missing))}"
            )
        if message.mid in message.dependencies:
            raise ValueError(f"{message.mid} cannot depend on itself.")
    return items


def fifo_order(messages: Iterable[Message]) -> list[Message]:
    """Group by sender and preserve that sender's sequence.

    FIFO alone does not define a single global order across different senders.
    The sender name is used as a deterministic display tie-breaker for this demo.
    """
    items = _validate_unique_ids(messages)
    seen: set[tuple[str, int]] = set()
    for m in items:
        key = (m.sender, m.seq)
        if key in seen:
            raise ValueError(f"Duplicate sequence {m.seq} for sender {m.sender}.")
        seen.add(key)
    return sorted(items, key=lambda m: (m.sender, m.seq, m.mid))


def causal_order(messages: Iterable[Message]) -> list[Message]:
    """Return a topological order that respects declared causal dependencies."""
    items = _validate_unique_ids(messages)
    by_id = {m.mid: m for m in items}
    remaining = set(by_id)
    delivered: set[str] = set()
    result: list[Message] = []

    # Preserve input order among messages that are currently eligible.
    while remaining:
        ready = [
            m for m in items
            if m.mid in remaining and set(m.dependencies).issubset(delivered)
        ]
        if not ready:
            unresolved = {
                mid: sorted(set(by_id[mid].dependencies) - delivered)
                for mid in sorted(remaining)
            }
            raise ValueError(f"Causal dependency cycle detected: {unresolved}")
        for m in ready:
            result.append(m)
            delivered.add(m.mid)
            remaining.remove(m.mid)
    return result


def total_order(messages: Iterable[Message]) -> list[Message]:
    """Create one deterministic total order using (timestamp, sender, message ID)."""
    items = _validate_unique_ids(messages)
    return sorted(items, key=lambda m: (m.timestamp, m.sender, m.mid))


def demo_messages() -> list[Message]:
    return [
        Message("M1", "P1", "P3", 1, 1, "A"),
        Message("M2", "P1", "P3", 2, 2, "B", ("M1",)),
        Message("M3", "P2", "P3", 1, 1, "C"),
        Message("M4", "P2", "P3", 2, 3, "D", ("M3",)),
    ]


def _ids(messages: Iterable[Message]) -> str:
    return " -> ".join(m.mid for m in messages) or "(no messages)"


def run_demo() -> None:
    messages = demo_messages()
    print("=== MESSAGE ORDERING SIMULATOR ===")
    print("Processes: P1 P2 P3 P4")
    print("Messages:", ", ".join(m.mid for m in messages))
    print("\nFIFO")
    print("Delivery:", _ids(fifo_order(messages)))
    print("\nCAUSAL")
    print("Dependencies:", {m.mid: list(m.dependencies) for m in messages})
    print("Delivery:", _ids(causal_order(messages)))
    print("\nTOTAL")
    print("Order key: (timestamp, sender, message ID)")
    print("Delivery:", _ids(total_order(messages)))
    print("\nNote: FIFO's cross-sender display order is a deterministic tie-break,")
    print("not a guarantee imposed by FIFO semantics.")


def interactive() -> None:
    while True:
        print("\nMessage Ordering Simulator")
        print("1. Run demo")
        print("2. Show message table")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            run_demo()
        elif choice == "2":
            for m in demo_messages():
                print(f"{m.mid}: {m.sender}->{m.receiver}, seq={m.seq}, "
                      f"timestamp={m.timestamp}, dependencies={list(m.dependencies)}")
        elif choice == "3":
            print("Goodbye.")
            return
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    import sys
    if "--interactive" in sys.argv:
        interactive()
    else:
        run_demo()
