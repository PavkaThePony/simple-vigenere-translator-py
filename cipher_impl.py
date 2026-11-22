import secrets

ALPHABETS = {
  "en": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
  "ru": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
  }

# returns tuple[encrypted_str, actual_key]
def vigenere(text: str, 
             key: str, 
             action: str, 
             lang: str, 
             case_mode: str, 
             strip_nac_chars: bool,
             key_policy: str) -> tuple[str, str]:

  alphabet = ALPHABETS[lang]
  alphabet = alphabet.upper()
  n = len(alphabet)

  if key_policy == "repeat":
    actual_key = [c.upper() for c in key if c.upper() in alphabet]
    if not actual_key:
      raise ValueError("Invalid key")
  elif key_policy == "random":
    if action == "encrypt":
      needed_length = sum(1 for c in text if c.upper() in alphabet)
      actual_key = [secrets.choice(alphabet) for _ in range(needed_length)]
    else: 
      actual_key = [c.upper() for c in key if c.upper() in alphabet]
      if not actual_key:
        raise ValueError("Invalid key")
  else:
    raise ValueError("Unknown key policy: ", key_policy)

  result: list[str] = []
  key_index = 0
  direction = 1 if action == "encrypt" else -1

  for char in text:
    upper_char = char.upper()
    if upper_char in alphabet:
      # find 0-based positions in alphabet
      text_char_pos = alphabet.index(upper_char)
      key_char      = actual_key[key_index % len(actual_key)]
      key_char_pos  = alphabet.index(key_char)

      # shift it!
      shifted_pos = (text_char_pos + key_char_pos * direction) % n # n=26 for "en" and n=33 for "ru"
      encrypted_char = alphabet[shifted_pos]
      
      if case_mode == "preserve":
        result.append(encrypted_char if char.isupper() else encrypted_char.lower())
      elif case_mode == "uppercase":
        result.append(encrypted_char)
      elif case_mode == "lowercase":
        result.append(encrypted_char.lower())

      key_index += 1

    else:
      if not strip_nac_chars:
        result.append(char)
      else:
        continue

  return "".join(result), "".join(actual_key)

