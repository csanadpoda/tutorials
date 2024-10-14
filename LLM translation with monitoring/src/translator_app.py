import os
import re
from typing import Tuple, List
import logging

import pandas as pd
import torch
import gradio as gr
from bert_score import score as bert_score
from dotenv import load_dotenv
import openai

from rouge import Rouge
import sacrebleu
from prometheus_client import start_http_server, Summary, Counter
from prompt_utils import construct_prompt

# Create metrics
TRANSLATE_TEXT_TIME = Summary('translate_text_processing_seconds', 'Time spent processing translate_text()')
TRANSLATE_AND_SCORE_TIME = Summary('translate_and_score_processing_seconds', 'Time spent processing translate_and_score()')
TRANSLATION_ERRORS = Counter('translation_errors_total', 'Total translation errors')
start_http_server(8000, addr="0.0.0.0")

# Load environment variables
load_dotenv()

# Check for CUDA availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Device information string
if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    device_info = (
        f"**Device Information:**\n"
        f"- **CUDA Available:** Yes\n"
        f"- **Device Name:** {device_name}"
    )
else:
    device_info = (
        f"**Device Information:**\n"
        f"- **CUDA Available:** No\n"
        f"- **Using CPU**"
    )

# Language options for multi-language translation tab
language_options = {
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Spanish": "es",
}

def initialize_openai_client():
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        # Initialize Azure OpenAI if Azure-specific keys are found
        return openai.AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-03-15-preview"
        ), os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    else:
        # Fallback to standard OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return openai, os.getenv("OPENAI_MODEL")

# Initialize the correct OpenAI client and model/deployment name based on environment variables
oai_client, model_name = initialize_openai_client()

def preprocess(text: str) -> str:
    """Lowercase and remove extra whitespace from the text."""
    return ' '.join(text.lower().split())

def extract_placeholders(text: str) -> List[str]:
    """Extract placeholders enclosed in square brackets."""
    return re.findall(r'\[.*?\]', text)

def replace_translated_placeholders(source_text: str, translated_text: str) -> str:
    """Replace any translated placeholders in the translated text with the original placeholders."""
    source_placeholders = extract_placeholders(source_text)
    translated_placeholders = extract_placeholders(translated_text)

    # Map placeholder content to original placeholders
    placeholder_map = {ph.strip(): ph for ph in source_placeholders}

    # Replace placeholders in translated text with originals
    for ph in translated_placeholders:
        content = ph.strip()
        if content in placeholder_map:
            translated_text = translated_text.replace(ph, placeholder_map[content])
        else:
            # If the placeholder content does not match, replace with original placeholder
            translated_text = translated_text.replace(ph, ph)

    return translated_text

@TRANSLATE_TEXT_TIME.time()
def translate_text(input_text: str, target_language: str) -> str:
    """Translate the input text to the target language using OpenAI API."""
    try:
        system_prompt = construct_prompt("", target_language)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ]
        response = oai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.0,  # Lower temperature for deterministic output
        )
        translated = response.choices[0].message.content.strip()
        # Post-processing to ensure placeholders are not translated
        translated = replace_translated_placeholders(input_text, translated)
        return translated
    except Exception as e:
        TRANSLATION_ERRORS.inc()
        logging.error(f"Translation failed: {e}")
        logging.error(f"Endpoint returned: {response}")
        raise e

def tokenize_text(text: str, language_code: str) -> List[str]:
    """Tokenize text based on the language code using sacrebleu's tokenizer."""
    return sacrebleu.tokenizers.TokenizerV14International().tokenize(text).split()

