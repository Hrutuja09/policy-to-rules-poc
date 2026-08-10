"""Shared Pydantic data models for the policy-to-rules POC.

This module is the data contract between the LLM extraction step and the
deterministic evaluation step. Every PolicyRule carries source_text so
derived rules remain auditable against the original policy span.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Condition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str  # e.g. "procedure_code", "units", "modifier", "place_of_service"
    operator: Literal["==", "!=", ">", "<", ">=", "<=", "in", "not_in"]
    value: str | int | float | list[str]


class PolicyRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    description: str  # plain-language statement of the rule
    conditions: list[Condition]
    action: Literal["allow", "flag", "deny", "limit_units"]
    code_references: list[str]  # CPT/HCPCS/ICD codes named in the policy
    source_text: str  # the exact policy span this rule was derived from


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    type: Literal["code", "modifier", "procedure", "diagnosis", "limit", "other"]


class ExtractedPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_ref: str  # which sample file this came from
    summary: str  # plain-language summary of the whole policy
    rules: list[PolicyRule]
    entities: list[Entity]


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    procedure_codes: list[str]
    units: int = 1
    modifiers: list[str] = Field(default_factory=list)
    diagnosis_codes: list[str] = Field(default_factory=list)
    place_of_service: str | None = None


class TriggeredRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    action: str
    reason: str
    source_text: str


class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    outcome: Literal["pass", "flag", "deny"]
    triggered_rules: list[TriggeredRule]
    explanation: str


if __name__ == "__main__":
    example_policy = ExtractedPolicy(
        source_ref="policy_01_coverage.txt",
        summary="Example coverage policy limiting units for CPT 97110.",
        rules=[
            PolicyRule(
                rule_id="R1",
                description="Flag claims billing more than 4 units of 97110.",
                conditions=[
                    Condition(field="procedure_code", operator="==", value="97110"),
                    Condition(field="units", operator=">", value=4),
                ],
                action="flag",
                code_references=["97110"],
                source_text="Therapeutic exercise (97110) is limited to 4 units per day.",
            )
        ],
        entities=[
            Entity(text="97110", type="code"),
            Entity(text="4 units", type="limit"),
        ],
    )

    example_claim = Claim(
        claim_id="CLM-001",
        procedure_codes=["97110"],
        units=6,
        modifiers=["GP"],
        diagnosis_codes=["M25.511"],
        place_of_service="11",
    )

    print(example_policy.model_dump_json(indent=2))
    print()
    print(example_claim.model_dump_json(indent=2))
