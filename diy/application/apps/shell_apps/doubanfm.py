import requests
import urllib2
import cookielib


class Doubanfm:
    def __init__(self):
        self.cookies = cookielib.MozillaCookieJar()
        try:
            self.cookies.load('./application/data/doubanfm.cookie')
        except Exception as e:
            print  e
        try:
            with open('./application/data/code.txt', "r") as fi:
                self.code = fi.read()
        except Exception as e:
            print e
        self.opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cookies),
                )
        urllib2.install_opener(self.opener)

    def get_list(self):
        url = 'http://douban.fm/mine?type=liked'
        content = urllib2.urlopen(url).read()
        return content


    def new_captcha(self):
        url = 'http://douban.fm/j/new_captcha'
        req = urllib2.Request(url)
        req.add_header('Referer', "http://douban.fm/")
        code = urllib2.urlopen(req).read()
        self.code = code
        with open('./application/data/code.txt', "w") as fi:
            fi.write(self.code)
        print code

    def getimg(self):
        url = 'http://douban.fm/misc/captcha?size=m&id=' + self.code.strip('"')
        req = urllib2.Request(url)
        req.add_header("Referer", "http://douban.fm/")
        with open('./application/static/verify_code.jpg', "w") as fi:
            fi.write(urllib2.urlopen(req).read())

    def login(self):
        url = 'http://douban.fm/j/login'
        data = {
                "source": "radio",
                "alias": self.username,
                "form_password": self.passwd,
                "captcha_solution": self.verify_code,
                "captcha_id":self.code.strip('"'),
                "remember":"on",
                "task": "sync_channel_list",
                }
        import urllib
        data = urllib.urlencode(data)
        self.result = urllib2.urlopen(url, data).read()
        self.cookies.save("./application/data/doubanfm.cookie")
        print self.result
    def logout(self):
        with open('./application/data/doubanfm.cookie', 'w') as fi:
            fi.write('')


if __name__ == "__main__":
    D = Doubanfm()
    D.username = "atupal@foxmail.com"
    D.passwd = "LKYs4690102"
    #D.new_captcha()
    #D.getimg()
    #verify_code = raw_input()
    #D.verify_code = verify_code
    #D.login()
    D.get_list()
