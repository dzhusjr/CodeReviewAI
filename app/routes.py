from fastapi import APIRouter, HTTPException
from app.models import ReviewRequest
from app.services.ai_service import generate_review
from app.services.github_service import fetch_repo_and_generate_message

router = APIRouter()

@router.post("/review")
async def review_code(request: ReviewRequest):
    
    repo_contents = fetch_repo_and_generate_message(request.github_repo_url)
    review = await generate_review(
        assignment_description=request.assignment_description,
        repo_contents=repo_contents,
        candidate_level=request.candidate_level,
    )
    return {"response": review}
