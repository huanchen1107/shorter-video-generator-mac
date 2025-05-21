from google import genai
import edge_tts
from tqdm import tqdm
import time
import itertools
import os
import torch
import numpy as np
from utility.text import *
#from kokoro import KPipeline
import soundfile as sf
import textwrap


'''
async def kokoro_tts_example(text, output_dir, filename, voice="zm_yunyang"):
    """
    Generates speech from text using Kokoro's KPipeline and saves it to a specific directory.
    
    :param text: Text to be converted to speech.
    :param output_dir: Directory where the audio file will be saved.
    :param filename: Name of the audio file.
    :param voice: The voice model to use.
    :return: Full path of the saved audio file.
    """
    if not text or text.strip() == "":
        print("⚠️ Warning: Received empty text for speech synthesis.")
        return None  # Skip empty text

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the full file path (using .wav for this example)
    output_file_path = os.path.join(output_dir, filename)
    
    # Initialize the KPipeline with an explicit repo_id to suppress the warning
    pipeline_instance = KPipeline(lang_code='z', repo_id="hexgrad/Kokoro-82M")
    
    try:
        print(f"🔊 Generating speech using voice: {voice}")
        # Create a generator that yields (graphemes, phonemes, audio)
        generator = pipeline_instance(
            text, voice=voice, speed=1, split_pattern=r'\n+'
        )
        
        # Merge audio segments (convert Tensors to NumPy arrays if needed)
        audio_segments = []
        for i, (_, _, audio) in enumerate(generator):
            # Check if the audio segment is a Tensor and convert it to a NumPy array
            if isinstance(audio, torch.Tensor):
                audio_np = audio.detach().cpu().numpy()
            else:
                audio_np = audio
            audio_segments.append(audio_np)
        
        if audio_segments:
            # Concatenate the segments along the first dimension
            final_audio = np.concatenate(audio_segments, axis=0)
            sf.write(output_file_path, final_audio, 24000)
            print(f"💾 Saved TTS audio to: {output_file_path}")
            return output_file_path
        else:
            print("⚠️ No audio was generated.")
            return None

    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        return None
'''

async def edge_tts_example(text, output_dir, filename, voice="en-US-KaiNeural"):
    """
    Generates speech from text and saves it to a specific directory.
    
    :param text: Text to be converted to speech.
    :param output_dir: Directory where the audio file will be saved.
    :param filename: Name of the audio file.
    :param voice: The voice model to use.
    :return: Full path of the saved audio file.
    """
    if not text or text.strip() == "":
        print("⚠️ Warning: Received empty text for speech synthesis.")
        return None  # Skip empty text

    # ✅ Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Define the full file path
    output_file_path = os.path.join(output_dir, filename)

    # ✅ Generate speech and save it to the file
    communicate = edge_tts.Communicate(text, voice, rate="+20%")
    
    try:
        print(f"💾 Saving TTS audio to: {output_file_path}")
        await communicate.save(output_file_path)
    except Exception as e:
        print(f"❌ Error saving audio: {e}")
        return None

    return output_file_path  # Return the saved file path



def gemini_chat(text_array=None, script=None, clients=None, keys=None, max_retries=100):
    if text_array is None or script is None:
        raise ValueError("script or text_array can't be None")
    
    if (clients is None or len(clients) == 0) and (keys is None or len(keys) == 0):
        raise ValueError("Either clients or keys must be provided")

    # ✅ If only keys are provided, create clients
    if clients is None or len(clients) == 0:
        clients = [genai.Client(api_key=key) for key in keys]

    # ✅ Ensure we have multiple clients to rotate
    client_cycle = itertools.cycle(clients)

    response_array_of_text = []
    count = 0
    for idx, text in enumerate(tqdm(text_array)):
        retries = 0
        client = next(client_cycle)  # Get the first client

        while retries < max_retries:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=textwrap.dedent(f'''\
                    以下是我們的完整講稿：{script}  
                    以下是第 {count} 張 Ptt 內容，前面幾張已經處理完畢：{text}  
                    根據上述資料，並從中萃取與此張投影片直接相關的重點，生成一段針對該投影片的講稿，每段講稿儘量在 15 秒內講完。  
                    要求如下：  
                    1. 你是一位講者，用像人講話的方式方式。   
                    2. 直接開始生成內容，不要開頭與、開場白，不要出現「好的」、「我們來看第幾張投影片」。
                    '''),

                )
                response_array_of_text.append(remove_markdown(response.text))
                count += 1
                break  # ✅ Successful request; exit retry loop
            except Exception as e:
                error_message = str(e)
                if "RESOURCE_EXHAUSTED" in error_message:
                    wait_time = 2 ** retries  # Exponential backoff
                    print(f"Rate limit reached for current client. Switching client and retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                    client = next(client_cycle)  # 🔄 Rotate to the next client
                else:
                    raise e  # ⚠️ Other errors should not be retried (e.g., invalid request)
        else:
            raise Exception("Max retries reached. Aborting.")
    
    return response_array_of_text



'''\
以下是我們的完整講稿：{script}  
以下是第 {count} 張 Ptt 內容，前面幾張已經處理完畢：{text}  
根據上述資料，並從中萃取與此張投影片直接相關的重點，生成一段針對該投影片的講稿，每段講稿儘量在 15 秒內講完。  
要求如下：  
1. 你是一位講者，用像人講話的方式方式。   
2. 直接開始生成內容，不要開頭與、開場白，不要出現「好的」、「我們來看第幾張投影片」。
'''

"""\
                        Here is our full script:
                        {script}

                        Here is the content from PTT for slide {idx+1}; previous slides have been processed:
                        {text}

                        Based on above, extract the key points directly related to this slide and generate
                        a ~15-second speaker script segment.

                        Requirements:
                        1. You are a presenter, speaking in a natural, conversational manner.
                        2. Keep segments short (≈15 seconds).
                        3. Do not include opening remarks or “Okay,” “Let’s look at slide X,” etc.
                        4. Begin generating immediately.
                        """
