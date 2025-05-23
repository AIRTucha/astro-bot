from datetime import datetime
from sqlalchemy.orm import Session
from astrogpt.models.warning import Warning, WarningType


def add_warning(
    session: Session, user_id: int, warning: WarningType, warning_explanation: str
):
    # Create a new message instance
    new_warning = Warning(
        user_id=user_id,
        warning=warning,
        timestamp=datetime.now(),
        warning_explanation=warning_explanation,
    )

    # Add the message to the session and commit it
    session.add(new_warning)
    session.commit()
    return new_warning
