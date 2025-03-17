
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

### Step 4: Run the Server

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
