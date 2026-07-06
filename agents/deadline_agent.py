"""
Deadline Agent
--------------
Checks whether a scheme has a fixed deadline and how many days
remain, so citizens don't miss application windows.
"""

from datetime import datetime


def get_deadline_status(scheme):
    deadline = scheme.get("deadline", "Rolling")

    if deadline == "Rolling":
        return {"status": "Rolling / No fixed deadline", "urgent": False}

    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        days_left = (deadline_date - datetime.now()).days

        if days_left < 0:
            return {"status": "Deadline has passed", "urgent": False}
        elif days_left <= 30:
            return {
                "status": f"Closing soon! Only {days_left} days left (by {deadline})",
                "urgent": True,
            }
        else:
            return {
                "status": f"{days_left} days left (deadline: {deadline})",
                "urgent": False,
            }
    except ValueError:
        return {"status": deadline, "urgent": False}
