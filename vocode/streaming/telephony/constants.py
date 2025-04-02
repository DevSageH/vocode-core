from vocode.streaming.models.audio import AudioEncoding, SamplingRate

# TODO(EPD-186): namespace as Twilio
DEFAULT_SAMPLING_RATE: int = SamplingRate.RATE_16000.value
DEFAULT_AUDIO_ENCODING = AudioEncoding.OPUS
DEFAULT_CHUNK_SIZE = 2000
MULAW_SILENCE_BYTE = b"\x00"

VONAGE_SAMPLING_RATE: int = SamplingRate.RATE_16000.value
VONAGE_AUDIO_ENCODING = AudioEncoding.LINEAR16
VONAGE_CHUNK_SIZE = 640  # 20ms at 16kHz with 16bit samples
VONAGE_CONTENT_TYPE = "audio/l16;rate=16000"
PCM_SILENCE_BYTE = b"\x00"
