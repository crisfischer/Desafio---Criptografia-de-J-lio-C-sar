import hashlib
import requests
import string
import json

    token_user = '297c54fd339da610deec689565cf7f5f4dd8e8a2'

r = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={token}'.format(token=token_user))
data = r.json()


def get_alphabet():
    return list(string.ascii_lowercase)


def decipher_message(imput_msg):
    alphabet = get_alphabet()
    message = list(imput_msg.get('cifrado'))
    result = ''
    for l in message:
        if l in alphabet:
            i = alphabet.index(l)
            i = i - imput_msg['numero_casas']
            result = result + alphabet[i]
        elif l == '.':
            result = result + l
        else:
            result = result + l
    return result


def transform_to_sha1(decifrado):
    return hashlib.sha1(str(decifrado).encode('utf-8')).hexdigest()


data['decifrado'] = decipher_message(data)
data['resumo_criptografico'] = transform_to_sha1(data['decifrado'])

with open('answer.json', 'w') as fp:
    json.dump(data, fp)

files = {'answer': open('answer.json', 'rb')}
url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={token}'.format(token=token_user)

r = requests.post(url=url, files=files)
print(r.content)
