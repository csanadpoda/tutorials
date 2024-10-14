def construct_prompt(source_text: str, target_language: str) -> str:
    """Construct the prompt for the OpenAI API call with language-specific examples and strengthened instructions."""
    # Language-specific examples
    examples = {
        "Arabic": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- Arabic: 'يرجى تأكيد [appointmentDate] الخاص بك.'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- Arabic: '[this] يجب أن يكون [that] التالي لي.'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect Arabic: 'يرجى تأكيد [تاريخالموعد] الخاص بك.' (Translated the placeholder)\n"
                f"- Incorrect Arabic: '[هذا] يجب أن يكون [ذلك] التالي لي.' (Translated placeholders)\n\n"
            )
        },
        "French": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- French: 'Veuillez confirmer votre [appointmentDate].'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- French: '[this] devrait être mon prochain [that].'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect French: 'Veuillez confirmer votre [dateDuRendezVous].' (Translated the placeholder)\n"
                f"- Incorrect French: '[ceci] devrait être mon prochain [cela].' (Translated placeholders)\n\n"
            )
        },
        "German": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- German: 'Bitte bestätigen Sie Ihren [appointmentDate].'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- German: '[this] sollte mein nächstes [that] sein.'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect German: 'Bitte bestätigen Sie Ihren [TerminDatum].' (Translated the placeholder)\n"
                f"- Incorrect German: '[das] sollte mein nächstes [das] sein.' (Translated placeholders)\n\n"
            )
        },
        "Hindi": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- Hindi: 'कृपया अपने [appointmentDate] की पुष्टि करें।'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- Hindi: '[this] मेरा अगला [that] होना चाहिए।'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect Hindi: 'कृपया अपने [नियुक्तिदिनांक] की पुष्टि करें।' (Translated the placeholder)\n"
                f"- Incorrect Hindi: '[यह] मेरा अगला [वह] होना चाहिए।' (Translated placeholders)\n\n"
            )
        },
        "Hungarian": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- Hungarian: 'Kérjük, erősítse meg a [appointmentDate]-t.'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- Hungarian: '[this] kellene legyen a következő [that].'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect Hungarian: 'Kérjük, erősítse meg a [időpont]ot.' (Translated the placeholder)\n"
                f"- Incorrect Hungarian: '[ez] kellene legyen a következő [az].' (Translated placeholders)\n\n"
            )
        },
        "Japanese": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- Japanese: 'あなたの[appointmentDate]を確認してください。'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- Japanese: '[this]は私の次の[that]であるべきです。'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect Japanese: 'あなたの[予約日]を確認してください。' (Translated the placeholder)\n"
                f"- Incorrect Japanese: '[これ]は私の次の[それ]であるべきです。' (Translated placeholders)\n\n"
            )
        },
        "Portuguese": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- Portuguese: 'Por favor, confirme seu [appointmentDate].'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- Portuguese: '[this] deve ser meu próximo [that].'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect Portuguese: 'Por favor, confirme seu [dataDaConsulta].' (Translated the placeholder)\n"
                f"- Incorrect Portuguese: '[isto] deve ser meu próximo [aquilo].' (Translated placeholders)\n\n"
            )
        },
        "Spanish": {
            "positive_examples": (
                f"**Positive Examples (Correct):**\n"
                f"- English: 'Please confirm your [appointmentDate].'\n"
                f"- Spanish: 'Por favor, confirme su [appointmentDate].'\n\n"
                f"- English: '[this] should be my next [that].'\n"
                f"- Spanish: '[this] debería ser mi próximo [that].'\n\n"
            ),
            "negative_examples": (
                f"**Negative Examples (Incorrect):**\n"
                f"- Incorrect Spanish: 'Por favor, confirme su [fechaDeCita].' (Translated the placeholder)\n"
                f"- Incorrect Spanish: '[esto] debería ser mi próximo [eso].' (Translated placeholders)\n\n"
            )
        },
    }

    # Default examples for languages not specified
    default_examples = {
        "positive_examples": (
            f"**Positive Examples (Correct):**\n"
            f"- English: 'Please confirm your [appointmentDate].'\n"
            f"- {target_language}: 'Please confirm your [appointmentDate].' (Do not translate placeholders)\n\n"
            f"- English: '[this] should be my next [that].'\n"
            f"- {target_language}: '[this] should be my next [that].'\n\n"
        ),
        "negative_examples": (
            f"**Negative Examples (Incorrect):**\n"
            f"- Incorrect {target_language}: 'Please confirm your [translatedPlaceholder].' (Translated the placeholder)\n"
            f"- Incorrect {target_language}: '[translatedThis] should be my next [translatedThat].' (Translated placeholders)\n\n"
        )
    }

    # Get examples for the target language
    lang_examples = examples.get(target_language, default_examples)

    return (
        f"Translate the following text from English to {target_language}.\n\n"
        f"**Important Instructions (Please Read Carefully):**\n"
        f"- DO **NOT TRANSLATE** ANY TEXT ENCLOSED IN SQUARE BRACKETS **[]**.\n"
        f"- Leave all placeholders within **[]** exactly as they are.\n"
        f"- Under no circumstances should the content inside **[]** be altered.\n"
        f"- DO NOT add or remove any square brackets.\n\n"
        f"{lang_examples['positive_examples']}"
        f"{lang_examples['negative_examples']}"
        f"**Text to translate:**\n"
        f"{source_text}"
    )