@TRANSLATE_AND_SCORE_TIME.time()
def translate_and_score(
    file, target_language: str = 'Hungarian'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Translate and evaluate translations from a CSV file."""
    try:
        df = pd.read_csv(file.name)
        translations = []

        lang_code = language_options.get(target_language, 'en')

        for _, row in df.iterrows():
            source_text = row['english']
            translated_text = translate_text(source_text, target_language)
            translations.append(translated_text)

        df['translated_by_model'] = translations
        df['translated_value'] = df['translated_value'].apply(preprocess)
        df['translated_by_model'] = df['translated_by_model'].apply(preprocess)

        # Prepare references and hypotheses
        references = df['translated_value'].tolist()
        model_translations = df['translated_by_model'].tolist()

        summary_data = {
            'Metric': ['BLEU', 'CHRF', 'ROUGE-1 F1', 'ROUGE-2 F1', 'ROUGE-L F1', 'BERTScore F1'],
            'Model Translations': [],
        }

        # Evaluation for Google Translate if available
        if 'Google Translate' in df.columns:
            df['Google Translate'] = df['Google Translate'].apply(preprocess)
            google_translations = df['Google Translate'].tolist()

            # Compute BLEU and ChrF using sacrebleu
            google_bleu = sacrebleu.corpus_bleu(google_translations, [references])
            google_chrf = sacrebleu.corpus_chrf(google_translations, [references])

            # Compute ROUGE scores
            google_rouge_scores = Rouge().get_scores(
                google_translations,
                references,
                avg=True
            )

            # Compute BERTScore
            _, _, google_bertscore_f1 = bert_score(
                google_translations,
                references,
                model_type='xlm-roberta-base',
                lang=lang_code,
                device=device
            )

            summary_data['Google Translate'] = [
                round(google_bleu.score, 2),
                round(google_chrf.score, 2),
                round(google_rouge_scores['rouge-1']['f'] * 100, 2),
                round(google_rouge_scores['rouge-2']['f'] * 100, 2),
                round(google_rouge_scores['rouge-l']['f'] * 100, 2),
                round(float(google_bertscore_f1.mean()) * 100, 2),
            ]

        # Evaluation for Model Translations
        # Compute BLEU and ChrF using sacrebleu
        model_bleu = sacrebleu.corpus_bleu(model_translations, [references])
        model_chrf = sacrebleu.corpus_chrf(model_translations, [references])

        # Compute ROUGE scores
        model_rouge_scores = Rouge().get_scores(
            model_translations,
            references,
            avg=True
        )

        # Compute BERTScore
        _, _, model_bertscore_f1 = bert_score(
            model_translations,
            references,
            model_type='xlm-roberta-base',
            lang=lang_code,
            device=device
        )

        summary_data['Model Translations'] = [
            round(model_bleu.score, 2),
            round(model_chrf.score, 2),
            round(model_rouge_scores['rouge-1']['f'] * 100, 2),
            round(model_rouge_scores['rouge-2']['f'] * 100, 2),
            round(model_rouge_scores['rouge-l']['f'] * 100, 2),
            round(float(model_bertscore_f1.mean()) * 100, 2),
        ]

        summary_df = pd.DataFrame(summary_data)
        return df, summary_df
    except Exception as e:
        TRANSLATION_ERRORS.inc()
        logging.error(f"Multi-translation failed: {e}")
        logging.error(f"Translations: {translations}")
        raise e

with gr.Blocks(css="""
    .qa-pairs .table-wrap {
        max-height: 400px;
        overflow-y: scroll;
    }
""") as demo:
    with gr.Tab("Translate Phrases"):
        gr.Markdown(device_info)
        input_text = gr.Textbox(label="Input Text")
        target_language = gr.Dropdown(
            list(language_options.keys()),
            label="Target Language",
            value=list(language_options.keys())[0]
        )
        translated_text = gr.Textbox(label="Translated Text")
        translate_button = gr.Button("Translate")
        translate_button.click(
            translate_text,
            inputs=[input_text, target_language],
            outputs=translated_text
        )

    with gr.Tab("Translate CSV & Score"):
        gr.Markdown(device_info)
        file = gr.File(label="Upload CSV")
        target_language_csv = gr.Dropdown(
            list(language_options.keys()),
            label="Target Language",
            value='Hungarian'
        )
        output_df = gr.Dataframe(
            headers=["hungarian", "translated_value", "translated_by_model"],
            interactive=False,
            elem_id="qa-pairs"
        )
        summary_df = gr.Dataframe(
            headers=["Metric", "Original Translations", "Generated Translations"],
            interactive=False
        )
        score_button = gr.Button("Translate and Evaluate")
        score_button.click(
            translate_and_score,
            inputs=[file, target_language_csv],
            outputs=[output_df, summary_df]
        )

demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)