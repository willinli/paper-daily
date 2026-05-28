import datetime as dt
import unittest

from scripts.collect_papers import merge_with_retained_papers, trim_papers_for_storage


def paper(paper_id: str, level: str, published: str) -> dict:
    return {
        "id": paper_id,
        "title": paper_id,
        "published": published,
        "best_match": {
            "topic_id": "topic",
            "topic_name": "Topic",
            "score": {"high": 0.9, "medium": 0.5, "low": 0.2}[level],
            "level": level,
            "reason": "test",
        },
        "matches": [],
        "chinese_summary": {},
    }


class RetentionTest(unittest.TestCase):
    def test_merge_retains_only_previous_high_and_medium(self) -> None:
        now = dt.datetime(2026, 5, 28, tzinfo=dt.timezone.utc)
        existing = {
            "generated_at_iso": "2026-05-27T00:00:00+00:00",
            "papers": [
                paper("old-high", "high", "2026-05-26T00:00:00+00:00"),
                paper("old-medium", "medium", "2026-05-25T00:00:00+00:00"),
                paper("old-low", "low", "2026-05-24T00:00:00+00:00"),
            ],
        }

        merged, stats = merge_with_retained_papers([paper("new-low", "low", "2026-05-28T00:00:00+00:00")], existing, now)

        self.assertEqual({item["id"] for item in merged}, {"new-low", "old-high", "old-medium"})
        self.assertEqual(stats["retained_paper_count"], 2)
        self.assertEqual(stats["dropped_low_relevance_count"], 1)
        self.assertTrue(next(item for item in merged if item["id"] == "old-high")["retained_from_previous_run"])

    def test_storage_trim_removes_low_then_oldest(self) -> None:
        payload = {
            "generated_at_iso": "2026-05-28T00:00:00+00:00",
            "papers": [
                paper("newer-high", "high", "2026-05-28T00:00:00+00:00"),
                paper("older-high", "high", "2026-05-20T00:00:00+00:00"),
                paper("newer-low", "low", "2026-05-28T00:00:00+00:00"),
            ],
            "stats": {},
        }

        trimmed, stats = trim_papers_for_storage(payload, max_stored_papers=2, max_data_bytes=0)
        self.assertEqual({item["id"] for item in trimmed}, {"newer-high", "older-high"})
        self.assertEqual(stats["storage_trimmed_by_level"]["low"], 1)

        payload["papers"] = trimmed
        trimmed, stats = trim_papers_for_storage(payload, max_stored_papers=1, max_data_bytes=0)
        self.assertEqual([item["id"] for item in trimmed], ["newer-high"])
        self.assertEqual(stats["storage_trimmed_by_level"]["high"], 1)


if __name__ == "__main__":
    unittest.main()
