# Intelligent Receipt OCR with Ollama (LLaVA + Streamlit)

This project allows you to extract structured text data from receipt images using [Ollama](https://ollama.com)'s `llava` model (LLaVA) and view or download results via a Streamlit web app. You can upload multiple receipt images, extract raw information, and view key line items in table form.

---

## Features

* Drag-and-drop receipt images through a web UI
* Uses `llava` vision model (LLaVA) locally via Ollama API
* Encodes image and sends prompt for receipt extraction
* Displays model response
* Extracts numeric line items into a Pandas DataFrame
* Allows CSV download of extracted data

---

## Requirements

* macOS or Linux
* Python 3.10+
* Ollama installed and running locally
* Installed Ollama model: `llava`

---

## Folder Structure

```
project/
├── app.py                  # Streamlit app
├── receipt_extractor.py   # CLI version (optional)
├── venv/                   # Python virtual environment (recommended)
├── pics/                   # Folder with sample receipt images
├── output/                 # Folder where results will be saved
└── README.md               # This file
```

---

## Setup Instructions

### 1. Install Ollama

Follow the instructions on [ollama.com](https://ollama.com/download) to install Ollama for your platform.

After installation, verify it's working:

```bash
ollama --version
```

### 2. Pull the LLaVA model

```bash
ollama pull llava
```

Wait for the model to fully download.

### 3. Create and activate Python virtual environment

```bash
cd /path/to/your/project
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install streamlit httpx pandas pillow
```

---

## Running the App

### Step 1: Start the `llava` model using Ollama

In a separate terminal (do not close it):

```bash
ollama run llava
```

Wait for it to load and show the prompt (`>>>`). Leave it running.

### Step 2: Launch the Streamlit app

In your activated virtual environment:

```bash
cd /path/to/your/project
streamlit run app.py
```

This will open the Streamlit app in your default web browser at:

```
http://localhost:8501
```

---

## Using the App

1. Upload one or more receipt images in JPG, JPEG, or PNG format.
2. The app will send the image to `llava` running locally.
3. Once the model returns text output:

   * The raw response will be displayed.
   * Extracted line items (containing numbers) will be shown in a table.
   * You can download the results as a CSV file.

---

## Notes

* The LLaVA model (`llava`) uses vision + language to analyze receipt images.
* This implementation uses the Ollama API at `http://localhost:11434/api/generate`.
* The Streamlit UI is designed for simplicity; more fields (like tax, subtotal) can be extracted with more complex prompts or with post-processing using another model (like `llama3`).

---

## Troubleshooting

### Error: "500 Internal Server Error" or "received zero length image"

This usually occurs when:

* The uploaded image was not correctly read.
* `.read()` was called multiple times on the same Streamlit `UploadedFile` object.

This app fixes that by calling `.getvalue()` once and using it consistently.

---

## License

This project is for educational and personal use. Attribution to Ollama and the model creators is recommended.


