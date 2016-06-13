import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key):
        self.key = key
        self.BLOCK_SIZE = 16

    def _pad(self, data):
        length = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        return data + chr(length)*length

    def _unpad(self, data):
        return data[:-ord(data[-1])]

    def encrypt(self, message):
        IV = Random.new().read(self.BLOCK_SIZE)
        aes = AES.new(self.key, AES.MODE_CBC, IV)
        return base64.b64encode(IV + aes.encrypt(self._pad(message)))

    def decrypt(self, encrypted):
        encrypted = base64.b64decode(encrypted)
        IV = encrypted[:self.BLOCK_SIZE]
        aes = AES.new(self.key, AES.MODE_CBC, IV)
        return self._unpad(aes.decrypt(encrypted[self.BLOCK_SIZE:]))


if __name__ == '__main__':

    BLOCK_SIZE = 16
    key = b"1234567890123456"

    def pad(data):
        length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        return data + chr(length)*length

    def unpad(data):
        return data[:-ord(data[-1])]

    def encrypt(message, passphrase):
        IV = Random.new().read(BLOCK_SIZE)
        aes = AES.new(passphrase, AES.MODE_CBC, IV)
        return base64.b64encode(IV + aes.encrypt(pad(message)))

    def decrypt(encrypted, passphrase):
        encrypted = base64.b64decode(encrypted)
        IV = encrypted[:BLOCK_SIZE]
        aes = AES.new(passphrase, AES.MODE_CBC, IV)
        return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))

    #texto = 'BfwmrhpP22itZi4JXC61mW/hobx8xm53w6mZAVrT9K/f/NzhhhVzYIEvuIcNpcnuhsfWcnWyr/5dsy0e3jMawNsV3ADIvCZil3eQu2wA4Gad68LUQCRY+G5h1/lFUXxhvA6PkiYo7uNW4f0spirkX1pj8Day3//YqYw+23O6mPOp5hsgEecOsHXjUMR+2wZJ6wt8v/O2NniEizU40NxgsNjzoDCdJlzhWTe5SEcn1ZpZBVyUNqB2Z+iaGhskbLrYruyNAM1V+GwFHfWzS3FDnFGOD0fvudPJwIozV/hXvLpKI1GZ0scw/VqEFdjbKj7e4/tDQ01vYVkKvCWZdu72zmqXmBqJCpVG1sOVYWfaUVXgXEkawHMCpYSwIQAnVA/95ncgE3ZpegwSjnp//DwuRaPZoMzTIHyV9pR+U9OWmdEYT6wgJIo6dUByRhilJ44H9eO6rRAi/n7OYGfwSheVH1xDlBdirxt3q2Kc+JiRv+pQ5R9ZSBK+kHgjUtR8ycgCdIVJL+Id2l9mpnTUIrofXzb9kDVvBkN8j2EKyS23XOph7yzH7qvpzFIvUW0uIZGkbQ/yLVk0hKhqmKILNBVwK+vaba4Lxd8lWQITFUzHcE1vMyybPEY+BPyEknQwoYXixKw9WPaDCN5FdSrmmZsPUCu1TbVRiRXjCCRhpVipeCfMW6FXel0f0Ei4/sI9eZ44hq62azhLZUN3jcOH2Dhjr++87DCtUjKmwC99i0B/3q136hkpiEECX9WnheWQE3jT6XpfOItpYjV5nfmofNvWRdny5phtPuwM3Nn4DE87k4FXwCQLu7U+o9OmoB268lU9WOM7WWSwAQG/l/kbgHokqlonf1/wSoKtVX9w7rn3D1aYdBBPob4y7e9wm/sbZr09FWhVD7AGxPM091sjRXN2S+wC8GYIGRzAAgYQiT19K9DNpLVEdWWlSFjFwnVYTOUH87YqyIW6WlMZKICzh4kHi6+6DoAbdZ4w98YI6xwFfPGwvi9A2QlbNthKBcEUweBfysaayXxfxS1Wyy7SRiHgklaSXhvwN6Wgi0mpFQi7f8CfYApZ/WrvFlNfbXVXH9MbCBd9Ffb/KTWj/pRALdZOoXDP6Wc6m9CTyCN/+0flTfUF+cD8LGOl46jqg/VL6xLxIFYoRBc1YtkAQxvlvbH688PgR5cM9vGevV40pSyPfLVZJf+PcwNGMcyxEu6uv/3UtCs7gRhoO7JZA6sXS1fQGWxrLtX68O+YC07MVhWYD24OqLD5HUu8DztXDXDoGKzT'
    texto = 'idi9Oqer9ax05E9x/F9jH3bmeg/J1jYQoi6QwWgBd8Gj9KSs+0N/VQxgTq2CA8Zsx5t1cDT01S6vOYatRFiKrOpnnuE4c8Iv/zzFWSSZPk/8elJoYVO+vJe/OuWQh7GYlhCxRvVwCk2hpCI2BOwHCEtPhoEaXIE+lW5x6vskVOsU74QYg1aVlG63wzvquTn17hqpIJfvubGe5/M5yQWpOTMPZKMCfRlVeXT2h+diF3BbiGYbUha/7wq9I62MDmZ4I6ec4EhgPZFoDxWoyk0lMTFHvbw0dBEJJxMTp0fsUl3fLfAuFZ5QcOkqL/pwXn7mg4t2rNfL7HVrwt8GRnPuLl+SKSXtsFxXp7axsZ+MNmJ5Fx+YqN/hiLauEoD7QBXkBI6LuFMxPxu+vk0TD8t8x1T5B+I55hs6KnerDoDUyN8c76/dYomPzhnntJ20HqAiiiuABjDiq0TYsKh6k85mobIS/tTVRBffrKKpEnYDXkn2c0tB12DP+qI3Qt7dm2AKIBo0RvMYzrDHFINzukE5k3WP4PvQDZjukWekumoQrJrIRPgNXEuPNCDkmlWhGFYS6lA3bcRwaF8+7NhLZpDtlTUmH5Afry5lqCkof2RYphRjzGUc92NeMlVmDZ6ZHezYVUyYkkEKfhW/+Z1tMYfBpudHGPd/z9NFmxqN/e8RJUvkr0qT4wdBoOxRbwiZhyQHwveQL1iB8qB0kxKl9Peq5r08ubf4K+0sfkkUF+yM30lLTyNbVrEd8SpFxO2TOAZuSJkG1O7AOLv1SILXLq3yjshJDpoJKJrzFNWySMCpRjkIiEPUiwG3LMu52MMmTfxrWPFC7XYgMXhYmySo68+c3ybwQ6+4uDQemCFOtlOt/wSWuL6WzPBELcaqtSxIlJ94AZzGg4eukJfvwgTPNOyo6C7zSWx2c26AyWKw7pb/0FQrxwMnQ5bYncKjbeDYBGxbfTXojkHNlY70eYoYifhEAcOu6qKWIbCJM2IBt21NjTkBUt93JcDR48B99kXY/yJsSj2YiWThl68Ha4VTgcmdDe3rvyoSW7Q9hwufwg/dBFetgfW6Lh7liSbGu0AHP94IUxEhFjkJjvIoWsCXhmFomgKdPFp6vPrwotu0S0TbN/xt1OIfsgj0uSd6SqUzYurRkPqXhZvIL7VN9HgxCpulFqkiIZRwyfoB45tfezI4lfYwdgJ/IxNyW1l625s8cEgine/YAvm3mhG/JHECrUN5vA=='

    key = b'abcdefghijklmnqw' # 16 bits!!
    print decrypt(texto, key)