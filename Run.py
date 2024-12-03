try:
    import requests, json, time, os, sys
    from requests.exceptions import RequestException
    from rich.console import Console
    from rich import print as printf
    from faker import Faker
    from fake_useragent import UserAgent
    from rich.panel import Panel
    from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
except ModuleNotFoundError:
    import sys
    print("Error: Required modules not installed. Please install them and try again!")
    sys.exit()

SUKSES, GAGAL, LOOPING, ERROR = (
    0, 0, 0, 0
)

def TampilkanLogo() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(
        Panel(r"""[bold red]● [bold yellow]● [bold green]●
[bold red],--.   ,--.,--.                      ,--.         ,--.   
|  |   `--'|  |,-. ,---.  ,---.      |  | ,---. ,-'  '-. 
|  |   ,--.|     /| .-. :(  .-' ,--. |  || .-. :'-.  .-' 
[bold white]|  '--.|  ||  \  \\   --..-'  `)|  '-'  /\   --.  |  |   
`-----'`--'`--'`--'`----'`----'  `-----'  `----'  `--'   
            [bold white on red]Free Instagram Likes - by Rozhak""", style="bold bright_black", width=60)
    )

def MemasukanTautan() -> None:
    TampilkanLogo()
    printf(
        Panel(f"[bold white]Please fill in your Instagram post link, you can use \"[bold green],[bold white]\" to fill in multiple links.\n*[bold red]Make sure your Instagram account is not private[bold white]!", style="bold bright_black", width=60, title="[bold bright_black]> [Link Postingan] <", title_align="center", subtitle="[bold bright_black]╭───────", subtitle_align="left")
    )
    tautanPostingan = Console().input("[bold bright_black]   ╰─> ")
    printf(
        Panel(f"[bold white]We are processing likes, you can use[bold yellow] CTRL + Z[bold white] to stop. *[bold red]Make sure your connection is good to avoid errors[bold white]!", style="bold bright_black", width=60, title="[bold bright_black]> [Catatan] <", title_align="center")
    )
    if len(tautanPostingan) != 0:
        while True:
            try:
                for tautan in tautanPostingan.split(","):
                    if not tautan.startswith("https://www.instagram.com/"):
                        printf(f"[bold bright_black]   ──>[bold red] Wrong post link found, skipping!     ", end="\r")
                        time.sleep(5.0)
                        continue
                    tautanAkhir = tautan
                    if not tautan.startswith("https://www.instagram.com/p/"):
                        tautanAkhir = tautan.replace("/reel/", "/p/").replace("/tv/", "/p/").replace("/reels/", "/p/")
                    KirimkanSuka(tautanPostingan=tautanAkhir)
                if LOOPING != 0:
                    with Progress(TextColumn("[bold green]{task.description}"), BarColumn(bar_width=10), TextColumn("[bold white]Response:[bold blue] {task.fields[sukses]}[bold white]/[bold red]{task.fields[gagal]}[bold white]/[bold yellow]{task.fields[looping]}[bold white]/[bold magenta]{task.fields[error]}"), TimeElapsedColumn(), TimeRemainingColumn()) as progress:
                        tugas = progress.add_task("[bold green] Loading...", total=24*60*60, sukses=SUKSES, gagal=GAGAL, looping=LOOPING, error=ERROR)
                        while not progress.finished:
                            time.sleep(1)
                            progress.update(tugas, advance=1, sukses=SUKSES, gagal=GAGAL, looping=LOOPING, error=ERROR)
                        print(f"[bold bright_black]   ──>[bold green] Resend likes...                ", end="\r")
                        time.sleep(5.0)
                    continue
                else:
                    printf(f"[bold bright_black]   ──>[bold red] No likes were sent successfully!", end="\r")
                    time.sleep(5.0)
                    break
            except KeyboardInterrupt:
                printf(f"                                                 ", end="\r")
                time.sleep(1.5)
                break
        printf(f"                                                 ", end="\r")
        if SUKSES == 0 and GAGAL >= 0 or ERROR >= 0:
            printf(
                Panel(f"[bold red]Sorry, no likes were sent successfully, this is caused by a wrong link or the service is down!", style="bold bright_black", width=60, title="[bold bright_black]> [Gagal] <", title_align="center")
            )
            sys.exit()
        else:
            Console().input("[bold white][[bold green]Selesai[bold white]]")
            sys.exit()
    else:
        printf(
            Panel(f"[bold red]The post link you entered is incorrect, please try again by entering the Instagram post link correctly!", style="bold bright_black", width=60, title="[bold bright_black]> [Link Salah] <", title_align="center")
        )
        sys.exit()

def ParameterPalsu(tautanPostingan: str) -> dict:
    fake = Faker()
    return {
        "instagram_username": fake.user_name(),
        "link": f"{tautanPostingan}",
        "email": fake.email(domain='gmail.com')
    }

def KirimkanSuka(tautanPostingan: str) -> bool:
    try:
        global SUKSES, GAGAL, LOOPING, ERROR
        with requests.Session() as session:
            session.headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'likesjet.com',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Connection': 'keep-alive',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'User-Agent': '{}'.format(UserAgent().random),
            }
            response = session.get('https://likesjet.com/free-instagram-likes', allow_redirects=True, verify=True)

            data = json.dumps(
                ParameterPalsu(tautanPostingan)
            )

            session.headers.update(
                {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json',
                    'Origin': 'https://likesjet.com',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Host': 'api.likesjet.com',
                    'Content-Length': '{}'.format(len(str(data))),
                    'Sec-Fetch-Site': 'same-site',
                    'Referer': 'https://likesjet.com/',
                }
            )

            response2 = session.post('https://api.likesjet.com/freeboost/7', data=data, verify=True, allow_redirects=False)
            LOOPING += 1
            if 'You can only receive likes once per day.' in response2.text:
                printf(f"[bold bright_black]   ──>[bold red] You can only receive likes once a day!         ", end="\r")
                time.sleep(5.0)
                GAGAL += 1
                return False
            elif 'Success! You will receive likes within next few minutes.' in response2.text:
                printf(f"[bold bright_black]   ──>[bold green] You will receive likes in the next few minutes!", end="\r")
                time.sleep(5.0)
                printf(
                    Panel(f"""[bold white]Status:[bold green] Successfully sent likes!
[bold white]Link : [bold red]{tautanPostingan}
[bold white]Likes Sent: [bold green]+50""", style="bold bright_black", width=60, title="[bold bright_black]> [Sukses] <", title_align="center")
                )
                SUKSES += 1
                return True
            else:
                printf(f"[bold bright_black]   ──>[bold red] Failed to send like, please try again later!   ", end="\r")
                time.sleep(5.0)
                ERROR += 1
                return False
    except RequestException:
        printf(f"[bold bright_black]   ──>[bold red] Your internet connection is having problems!   ", end="\r")
        time.sleep(10.0)
        KirimkanSuka(tautanPostingan)

if __name__ == '__main__':
    try:
        if not os.path.exists("Penyimpanan/Subscribe.json"):
            youtubeLink = requests.get('https://raw.githubusercontent.com/RozhakXD/LikesJet/refs/heads/main/Penyimpanan/Youtube.json').json()['Link']
            os.system(f'xdg-open {youtubeLink}')
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                json.dump({"Status": True}, w, indent=4)
            time.sleep(2.5)
        MemasukanTautan()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        printf(
            Panel(f"[bold red]{str(e).capitalize()}!", style="bold bright_black", width=60, title="[bold bright_black]> [Error] <", title_align="center")
        )
        sys.exit()