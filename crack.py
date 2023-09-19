import sys
import hashlib
import create_table

target_hash = sys.argv[1] # このハッシュ値から元のパスワードを知りたい
file_path = create_table.file_path
chain_len = create_table.chain_len
reduction = create_table.reduction
to_str = create_table.to_str
first_passwords = []
last_hashes = []

with open(file_path) as f:
    for s in f.readlines():
        first_password, last_hash = s[:-1].split(',')
        first_passwords.append(first_password)
        last_hashes.append(last_hash)

for i in range(chain_len):
    now_hash = target_hash

    for j in range(i):
        now_password = to_str(reduction(int(now_hash, 16), chain_len - 1 - i + j))
        now_hash = hashlib.sha256(now_password.encode()).hexdigest()

    if now_hash in last_hashes:
        pos = last_hashes.index(now_hash)
        first_password = first_passwords[pos]
        now_password = first_password

        for j in range(chain_len - i - 1):
            now_hash = hashlib.sha256(now_password.encode()).hexdigest()
            now_password = to_str(reduction(int(now_hash, 16), j))

        assert(hashlib.sha256(now_password.encode()).hexdigest() == target_hash)
        exit(print(f'password found! : {now_password}'))

print('password not found.')