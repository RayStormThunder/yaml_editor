import numpy as np
import pyaudio

def play_pcm_audio(filepath, sample_rate=32000, channels=1):
	# Read raw bytes
	with open(filepath, 'rb') as f:
		raw_data = f.read()

	# Convert bytes to numpy array (big-endian 8-bit signed)
	audio_array = np.frombuffer(raw_data, dtype='>i1')  # '>i1' = big-endian, signed 8-bit

	# If stereo, reshape into 2D (samples x channels)
	if channels == 2:
		if len(audio_array) % 2 != 0:
			audio_array = audio_array[:-1]  # Ensure even length
		audio_array = audio_array.reshape(-1, 2)

	# Convert to little-endian signed 8-bit PCM (for PyAudio)
	audio_array = audio_array.astype('<i1')  # Convert to little-endian signed 8-bit

	# Flatten for PyAudio
	byte_data = audio_array.tobytes()

	# PyAudio setup
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt8,
					channels=channels,
					rate=sample_rate,
					output=True)

	stream.write(byte_data)

	stream.stop_stream()
	stream.close()
	p.terminate()