
# Installation

### Step 1: Clone the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/Louis-Li-dev/Shorter.Video.Generator.git
```

---

### Step 2: Build Dependencies (Linux Only)

For a newly created VM, run the setup script to install dependencies (including *ffmpeg* and virtual environments):

```bash
bash setup.sh
```

---

### Step 3: Install Dependencies

- **For CPU-only Machines:**

  ```bash
  pip install -r cpu_requirements.txt
  ```

- **For Machines with GPU Support:**

  ```bash
  pip install -r gpu_requirements.txt
  ```

---

### Step 4: Create a `.env` file in the root direcotry

Go to your [**Google AI Studio**](https://aistudio.google.com/) and create your own API key.

---
### Step 5: Run the Server

Start the server by running the `app.py` file located in the root directory.

```bash
python app.py
```

---

# Expected Result

## Main Interface

After uploading your MP4 file and the corresponding PDF slides, simply click the **Generate** button to initiate the process.

<div align="center">
  <img src="https://github.com/user-attachments/assets/f943eb89-2485-473b-b4c0-6d6c09755035" alt="Main Interface" style="height:500px; width:auto;"/>
</div>

---

## Downloadable Files Interface

Manage your generated results by collecting or removing files from the interface.

<div align="center">
  <img src="https://github.com/user-attachments/assets/a2038638-d579-4907-bb4a-1f4c36e1cdac" alt="Downloadable Files Interface" style="height:500px; width:auto;"/>
</div>

---

# References
Gemini (Gemini 2.0 Flash)
If you are specifically using Gemini 2.0 Flash through Google Cloud, please refer to the official Google Cloud documentation for detailed setup instructions and licensing. Below is a placeholder citation:

Google Cloud. (2023). Gemini 2.0 Flash: Next-Generation Language Model. Retrieved from [https://cloud.google.com/](https://aistudio.google.com/prompts/new_chat)

(Replace the URL with the direct Gemini 2.0 Flash documentation link if available.)

Whisper
For citing Whisper, you can use the following format based on OpenAI's guidelines:

OpenAI. (2022). Whisper: A General-Purpose Speech Recognition Model. Retrieved from [https://github.com/openai/whisper](https://github.com/openai/whisper)

