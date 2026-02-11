"""Validators for external data sources (Art Institute API, etc.)"""
import logging
from typing import Optional

import httpx



ART_INSTITUTE_BASE_URL = "https://api.artic.edu/api/v1"
VALIDATION_TIMEOUT = 5.0


async def validate_artwork(artwork_id: int) -> bool:
    """
    Check if artwork exists in Art Institute collection.
    
    Args:
        artwork_id: External artwork ID from Art Institute
        
    Returns:
        True if artwork found, False otherwise
        
    Note:
        This function calls the Art Institute API which can be slow.
        Consider caching results in production.
    """
    try:
        async with httpx.AsyncClient(timeout=VALIDATION_TIMEOUT) as client:
            response = await client.get(
                f"{ART_INSTITUTE_BASE_URL}/artworks/{artwork_id}"
            )
            
        if response.is_success:
            
            return True
        elif response.status_code == 404:
            return False
        else:
            return False
            
    except httpx.TimeoutException:
        return False
    except httpx.RequestError as e:
        return False
    except Exception as e:
        return False
