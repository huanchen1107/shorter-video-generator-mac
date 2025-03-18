
# Installation

### Step 1: Clone the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/Louis-Li-dev/Shorter.Video.Generator.git
```

---

### Step 2: Build Dependencies (Linux Only, Windows Users Can Skip This One)

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

- Go to your [**Google AI Studio**](https://aistudio.google.com/) and create your own API key.
- Set admin account number and password.
---
### Step 5: Run the Server

Start the server by running the `app.py` file located in the root directory.

```bash
python app.py
```

---



# Expected Result

| Main Interface | Downloadable Files Interface | Admin Interface for File Management |
| -------------- | ---------------------------- | ----------------------------------- |
| <img src="https://github.com/user-attachments/assets/f943eb89-2485-473b-b4c0-6d6c09755035" alt="Main Interface" /> | <img src="https://github.com/user-attachments/assets/a2038638-d579-4907-bb4a-1f4c36e1cdac" alt="Downloadable Files Interface" /> | <img src="https://github.com/user-attachments/assets/f6fd6f50-768c-4735-8e39-9e0528fc6445" alt="Admin Interface for File Management"/> |

---

# References
- Gemini (Gemini 2.0 Flash)

  - Google Cloud. (2023). Gemini 2.0 Flash: Next-Generation Language Model. Retrieved from [https://cloud.google.com/](https://aistudio.google.com/prompts/new_chat)

- Whisper
  - OpenAI. (2022). Whisper: A General-Purpose Speech Recognition Model. Retrieved from [https://github.com/openai/whisper](https://github.com/openai/whisper)
- Kokoro TTS (text to speech)
  - hexgrad/Kokoro-82M. Retrieved from [https://github.com/hexgrad/kokoro](https://github.com/hexgrad/kokoro)
    

