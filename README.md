# Python Számla Képfeldolgozó

Ez a program képes kinyerni az adószámot, számlaszámot és bankszámlaszámot egy számla képéből OCR (Optical Character Recognition) technológia segítségével. A program a Python `pytesseract` könyvtárát használja a szöveg felismerésére.

## Telepítés

1. **Python telepítése**: Győződj meg róla, hogy a Python 3.x verziója telepítve van a gépeden. Letöltheted a [Python hivatalos weboldaláról](https://www.python.org/downloads/).

2. **Tesseract OCR telepítése**:
   - **Windows**: Töltsd le és telepítsd a Tesseract OCR-t a [hivatalos oldalról](https://github.com/tesseract-ocr/tesseract). Ne felejtsd el beállítani a `pytesseract.pytesseract.tesseract_cmd` változót a programban, hogy mutasson a Tesseract telepítési helyére.
   - **Linux**: Telepítsd a Tesseract-et a következő paranccsal:
     ```bash
     sudo apt-get install tesseract-ocr
     ```
   - **macOS**: Telepítsd a Tesseract-et a Homebrew segítségével:
     ```bash
     brew install tesseract
     ```

3. **Függőségek telepítése**: A program függőségeit a `requirements.txt` fájl segítségével telepítheted. Futtasd a következő parancsot:
   ```bash
   pip install -r requirements.txt