import os
import numpy as np
import scipy.io.wavfile as wavfile


def extract_tick_segments(audio_file, threshold, segment_duration, min_avg_amplitude):
    # insert audio file
    sample_rate, audio_data = wavfile.read(audio_file)

    # convert audio data to mono
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)

    # normalise audio data to the range [-1, 1]
    audio_data = audio_data / np.max(np.abs(audio_data))

    tick_segments = []
    tick_count = 0
    in_tick = False
    tick_start = 0

    # create new folder
    folder_path = "good_segmented"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # number of samples for segment duration
    segment_length = int(sample_rate * segment_duration)

    # iterate through the audio
    for i in range(len(audio_data)):
        amplitude = np.abs(audio_data[i])

        # check if the amplitude exceeds the threshold
        if amplitude > threshold:
            # start a new segment (if not in tick segment)
            if not in_tick:
                in_tick = True
                tick_start = i

        # check if the segment duration is reached
        if in_tick and i - tick_start >= segment_length:
            in_tick = False

            # extract segment from the audio
            tick_segment = audio_data[tick_start:i]

            # calculate the average amplitude of the tick segment
            avg_amplitude = np.mean(np.abs(tick_segment))

            # check if the average amplitude is above the minimum threshold
            if avg_amplitude > min_avg_amplitude:
                tick_segments.append(tick_segment)

                # save the segment as a separate file in the new folder
                tick_count += 1
                tick_filename = os.path.join(folder_path, f"good_tick_{tick_count}.wav")
                wavfile.write(tick_filename, sample_rate, tick_segment)

    return tick_segments


audio_file = "audio_file.wav"
threshold = 0.8
segment_duration = 0.25
min_avg_amplitude = 0 # only needed in special circumstances (e.g. extra resonance with bad tiles)
tick_segments = extract_tick_segments(audio_file, threshold, segment_duration, min_avg_amplitude)
