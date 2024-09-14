""" from https://github.com/keithito/tacotron """
from text import cleaners
from text.symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def text_to_sequence(text, cleaner_names):
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
    """
    sequence = []
    if cleaner_names == ["tab_separated"]:
        # not using cleaners -- assume text is already cleaned, with ipa phonemes separated by tabs
        return cleaned_text_to_sequence(text.strip())
    else:
        # uses cleaners
        clean_text = _clean_text(text, cleaner_names)
        for symbol in clean_text:
            if symbol in _symbol_to_id.keys():
                symbol_id = _symbol_to_id[symbol]
                sequence += [symbol_id]
            else:
                continue
        return sequence


def cleaned_text_to_sequence(cleaned_text):
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence, with ipa phonemes separated by tabs
      e.g "t\tɛ\tk\ts\tt\t𝑎𝑙𝑙𝑒𝑔𝑟𝑜"
    Returns:
      List of integers corresponding to the symbols in the text
    """
    sequence = []
    cleaned_text_ = cleaned_text.split("\t")
    for symbol in cleaned_text_:
        if symbol in _symbol_to_id.keys():
            symbol_id = _symbol_to_id[symbol]
            sequence += [symbol_id]
        else:
            continue
    return sequence


def sequence_to_text(sequence):
    """Converts a sequence of IDs back to a string"""
    result = ""
    for symbol_id in sequence:
        s = _id_to_symbol[symbol_id]
        result += s
    return result


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception("Unknown cleaner: %s" % name)
        text = cleaner(text)
    return text
