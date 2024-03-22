import requests
from bs4 import BeautifulSoup
import webbrowser

maxLevel = 9
apiKey = "STEAM_API_KEY"
group_id = "STEAM_ID"
openPage = True

def obtener_nivel_usuario(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={apiKey}&steamid={steam_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            level = response.json()["response"]["player_level"]
            return level
        except KeyError:
            print(f"No se pudo obtener el nivel para el usuario con SteamID {steam_id}")
            return None
    else:
        print(f"Error al obtener el nivel para el usuario con SteamID {steam_id}")
        return None

def verificar_baneos(steam_id):
    url = f"https://steamcommunity.com/profiles/{steam_id}/?xml=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        vac_banned = soup.find("vacBanned").text
        trade_ban_state = soup.find("tradeBanState").text
        is_limited_account = soup.find("isLimitedAccount").text
        
        if vac_banned == "0" and trade_ban_state == "None" and is_limited_account == "0":
            return True
        else:
            return False
    else:
        print(f"Error al obtener información del perfil para el usuario con SteamID {steam_id}")
        return False

def abrir_en_navegador(url):
    webbrowser.open_new_tab(url)

def buscar_usuarios_grupo():
    url = f"https://steamcommunity.com/groups/{group_id}/memberslistxml/?xml=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        members = response.text.split("<steamID64>")[1:]

        for member in members:
            steam_id = member.split("</steamID64>")[0]
            level = obtener_nivel_usuario(steam_id)
            if level is not None and level <= maxLevel:
                if verificar_baneos(steam_id):
                    perfil_url = f"https://steamcommunity.com/profiles/{steam_id}"
                    print(f"Steam: {perfil_url}, Nivel: {level}")
                    if openPage:
                        abrir_en_navegador(perfil_url)
                    
    else:
        print("Error al obtener la página del grupo")

if __name__ == "__main__":
    print("Usuarios con nivel menor a ", maxLevel ," en el grupo:")
    buscar_usuarios_grupo()
