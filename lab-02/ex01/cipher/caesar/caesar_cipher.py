from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET
        
    def encrypt_text(self, text: str, key: int) -> str:
            alphabet_len = len(self.alphabet)
            text = text.upper()
            encrypt_text = []
            for letter in text:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + key) % alphabet_len
                output_letter = self.alphabet[output_index]
                encrypt_text.append(output_letter)
            return "".join(encrypt_text)
            
    def decrypt_text(self, text: str, key: int) -> str:
                alphabet_len = len(self.alphabet)
                text = text.upper()
                decrypt_text = []
                for letter in text:
                    letter_index = self.alphabet.index(letter)
                    output_index = (letter_index - key) % alphabet_len
                    output_letter = self.alphabet[output_index]
                    decrypt_text.append(output_letter)
                return "".join(decrypt_text)