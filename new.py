import random, os, requests, json, time

TOKEN = "Nzk4MzQyNjExMjUzMDY3ODE3.YEAUtA.xLLSDaTRYdpJvXkNcu2Sspbhe54"
DELAY = 4

STATUS = [
    ".gg/feds | I be strapped like a gay bitch",
    ".gg/feds | Please dont confuse me for a lame nigga",
    ".gg/feds | What you fuck niggas saying",
    ".gg/feds | Dont let a bitch be the reason you lose ur life",
    ".gg/feds | Young nigga wit a draco, cuz a bitch on the pole",
    ".gg/feds | Whole lotta sticks in the house, its a gun show"
]

def change_status(status):
    status_data = json.dumps(
            {
                "custom_status":
                {
                    "text": status
                }
            }
        )
    return requests.patch("https://discordapp.com/api/v6/users/@me/settings", headers={"Authorization": TOKEN, "Content-Type": "application/json"}, data=status_data)

def main():
    print("[+] Changing discord status.")
    while True:
        for stat in STATUS:
            change_status(stat)
            time.sleep(DELAY)



if __name__ == "__main__":
    main()
    