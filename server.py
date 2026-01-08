import os
import requests, threading, random, time, secrets, uuid, json
from urllib.parse import urlencode, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, BaseHTTPRequestHandler
import SignerPy

# ================= TikTok API =================
class TikTokAPI:
    HOSTS = [
        "api16-normal-c-alisg.tiktokv.com","api.tiktokv.com","api-h2.tiktokv.com",
        "api-va.tiktokv.com","api16.tiktokv.com","api16-va.tiktokv.com",
        "api19.tiktokv.com","api19-va.tiktokv.com","api21.tiktokv.com",
        "api15-h2.tiktokv.com","api21-h2.tiktokv.com","api21-va.tiktokv.com",
        "api22.tiktokv.com","api22-va.tiktokv.com","api-t.tiktok.com",
        "api16-normal-baseline.tiktokv.com","api23-normal-zr.tiktokv.com",
        "api21-normal.tiktokv.com","api22-normal-zr.tiktokv.com",
        "api33-normal.tiktokv.com","api22-normal.tiktokv.com",
        "api31-normal.tiktokv.com","api15-normal.tiktokv.com",
        "api31-normal-cost-sg.tiktokv.com","api3-normal.tiktokv.com",
        "api31-normal-zr.tiktokv.com","api9-normal.tiktokv.com",
        "api16-normal.tiktokv.com","api16-normal.ttapis.com",
        "api19-normal-zr.tiktokv.com","api16-normal-zr.tiktokv.com",
        "api16-normal-apix.tiktokv.com","api74-normal.tiktokv.com",
        "api32-normal-zr.tiktokv.com","api23-normal.tiktokv.com",
        "api32-normal.tiktokv.com","api16-normal-quic.tiktokv.com",
        "api-normal.tiktokv.com","api16-normal-apix-quic.tiktokv.com",
        "api19-normal.tiktokv.com","api31-normal-cost-mys.tiktokv.com",
        "im-va.tiktokv.com","imapi-16.tiktokv.com","imapi-16.musical.ly",
        "imapi-mu.isnssdk.com","api.tiktok.com","api.ttapis.com",
        "api.tiktokv.us","api.tiktokv.eu","api.tiktokw.us","api.tiktokw.eu"
    ]

    @staticmethod
    def send_single_request(host, username, attempt_num=1):
        try:
            secret = secrets.token_hex(16)
            cookies = {"passport_csrf_token": secret, "passport_csrf_token_default": secret}

            params_step1 = {
                'request_tag_from': "h5",'manifest_version_code': "410203",
                '_rticket': str(int(time.time() * 1000)),'app_language': "ar",
                'app_type': "normal",'iid': str(random.randint(1, 10**19)),
                'app_package': "com.zhiliaoapp.musically.go",'channel': "googleplay",
                'device_type': "RMX3834",'language': "ar",'host_abi': "arm64-v8a",
                'locale': "ar",'resolution': "720*1454",'openudid': "b57299cf6a5bb211",
                'update_version_code': "410203",'ac2': "lte",'cdid': str(uuid.uuid4()),
                'sys_region': "EG",'os_api': "34",'timezone_name': "Asia/Baghdad",
                'dpi': "272",'carrier_region': "IQ",'ac': "4g",
                'device_id': str(random.randint(1, 10**19)),'os': "android",
                'os_version': "14",'timezone_offset': "10800",'version_code': "410203",
                'app_name': "musically_go",'ab_version': "41.2.3",'version_name': "41.2.3",
                'device_brand': "realme",'op_region': "IQ",'ssmix': "a",
                'device_platform': "android",'build_number': "41.2.3",'region': "EG",
                'aid': "1340",'ts': str(int(time.time())),'okhttp_version': "4.1.103.107-ul",
                'use_store_region_cookie': "1"
            }

            url_step1 = f"https://{host}/passport/find_account/tiktok_username/?" + urlencode(params_step1)
            payload_step1 = {'mix_mode': "1", 'username': username}
            signature = SignerPy.sign(params=url_step1, payload=payload_step1, version=4404)

            headers_step1 = {
                'User-Agent': "com.zhiliaoapp.musically.go/410203 (Linux; U; Android 14; ar; RMX3834; Build/UP1A.231005.007;tt-ok/3.12.13.44.lite-ul)",
                'x-ss-req-ticket': signature['x-ss-req-ticket'],
                'x-ss-stub': signature['x-ss-stub'],
                'x-gorgon': signature["x-gorgon"],
                'x-khronos': signature["x-khronos"],
                'x-tt-passport-csrf-token': cookies['passport_csrf_token'],
                'passport_csrf_token': cookies['passport_csrf_token'],
                'content-type': "application/x-www-form-urlencoded",
                'x-ss-dp': "1340",'sdk-version': "2",'x-tt-ultra-lite': "1",
                'x-vc-bdturing-sdk-version': "2.3.15.i18n",'ttzip-tlb': "1",
            }

            response_step1 = requests.post(url_step1, data=payload_step1, headers=headers_step1, cookies=cookies, timeout=15)
            response_json_step1 = response_step1.json()

            if "token" in response_json_step1.get("data", {}):
                token = response_json_step1["data"]["token"]
                params_step2 = params_step1.copy()
                params_step2['not_login_ticket'] = token
                params_step2['ts'] = str(int(time.time()))
                params_step2['_rticket'] = str(int(time.time() * 1000))

                url_step2 = f"https://{host}/passport/auth/available_ways/?" + urlencode(params_step2)
                signature_step2 = SignerPy.sign(params=url_step2, payload=None, version=4404)

                headers_step2 = {
                    'User-Agent': headers_step1['User-Agent'],
                    'x-ss-req-ticket': signature_step2['x-ss-req-ticket'],
                    'x-ss-stub': signature_step2['x-ss-stub'],
                    'x-gorgon': signature_step2["x-gorgon"],
                    'x-khronos': signature_step2["x-khronos"],
                    'x-tt-passport-csrf-token': cookies['passport_csrf_token'],
                    'passport_csrf_token': cookies['passport_csrf_token'],
                    'content-type': "application/x-www-form-urlencoded",
                    'x-ss-dp': "1340",'sdk-version': "2",'x-tt-ultra-lite': "1",
                }

                res_step2 = requests.post(url_step2, headers=headers_step2, cookies=cookies, timeout=15)
                response_json_step2 = res_step2.json()

                if 'success' in response_json_step2.get("message", ""):
                    data = response_json_step2.get('data', {})
                    return {
                        'data': {
                            'has_email': data.get('has_email', False),
                            'has_mobile': data.get('has_mobile', False),
                            'has_oauth': data.get('has_oauth', False),
                            'has_passkey': data.get('has_passkey', False),
                            'oauth_platforms': data.get('oauth_platforms', [])
                        },
                        'message': 'success'
                    }
            elif "verify_center_decision_conf" in response_step1.text:
                return {"message": "error", "status": "captcha"}
            else:
                return {"message": "error", "status": "user not found"}

        except:
            return {"message": "error", "status": "request_failed"}
        return {"message": "error", "status": "unknown"}

    @staticmethod
    def send_with_threading(username, max_workers=15):
        successful_responses = []

        def worker(host):
            result = TikTokAPI.send_single_request(host, username, 1)
            if result.get('message') == 'success':
                successful_responses.append(result)
            return result

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(worker, host): host for host in TikTokAPI.HOSTS}
            for future in as_completed(futures):
                if successful_responses:
                    break

        return successful_responses[0] if successful_responses else {"message": "error", "status": "failed"}

# ================= HTTP SERVER =================
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/check", methods=["GET", "POST"])
def check_user():
    username = ""
    if request.method == "GET":
        username = request.args.get("username", "").strip().lstrip("@")
    elif request.method == "POST":
        data = request.get_json() or {}
        username = data.get("username", "").strip().lstrip("@")

    if not username:
        return jsonify({"error": "username_required"}), 400

    res = TikTokAPI.send_with_threading(username)
    return jsonify({"username": username, "status": res.get("message"), "data": res.get("data", {})})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
