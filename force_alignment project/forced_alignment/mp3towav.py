from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_path)

        # Export the audio to WAV format
        audio.export(wav_path, format="wav")

        print("Conversion successful.")
    except Exception as e:
        print(f"Error during MP3 to WAV conversion: {str(e)}")