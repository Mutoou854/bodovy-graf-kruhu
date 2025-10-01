import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import re
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Seznam platných názvů barev
valid_colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
    'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown',
    'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
    'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray',
    'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid',
    'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise',
    'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite',
    'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray',
    'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory',
    'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue',
    'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgrey', 'lightpink',
    'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue',
    'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine',
    'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
    'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin',
    'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
    'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip',
    'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red',
    'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell',
    'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen',
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat',
    'white', 'whitesmoke', 'yellow', 'yellowgreen']

# Funkce pro validaci barvy
def ziskej_barvu():
    barva = st.text_input("Zadej barvu grafu (angl. název nebo hex kód):", "")
    
    if barva in valid_colors:
        return barva
    elif re.match(r'^#[0-9A-Fa-f]{6}$', barva):
        return barva
    else:
        return None

# Funkce vykreslení kruhu
def vykresli_kruh(pocet_bodu=100, barva='blue', x_0=0, y_0=0):
    r = polomer
    t = np.linspace(0, 2 * np.pi, pocet_bodu+1)

    x = x_0 + r * np.cos(t)
    y = y_0 + r * np.sin(t)

    # Vytvoření grafu s větší velikostí
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.scatter(x, y, color=barva, s=50)

    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    ax.set_xlabel('x [m]', fontsize=12)
    ax.set_ylabel('y [m]', fontsize=12)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(x_0 - r - 1, x_0 + r + 1)
    ax.set_ylim(y_0 - r - 1, y_0 + r + 1)

    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

    step = polomer_slider / 20
    ax.set_xticks(np.arange(x_0 - r - 1, x_0 + r + 1, step))
    ax.set_yticks(np.arange(y_0 - r - 1, y_0 + r + 1, step))

    ax.tick_params(axis='x', labelrotation=90)

    ax.set_title(f"Bodový graf kruhu")

    st.pyplot(fig)

    # Uložení obrázku do bufferu
    img_buf = BytesIO()
    fig.savefig(img_buf, format="png")
    img_buf.seek(0)
    plt.close(fig)  # Zavření grafu po jeho vykreslení
    return img_buf

# Funkce pro generování PDF s osobními údaji a grafem
def vytvor_pdf():
    pdf_buf = BytesIO()

    # Nastavení orientace na šířku (landscape)
    c = canvas.Canvas(pdf_buf, pagesize=landscape(A4))

    # Registrování písma DejaVuSans
    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

    # Registrování písma
    c.setFont("DejaVuSans", 9)
    
    c.translate(15 * 2.83465, 15 * 2.83465)  # Okraje 15mm

    img_buf = vykresli_kruh(barva=barva, x_0=0, y_0=0)  # Zavolání správné funkce
    image = ImageReader(img_buf)
    c.drawImage(image, -120, 20, width=730, height=525)

    # Osobní údaje
    c.drawString(560, 500, "Osobní údaje:")
    c.drawString(560, 480, "    Jméno: Matěj Rajm")
    c.drawString(560, 460, "    Věk: 22 let")
    c.drawString(560, 440, "    Email: Matej.Rajm@vutbr.cz")
    c.drawString(560, 420, "    Město trv. pobytu: Mnichovo Hradiště")
    c.drawString(560, 400, "    Studium: 1. ročník oboru Všeobecné stavitelství" )
    c.drawString(560, 380, "                    na Fakultě stavební VUT v Brně")
    c.drawString(560, 360, "Použité technologie: Streamlit, GitHub, ChatGPT")
    c.drawString(560, 220, "Parametry úlohy:")
    c.drawString(560, 200, f"   Poloměr kruhu: {polomer_slider}")
    c.drawString(560, 180, f"   Počet bodů na kruhu: {pocet_bodu_slider}")
    c.drawString(560, 160, f"   Souřadnice středu kruhu: ({x_0}, {y_0})")
    c.drawString(560, 140, f"   Barva kruhu: {barva}")

    c.save()

    pdf_buf.seek(0)
    return pdf_buf

# Streamlit UI: Uživatelský vstup pro poloměr, počet bodů a střed kruhu
st.title("Interaktivní vykreslení bodového grafu kruhu")

polomer_slider = st.slider("Zadej poloměr kruhu:", min_value=0.5, max_value=50.0, step=0.5, format="%.2f")
polomer_input = st.number_input("Nebo zadej přesnou hodnotu poloměru:", value=polomer_slider, step=0.1)

pocet_bodu_slider = st.slider("Zadej počet bodů na kruhu (3-500):", min_value=3, max_value=500, step=1)
pocet_bodu_input = st.number_input("Nebo zadej přesný počet bodů:", value=pocet_bodu_slider, min_value=3, max_value=500, step=1)

x_0 = st.number_input("Zadej souřadnici x středu:", value=0.0, min_value=-polomer_slider, max_value=polomer_slider)
y_0 = st.number_input("Zadej souřadnici y středu:", value=0.0, min_value=-polomer_slider, max_value=polomer_slider)

barva = ziskej_barvu()

# Přidání odkazu na seznam barev
st.markdown("""
    Seznam platných  názvů barev a jejich HEX kódů můžete najít [zde](https://www.w3schools.com/colors/colors_names.asp).
""")

polomer = polomer_input if polomer_input else polomer_slider
pocet_bodu = pocet_bodu_input if pocet_bodu_input else pocet_bodu_slider

if barva:
    if st.button("Vykresli kruh"):
        vykresli_kruh(pocet_bodu=pocet_bodu, barva=barva, x_0=x_0, y_0=y_0)
else:
    st.warning("Zadejte prosím platnou barvu!")

# Titul aplikace
st.title("Osobní údaje")

# Kontrola, zda sekce je otevřená nebo zavřená pomocí session_state
if 'is_open' not in st.session_state:
    st.session_state.is_open = False

def toggle_personal_info():
    st.session_state.is_open = not st.session_state.is_open

if st.button("Otevřít / Zavřít osobní údaje"):
    toggle_personal_info()

if st.session_state.is_open:
    with st.expander("Můj profil"):
        st.subheader("Osobní údaje")
        st.write("**Jméno**: Matěj Rajm")
        st.write("**Věk**: 22 let")
        st.write("**Email**: Matej.Rajm@vutbr.cz")
        st.write("**Město trv. pobytu**: Mnichovo Hradiště")
        st.write("**Studium**: 1. ročník oboru Všeobecné stavitelství na Fakultě stavební VUT v Brně")
        st.write("**Použité technologie**: Streamlit, GitHub, ChatGPT")
else:
    st.write("Klikněte na tlačítko pro zobrazení osobních údajů.")

# Streamlit UI: Tlačítko pro stažení PDF souboru
st.title("Generování PDF souboru s osobními údaji a grafem")

# Tlačítko pro generování a stažení PDF
if st.button("Stáhnout PDF s osobními údaji a grafem"):
    pdf_buf = vytvor_pdf()
    st.download_button(
        label="Stáhnout PDF",
        data=pdf_buf,
        file_name="profil_a_graf.pdf",
        mime="application/pdf"
    )
