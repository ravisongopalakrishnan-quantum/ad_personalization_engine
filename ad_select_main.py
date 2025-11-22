from fastapi import FastAPI, HTTPException
from ad_select_factory import AdSelectFactory
from ad_select_data_model import (
    RegisterPersonaAdsRequest,
    RegisterPersonaAdsResponse,
    UpdateRequest,
    UpdateResponse,
    SelectAdRequest,
    SelectAdResponse,
    ErrorResponse
)

# Initialize the factory with Thompson Sampling strategy
factory = AdSelectFactory("thompson_sampling")

app = FastAPI(
    title="Advertisement Selection API",
    description="Multi-armed bandit API for personalized advertisement selection",
    version="1.0.0"
)


@app.post(
    "/register_persona_ads",
    response_model=RegisterPersonaAdsResponse,
    responses={400: {"model": ErrorResponse}}
)
def register_persona_ads(request: RegisterPersonaAdsRequest) -> RegisterPersonaAdsResponse:
    """
    Register a set of advertisements for a specific user persona.
    
    This endpoint associates advertisement IDs with a persona, allowing the
    bandit algorithm to select from these ads for that persona.
    """
    try:
        factory.register_persona_ads(request.persona_id, request.ad_ids)
        return RegisterPersonaAdsResponse(
            message="Persona ads registered successfully",
            persona_id=request.persona_id,
            ad_count=len(request.ad_ids)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/update",
    response_model=UpdateResponse,
    responses={400: {"model": ErrorResponse}}
)
def update(request: UpdateRequest) -> UpdateResponse:
    """
    Update the bandit algorithm with feedback from a user interaction.
    
    Call this endpoint after showing an ad to a user to record whether
    the interaction was successful (click/conversion) or not.
    """
    try:
        # Convert Pydantic model to dict for the factory
        reward_dict = {
            "success": request.reward.success,
            "failure": request.reward.failure
        }
        factory.update(request.ad_id, reward_dict)
        return UpdateResponse(
            message="Reward updated successfully",
            ad_id=request.ad_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/select_ad",
    response_model=SelectAdResponse,
    responses={404: {"model": ErrorResponse}}
)
def select_ad(request: SelectAdRequest) -> SelectAdResponse:
    """
    Select the optimal advertisement for a given persona.
    
    Uses the Thompson Sampling algorithm to balance exploration and
    exploitation when choosing which ad to show.
    """
    try:
        ad_id = factory.select_ad(request.persona_id)
        if ad_id is None:
            raise HTTPException(
                status_code=404,
                detail=f"No ads registered for persona: {request.persona_id}"
            )
        return SelectAdResponse(
            ad_id=ad_id,
            persona_id=request.persona_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
