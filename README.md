**IMPORTANT NOTICE:**  
This project was developed by [**Louis-Li-dev**](https://github.com/Louis-Li-dev). The original project can be found at [**Shorter.Video.Generator**](https://github.com/Louis-Li-dev/Shorter.Video.Generator). This fork is specifically tailored for macOS usage.

# Overview
*This system is specifically designed for you to upload audio or audio and pdf files for AI-Generated Content*
[*Demo Link*](https://www.youtube.com/watch?v=Kei59Z9Ze_8)    
By taking advantage of this system, you can
- Generate sample presentation with AI-TTS-generated speech.
- Shorten the existing video for clarity.

---

# Prerequisites

Before installing Python dependencies, ensure that your system has the following tools installed:

- **Homebrew**: [Installation instructions](https://brew.sh/)
- **ffmpeg**: Used for video processing  
  ```bash
  brew install ffmpeg
  ```
- **poppler**: Contains tools (like pdftoppm) required for PDF processing  
  ```bash
  brew install poppler
  ```

---
# Installation

### Step 1: Clone the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/YANGCHIHUNG/shorter-video-generator-mac.git
```

---
### Step 2: Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```
---

### Step 3: Create a `.env` file in the root direcotry

- Go to your [**Google AI Studio**](https://aistudio.google.com/) and create your own API key.
- Set admin account number and password.
---
### Step 4: Run the Server

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