from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil
from pydub import AudioSegment
import wave
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from texttolab import convert_txt_to_lab
from texttotime import convert_textgrid_to_srt
from docxtolab import convert_docx_to_lab
import os
import time
import subprocess

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
INPUT_FOLDER = 'input_file'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['INPUT_FOLDER'] = INPUT_FOLDER

def convert_mp3_to_wav(audio_path, wav_output_path):
    try:
        audio = AudioFileClip(audio_path)
        
        temp_dir = tempfile.mkdtemp()

        try:
            temp_audio_file = tempfile.NamedTemporaryFile(
                suffix=".wav", dir=temp_dir, delete=False
            )
            temp_audio_filename = temp_audio_file.name
            audio.write_audiofile(temp_audio_filename)

            audio_filename = os.path.splitext(os.path.basename(audio_path))[0]
            #output_file_path = os.path.join(wav_output_path, "output.wav")

            audio.close()
            temp_audio_file.close()
            shutil.move(temp_audio_filename, wav_output_path)

            print(f"Audio processed. Output path: {wav_output_path}")
            return wav_output_path
        finally:
            audio.close()
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Error during audio processing: {str(e)}")
    

def process_video(video_path, wav_output_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        temp_dir = tempfile.mkdtemp()

        try:
            temp_audio_file = tempfile.NamedTemporaryFile(
                suffix=".wav", dir=temp_dir, delete=False
            )
            temp_audio_filename = temp_audio_file.name
            audio.write_audiofile(temp_audio_filename)

            video_filename = os.path.splitext(os.path.basename(video_path))[0]
            #output_file_path = os.path.join(wav_output_path, "output.wav")

            audio.close()
            temp_audio_file.close()
            shutil.move(temp_audio_filename, wav_output_path)

            print(f"Video processed. Output path: {wav_output_path}")
            return wav_output_path
        finally:
            video.close()
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Error during video processing: {str(e)}")

def run_mfa(acoustic_directory, acoustic_model_path, dictionary_path, output_directory):
    try:
        # Replace the placeholders with the correct paths
        conda_activate_script = r"C:\\Users\\DELL\\miniconda3\\Scripts\\activate.bat"
        mfa_env_name = "aligner"

        # Activate the conda environment
        activate_command = f'call "{conda_activate_script}" {mfa_env_name} && '

        # Construct the MFA command
        mfa_command = [
            'mfa',
            'align',
            acoustic_directory,
            acoustic_model_path,
            dictionary_path,
            output_directory,
            '--single_speaker'
        ]

        # Combine the activate command and MFA command
        full_command = activate_command + " ".join(mfa_command)

        # Run MFA as a subprocess
        subprocess.run(full_command, check=True, shell=True)
        print("MFA process completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running MFA: {e}")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/align', methods=['POST'])
def align():
    output_path = app.config['OUTPUT_FOLDER']
    input_path = app.config['INPUT_FOLDER']

    try:
        if 'videoFile' not in request.files or 'scriptFile' not in request.files:
            return render_template('index.html', error='Please upload both video and script files.')

        video_file = request.files['videoFile']
        script_file = request.files['scriptFile']

        if video_file.filename == '' or script_file.filename == '':
            return render_template('index.html', error='Please select both video and script files.')

        video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_file.filename))
        script_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(script_file.filename))

        video_file.save(video_path)
        script_file.save(script_path)

        print(f"Video Path: {video_path}")
        print(f"Script Path: {script_path}")

        if video_file.filename.lower().endswith('.mp3'):
            wav_output_path = os.path.join(output_path, 'output.wav')
            convert_mp3_to_wav(video_path, wav_output_path)
        else:
            wav_output_path = os.path.join(output_path, 'output.wav')
            process_video(video_path, wav_output_path)
        
        if script_file.filename.lower().endswith('.txt'):
            script_output_path = os.path.join(output_path, 'output.lab')
            convert_txt_to_lab(script_path, script_output_path)
        else:
            script_output_path = os.path.join(output_path, 'output.lab') 
            convert_docx_to_lab(script_path, script_output_path)

        print(f"WAV File Path: {wav_output_path}")
        
        run_mfa('C:\\Users\\DELL\\OneDrive\\Desktop\\TimeCode_Generation_Project\\output', 'tamil_cv', 'tamil_cv', 'C:\\Users\\DELL\\OneDrive\\Desktop\\TimeCode_Generation_Project\\input_file')
        
        textGrid_output_path = os.path.join(input_path, 'output.TextGrid')
        #srt_output_path = os.path.join(output_path, 'output.srt')
        convert_textgrid_to_srt(textGrid_output_path, output_path)
        srt_output_path = os.path.join(output_path, 'output.srt')
        print(f"SRT Output Path: {srt_output_path}")

        response = send_file(srt_output_path, as_attachment=True)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    except Exception as e:
        print(f"Error during alignment: {str(e)}")
        return render_template('index.html', error=f'Error during alignment: {str(e)}')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0')
