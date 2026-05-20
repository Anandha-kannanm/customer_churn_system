"""Business rules: discounts, alerts, retention actions."""
from dataclasses import dataclass


@dataclass
class RetentionAction:
    customer_id: str
    action: str
    priority: str
    message: str


def get_retention_actions(
    customer_id: str,
    churn_probability: float,
    tenure: int,
    monthly_charges: float,
    contract: str,
) -> list[RetentionAction]:
    """Determine retention actions based on churn risk and profile."""
    actions = []

    if churn_probability >= 0.7:
        actions.append(RetentionAction(
            customer_id=customer_id,
            action="immediate_call",
            priority="critical",
            message="High churn risk — schedule retention call within 24h",
        ))
        if contract == "Month-to-month":
            actions.append(RetentionAction(
                customer_id=customer_id,
                action="offer_discount",
                priority="high",
                message="Offer 20% discount for 12-month contract upgrade",
            ))
    elif churn_probability >= 0.4:
        actions.append(RetentionAction(
            customer_id=customer_id,
            action="send_survey",
            priority="medium",
            message="Send satisfaction survey and loyalty offer",
        ))

    if tenure < 6 and churn_probability >= 0.5:
        actions.append(RetentionAction(
            customer_id=customer_id,
            action="onboarding_support",
            priority="high",
            message="New customer at risk — assign onboarding specialist",
        ))

    if monthly_charges > 80 and churn_probability >= 0.4:
        actions.append(RetentionAction(
            customer_id=customer_id,
            action="plan_review",
            priority="medium",
            message="Review plan pricing — high monthly charges detected",
        ))

    return actions
