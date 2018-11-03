# -*- coding: latin-1 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

bib="386030"
pesquisa="populista"
url = "http://memoria.bn.br/docreader/DocReader.aspx?bib=" + bib + "&Pesq=" + pesquisa

out = open("memoria.bn.br_" + bib + "_" + pesquisa + ".csv", 'w')
out.write("Ano,Edição,link\n")

chrome_options = Options()  
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(url)

cur, tot = driver.find_element_by_id("OcorNroLbl").text.strip().split("/")

for i in range(1,int(tot)+1):
    pag = driver.find_element_by_id("hPagFis").get_attribute("value")
    ano, edi = driver.find_element_by_id("PastaTxt").get_attribute("title").strip().split("\\")
    link = "http://memoria.bn.br/docreader/" + bib + "/" + pag

    out.write(ano.encode('utf-8')[4:] + "," + edi.encode('utf-8')[9:] + "," + link.encode('utf-8') + "\n")

    print "[" + str(i) + "/" + tot + "] - " + ano.encode('utf-8')[4:] + "\\" + edi.encode('utf-8')[9:] + " - " + link.encode('utf-8')
    print

    if (i!=int(tot)):
        next_pg = driver.find_element_by_id("OcorPosBtn")
        ActionChains(driver).move_to_element(next_pg).click(next_pg).perform()
        WebDriverWait(driver, 30).until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, 'OcorNroLbl'), str(i+1)+'/'+tot)
        )

out.close()
driver.quit()
