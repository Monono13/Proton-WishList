import pytest
import allure
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time as tm

@allure.title("Test Proton Wishlist")
@allure.description("Test de prueba para busqueda de Wishlist de juegos de Steam y verificar el estado de Proton de estos")
@pytest.fixture
def driver():
    driver = wd.Chrome()
    yield driver
    driver.quit()

def test_proton_wishlist(driver):
    gameList = []
    time10 = 10
    time20 = 20 
    driver.get("https://store.steampowered.com/wishlist/profiles/76561198287388908/#sort=order")
    print("Abriendo Wishlist \n")

    try: 

        viewcompact = WebDriverWait(driver, time20).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "filter_tab"))
        )
        viewcompact.click()

        modecompact = WebDriverWait(driver, time20).until(
            ec.visibility_of_element_located((By.ID, "viewmode_compact"))
        )
        modecompact.click()

        games = WebDriverWait(driver, time20).until(
                ec.visibility_of_all_elements_located((By.XPATH, "//a[contains(@class, 'title')]"))
            )
        for game in games:
            gameTitle = game.text
            gameList.append(gameTitle.replace("™", ""))
            print(f"{gameTitle} Agregado a la lista")

        print("Lista creada \n")
        print(gameList)

    except:
        print("Error encontrado al crear lista")

    driver.get("https://www.protondb.com/explore")
    print("Abriendo buscador protondb \n")

    try: 
        gameInput = WebDriverWait(driver, time10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "sc-gUMnWI"))
        )
        file = open("test_GameStatus.txt", "w")
        for i in range(len(gameList)):
            print(f"Buscando: {gameList[i]}")
            gameInput.send_keys(Keys.CONTROL + "a")
            gameInput.send_keys(Keys.DELETE)
            gameInput.send_keys(gameList[i])
            gameInput.send_keys(Keys.RETURN)
            while True:
                gameName = WebDriverWait(driver, time10).until(
                    ec.visibility_of_element_located((By.CLASS_NAME, "GameSliceLegacy__Headline-sc-1ka41zm-1"))
                ).text
                if gameName == gameList[i]:
                    print(f"{gameName} Encontrado en protondb")
                    try:
                        gameStatus = WebDriverWait(driver, time20).until(
                            ec.presence_of_element_located((By.CLASS_NAME, "MedalSummary__ExpandingSpan-sc-1fjwtnh-1"))
                        )
                        status = gameStatus.text
                    except TimeoutException:
                        status = "Unverifed"
                    print(f"Estado: {status} \n")
                    file.write(f'Name: {gameName} | Status: {status} \n')
                    break
                else:
                    continue    
    except:
        print("Error buscando juegos en protondb")

    print("Finalizando...")