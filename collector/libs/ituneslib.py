import re

from requests import session


class MyTunesConnect:

    def __init__(self, username, password):
        self.cookies = None
        self.session = None
        self.start_session(username, password)

    def start_session(self, username, password):
        self.session = session()

        headers = {
            'Content-Type': 'application/json',
            'X-Apple-Widget-Key': '22d448248055bab0dc197c6271d738c3'
        }

        payload = {
            'accountName': username,
            'password': password,
            'rememberMe': False
        }

        resp = self.session.post('https://idmsa.apple.com/appleauth/auth/signin', json=payload, headers=headers)
        cookies = resp.headers['set-cookie'] if 'set-cookie' in resp.headers else None

        if cookies:
            acc_info = re.search(r"myacinfo=.+?;", cookies).group(0)
            if acc_info and len(acc_info) > 0:
                resp = self.session.get('https://olympus.itunes.apple.com/v1/session',
                                        allow_redirects=False,
                                        headers={'Cookie': acc_info})
                cookies = resp.headers['set-cookie'] if 'set-cookie' in resp.headers else None
                itctx = re.search(r"itctx=.+?;", cookies).group(0)
                if itctx and len(itctx) > 0:
                    self.cookies = cookies
                else:
                    raise Exception("Not found itctx cookie, so apple may be changed login process")

            else:
                print("No account info found while loading login page cookies")
                self.session = None

    def get_apps(self):
        request = self.session.get(
            'https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/apps/manageyourapps/summary/v2',
            cookies={"Cookies": self.cookies})
        response = request.json()
        return response

    def get_in_app_products(self, app_id):
        request = self.session.get(
            'https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/apps/{}/iaps'.format(app_id),
            cookies={"Cookies": self.cookies})
        response = request.json()
        return response

    def get_in_app_product_details(self, app_id, product_id):
        request = self.session.get(
            'https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/apps/{}/iaps/{}'.format(app_id,
                                                                                                     product_id),
            cookies={"Cookies": self.cookies})
        response = request.json()

        return response

