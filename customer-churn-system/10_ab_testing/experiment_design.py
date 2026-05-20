"""A/B testing experiment design for retention campaigns."""
import hashlib
from dataclasses import dataclass
from enum import Enum


class Variant(Enum):
    CONTROL = "control"
    TREATMENT = "treatment"


@dataclass
class Experiment:
    name: str
    control_pct: float = 0.5
    description: str = ""


DEFAULT_EXPERIMENT = Experiment(
    name="retention_discount_v1",
    control_pct=0.5,
    description="Test 20% discount offer vs standard retention email",
)


def assign_variant(customer_id: str, experiment: Experiment = DEFAULT_EXPERIMENT) -> Variant:
    """Deterministically assign customer to control or treatment."""
    hash_val = int(hashlib.md5(f"{experiment.name}:{customer_id}".encode()).hexdigest(), 16)
    return Variant.TREATMENT if (hash_val % 100) / 100 >= experiment.control_pct else Variant.CONTROL


def get_treatment_action(variant: Variant) -> str:
    """Return action for assigned variant."""
    if variant == Variant.TREATMENT:
        return "send_20pct_discount_offer"
    return "send_standard_retention_email"
