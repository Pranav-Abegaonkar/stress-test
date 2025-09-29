from videosdk import Participant, MeetingEventHandler
from participant_events import MyParticipantEventHandler
import logging

logger = logging.getLogger(__name__)

class MyMeetingEventHandler(MeetingEventHandler):
    def __init__(self, meeting_id: str = None):
        super().__init__()
        self.meeting_id = meeting_id
        self.participant_count = 0

    def on_meeting_joined(self, data):
        logger.info(f"Meeting joined: {data} (Meeting ID: {self.meeting_id})")

    def on_meeting_left(self, data):
        logger.info(f"Meeting left: {data} (Meeting ID: {self.meeting_id})")

    def on_participant_joined(self, participant: Participant):
        self.participant_count += 1
        logger.info(f"Participant joined: {participant.id} (Meeting: {self.meeting_id}, Total participants: {self.participant_count})")
        participant.add_event_listener(MyParticipantEventHandler(
            participant_id=participant.id, 
            meeting_id=self.meeting_id
        ))

    def on_participant_left(self, participant: Participant):
        self.participant_count -= 1
        logger.info(f"Participant left: {participant.id} (Meeting: {self.meeting_id}, Remaining participants: {self.participant_count})")

    def on_meeting_error(self, error):
        logger.error(f"Meeting error in {self.meeting_id}: {error}")

    def on_meeting_state_changed(self, state):
        logger.info(f"Meeting state changed in {self.meeting_id}: {state}")
