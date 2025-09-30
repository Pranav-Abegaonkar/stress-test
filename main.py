import asyncio
import os
import time
from videosdk import (
    MeetingConfig,
    VideoSDK,
    Participant,
    Stream,
    MeetingEventHandler,
    ParticipantEventHandler,
    Meeting,
)
from dotenv import load_dotenv

load_dotenv()
VIDEOSDK_TOKEN = os.getenv("VIDEOSDK_TOKEN")
Meeting_id = os.getenv("MEETING_ID")
Number_of_participants = int(os.getenv("COUNT", "1"))

loop = asyncio.get_event_loop()
meetings: list[Meeting] = []


class MyMeetingEventHandler(MeetingEventHandler):
    def __init__(self, participant_id: str):
        super().__init__()
        self.participant_id = participant_id

    def on_meeting_left(self, data):
        print(f"Participant {self.participant_id} left meeting")

    def on_meeting_joined(self, data):
        print(f"Participant {self.participant_id} joined meeting")

    def on_participant_joined(self, participant: Participant):
        print(f"Participant {self.participant_id} - New participant joined: {participant.id}")
        participant.add_event_listener(ParticipantEventHandler(participant=participant, participant_id=self.participant_id))

    def on_participant_left(self, participant: Participant):
        print(f"Participant {self.participant_id} - Participant left: {participant.id}")


class ParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant: Participant, participant_id: str):
        super().__init__()
        self.participant = participant
        self.participant_id = participant_id

    def on_stream_enabled(self, stream: Stream):
        print(f"Participant {self.participant_id} - Stream enabled: {stream.kind}")

    def on_stream_disabled(self, stream: Stream):
        print(f"Participant {self.participant_id} - Stream disabled: {stream.kind}")


def create_participant(participant_id: int):
    """Create a single participant and join the meeting"""
    try:
        print(f"Creating participant {participant_id}...")
        
        meeting_config = MeetingConfig(
            meeting_id=Meeting_id,
            name="dummy participant",
            mic_enabled=False,
            webcam_enabled=False,
            token=VIDEOSDK_TOKEN,
        )
        
        meeting = VideoSDK.init_meeting(**meeting_config)
        meeting.add_event_listener(MyMeetingEventHandler(f"Participant-{participant_id}"))
        
        print(f"Participant {participant_id} joining meeting...")
        meeting.join()
        
        return meeting
        
    except Exception as e:
        print(f"Error creating participant {participant_id}: {e}")
        return None


def main():
    global meetings
    
    print("="*50)
    print("VideoSDK Load Test - Single Room")
    print("="*50)
    print(f"Meeting ID: {Meeting_id}")
    print(f"Participant Count: {Number_of_participants}")
    print(f"Token: {VIDEOSDK_TOKEN[:20]}..." if VIDEOSDK_TOKEN else "No token")
    print("="*50)
    
    if not VIDEOSDK_TOKEN:
        print("❌ Error: VIDEOSDK_TOKEN not found in environment variables")
        return
    
    if not Meeting_id:
        print("❌ Error: Meeting_id not found in environment variables")
        return
    
    print(f"\n🚀 Creating {Number_of_participants} participants...")
    
    # Create participants with small delay between each
    for i in range(1, Number_of_participants + 1):
        meeting = create_participant(i)
        if meeting:
            meetings.append(meeting)
            print(f"✅ Participant {i} created successfully")
        else:
            print(f"❌ Failed to create participant {i}")
        
        # Small delay between participants to avoid overwhelming the system
        if i < Number_of_participants:
            time.sleep(0.5)
    
    print(f"\n📊 Load Test Summary:")
    print(f"   Total participants created: {len(meetings)}")
    print(f"   Target participants: {Number_of_participants}")
    print(f"   Success rate: {len(meetings)/Number_of_participants*100:.1f}%")
    
    print(f"\n🔄 Keeping participants alive... Press Ctrl+C to stop")
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping load test...")
        for i, meeting in enumerate(meetings, 1):
            try:
                meeting.leave()
                print(f"✅ Participant {i} left meeting")
            except Exception as e:
                print(f"❌ Error leaving participant {i}: {e}")


if __name__ == "__main__":
    main()
