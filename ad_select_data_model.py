from pydantic import BaseModel, Field, field_validator
from typing import Optional


class RegisterPersonaAdsRequest(BaseModel):
    """
    Request model for registering advertisements available for a persona.
    
    This associates a set of advertisement IDs with a specific user persona,
    allowing the bandit algorithm to select from these ads for that persona.
    """
    persona_id: str = Field(
        ...,
        description="Unique identifier for the user persona",
        examples=["persona_123", "tech_enthusiast_25_34"]
    )
    ad_ids: list[str] = Field(
        ...,
        min_length=1,
        description="List of advertisement IDs to associate with this persona",
        examples=[["ad_001", "ad_002", "ad_003"]]
    )
    
    @field_validator('ad_ids')
    @classmethod
    def validate_unique_ads(cls, v):
        """Ensure all ad IDs are unique."""
        if len(v) != len(set(v)):
            raise ValueError("ad_ids must contain unique values")
        return v


class RegisterPersonaAdsResponse(BaseModel):
    """Response model for persona-ads registration."""
    message: str = Field(
        default="Persona ads registered successfully",
        description="Success message"
    )
    persona_id: str = Field(description="The registered persona ID")
    ad_count: int = Field(description="Number of ads registered for this persona")


class RewardUpdate(BaseModel):
    """
    Model representing reward feedback for an advertisement interaction.
    
    Used to update the bandit algorithm's belief about ad performance based
    on user interactions (clicks, conversions, etc.).
    """
    success: int = Field(
        default=0,
        ge=0,
        description="Number of successful interactions (e.g., clicks, conversions)",
        examples=[1, 0]
    )
    failure: int = Field(
        default=0,
        ge=0,
        description="Number of failed interactions (e.g., impressions without clicks)",
        examples=[0, 1]
    )
    
    @field_validator('success', 'failure')
    @classmethod
    def validate_at_least_one(cls, v, info):
        """Ensure at least one of success or failure is non-zero."""
        # This validation happens after both fields are set
        return v


class UpdateRequest(BaseModel):
    """
    Request model for updating the bandit algorithm with interaction feedback.
    
    This is called after an ad is shown to a user to record whether the
    interaction was successful or not.
    """
    ad_id: str = Field(
        ...,
        description="Unique identifier for the advertisement that was shown",
        examples=["ad_001"]
    )
    reward: RewardUpdate = Field(
        ...,
        description="Reward feedback indicating success or failure of the interaction"
    )


class UpdateResponse(BaseModel):
    """Response model for reward update."""
    message: str = Field(
        default="Reward updated successfully",
        description="Success message"
    )
    ad_id: str = Field(description="The advertisement ID that was updated")


class SelectAdRequest(BaseModel):
    """
    Request model for selecting an advertisement for a persona.
    
    The bandit algorithm will choose the optimal ad based on historical
    performance and exploration-exploitation tradeoff.
    """
    persona_id: str = Field(
        ...,
        description="Unique identifier for the user persona",
        examples=["persona_123"]
    )


class SelectAdResponse(BaseModel):
    """
    Response model for advertisement selection.
    
    Returns the selected advertisement ID chosen by the bandit algorithm.
    """
    ad_id: Optional[str] = Field(
        default=None,
        description="Selected advertisement ID, or null if no ads registered for persona",
        examples=["ad_002"]
    )
    persona_id: str = Field(description="The persona ID for which ad was selected")


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(description="Error message describing what went wrong")
    detail: Optional[str] = Field(
        default=None,
        description="Additional details about the error"
    )
