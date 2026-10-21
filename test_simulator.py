import unittest

from simulator import Message, causal_order, fifo_order, total_order


class OrderingTests(unittest.TestCase):
    def setUp(self):
        self.messages = [
            Message("M1", "P1", "P3", 1, 1, "A"),
            Message("M2", "P1", "P3", 2, 2, "B", ("M1",)),
            Message("M3", "P2", "P3", 1, 1, "C"),
            Message("M4", "P2", "P3", 2, 3, "D", ("M3",)),
        ]

    def test_fifo_preserves_each_sender_sequence(self):
        result = fifo_order(self.messages)
        positions = {m.mid: i for i, m in enumerate(result)}
        self.assertLess(positions["M1"], positions["M2"])
        self.assertLess(positions["M3"], positions["M4"])

    def test_causal_dependencies_precede_dependents(self):
        result = causal_order(self.messages)
        positions = {m.mid: i for i, m in enumerate(result)}
        self.assertLess(positions["M1"], positions["M2"])
        self.assertLess(positions["M3"], positions["M4"])

    def test_total_order_is_deterministic(self):
        first = [m.mid for m in total_order(self.messages)]
        second = [m.mid for m in total_order(reversed(self.messages))]
        self.assertEqual(first, second)
        self.assertEqual(first, ["M1", "M3", "M2", "M4"])

    def test_unknown_dependency_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            causal_order([Message("M1", "P1", "P2", 1, 1, dependencies=("M9",))])

    def test_dependency_cycle_is_rejected(self):
        messages = [
            Message("M1", "P1", "P2", 1, 1, dependencies=("M2",)),
            Message("M2", "P2", "P1", 1, 2, dependencies=("M1",)),
        ]
        with self.assertRaisesRegex(ValueError, "cycle"):
            causal_order(messages)

    def test_duplicate_ids_are_rejected(self):
        messages = [
            Message("M1", "P1", "P2", 1, 1),
            Message("M1", "P2", "P1", 1, 2),
        ]
        with self.assertRaisesRegex(ValueError, "unique"):
            total_order(messages)


if __name__ == "__main__":
    unittest.main()
