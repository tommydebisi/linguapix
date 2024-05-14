from modernmt import ModernMT


mmt = ModernMT("A864DC0E-CA4A-02D4-8BAC-0557155941C5")
def translate_srt(file_path, input_lang, output_lang, output_file_path):
    """
    Translates the content of an SRT file from one language to another using the ModernMT service.
    This function supports translations between English (en), French (fr), Fon (fon), and Yoruba (yo).

    Args:
        file_path (str): The path to the input SRT file.
        input_lang (str): The language code of the input file's language. Possible values are 'en', 'fr', 'fon', 'yo'.
        output_lang (str): The language code of the target translation language. Possible values are 'en', 'fr', 'fon', 'yo'.
        output_file_path (str): The path where the translated SRT file will be saved.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    translated_lines = []
    for line in lines:
        if line.strip().isdigit() or '-->' in line:
            translated_lines.append(line)
        else:
            # Ensure that the line is not empty before attempting translation
            if line.strip():
                translation_result = mmt.translate(input_lang, output_lang, line.strip())
                translated_text = translation_result.translation
                translated_lines.append(translated_text + '\n')
            else:
                translated_lines.append('\n')  # Preserve empty lines
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(translated_lines)
 

