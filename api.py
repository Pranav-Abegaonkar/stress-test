import requests
import asyncio
import time
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoSDKAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.videosdk.live/v2"
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json"
        }
    
    def create_meeting(self) -> str:
        """Create a single meeting with recording enabled and return the meeting ID"""
        try:
            # Configure recording and auto-close settings
            payload = {
                "autoStartConfig": {
                    "recording": {
                        "enabled": True,
                      'config': {
                        'layout': { 
                        'type': 'GRID',
                        'priority': 'SPEAKER',
                        'gridSize': 2
                    }
                }
                }
                },
                "autoCloseConfig": {
                    "type": "session-ends",
                    "duration": 2  # 2 minutes = 120 seconds
                }
            }
            
            response = requests.post(
                f"{self.base_url}/rooms",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            response_data = response.json()
            room_id = response_data.get("roomId")
            logger.info(f"Created meeting with recording enabled: {room_id}")
            return room_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create meeting: {e}")
            raise
    
    async def create_multiple_meetings(self, count: int, delay: float = 0.1) -> List[str]:
        """Create multiple meetings with optional delay between requests"""
        meeting_ids = []
        
        for i in range(count):
            try:
                meeting_id = self.create_meeting()
                meeting_ids.append(meeting_id)
                logger.info(f"Created meeting {i+1}/{count}: {meeting_id}")
                
                # Add delay to avoid rate limiting
                if delay > 0:
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Failed to create meeting {i+1}: {e}")
                continue
        
        return meeting_ids
    
    def create_meetings_batch(self, count: int) -> List[str]:
        """Create meetings in batches to avoid rate limiting"""
        meeting_ids = []
        batch_size = 10  # Create 10 meetings at a time
        batches = [count // batch_size] * batch_size
        remainder = count % batch_size
        if remainder > 0:
            batches.append(remainder)
        
        for batch_num, batch_count in enumerate(batches):
            logger.info(f"Creating batch {batch_num + 1} with {batch_count} meetings")
            
            for i in range(batch_count):
                try:
                    meeting_id = self.create_meeting()
                    meeting_ids.append(meeting_id)
                    time.sleep(0.1)  # Small delay between requests
                except Exception as e:
                    logger.error(f"Failed to create meeting in batch {batch_num + 1}: {e}")
                    continue
            
            # Longer delay between batches
            if batch_num < len(batches) - 1:
                time.sleep(1)
        
        return meeting_ids
