import datetime
import json
import os
import random
import ssl
import time

import cloudscraper
import requests
import warnings

import ua_generator
from bs4 import BeautifulSoup

from NicknameGenerator import GenerateNickname
from Utils.Check_mail import check_mail

warnings.filterwarnings("ignore", category=DeprecationWarning)



class FanslyModel:

    def __init__(self, authorization_token, proxy, user_agent=None):

        self.access_token = authorization_token if authorization_token != "" else None
        self.refresh_token = None
        self.password_ = None

        if user_agent:
            self.ua = user_agent
        else:
            self.ua = self.generate_user_agent

        self.session = self._make_scraper
        self.proxy = proxy
        self.session.proxies = {"http": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                "https": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"}
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.session.headers.update({"user-agent": self.ua,
                                     'content-type': 'application/json'})

        if self.access_token:
            self.session.headers.update({"authorization": self.access_token})



    def GetClients(self) -> list:

        clients = []

        startFrom = 0
        while True:

            with self.session.post(f"https://apiv3.fansly.com/api/v1/messaging/groups?sortOrder=1&flags=0&subscriptionTierId=&search=&limit=25&offset={startFrom}&ngsw-bypass=true") as response:

                for user in response.json()["response"]["data"]:
                    clients.append(user)

                if len(response.json()["users"]) == 25:
                    startFrom += 25
                    continue

                else:

                    break

        return clients

    def GetMe(self):

        with self.session.get("https://apiv3.fansly.com/api/v1/account/me?ngsw-bypass=true") as response:

            return response.json()

    def GetMessages(self, user_id):

        messages = []
        startFrom = 0

        while True:

            with self.session.post(f"https://apiv3.fansly.com/api/v1/message?groupId={user_id}&limit=25&ngsw-bypass=true") as response:

                messages_ = response.json()["response"]["messages"]

                for message in messages_:
                    messages.append(message)

                if len(messages_) == 25:
                    startFrom += 25
                    continue

                else:

                    break

        return messages

    def Registration(self, password, email):

        while True:

            payload = {"email": email,
                       "password": password,
                       "username": GenerateNickname()}
            # print(payload)

            with self.session.post("https://apiv3.fansly.com/api/v1/registernew?ngsw-bypass=true",
                                   json=payload) as response:

                print(response.json())
                if response.json()["success"] == False:
                    time.sleep(random.randint(1, 5))
                    continue
                else:
                    self.access_token = response.json()["response"]["session"]["token"]

                    self.session.headers.update({"authorization": self.access_token})
                    data = response.json()
                    return self.access_token, data['response']['session']['accountId']

    def LoginWithTwitter(self, ct0, auth_token):

        with self.session.post("https://apiv3.fansly.com/api/v1/thirdpartyconnect/authorization?ngsw-bypass=true", json={"providerId":"1","type":1}) as response:

            # print(response.json())

            special_token = response.json()["response"]["token"]
            link = response.json()["response"]["redirectUri"]
            oauth_token = link.split("oauth_token=")[-1]

            self.session.cookies.update({'auth_token': auth_token, 'ct0': ct0})
            self.session.headers.update({
                'content-type': 'application/x-www-form-urlencoded'})

            with self.session.get(f'https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}',timeout=15) as response:

                soup = BeautifulSoup(response.text, 'html.parser')
                authenticity_token = soup.find('input', attrs={'name': 'authenticity_token'}).get('value')
                payload = {'authenticity_token': authenticity_token,
                           'redirect_after_login': f'https://api.twitter.com/oauth/authorize?oauth_token={oauth_token}',
                           'oauth_token': oauth_token}

                # self.session.cookies.update({'auth_token': self.tw_auth_token, 'ct0': self.tw_csrf})
                with self.session.post(f'https://api.twitter.com/oauth/authorize', data=payload, timeout=15,
                                       allow_redirects=True) as response:
                    # self.session.cookies.update({'auth_token': self.tw_auth_token, 'ct0': self.tw_csrf})
                    soup = BeautifulSoup(response.text, 'html.parser')
                    link = soup.find('a', class_='maintain-context').get('href')
#                     print(link)

                    self.session.headers.update({"dnt": "1",
                                                 "sec-fetch-dest": "document",})

                    self.session.headers.update({"authorization": None})

                    with self.session.get(link, timeout=15, allow_redirects=False) as response:

#                         print(response.headers)
#                         print(response.text)

                        special_token = response.headers['Location'].split("thirdpartyconnect/login/")[-1]

                        with self.session.get(response.headers['Location']) as response:

                            if response.ok:

                                with self.session.get("https://apiv3.fansly.com/api/v1/versioning?ngsw-bypass=true") as response:
#                                     print(response.json())
                                    pass

                                self.session.headers.update({"content-type": "application/json",
                                                             "sec-fetch-dest": "empty",
                                                             "fansly-client-ts": f"{response.json()['response']['ts']}"})

                                with self.session.post("https://apiv3.fansly.com/api/v1/thirdpartyconnect/login?ngsw-bypass=true", json={"token":special_token}) as response:
                                    print(response.json())
                                    self.access_token = response.json()["response"]["session"]["token"]

                                    self.session.headers.update({"authorization": self.access_token})
                                    return self.access_token, self.ua

                            else:
#                                 print(f'Twitter connection failed')
                                return False

    def ChangePassword(self, password):

        payload = {"password":password}

        with self.session.post("https://apiv3.fansly.com/api/v1/login/password/create?ngsw-bypass=true",
                               json=payload) as response:
            return response.json()['success']

    def ChangeUsername(self, password):

        while True:

            payload = {"username": GenerateNickname(), "password": password}

            with self.session.post("https://apiv3.fansly.com/api/v1/account/username?ngsw-bypass=true", json=payload) as response:

                if response.json()['success'] == True:
                    return response.json()

    def ChangeDisplayName(self, account_id , name):

        payload = {"accountId":str(account_id),
                   "categories":
                       [{"name":"account","inputs":
                           [{"type":1,"name":"displayName","data":f'{{"key":"displayName","value":"{name}"}}'}]}]
                   }


        with self.session.post("https://apiv3.fansly.com/api/v1/account/settings?ngsw-bypass=true", json=payload) as response:
            # print(response.text)
            return response.json()

    def ChangeProfile(self, about=None, banner_path=None, avatar_path=None):

        if avatar_path:
            result = self.UploadPhoto(avatar_path)
            avatar_mediaId = result["response"]["mediaId"]

        if banner_path:
            result = self.UploadPhoto(banner_path)
            banner_mediaId = result["response"]["mediaId"]

        payload = {"accountId":"","avatarId": "" if avatar_path == None else avatar_mediaId,"bannerId":"" if banner_path == None else banner_mediaId,"about":about if about != None else "Hey, I am using Fansly.","socials":[]}

        with self.session.post("https://apiv3.fansly.com/api/v1/profile?ngsw-bypass=true", json=payload) as response:
            print(response.json())
            return response.json()


    def Follow(self, account_id):

        with self.session.post(f"https://apiv3.fansly.com/api/v1/account/{account_id}/followers?ngsw-bypass=true") as response:
            return response.json()["success"]

    def Like(self, post_id):

        with self.session.post(f"https://apiv3.fansly.com/api/v1/likes?ngsw-bypass=true", json={"postId":str(post_id)}) as response:
            return response.json()["success"]

    def SendMessage(self, text, groupId, attachments=None, inReplyTo=None):

        '''
        attachments = [[{"messageId":None,"pos":0,"contentId":"570993112818659328","contentType":1}]]

        Ставим inReplyTo "547635743430811648" чтобы сделать коммент
        '''

        payload = {"type":1,
                   "attachments": attachments if attachments else [],
                   "likes":[],
                   "content":text,
                   "groupId":groupId,
                   "scheduledFor":0,
                   "inReplyTo":inReplyTo,
                   "createdAt":datetime.datetime.utcnow()}

        with self.session.post(f"https://apiv3.fansly.com/api/v1/message?ngsw-bypass=true", json=payload) as response:
            return response.json()["success"]

    def MakePost(self, text, inReplyTo=None, attachments=None):

        '''
        attachments = [[{"messageId":None,"pos":0,"contentId":"570993112818659328","contentType":1}]]

        Ставим inReplyTo "547635743430811648" чтобы сделать коммент
        '''

        payload = {"content":text,
                   "fypFlags":0,
                   "inReplyTo":inReplyTo,
                   "quotedPostId":None,
                   "attachments":attachments if attachments else [],
                   "scheduledFor":0,
                   "expiresAt":0,
                   "postReplyPermissionFlags":[],
                   "pinned":0,
                   "wallIds":[]}

        with self.session.post(f"https://apiv3.fansly.com/api/v1/post?ngsw-bypass=true", json=payload) as response:
            return response.json()["success"]

    def ConfirmMail(self, mail, password):

        code = check_mail(mail, password, "no-reply@fansly.com")
        print(code)

        input()

        with self.session.post("https://apiv3.fansly.com/api/v1/login/email/verification?ngsw-bypass=true", json={"token": str(code)}) as response:
            print(response.text)

    def ExportComments(self, postID):

        list_ = []
        with self.session.get(f"https://apiv3.fansly.com/api/v1/post/{postID}/replies?ngsw-bypass=true") as response:

            posts = response.json()['response']['posts']

            for post in posts:
                if len(post['content']) == 0 or len(post['content']) > 100:
                    continue
                else:
                    list_.append(post['content'])

            time.sleep(5)

        return list_


    def UploadPhoto(self, path):

        with open(path, 'rb') as image_file:

            size = os.stat(path).st_size
            payload = {"fileSize":size, "mimeType":"image/jpeg", "fileName":path.split("/")[-1]}
            # print(payload)

            with self.session.post("https://mediav2.fansly.com/api/v1/media/upload/create?ngsw-bypass=true", json=payload) as response:

#                 print(response.json())

                part_size = response.json()['response']['partSize']
                id = response.json()['response']['id']
                headers = {"ngsw-bypass": "true",
                           "Connection": "keep-alive",
                           "Referer": "https://fansly.com/",
                           "Origin": "https://fansly.com",
                           "content-type": None,
                           "Authorization": None,
                           "DNT": "1",
                           "Host": "fansly-upload.s3.eu-central-1.amazonaws.com",
                           "user-agent": self.ua,
                           'sec-ch-ua-platform': '"Windows"',
                           "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "en-US,en;q=0.9"}

                uploadUrl = response.json()['response']['parts'][0]['uploadUrl']

                with self.session.put(uploadUrl, data=image_file.read(), headers=headers, stream=True) as response:
#                     print(response.text)
#                     print(response.status_code)

                    eTag = response.headers['ETag'].replace('"', '')

                    # print('\\"{}\\"'.format(eTag))

                    self.session.headers.update({"content-type": "application/json",
                                                 "accept": "application/json, text/plain, */*",
                                                "accept-encoding": "gzip, deflate, br",
                                                "accept-language": "en-US,en;q=0.9",
                                                 "dnt": "1",
                                                 "origin": "https://fansly.com",
                                                "referer": "https://fansly.com/"})
                    # print(self.session.headers)


                    with self.session.post("https://mediav2.fansly.com/api/v1/media/upload/complete?ngsw-bypass=true", json={"id":id,"type":1,"partSize":part_size,"status":0,"parts":[{"index":0,"eTag":'"{}"'.format(eTag)}],"waitForComplete":0}) as response:
                        # print(response.text)
                        # print('')

                        while True:

                            self.session.headers.update({"content-type": None})

                            with self.session.get(f"https://mediav2.fansly.com/api/v1/media/upload/{id}?ngsw-bypass=true") as response:

                                # print(response.text)

                                if response.json()["response"]["mediaId"] == None:
                                    time.sleep(random.randint(1,5))

                                else:

                                    return response.json()

    def GetUserPosts(self, id):

        with self.session.get(f"https://apiv3.fansly.com/api/v1/timelinenew/{id}?before=0&after=0&wallId=&contentSearch=&ngsw-bypass=true") as response:
            return response.json()

    @property
    def MakeActivity(self):

        with self.session.post("https://apiv3.fansly.com/api/v1/status?ngsw-bypass=true", json={"statusId": 1}) as response:
            return None

    @property
    def GetRecomendationUsers(self, limit=8, offset=0):

        with self.session.get(f"https://apiv3.fansly.com/api/v1/contentdiscovery/suggestions?limit={limit}&offset={offset}&ngsw-bypass=true") as response:
            return response.json()


    @property
    def GetRecomendationPosts(self, before=0, after=0, mode=0):

        with self.session.get(f"https://apiv3.fansly.com/api/v1/timeline/home?before={before}&after={after}&mode={mode}&ngsw-bypass=true") as response:
            return response.json()

    @property
    def generate_user_agent(self) -> str:
        return ua_generator.generate(platform="windows").text

    @property
    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


if __name__ == '__main__':

    model = FanslyModel("", "", "")

    for i in []:
        res = model.ExportComments(i)
        for ii in res:
            print(ii)



