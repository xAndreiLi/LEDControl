import soundcard as sc
import numpy as np
import asyncio


class AudioListener:

	def __init__(self):
		# Gets default speaker to use as name match for loopback
		self.speaker = sc.default_speaker()
		# Sets input as loopback for default speaker
		self.input = sc.get_microphone(self.speaker.name, include_loopback=True)
		self.currentFreq = 0
		self.previousFreq = 0
    
	async def record(self):
		with self.input.recorder(samplerate=48000, channels=2) as recorder:
			data = recorder.record(numframes=1024)
			data = np.average(data, axis=1)

			fft = np.fft.fft(data)
			freqs = np.fft.fftfreq(len(fft))
			l = len(data)
			imax = np.argmax(np.abs(fft))
			fs = freqs[imax]
			freq = abs(fs*20480)
			print(freq)
			return freq

	async def startListen(self):
		while(True):
			self.previousFreq = self.currentFreq
			self.currentFreq = await self.record()
			await asyncio.sleep(0.005)
