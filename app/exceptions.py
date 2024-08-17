from fastapi import HTTPException

class ContentGenerationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Content generation failed: {detail}")

class SEOOptimizationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"SEO optimization failed: {detail}")