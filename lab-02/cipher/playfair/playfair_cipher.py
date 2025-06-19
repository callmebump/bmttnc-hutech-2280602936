class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace('J', 'I')
        key_set = []
        for letter in key:
            if letter not in key_set and letter.isalpha():
                key_set.append(letter)

        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # J được gộp vào I
        for letter in alphabet:
            if letter not in key_set:
                key_set.append(letter)

        matrix = [key_set[i:i+5] for i in range(0, 25, 5)]
        return matrix

    def find_letter_coordinates(self, matrix, letter):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == letter:
                    return i, j

    def prepare_text(self, plain_text):
        plain_text = plain_text.upper().replace('J', 'I')
        text = ''
        i = 0
        while i < len(plain_text):
            a = plain_text[i]
            b = ''
            if (i + 1) < len(plain_text):
                b = plain_text[i + 1]
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2

            text += a + b

        if len(text) % 2 != 0:
            text += 'X'
        return text

    def encrypt(self, plain_text, key):
        matrix = self.create_playfair_matrix(key)
        plain_text = self.prepare_text(plain_text)
        encrypted_text = ''
        for i in range(0, len(plain_text), 2):
            a = plain_text[i]
            b = plain_text[i + 1]
            row1, col1 = self.find_letter_coordinates(matrix, a)
            row2, col2 = self.find_letter_coordinates(matrix, b)

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def decrypt(self, cipher_text, key):
        matrix = self.create_playfair_matrix(key)
        decrypted_text = ''
        for i in range(0, len(cipher_text), 2):
            a = cipher_text[i]
            b = cipher_text[i + 1]
            row1, col1 = self.find_letter_coordinates(matrix, a)
            row2, col2 = self.find_letter_coordinates(matrix, b)

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return decrypted_text
