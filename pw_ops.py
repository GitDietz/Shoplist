from werkzeug.security import generate_password_hash, check_password_hash

hash = generate_password_hash('mysecret')
print(hash)
if check_password_hash(hash,'mysecrets'):
    print('Pw is ok')
else:
    print('pw is rubbish')