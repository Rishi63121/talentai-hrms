from typing import List
from sqlalchemy.orm import Session
from backend.models.models import CandidateScore


def recompute_ranks(job_id: int, db: Session) -> None:
    """
    Re-rank all CandidateScore rows for a given job by descending match_score.
    Updates the `rank` column in-place.
    """
    scores: List[CandidateScore] = (
        db.query(CandidateScore)
        .filter(CandidateScore.job_id == job_id)
        .order_by(CandidateScore.match_score.desc())
        .all()
    )
    for position, record in enumerate(scores, start=1):
        record.rank = position
    db.commit()
