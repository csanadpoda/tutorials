# Translation App with Monitoring

A Dockerized application for translating text using OpenAI's API with built-in monitoring through Prometheus and Grafana.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Translating Text](#translating-text)
  - [Translating CSV Files and Scoring](#translating-csv-files-and-scoring)
  - [Monitoring](#monitoring)
- [Supported Languages](#supported-languages)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application allows users to translate text and CSV files into multiple languages using OpenAI's API. It also provides evaluation metrics for translations and includes monitoring capabilities via Prometheus and Grafana.

## Features

- **Text Translation**: Translate individual phrases or sentences.
- **CSV Translation and Scoring**: Upload CSV files for batch translation and receive evaluation metrics like BLEU, ROUGE, and BERTScore.
- **Monitoring**: Real-time monitoring of translation performance using Prometheus and Grafana.
- **Dockerized Setup**: Easy deployment using Docker Compose.

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- **NVIDIA GPU Drivers** (optional but recommended for better performance).
- Access to the **OpenAI API** or **Azure OpenAI Service**.
- **API Keys** for OpenAI or Azure OpenAI.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/translation-app.git
   cd translation-app
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your API keys:

   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   ```

   > **Note**: If you're using the standard OpenAI API, set `OPENAI_API_KEY` and `OPENAI_MODEL` instead.

3. **Build and Run the Docker Containers**

   ```bash
   docker-compose up -d
   ```

   This command will build the `translator_app` image and start all services defined in `docker-compose.yml`.

## Usage

### Translating Text

1. Open your web browser and navigate to [http://localhost:7860](http://localhost:7860).

2. Select the **Translate Phrases** tab.

3. Enter the text you wish to translate and select the target language from the dropdown.

4. Click **Translate** to receive the translated text.

### Translating CSV Files and Scoring

1. Prepare a CSV file with the following columns:

   - `english`: The text in English.
   - `translated_value`: The reference translation in the target language.
   - (Optional) `Google Translate`: Translations from Google Translate for comparison.

2. In the web interface, select the **Translate CSV & Score** tab.

3. Upload your CSV file and choose the target language.

4. Click **Translate and Evaluate** to perform translations and receive evaluation metrics.

### Monitoring

- **Prometheus** is accessible at [http://localhost:9090](http://localhost:9090).
- **Grafana** is accessible at [http://localhost:3000](http://localhost:3000).
  - Default Grafana credentials:
    - **Username**: `admin`
    - **Password**: `admin`

Use these interfaces to monitor translation performance and system metrics in real-time.

## Supported Languages

- Arabic
- French
- German
- Hindi
- Hungarian
- Japanese
- Portuguese
- Spanish

## Environment Variables

Set the following environment variables in your `.env` file:

- **For Azure OpenAI Service**:

  ```env
  AZURE_OPENAI_API_KEY=your_azure_openai_api_key
  AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
  ```

- **For OpenAI API**:

  ```env
  OPENAI_API_KEY=your_openai_api_key
  OPENAI_MODEL=your_openai_model
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## License

This project is licensed under the [MIT License](LICENSE).