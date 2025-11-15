# 🌍 Zaawansowany Symulator Gospodarczy

Kompleksowy symulator ekonomiczny łączący klasyczne teorie ekonomiczne (Keynes, Solow) z nowoczesnymi czynnikami wpływającymi na gospodarkę (AI, automatyzacja, globalizacja).

## 📋 Spis treści

- [Opis](#opis)
- [Funkcjonalności](#funkcjonalności)
- [Modele Ekonomiczne](#modele-ekonomiczne)
- [Instalacja i Uruchomienie](#instalacja-i-uruchomienie)
- [Użycie](#użycie)
- [Scenariusze](#scenariusze)
- [Parametry](#parametry)

## 📖 Opis

Symulator pozwala na analizę wpływu różnych polityk ekonomicznych (monetarnej, fiskalnej, handlowej) na kluczowe wskaźniki makroekonomiczne:

- **PKB** - Produkt Krajowy Brutto
- **Stopa bezrobocia**
- **Inflacja**
- **Kapitał**
- **Poziom technologii**
- **Zaufanie konsumentów**

## ✨ Funkcjonalności

### 🎯 Wersja Python (Tkinter)

- Interaktywny interfejs z suwakami do kontroli polityki
- 6 wykresów w czasie rzeczywistym
- Symulacje: 1 rok, 5 lat, 10 lat (prognoza)
- 6 scenariuszy ekonomicznych
- Eksport danych do analizy

### 🌐 Wersja Webowa (HTML/CSS/JavaScript)

- Responsywny design działający w przeglądarce
- Nowoczesny interfejs z gradientami i animacjami
- Wykresy Chart.js
- Wszystkie funkcje wersji desktopowej
- Brak wymagań instalacyjnych (oprócz przeglądarki)

## 📊 Modele Ekonomiczne

### 1. Model Solowa (Wzrost Długookresowy)

**Funkcja produkcji Cobba-Douglasa:**

```
Y = A × K^α × L^(1-α)
```

Gdzie:
- Y = PKB
- A = Poziom technologii
- K = Kapitał
- L = Siła robocza
- α = 0.35 (udział kapitału w produkcji)

**Akumulacja kapitału:**

```
ΔK = I - δK
```

Gdzie:
- I = Inwestycje
- δ = Stopa deprecjacji (5%)

### 2. Model Keynesa (Popyt Agregowany)

**Równanie PKB:**

```
Y = C + I + G + NX
```

Gdzie:
- C = Konsumpcja (zależna od dochodu rozporządzalnego i zaufania)
- I = Inwestycje (zależne od stopy procentowej)
- G = Wydatki rządowe
- NX = Eksport netto (zależny od ceł)

**Mnożnik keynesowski:**

```
k = 1 / (1 - MPC)
```

Gdzie MPC = 0.75 (krańcowa skłonność do konsumpcji)

### 3. Krzywa Phillipsa (Inflacja-Bezrobocie)

```
π = π_e + β(u_n - u)
```

Gdzie:
- π = Inflacja
- π_e = Oczekiwana inflacja
- u = Stopa bezrobocia
- u_n = NAIRU (5%) - naturalna stopa bezrobocia
- β = 0.5 (nachylenie krzywej)

### 4. Prawo Okuna (PKB-Bezrobocie)

```
Δu = -β(g - g*)
```

Gdzie:
- Δu = Zmiana bezrobocia
- g = Wzrost PKB
- g* = Potencjalny wzrost (2.5%)
- β = 0.4 (współczynnik Okuna)

### 5. Reguła Taylora (Polityka Monetarna)

```
i = r* + π + 0.5(π - π*) + 0.5(y - y*)
```

Gdzie:
- i = Nominalna stopa procentowa
- r* = Naturalna stopa (2%)
- π = Inflacja
- π* = Cel inflacyjny (2%)
- y - y* = Luka popytowa

## 🚀 Instalacja i Uruchomienie

### Wersja Python (Tkinter)

**Wymagania:**
```bash
pip install tkinter matplotlib numpy
```

**Uruchomienie:**
```bash
python economy_simulator.py
```

### Wersja Webowa

**Nie wymaga instalacji!** Po prostu otwórz plik `index.html` w przeglądarce:

```bash
# Linux/Mac
open index.html

# Windows
start index.html

# Lub kliknij dwukrotnie na plik index.html
```

Możesz również uruchomić lokalny serwer:

```bash
# Python 3
python -m http.server 8000

# Następnie otwórz http://localhost:8000
```

## 🎮 Użycie

### 1. Wybierz parametry polityki

Użyj suwaków aby dostosować:

- **Stopa procentowa** (0-15%): Niższe stopy stymulują inwestycje, ale mogą zwiększyć inflację
- **Podatki** (0-50%): Wpływają na konsumpcję i dochody budżetu
- **Wydatki rządowe** (5-50% PKB): Mnożnik keynesowski, wpływ na bezrobocie
- **Cła** (0-30%): Wpływają na handel międzynarodowy
- **Stopa inwestycji** (5-40% PKB): Kluczowa dla wzrostu kapitału

### 2. Wybierz scenariusz

- **📊 Normalny**: Standardowe warunki ekonomiczne
- **🚀 Boom Technologiczny**: Szybki postęp technologiczny (+3% produktywności/rok)
- **🤖 Rewolucja AI**: Masowa adopcja AI (+8% produktywności, ale ryzyko bezrobocia)
- **📉 Kryzys Krajowy**: Szok popytowy, spadek zaufania
- **🌐 Kryzys Globalny**: Recesja światowa, spadek handlu o 50%
- **🌱 Zielona Transformacja**: Inwestycje w czyste technologie

### 3. Uruchom symulację

- **1 Rok**: Krótkoterminowa analiza (4 kwartały)
- **5 Lat**: Średnioterminowa projekcja (20 kwartałów)
- **Prognoza 10 Lat**: Długoterminowa analiza trendów (40 kwartałów)

### 4. Analizuj wyniki

Obserwuj 6 wykresów pokazujących:
- Wzrost PKB
- Zmiany bezrobocia
- Dynamikę inflacji
- Akumulację kapitału
- Postęp technologiczny
- Zaufanie konsumentów

## 🎭 Scenariusze - Szczegóły

### Rewolucja AI 🤖

**Parametry:**
- Wzrost produktywności: +8%/rok
- Wzrost technologii: +7%/rok
- Globalizacja: +50%
- Ryzyko: Wzrost bezrobocia strukturalnego

**Najlepsze polityki:**
- Wysokie wydatki rządowe (programy przekwalifikowania)
- Niskie stopy procentowe (wspieranie innowacji)
- Umiarkowane podatki (finansowanie edukacji)

**Oczekiwane rezultaty:**
- PKB: +150-200% w 10 lat
- Bezrobocie: Wzrost o 2-4% krótkoterminowo, stabilizacja długoterminowo
- Inflacja: Presja deflacyjna z powodu wzrostu produktywności

### Kryzys Globalny 🌐

**Parametry:**
- Wzrost technologii: -1%/rok
- Globalizacja: -50%
- Spadek zaufania konsumentów

**Najlepsze polityki (wg Keynesa):**
- Bardzo wysokie wydatki rządowe (35-45% PKB)
- Niskie stopy procentowe (0-2%)
- Niskie podatki (stymulacja popytu)
- Niskie cła (unikanie wojen handlowych)

**Oczekiwane rezultaty:**
- PKB: Spadek o 10-20% w pierwszym roku
- Bezrobocie: Wzrost do 12-18%
- Inflacja: Ryzyko deflacji

### Zielona Transformacja 🌱

**Parametry:**
- Wzrost zielonej technologii: +4%/rok
- Wzrost ogólnej technologii: +3%/rok
- AI boost: +2%/rok

**Najlepsze polityki:**
- Wysokie wydatki rządowe (inwestycje w infrastrukturę)
- Umiarkowane podatki (subsydia dla zielonych technologii)
- Niskie cła na technologie odnawialne

**Oczekiwane rezultaty:**
- PKB: Wzrost o 40-60% w 10 lat
- Bezrobocie: Stabilne (tworzenie "zielonych" miejsc pracy)
- Inflacja: Kontrolowana (2-3%)

## 📈 Kluczowe Wnioski z Modelu

### 1. Kompromis Inflacja-Bezrobocie (Krzywa Phillipsa)

Polityka obniżająca bezrobocie (np. wysokie wydatki rządowe, niskie stopy procentowe) **krótkoterminowo** zmniejsza bezrobocie, ale **długoterminowo** prowadzi do wzrostu inflacji.

### 2. Wzrost Długookresowy (Model Solowa)

Kluczowe czynniki:
- **Inwestycje** w kapitał fizyczny
- **Postęp technologiczny** (A)
- **Edukacja** (wydatki rządowe wpływają na produktywność)

### 3. Stabilizacja Keynesowska

W czasie kryzysu:
- ✅ Zwiększ wydatki rządowe (mnożnik = 1.5)
- ✅ Obniż stopy procentowe
- ✅ Obniż podatki (ale uważaj na deficyt)

W czasie boomu (przegrzanie):
- ✅ Zmniejsz wydatki rządowe
- ✅ Podnieś stopy procentowe (chłodzenie gospodarki)
- ✅ Podnieś podatki (ograniczenie popytu)

### 4. Wpływ AI i Automatyzacji (Kluczowe dla XXI wieku!)

**Krótkoterminowo (1-3 lata):**
- Wzrost bezrobocia (+2-4%)
- Wzrost nierówności
- Potrzeba programów reskillingu

**Długoterminowo (5-10 lat):**
- Masywny wzrost produktywności (+50-100%)
- Nowe rodzaje miejsc pracy
- Wzrost PKB o 100-200%
- Ryzyko: Strukturalne bezrobocie jeśli brak adaptacji

**Rekomendowane polityki:**
1. Inwestycje w edukację i przekwalifikowanie (30-40% wydatków rządowych)
2. Universal Basic Income (UBI) jako siatka bezpieczeństwa
3. Podatki od automatyzacji (finansowanie UBI)
4. Wspieranie startupów i innowacji (niskie stopy procentowe)

### 5. Handel Międzynarodowy i Cła

**Niskie cła (0-5%):**
- ✅ Wzrost handlu i specjalizacji
- ✅ Niższe ceny dla konsumentów
- ❌ Ryzyko dla krajowych producentów

**Wysokie cła (20-30%):**
- ✅ Ochrona krajowych miejsc pracy (krótkoterminowo)
- ❌ Wyższe ceny
- ❌ Wojny handlowe
- ❌ Spadek PKB (długoterminowo)

## 🔬 Zaawansowane Analizy

### Eksperyment 1: Optymalna Polityka dla Wzrostu

**Cel:** Maksymalizacja PKB w 10 lat

**Parametry:**
- Stopa procentowa: 1-2% (stymulacja inwestycji)
- Podatki: 15-20% (zachęta do przedsiębiorczości)
- Wydatki rządowe: 25-30% (infrastruktura + edukacja)
- Cła: 0-5% (maksymalizacja handlu)
- Inwestycje: 30-35% PKB
- Scenariusz: Rewolucja AI

**Rezultat:** PKB wzrasta o 180-220% w 10 lat

### Eksperyment 2: Minimalizacja Bezrobocia

**Cel:** Najniższe bezrobocie

**Parametry:**
- Wydatki rządowe: 40-50% PKB (tworzenie miejsc pracy)
- Stopa procentowa: 0-1%
- Podatki: 25-30% (finansowanie wydatków)
- Inwestycje: 25-30%

**Rezultat:** Bezrobocie 1-2%, ale ryzyko wysokiej inflacji (5-8%)

### Eksperyment 3: Stabilność Cenowa

**Cel:** Inflacja 2% ± 0.5%

**Parametry (Reguła Taylora):**
- Aktywne dostosowywanie stopy procentowej
- Umiarkowane wydatki rządowe (18-22% PKB)
- Stabilne podatki (20%)

**Rezultat:** Inflacja 1.5-2.5%, stabilny wzrost PKB

## 🛠️ Technologie

### Wersja Python
- **Tkinter** - GUI
- **Matplotlib** - Wykresy
- **NumPy** - Obliczenia numeryczne

### Wersja Web
- **HTML5** - Struktura
- **CSS3** - Stylowanie (gradienty, animacje)
- **JavaScript (ES6+)** - Logika
- **Chart.js** - Interaktywne wykresy

## 📚 Bibliografia

1. **Solow, R. M.** (1956). "A Contribution to the Theory of Economic Growth"
2. **Keynes, J. M.** (1936). "The General Theory of Employment, Interest and Money"
3. **Phillips, A. W.** (1958). "The Relation between Unemployment and the Rate of Change of Money Wage Rates"
4. **Okun, A. M.** (1962). "Potential GNP: Its Measurement and Significance"
5. **Taylor, J. B.** (1993). "Discretion versus Policy Rules in Practice"

## 📝 Licencja

MIT License - Wolne do użytku edukacyjnego i komercyjnego

## 👨‍💻 Autor

Stworzony z wykorzystaniem modeli ekonomicznych i najnowszej wiedzy o wpływie AI na gospodarkę.

---

**Enjoy exploring macroeconomics! 🌍📊💰**
