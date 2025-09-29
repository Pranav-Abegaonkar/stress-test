from videosdk import ParticipantEventHandler, Stream
import logging

logger = logging.getLogger(__name__)

class MyParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant_id: str, meeting_id: str = None):
        super().__init__()
        self.participant_id = participant_id
        self.meeting_id = meeting_id

    def on_stream_enabled(self, stream: Stream):
        logger.info(f"Participant {self.participant_id} stream enabled: {stream.kind} (Meeting: {self.meeting_id})")

    def on_stream_disabled(self, stream: Stream):
        logger.info(f"Participant {self.participant_id} stream disabled: {stream.kind} (Meeting: {self.meeting_id})")

    def on_audio_enabled(self):
        logger.info(f"Participant {self.participant_id} audio enabled (Meeting: {self.meeting_id})")

    def on_audio_disabled(self):
        logger.info(f"Participant {self.participant_id} audio disabled (Meeting: {self.meeting_id})")

    def on_video_enabled(self):
        logger.info(f"Participant {self.participant_id} video enabled (Meeting: {self.meeting_id})")

    def on_video_disabled(self):
        logger.info(f"Participant {self.participant_id} video disabled (Meeting: {self.meeting_id})")
