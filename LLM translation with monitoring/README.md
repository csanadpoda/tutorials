# LLM Translation App with Monitoring

A Dockerized application for translating text using (Azure) OpenAI's API with built-in monitoring through Prometheus and Grafana.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Translating Text](#translating-text)
  - [Translating CSV Files and Scoring](#translating-csv-files-and-scoring)
  - [Monitoring](#monitoring)
- [Evaluation Metrics](#evaluation-metrics)
- [Supported Languages](#supported-languages)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application allows users to translate text and CSV files into multiple languages using OpenAI's API. It also provides evaluation metrics for translations and includes monitoring capabilities via Prometheus and Grafana.

## Features

- **Text Translation**: Translate individual phrases or sentences with [placeholder] support.
- **CSV Translation and Evaluation**: Upload CSV files for batch translation and receive evaluation metrics like BLEU, ROUGE, and BERTScore.
- **Monitoring**: Real-time monitoring of translation performance using Prometheus and Grafana.
- **Dockerized Setup**: Easy deployment using Docker Compose.

## Prerequisites

- **Docker** (and **Docker Compose**) installed on your system.
- **NVIDIA GPU Drivers** (optional but recommended for better evaluation performance).
- Access to the **OpenAI API** or **Azure OpenAI Service** with **API Keys**.

## Installation

1. **Clone the Repository or Copy the Solution**

   Git:
   ```bash
   git clone https://github.com/csanadpoda/tutorials.git
   cd "LLM translation with monitoring"
   ```

   Or just copy and change into the directory in CMD.

2. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your API keys. 
   Template `.env` files are provided (`.env_azure_oai` and `.env_oai`) - add your credentials to the one you use and rename it to `.env`.

   > **Note**: The solution has been tested with Azure OpenAI only. Some code changes might thus be needed for OpenAI.

3. **Build and Run the Docker Containers**

   ```bash
   docker-compose up -d
   ```

   This command will build the `translator_app` image and start all services defined in `docker-compose.yml`.

## Usage

### Translating Text

1. Open your web browser and navigate to [http://localhost:7860](http://localhost:7860).

2. Select the **Translate Phrases** tab.

3. Enter the English text you wish to translate and select the target language from the dropdown. Use `[]` to add placeholders, like this: `[placeHolder]`.

4. Click **Translate** to receive the translated text.

### Translating CSV Files and Scoring

1. Prepare a CSV file with the following columns:

   - `english`: The text in English.
   - `translated_value`: The reference translation in the target language.
   - (Optional) `Google Translate`: Translations from Google Translate for comparison.
   
   > **Note**: [`[placeHolders]` are also supported in this mode.].

2. In the web interface, select the **Translate CSV & Score** tab.

3. Upload your CSV file.
   > **Note**: [Example CSV's are provided in the solution folder.].

4. Click **Translate and Evaluate** to perform translations and receive evaluation metrics.

### Monitoring

- **Prometheus** is accessible at [http://localhost:9090](http://localhost:9090).
- **Grafana** is accessible at [http://localhost:3000](http://localhost:3000).
  - Default Grafana credentials:
    - **Username**: `admin`
    - **Password**: `admin`

Use these interfaces to monitor translation performance and system metrics in real-time.

## Evaluation Metrics

When translating a CSV file, the application computes several evaluation metrics to assess the quality of the translations. These metrics are displayed in a summary table and include:

### BLEU (Bilingual Evaluation Understudy Score)
Measures the correspondence between the machine's output and that of human translations by calculating n-gram overlaps.

- *Score Range*: 0 to 100 (higher is better).
- *Interpretation*: A higher BLEU score indicates a closer match to the reference translation.

### ChrF (Character n-gram F-score)
Evaluates translation quality based on character-level n-gram precision and recall, making it effective for morphologically rich languages.

- *Score Range*: 0 to 100 (higher is better).
- *Interpretation*: Higher ChrF scores suggest better translation quality at the character level.

### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

Measures the overlap between the machine translation and reference translation.
Metrics:

- **ROUGE-1 F1**: Overlap of unigrams (individual words).
- **ROUGE-2 F1**: Overlap of bigrams (two-word sequences).
- **ROUGE-L F1**: Longest Common Subsequence, capturing sentence-level structure similarity.
- *Score Range*: 0 to 100 (higher is better).
- *Interpretation*: Higher ROUGE scores indicate better recall and precision in capturing relevant information.

### BERTScore F1

Uses contextual embeddings from BERT models to measure the semantic similarity between the machine translation and the reference.

- *Score Range*: 0 to 100 (higher is better).
- *Interpretation*: A higher BERTScore F1 means the translation is semantically closer to the reference translation.

## Supported Languages

- Arabic
- French
- German
- Hindi
- Hungarian
- Japanese
- Portuguese
- Spanish

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## License

This project is licensed under the [MIT License](LICENSE).