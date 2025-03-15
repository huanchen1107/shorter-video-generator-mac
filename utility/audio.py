import os
import whisper
from moviepy.editor import VideoFileClip
import torch
def convert_mp4_to_mp3(input_file, output_file=None):
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".mp3"
    
    try:
        video = VideoFileClip(input_file)
        audio = video.audio
        audio.write_audiofile(output_file)
        print(f"Conversion successful: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if 'audio' in locals() and audio:
            audio.close()
        if 'video' in locals() and video:
            video.close()

def transcribe_audio(audio_path, model_size="medium"):  # Load large Whisper model
    if not os.path.exists(audio_path):
        print(f"Error: File {audio_path} not found.")
        return
    # Determine the device: use GPU if available, otherwise CPU.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading Whisper model: {model_size} on {device}")

    model = whisper.load_model(model_size).to(device)
    print("Start transcribing...")
    result = model.transcribe(audio_path)
    print("Transcription:")
    print(result.get("text", "No transcription available."))
    return result
