import simpleaudio


wav=simpleaudio.WaveObject.from_wave_file("alarm_sound.wav")
playO=wav.play()
playO.wait_done()