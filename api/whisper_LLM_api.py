import os
import sys
import asyncio
import time
import nest_asyncio
from IPython.display import clear_output
from tqdm import tqdm
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

# ✅ Add parent directory to sys.path to import custom utility modules
parent_dir = os.path.join(os.getcwd(), "..")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utility.audio import *
from utility.pdf import *
from utility.api import *
from dotenv import load_dotenv
load_dotenv()
THREAD_COUNT = int(os.getenv("THREAD_COUNT"))
# ✅ Apply async fix for Jupyter Notebook environments
nest_asyncio.apply()


# ✅ Resolution Mapping
RESOLUTION_MAP = {
    144: (256, 144),  # 144p
    240: (426, 240),  # 240p
    360: (640, 360),  # 360p
    480: (854, 480),  # 480p
    720: (1280, 720),  # 720p
}
# ✅ Function to ensure all required directories exist
def ensure_directories_exist(*dirs):
    """
    Creates directories if they do not exist.
    :param dirs: List of directory paths to create.
    """
    for directory in dirs:
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created missing directory: {directory}")


# ✅ Define main async function with resolution parameter
async def api(
    video_path: str,
    pdf_file_path: str,
    poppler_path: str,
    output_audio_dir: str,
    output_video_dir: str,
    output_text_path: str,
    num_of_pages="all",
    resolution: int = 480,  # Default to 480p
    tts_model: str = 'edge'
):
    print("\n🚀 Starting the process...\n")
    ensure_directories_exist(output_audio_dir, output_video_dir, os.path.dirname(output_text_path))
    # ✅ Validate resolution input
    if resolution not in RESOLUTION_MAP:
        print(f"⚠️ Invalid resolution selected: {resolution}p. Defaulting to 480p.")
        resolution = 480

    TARGET_WIDTH, TARGET_HEIGHT = RESOLUTION_MAP[resolution]
    print(f"📏 Selected Resolution: {resolution}p ({TARGET_WIDTH}x{TARGET_HEIGHT})")
    if video_path is None:
        print(f"No MP4 passed in. Go on processing without video.")
        script = "No video for this file. Please use the passage only to generate."
    else:
        # ✅ Step 1: Convert MP4 to MP3
        print(f"🎵 Converting MP4 to MP3: {video_path}")
        audio = convert_mp4_to_mp3(video_path)

        # ✅ Step 2: Transcribe the audio
        print("📝 Transcribing audio to text...")
        script = transcribe_audio(audio, model_size="base")['text']

    # ✅ Step 4: Get API key and process PDF
    keys = eval(os.getenv("api_key"))
    print(f"📄 Extracting text from PDF: {pdf_file_path}")

    # ✅ Detect total number of pages if 'all' is set
    if num_of_pages == "all":
        total_pages = len(convert_from_path(
            pdf_file_path, poppler_path=poppler_path,thread_count=THREAD_COUNT
        ))
        print(f"📚 Detected total pages: {total_pages}")
    else:
        try:
            total_pages = int(num_of_pages)  # Convert to integer
        except Exception:
            total_pages = len(convert_from_path(
                pdf_file_path, poppler_path=poppler_path, thread_count=THREAD_COUNT
            ))
    print(f"📃Selected Number of Pages: {num_of_pages}")
    text_array = pdf_to_text_array(pdf_file_path)

    # ✅ Step 5: Use AI model to generate responses
    print(f"🤖 Generating AI responses for {total_pages} pages...")
    response_array = gemini_chat(text_array[:total_pages], script=script, keys=keys)
    

    # ✅ Step 6: Convert AI-generated text to speech (without saving permanently)
    print("🔊 Generating speech from AI responses...")
    audio_files = []  # Store temporary file paths

    tasks = []
    for idx, response in enumerate(tqdm(response_array, desc="Processing Audio")):
        filename = f"audio_{idx}.mp3"  # Unique name for each file
        tasks.append(edge_tts_example(response, output_audio_dir, filename, tts_model))   

    # ✅ Gather all async tasks
    audio_files = await asyncio.gather(*tasks)

    print("✅ All audio responses generated as temporary files!")
    # ✅ Step 7: Convert PDF pages to images
    print(f"🖼️ Converting {total_pages} PDF pages to images...")

    pages = convert_from_path(
        pdf_file_path,
        poppler_path=poppler_path,
        first_page=1,
        last_page=total_pages,
        thread_count=THREAD_COUNT
    )
    print("🎬 Creating video clips...")
    video_clips = []

    for img, audio_file in tqdm(zip(pages, audio_files), total=len(audio_files), desc="Processing Videos"):
        # ✅ Resize Image to Selected Resolution
        img_resized = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)

        # ✅ Convert resized PIL image to NumPy array for MoviePy
        frame = np.array(img_resized)

        # ✅ Load audio from temporary file
        audioclip = AudioFileClip(audio_file)  # Load using file path
        duration = audioclip.duration  # Match image duration to audio

        # ✅ Create ImageClip & Set Duration
        image_clip = ImageClip(frame).set_duration(duration)

        # ✅ Attach audio to the image clip
        video_clip = image_clip.set_audio(audioclip)

        # ✅ Store the video clip in the list
        video_clips.append(video_clip)
    


    # ✅ Step 10: Concatenate video clips
    print("📹 Concatenating video clips...")
    final_video = concatenate_videoclips(video_clips, method="chain")

    # ✅ Step 12: Export final video
    output_video_path = os.path.join(output_video_dir, f"output_video_{resolution}p.mp4")
    print(f"📤 Exporting final video to: {output_video_path}")
    final_video.write_videofile(
        output_video_path,
        fps=24,
        logger=None,
        audio_bitrate="50k",
        write_logfile=False,
        threads=THREAD_COUNT,
        ffmpeg_params=[
            "-b:v", "5M",  # ✅ Controls bitrate (~5Mbps for faster encoding)
            "-preset", "ultrafast",  # ✅ Faster encoding, slightly lower quality
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # ✅ Ensures correct resolution
            "-pix_fmt", "yuv420p",  # ✅ Standard pixel format
        ],
    )

    clear_output(wait=True)
    print(f"🎉 Final {resolution}p video created successfully with {total_pages} pages!")


    temp_audiofile = os.path.join(output_audio_dir, "output_videoTEMP_MPY_wvf_snd.mp3")
    
    # ✅ Ensure temp audio file is not locked
    time.sleep(3)
    try:
        if os.path.exists(temp_audiofile):
            os.remove(temp_audiofile)
            print(f"✅ Deleted temp audio file: {temp_audiofile}")
    except PermissionError:
        print(f"⚠️ Warning: Could not delete {temp_audiofile}. It might still be in use.")

    # ✅ Step 13: Remove the transcript text file
    if os.path.exists(output_text_path):
        try:
            os.remove(output_text_path)
            print(f"✅ Deleted transcript file: {output_text_path}")
        except Exception as e:
            print(f"⚠️ Failed to delete transcript file: {e}")

    print("✅ Cleanup process completed!")
# ✅ Step 14: Run async function properly with parameters
if __name__ == "__main__":
    asyncio.run(api(
        video_path="../video/video1.mp4",
        pdf_file_path="../pdf/1_Basics_1.pdf",
        poppler_path=None,
        output_audio_dir="../output_audio",
        output_text_path="../output_text/text_output.txt",
        num_of_pages=1,  # Set to 'all' for full PDF processing
        resolution=480  # ✅ Change this to 144, 240, 360, 480, or 720
    ))
