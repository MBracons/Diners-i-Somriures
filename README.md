# README

Aquest projecte mostra un estudi de la felicitats i els factors que més hi influeixen, com ara el PIB per càpita o el nivell de corrupció percebut, a més d’altres factors. El codi adjunt permet fa servir [Streamlit](https://streamlit.io/) i està estructurat de la següent forma:

1. **Carregar i filtrar** les dades (anys 2010 - 2021).  
2. **Visualitzar** un mapa mundial amb l’índex de felicitat per a l’any seleccionat.  
3. **Analitzar correlacions** de les diverses variables amb la felicitat.  
4. **Generar** gràfics de dispersió per explorar en detall la relació entre variables específiques i el nivell de felicitat.  
5. **Comparar** diversos països al llarg del temps.

---

## Propietari

Aquesta és la entrega de la segona pràctica, de Marc Bracons Cucó, per l'assignatura de Visualització de Dades, del Màster de Ciència de Dades de la UOC, del curs 2024/2025. La visualització es pot veure a https://diners-i-somriures-uoc-braconsm.streamlit.app/

---

## Arxius principals

- **`Money_vs_Happiness_dataset_corrected.csv`**: Conjunt de dades que conté, per país i any, les següents columnes rellevants:  
  - `Country`  
  - `Year`  
  - `Life Ladder` (índex de felicitat)  
  - i altres variables (p. ex. `Log GDP per capita`, `Human Development Index`, etc.)

- **`mapa/ne_110m_admin_0_countries.shp`**: Fitxer *shapefile* amb la informació geogràfica de tots els països del món. És necessari per poder pintar el mapa amb GeoPandas.

- **`main.py`**: El codi on es defineix tota la lògica de l’aplicació Streamlit i els diferents apartats (selecció de l’any, càlcul de correlacions, gràfics, etc.).

---

## Com executar l'aplicació

1. **Clona** aquest repositori o descarrega’t els arxius al teu ordinador.  
2. **Instal·la** els requisits:
   ```bash
   pip install -r requirements.txt
   ```
3. **Executa** l'apliació Streamlit:
   ```bash
   streamlit run main.py
   ```
4. **Obre** el navegador a l'adreça que aparegui al terminal (normalment http://localhost:8501)
