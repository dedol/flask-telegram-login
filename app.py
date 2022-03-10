from flask import Flask, request
import hmac
import hashlib


app = Flask(__name__)
app.config['TELEGRAM_BOT_TOKEN'] = '0000000000:AAAAA-BBBBBBBB_CCC_DDDDDDDDDDDDDDDD'


@app.route('/')
def index():
    return '''
    <body>
        <script async 
            src="https://telegram.org/js/telegram-widget.js?16" 
            data-telegram-login="example_bot" 
            data-size="large" 
            data-auth-url="http://your_domain.ngrok.io/login/telegram" 
            data-request-access="write">
        </script>
    </body>
    '''


def check_response(data):
    d = data.copy()
    del d['hash']
    d_list = []
    for key in sorted(d.keys()):
        if d[key] != None:
            d_list.append(key + '=' + d[key])
    data_string = bytes('\n'.join(d_list), 'utf-8')

    secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
    hmac_string = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
    if hmac_string == data['hash']:
        return True
    return False


@app.route('/login/telegram')
def login_telegram():
    data = {
        'id': request.args.get('id', None),
        'first_name': request.args.get('first_name', None),
        'last_name': request.args.get('last_name', None),
        'username': request.args.get('username', None),
        'photo_url': request.args.get('photo_url', None),
        'auth_date': request.args.get('auth_date', None),
        'hash': request.args.get('hash', None)
    }

    if check_response(data):
        # Authorize user
        return data
    else:
        return 'Authorization failed'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)