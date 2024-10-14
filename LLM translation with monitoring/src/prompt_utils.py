def construct_prompt(source_text: str, target_language: str) -> str:
    """Construct the prompt for the OpenAI API call with language-specific
    examples and strengthened instructions."""
    # Language-specific examples
    examples = {
        "Arabic": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- Arabic: 'يرجى تأكيد [appointmentDate] الخاص بك.'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- Arabic: '[this] يجب أن يكون [that] التالي لي.'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect Arabic: 'يرجى تأكيد [تاريخالموعد] الخاص بك.' \
                (Translated the placeholder)\n"
                "- Incorrect Arabic: '[هذا] يجب أن يكون [ذلك] التالي لي.' \
                (Translated placeholders)\n\n"
            )
        },
        "French": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- French: 'Veuillez confirmer votre [appointmentDate].'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- French: '[this] devrait être mon prochain [that].'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect French: 'Veuillez confirmer votre \
                    [dateDuRendezVous].'(Translated the placeholder)\n"
                "- Incorrect French: '[ceci] devrait être mon prochain [cela].\
                     ' (Translated placeholders)\n\n"
            )
        },
        "German": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- German: 'Bitte bestätigen Sie Ihren [appointmentDate].'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- German: '[this] sollte mein nächstes [that] sein.'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect German: 'Bitte bestätigen Sie Ihren \
                [TerminDatum].'(Translated the placeholder)\n"
                "- Incorrect German: '[das] sollte mein nächstes [das] sein.'\
                      (Translated placeholders)\n\n"
            )
        },
        "Hindi": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- Hindi: 'कृपया अपने [appointmentDate] की पुष्टि करें।'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- Hindi: '[this] मेरा अगला [that] होना चाहिए।'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect Hindi: 'कृपया अपने [नियुक्तिदिनांक] की \
                    पुष्टि करें।' (Translated the placeholder)\n"
                "- Incorrect Hindi: '[यह] मेरा अगला [वह] होना चाहिए।' \
                    (Translated placeholders)\n\n"
            )
        },
        "Hungarian": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- Hungarian: 'Kérjük, erősítse meg a \
                    [appointmentDate]-t.'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- Hungarian: '[this] kellene legyen a következő [that].'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect Hungarian: 'Kérjük, erősítse meg a [időpont]ot.'\
                    (Translated the placeholder)\n"
                "- Incorrect Hungarian: '[ez] kellene legyen a következő \
                    [az].' (Translated placeholders)\n\n"
            )
        },
        "Japanese": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- Japanese: 'あなたの[appointmentDate]を確認してください。'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- Japanese: '[this]は私の次の[that]であるべきです。'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect Japanese: 'あなたの[予約日]を確認してください。' \
                    (Translated the placeholder)\n"
                "- Incorrect Japanese: '[これ]は私の次の[それ]であるべきです。' \
                    (Translated placeholders)\n\n"
            )
        },
        "Portuguese": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- Portuguese: 'Por favor, confirme seu [appointmentDate].'\n"
                "- English: '[this] should be my next [that].'\n"
                "- Portuguese: '[this] deve ser meu próximo [that].'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect Portuguese: 'Por favor, confirme seu \
                    [dataDaConsulta].' (Translated the placeholder)\n"
                "- Incorrect Portuguese: '[isto] deve ser meu próximo \
                    [aquilo].' (Translated placeholders)\n\n"
            )
        },
        "Spanish": {
            "positive_examples": (
                "**Positive Examples (Correct):**\n"
                "- English: 'Please confirm your [appointmentDate].'\n"
                "- Spanish: 'Por favor, confirme su [appointmentDate].'\n\n"
                "- English: '[this] should be my next [that].'\n"
                "- Spanish: '[this] debería ser mi próximo [that].'\n\n"
            ),
            "negative_examples": (
                "**Negative Examples (Incorrect):**\n"
                "- Incorrect Spanish: 'Por favor, confirme su [fechaDeCita].' \
                    (Translated the placeholder)\n"
                "- Incorrect Spanish: '[esto] debería ser mi próximo [eso].' \
                    (Translated placeholders)\n\n"
            )
        },
    }

    # Default examples for languages not specified
    default_examples = {
        "positive_examples": (
            "**Positive Examples (Correct):**\n"
            "- English: 'Please confirm your [appointmentDate].'\n"
            f"- {target_language}: 'Please confirm your [appointmentDate].' \
                (Do not translate placeholders)\n\n"
            "- English: '[this] should be my next [that].'\n"
            f"- {target_language}: '[this] should be my next [that].'\n\n"
        ),
        "negative_examples": (
            "**Negative Examples (Incorrect):**\n"
            f"- Incorrect {target_language}: 'Please confirm your \
                [translatedPlaceholder].' (Translated the placeholder)\n"
            f"- Incorrect {target_language}: '[translatedThis] should be my \
                next [translatedThat].' (Translated placeholders)\n\n"
        )
    }

    # Get examples for the target language
    lang_examples = examples.get(target_language, default_examples)

    return (
        f"Translate the following text from English to {target_language}.\n\n"
        "**Important Instructions (Please Read Carefully):**\n"
        "- DO **NOT TRANSLATE** ANY TEXT ENCLOSED IN SQUARE BRACKETS **[]**.\n"
        "- Leave all placeholders within **[]** exactly as they are.\n"
        "- Under no circumstances should content inside **[]** be altered.\n"
        "- DO NOT add or remove any square brackets.\n\n"
        f"{lang_examples['positive_examples']}"
        f"{lang_examples['negative_examples']}"
        "**Text to translate:**\n"
        f"{source_text}"
    )
