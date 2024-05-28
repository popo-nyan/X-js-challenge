import re
import pythonmonkey

from urllib import request


def main():
    req = request.Request("https://twitter.com/i/js_inst?native=true&native_js=true",
                          headers={'Host': 'twitter.com',
                                   'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Android SDK built for x86 Build/RSR1.210210.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 TwitterAndroid/10.12.0-release.0 (310120000-r-0) Android+SDK+built+for+x86/11 (unknown;Android+SDK+built+for+x86;Android;sdk_phone_x86;0;;1;2015)',
                                   'X-Requested-With': 'com.twitter.android'},
                          method="GET")
    with request.urlopen(req) as response:
        response_body = response.read()

    # 参考 https://github.com/tsukumijima/tweepy-authlib/blob/de0cd2bb522601ad5ff2d51c7c697215943b180b/tweepy_authlib/CookieSessionUserHandler.py#L421-L500
    mock = """
    let _element = {
        appendChild: function (tag) {
        },
        removeChild: function (tag) {
        },
        setAttribute: function (tag, value) {
        },
    };
    _element.children = [_element];
    _element.lastElementChild = _element;
    _element.parentNode = _element;
    document = {
        createElement: function (tag) {
            return _element;
        },
        getElementsByTagName: function (tag) {
            return [_element];
        }
    };
    """

    js_inst = response_body.decode().split("\n")[1]
    js_inst_function_name = re.search(r"function [a-zA-Z]+", js_inst).group(0).replace("function ", "")
    js_inst = js_inst.replace(f"{js_inst_function_name}();", "").replace(f"function {js_inst_function_name}()", "() =>")
    js_challenge = mock + "\n" + js_inst
    js_challenge_function = pythonmonkey.eval(js_challenge)
    print(js_challenge_function())


if __name__ == "__main__":
    main()
