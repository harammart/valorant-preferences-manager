import base64

import requests

import structs
import constants

class ValorantAPI:
    @staticmethod
    def get_version():
        resp = requests.get("https://valorant-api.com/v1/version")
        return resp.json()

class ValorantInternal:
    def __init__(self):
        lockfile_data = open(constants.lock_file_path, "r").read().split(":")

        self.auth = f"riot:{lockfile_data[3]}"
        self.url = f"https://127.0.0.1:{lockfile_data[2]}"
        self.internal_headers = {
            "Authorization": f"Basic {base64.b64encode(self.auth.encode()).decode()}"
        }
        self.headers = {
            "Authorization": f"Bearer {self.get_token().accessToken}",
            "X-Riot-Entitlements-JWT": self.get_token().token,
            "X-Riot-ClientVersion": ValorantAPI.get_version()["data"]["riotClientVersion"],
            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        }

    def get_token(self) -> structs.EntitlementsTokenResponse:
        resp = requests.get(f"{self.url}/entitlements/v1/token", headers=self.internal_headers, verify=False)

        if resp.status_code != 200:
            raise RuntimeError(resp.status_code)
        return structs.EntitlementsTokenResponse(**resp.json())

    def get_preferences(self) -> dict:
        resp = requests.get(f"https://player-preferences-usw2.pp.sgp.pvp.net/playerPref/v3/getPreference/Ares.PlayerSettings", headers=self.headers, verify=False)

        if resp.status_code != 200:
            print(self.headers)
            print(resp.text)
            raise RuntimeError(resp.status_code)
        return resp.json()

    def set_preferences(self, preferences: dict) -> int:
        resp = requests.put("https://player-preferences-usw2.pp.sgp.pvp.net/playerPref/v3/savePreference", headers=self.headers, json=preferences, verify=False)

        if resp.status_code != 200:
            raise RuntimeError(resp.status_code)
        return resp.status_code