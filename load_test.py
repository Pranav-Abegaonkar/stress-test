#!/usr/bin/env python3
"""
VideoSDK Load Test Script
Creates n meetings with m participants each for load testing
"""

import asyncio
import os
import time
import logging
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from vsaiortc.contrib.media import MediaPlayer
from dotenv import load_dotenv

from videosdk import MeetingConfig, VideoSDK, Meeting
from api import VideoSDKAPI
from meeting_events import MyMeetingEventHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('load_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LoadTestManager:
    def __init__(self, token: str, total_meetings: int = 500, participants_per_meeting: int = 2):
        self.token = token
        self.total_meetings = total_meetings
        self.participants_per_meeting = participants_per_meeting
        self.api = VideoSDKAPI(token)
        self.meetings: List[Meeting] = []
        self.meeting_ids: List[str] = []
        self.active_meetings = 0
        self.total_participants = 0
        self.lock = threading.Lock()
        
    async def create_meetings(self) -> List[str]:
        """Create all meetings for the load test"""
        logger.info(f"Creating {self.total_meetings} meetings...")
        
        # Create meetings in batches to avoid rate limiting
        meeting_ids = self.api.create_meetings_batch(self.total_meetings)
        
        logger.info(f"Successfully created {len(meeting_ids)} meetings")
        self.meeting_ids = meeting_ids
        return meeting_ids
    
    async def create_participant(self, meeting_id: str, participant_name: str) -> Meeting:
        """Create a single participant and join a meeting"""
        try:
            logger.info(f"Creating participant {participant_name} for meeting {meeting_id}")

            player = MediaPlayer("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")   
            video_track = player.video
            audio_track = player.audio
            meeting_config = MeetingConfig(
                meeting_id=meeting_id,
                name=participant_name,
                mic_enabled=True,  # Disable mic for load testing
                webcam_enabled=True,  # Disable webcam for load testing
                custom_microphone_audio_track=audio_track,
                custom_camera_video_track=video_track,
                token=self.token
            )
            
            meeting = VideoSDK.init_meeting(**meeting_config)
            meeting.add_event_listener(MyMeetingEventHandler(meeting_id=meeting_id))
            
            logger.info(f"Joining participant {participant_name} to meeting {meeting_id}")
            # Join the meeting
            meeting.join()
            
            # Small delay to ensure proper connection
            await asyncio.sleep(0.5)
            
            with self.lock:
                self.active_meetings += 1
                self.total_participants += 1
            
            logger.info(f"✅ Participant {participant_name} successfully joined meeting {meeting_id}")
            return meeting
            
        except Exception as e:
            logger.error(f"❌ Failed to create participant {participant_name} for meeting {meeting_id}: {e}")
            return None
    
    async def join_meeting_participants(self, meeting_id: str, participant_count: int) -> List[Meeting]:
        """Join multiple participants to a single meeting"""
        participants = []
        
        # Create participants concurrently
        tasks = []
        for i in range(participant_count):
            participant_name = f"Participant-{i+1}-{meeting_id[:8]}"
            task = asyncio.create_task(
                self.create_participant(meeting_id, participant_name)
            )
            tasks.append(task)
        
        # Wait for all participants to join
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Participant creation failed: {result}")
            elif result is not None:
                participants.append(result)
        
        return participants
    
    async def run_in_thread(self, func, *args, **kwargs):
        """Run a function in a thread pool"""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, func, *args, **kwargs)
    
    async def run_load_test(self):
        """Run the complete load test"""
        start_time = time.time()
        logger.info(f"Starting load test: {self.total_meetings} meetings, {self.participants_per_meeting} participants each")
        logger.info("📹 Recording enabled for all meetings (auto-start, 120s duration)")
        
        try:
            # Step 1: Create all meetings
            await self.create_meetings()
            
            if not self.meeting_ids:
                logger.error("No meetings created. Exiting.")
                return
            
            # Step 2: Join participants to meetings in batches
            batch_size = 10  # Process 10 meetings at a time
            total_batches = (len(self.meeting_ids) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(self.meeting_ids))
                batch_meetings = self.meeting_ids[start_idx:end_idx]
                
                logger.info(f"Processing batch {batch_num + 1}/{total_batches} ({len(batch_meetings)} meetings)")
                
                # Create tasks for all meetings in this batch
                tasks = []
                for meeting_id in batch_meetings:
                    task = self.join_meeting_participants(meeting_id, self.participants_per_meeting)
                    tasks.append(task)
                
                # Execute batch concurrently
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Collect all participants from this batch
                for result in batch_results:
                    if isinstance(result, Exception):
                        logger.error(f"Batch processing failed: {result}")
                    else:
                        self.meetings.extend(result)
                
                # Small delay between batches
                if batch_num < total_batches - 1:
                    await asyncio.sleep(2)
            
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info(f"Load test completed!")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Total meetings: {len(self.meeting_ids)}")
            logger.info(f"Active meetings: {self.active_meetings}")
            logger.info(f"Total participants: {self.total_participants}")
            logger.info(f"Meetings per second: {len(self.meeting_ids) / duration:.2f}")
            logger.info(f"Participants per second: {self.total_participants / duration:.2f}")
            logger.info(f"📹 All meetings are being recorded (120s duration each)")
            
            # Keep the meetings alive for monitoring
            logger.info("Keeping meetings alive for monitoring. Press Ctrl+C to stop.")
            await self.keep_meetings_alive()
            
        except KeyboardInterrupt:
            logger.info("Load test interrupted by user")
        except Exception as e:
            logger.error(f"Load test failed: {e}")
        finally:
            await self.cleanup()
    
    async def keep_meetings_alive(self):
        """Keep all meetings alive for monitoring"""
        try:
            while True:
                await asyncio.sleep(30)  # Check every 30 seconds
                with self.lock:
                    logger.info(f"Status: {self.active_meetings} active meetings, {self.total_participants} participants")
        except KeyboardInterrupt:
            logger.info("Stopping meetings...")
    
    async def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        for meeting in self.meetings:
            try:
                if meeting:
                    meeting.leave()
            except Exception as e:
                logger.error(f"Error leaving meeting: {e}")

async def main():
    """Main function to run the load test"""
    # Get configuration from environment
    token = os.getenv("VIDEOSDK_TOKEN")
    if not token:
        logger.error("VIDEOSDK_TOKEN not found in environment variables")
        print("\n❌ Error: VIDEOSDK_TOKEN not found in environment variables")
        print("Please create a .env file with your VideoSDK token:")
        print("VIDEOSDK_TOKEN=your_token_here")
        return
    
    # Get load test parameters from environment
    total_meetings = int(os.getenv("TOTAL_MEETINGS", "5"))
    participants_per_meeting = int(os.getenv("PARTICIPANTS_PER_MEETING", "2"))
    
    print(f"\n🚀 VideoSDK Load Test Configuration")
    print("="*50)
    print(f"📞 Total Calls: {total_meetings}")
    print(f"👥 Participants per Call: {participants_per_meeting}")
    print(f"👥 Total Participants: {total_meetings * participants_per_meeting}")
    print("="*50)
    
    print(f"\n🚀 Starting load test...")
    print(f"   Creating {total_meetings} calls with {participants_per_meeting} participants each...")
    
    # Create and run load test
    load_test = LoadTestManager(
        token=token,
        total_meetings=total_meetings,
        participants_per_meeting=participants_per_meeting
    )
    
    await load_test.run_load_test()

if __name__ == "__main__":
    asyncio.run(main())
