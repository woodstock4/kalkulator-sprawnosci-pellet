# Kalkulator sprawności kotła na pellet (O₂ / strata kominowa)

Interaktywny kalkulator HTML oraz skrypt w Pythonie do oceny wpływu zawartości tlenu ($\text{O}_2$) w spalinach na **stratę kominową ($q_A$)** i **sprawność spalania** kotła pelletowego.

Projekt powstał do szybkiego porównania pracy kotła przed i po regulacji nadmiaru powietrza (np. przejście z przewietrzonego palnika przy $18\%\ \text{O}_2$ do $11\%\ \text{O}_2$ lub docelowych $7\text{–}9\%\ \text{O}_2$).

---

## Zawartość repozytorium

| Plik | Opis |
|---|---|
| `index.html` | Samowystarczalny kalkulator w przeglądarce (HTML + CSS + JS w jednym pliku, zero zewnętrznych zależności). Gotowy pod **GitHub Pages**. |
| `obliczenia_sprawnosci.py` | Skrypt w Pythonie 3 liczący sprawność dwiema niezależnymi metodami: wzorem Siegerta oraz pełnym stechiometrycznym bilansem cieplnym spalin dla pelletu. |
| `LICENSE` | Licencja MIT. |

---

## Szybki start

### 1. Kalkulator w przeglądarce (`index.html`)
Wystarczy otworzyć plik `index.html` dwuklikiem w dowolnej przeglądarce (działa też offline na telefonie i komputerze).

**Publikacja na GitHub Pages:**
1. Wrzuć pliki z tej paczki do nowego repozytorium na GitHubie.
2. Wejdź w **Settings → Pages**.
3. W sekcji **Build and deployment** wybierz **Deploy from a branch**, gałąź `main` (folder `/ (root)`) i kliknij **Save**.
4. Po kilkudziesięciu sekundach kalkulator będzie dostępny pod adresem `https://<twoj-login>.github.io/<nazwa-repo>/`.

### 2. Skrypt w Pythonie (`obliczenia_sprawnosci.py`)
Skrypt nie wymaga żadnych dodatkowych bibliotek (korzysta wyłącznie ze standardowej biblioteki Pythona 3).

Uruchomienie domyślnego zestawienia tabelarycznego:
```bash
python3 obliczenia_sprawnosci.py
```

Porównanie własnych pomiarów z linii poleceń:
```bash
python3 obliczenia_sprawnosci.py --o2-przed 18 --tg-przed 180 --o2-po 11 --tg-po 180 --ta 20
```

---

## Metodyka obliczeń

### 1. Współczynnik nadmiaru powietrza ($\lambda$)
$$\lambda = \frac{21}{21 - \text{O}_2}$$

* $\text{O}_2 = 18\% \implies \lambda = 7{,}00$ (600% nadmiaru powietrza — bardzo duże przewietrzenie / nieszczelność)
* $\text{O}_2 = 11\% \implies \lambda = 2{,}10$ (110% nadmiaru powietrza)
* $\text{O}_2 = 8\% \implies \lambda = 1{,}62$ (typowy zakres optymalny dla palnika pelletowego przy mocy nominalnej: $7\text{–}9\%\ \text{O}_2$)

### 2. Strata kominowa — wzór Siegerta
Wariant tlenowy stosowany w obliczeniach inżynierskich:
$$q_A = (t_{\text{spalin}} - t_{\text{otoczenia}}) \cdot \left(\frac{A_1}{21 - \text{O}_2} + B\right) \quad [\%]$$

Dla drewna suszonego / pelletu drzewnego:
* $A_1 \approx 0{,}65\text{–}0{,}68$, $B \approx 0$ (w kalkulatorze dostępny wybór współczynników oraz wpisanie własnych).
* Sprawność spalania (netto): $\eta_{\text{spalania}} = 100\% - q_A$.

### 3. Stechiometryczny bilans cieplny (weryfikacja w `obliczenia_sprawnosci.py`)
Model referencyjny dla $1\ \text{kg}$ pelletu ($W_u = 17{,}0\ \text{MJ/kg}$, wilgotność $8\%$, popiół $0{,}5\%$):
* Zapotrzebowanie stechiometryczne powietrza: $4{,}19\ \text{nm}^3/\text{kg}$ ($5{,}42\ \text{kg/kg}$).
* Objętość spalin suchych rośnie z $8{,}78\ \text{nm}^3/\text{kg}$ (przy $11\%\ \text{O}_2$) do $29{,}31\ \text{nm}^3/\text{kg}$ (przy $18\%\ \text{O}_2$).

---

## Przykładowe wyniki ($t_{\text{otoczenia}} = 20\ ^\circ\text{C}$, $A_1 = 0{,}65$, $B = 0$)

| $\text{O}_2$ w spalinach | $\lambda$ | $t_{\text{sp}} = 120\ ^\circ\text{C}$ | $t_{\text{sp}} = 150\ ^\circ\text{C}$ | $t_{\text{sp}} = 180\ ^\circ\text{C}$ | $t_{\text{sp}} = 210\ ^\circ\text{C}$ |
|---:|---:|---:|---:|---:|---:|
| **18,0 %** | 7,00 | 78,3 % | 71,8 % | **65,3 %** | 58,8 % |
| **11,0 %** | 2,10 | 93,5 % | 91,5 % | **89,6 %** | 87,7 % |
| **9,0 %** | 1,75 | 94,6 % | 93,0 % | **91,3 %** | 89,7 % |
| **6,0 %** | 1,40 | 95,7 % | 94,4 % | **93,1 %** | 91,8 % |

---

## Ważne uwagi praktyczne

1. **Sprawność spalania vs sprawność całkowita kotła:** metoda straty kominowej uwzględnia ciepło unoszone ze spalinami. Całkowita sprawność kotła jest o ok. $3\text{–}5\ \text{p.p.}$ niższa (straty promieniowania/konwekcji do kotłowni, niedopał w popiele, strata niezupełnego spalania $\text{CO}$).
2. **Temperatura spalin zmienia się wraz z nadmiarem powietrza:** zmniejszenie strumienia powietrza często powoduje wzrost temperatury spalin — dlatego w kalkulatorze warto wpisać rzeczywistą temperaturę zmierzoną przed i po regulacji.
3. **Kontrola $\text{CO}$:** obniżając $\text{O}_2$ poniżej $8\text{–}9\%$, należy kontrolować stężenie tlenku węgla ($\text{CO}$), aby nie wejść w zakres niedoboru tlenu i smolenia wymiennika.
4. **Warunki pomiaru:** porównania wykonuj przy tej samej mocy palnika (w stanie ustabilizowanym) i przy szczelnym króćcu pomiarowym.
