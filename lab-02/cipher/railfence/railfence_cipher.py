class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # +1 đi xuống, -1 đi lên

        for char in plain_text:
            rails[rail_index].append(char)

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        cipher_text = ''.join([''.join(rail) for rail in rails])
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        # Bước 1: Xác định số lượng ký tự trên mỗi rail
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        # Bước 2: Cắt cipher_text thành các phần cho từng rail
        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(cipher_text[start:start + length])
            start += length

        # Bước 3: Ghép từng ký tự lại đúng thứ tự ban đầu
        plain_text = ''
        rail_index = 0
        direction = 1

        rail_pointers = [0] * num_rails  # vị trí lấy ký tự tiếp theo cho mỗi rail

        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index][rail_pointers[rail_index]]
            rail_pointers[rail_index] += 1

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        return plain_text
