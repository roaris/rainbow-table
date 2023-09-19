# パスワードの集合は[a-zA-Z0-9]{1,12}とする

import string
import random
import hashlib

random.seed(0)

characters = string.ascii_letters + string.digits # [a-zA-Z0-9]
password_max_len = 12
chain_num = 1000 # 本当はもっと大きい
chain_len = 1000 # 本当はもっと大きい
file_path = 'table.txt'

def reduction(x, i): # https://crypto.stackexchange.com/questions/37832/how-to-create-reduction-functions-in-rainbow-tables
    return (x + i) % (62 ** password_max_len)

def to_str(x):
    if x == 0:
        return characters[0]

    l = []

    while x:
        l.append(characters[x % 62])
        x //= 62

    l.reverse()
    return ''.join(l)

if __name__ == '__main__':
    pairs = [] # 各チェインの開始と末尾を格納する

    for i in range(chain_num):
        first_password_len = random.randrange(1, password_max_len + 1)
        first_password = ''.join([random.choice(characters) for _ in range(first_password_len)])
        now_password = first_password

        for j in range(chain_len):
            now_hash = hashlib.sha256(now_password.encode()).hexdigest()
            now_password = to_str(reduction(int(now_hash, 16), j))

        pairs.append((first_password, now_hash))

        if (i + 1) % 10 == 0:
            print(f'chain {i + 1} created.')

    print(f'all chain created.')

    with open(file_path, mode='w') as f:
        for p, h in pairs:
            f.write(f'{p},{h}\n')