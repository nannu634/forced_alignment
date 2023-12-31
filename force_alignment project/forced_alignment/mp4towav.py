import os
import tempfile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def process_video(video_path, output_path):
    print(f"Processing video: {video_path}")
    video = VideoFileClip(video_path)

    # Get the duration of the video in seconds
    video_duration = video.duration

    # Extract the audio from the video
    audio = video.audio

    # Create the output directory if it does not exist
    os.makedirs(output_path, exist_ok=True)

    # Export the audio to a temporary WAV file using moviepy
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_audio_filename = temp_audio_file.name
        audio.write_audiofile(temp_audio_filename)

    # Close the temporary audio file
    temp_audio_file.close()

    # Move the temporary WAV file to the output directory
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_file_path = os.path.join(output_path, f"{video_filename}.wav")
    os.replace(temp_audio_filename, output_file_path)

    # Load the exported audio as an AudioSegment using pydub
    audio = AudioSegment.from_file(output_file_path, format='wav')

    # Close the video object
    video.close()

    return output_file_path

    print(f"Video processed. Output path: {output_file_path}")
