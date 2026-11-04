import re

import streamlit as st
import pdfplumber

st.set_page_config(
    page_title="Ön Fizibilite",
    layout="wide"
)
col_logo, col_baslik = st.columns([1,3])

with col_logo:
    st.image(".streamlit/albond logo.png", width=180)

with col_baslik:
    st.markdown(
        """
        <h1 style='color:#c1121f; margin-top:15px;'>
        Kalıphane Değerlendirme Sistemi
        </h1>

        <h4 style='color:#666666;'>
        Alüminyum Ekstrüzyon Kalıp Ön Fizibilite
        </h4>
        """,
        unsafe_allow_html=True
    )

st.subheader("Teknik Resim")
bulunan_alan = 0.0
bulunan_cevre = 0.0
bulunan_du = 0.0
uploaded_pdf = st.file_uploader(
    "PDF Teknik Resim Yükle",
    type=["pdf"]
)

if uploaded_pdf is not None:
    
    try:
        with pdfplumber.open(uploaded_pdf) as pdf:

            ilk_sayfa = pdf.pages[0]

            metin = ilk_sayfa.extract_text()
            im = ilk_sayfa.to_image(resolution=200)
            
            st.subheader("Kesit Görüntüsü")
            st.image(
            im.original,
            width=800
)

        
            alan = (
            re.search(
            r"ALAN \(mm²\)\s*([\d.,]+)",
                metin,
                re.IGNORECASE
            )
            or
            re.search(
            r"KESIT ALANI\s*([\d.,]+)",
                metin,
                re.IGNORECASE
            )
        )

            cevre = (
            re.search(
            r"ÇEVRE \(mm\)\s*([\d.,]+)",
                metin,
                re.IGNORECASE
            )
            or
            re.search(
            r"PRF\.?\s*CEVRESI\s*([\d.,]+)",
                metin,
                re.IGNORECASE
            )
        )

            agirlik = re.search(
            r"([\d.,]+)\s*kg\s*/\s*m",
            metin,
            re.IGNORECASE
        )
            du_pdf = re.search(
            r"PROFIL DU\s*([\d.,]+)",
            metin,
            re.IGNORECASE
)
    
            if alan:
              
                bulunan_alan = float(
                alan.group(1)
                .replace(".", "")
                .replace(",", ".")
    )
                

            if cevre:
                bulunan_cevre = float(
                cevre.group(1).replace(",", ".")
            )

            if du_pdf:

                bulunan_du = float(
                du_pdf.group(1).replace(",", ".")
    )
              

    except Exception as e:
                st.error(f"PDF okunamadı: {e}")

col1, col2 = st.columns(2)


with col1:

    kesit_alani = st.number_input(
    "🟢 Kesit Alanı (mm²)",
    min_value=0.0,
    value=bulunan_alan
)
    profil_cevresi = st.number_input(
    "🟢 Profil Çevresi (mm)",
    min_value=0.0,
    value=bulunan_cevre
)
    sorti = st.number_input(
        "🔴 Sorti Sayısı",
        min_value=1,
        value=1
    )
    pres_tipi = st.selectbox(
    "Pres",
    ["6 İNÇ", "8 İNÇ"]
)

    if pres_tipi == "6 İNÇ":
        kovan_alani = 19597

    else:
        kovan_alani = 34619
   


    if kesit_alani > 0 and sorti > 0:
        ekstruzyon_orani = (
        kovan_alani /
        kesit_alani /
        sorti
    )
    else:
        ekstruzyon_orani = 0

    st.info(
        f"Ekstrüzyon Oranı = {round(ekstruzyon_orani,2)}"
    )

    if kesit_alani > 0:
        sekil_orani = (
        profil_cevresi /
        kesit_alani
    )
    else:
        sekil_orani = 0

    st.info(
        f"Şekil Oranı = {round(sekil_orani,3)}"
    )


    du = st.number_input(
    "🟢 DU",
    min_value=0.0,
    value=bulunan_du
)
    

    ana_et = st.number_input(
        "🔴 Ana Et Kalınlığı",
        min_value=0.1,
        value=1.0
    )

with col2:

    u_dil = st.number_input(
        "🔴 U Formu Dil Oranı",
        min_value=0.0
    )

    c_dil = st.selectbox(
    "🔴 C Formu Dil Sayısı",
    ["Yok", "1", "2", "3", "3+"]
)
    

    zivana_sayisi = st.number_input(
        "🔴 Zıvana Sayısı",
        min_value=0,
        step=1
    )

    zivana_olcusu = st.number_input(
        "🔴 En Küçük Zıvana Ölçüsü (mm)",
        min_value=0.0
    )

    profil_ebat = st.number_input(
    "🟢 Profil Ebatı (mm)",
    min_value=0.0,
    value=bulunan_du
)
    

    smax = st.number_input(
        "🔴 Smax",
        min_value=0.0
    )

    smin = st.number_input(
        "🔴 Smin",
        min_value=0.1,
        value=1.0
    )

    t_baglanti = st.number_input(
        "🔴 T Bağlantı Sayısı",
        min_value=0,
        step=1
    )



if st.button("Kalıphane Puanını Hesapla"):

    if (
        kesit_alani <= 0 or
        profil_cevresi <= 0 or
        du <= 0 or
        profil_ebat <= 0
    ):
        st.error("Lütfen tüm zorunlu alanları doldurun.")
        st.stop()

        # Zıvana varsa ölçüsü zorunlu

    if zivana_sayisi > 0 and zivana_olcusu <= 0:
        st.error("Zıvana ölçüsü girilmelidir.")
        st.stop()

        # Ekstrüzyon Oranı

    if 40 <= ekstruzyon_orani <= 50:
        p_ekstruzyon = 10
    elif 51 <= ekstruzyon_orani <= 70:
        p_ekstruzyon = 7
    elif 71 <= ekstruzyon_orani <= 90:
        p_ekstruzyon = 4
    else:
        p_ekstruzyon = 1

    # Şekil Oranı

    if sekil_orani < 0.4:
        p_sekil = 10
    elif sekil_orani <= 0.75:
        p_sekil = 7
    elif sekil_orani <= 1:
        p_sekil = 4
    else:
        p_sekil = 1


   # DU / Ana Et

    du_orani = du / ana_et

    if du < 50:

        if du_orani <= 10:
            p_du = 10
        elif du_orani <= 20:
            p_du = 7
        elif du_orani <= 35:
            p_du = 4
        else:
            p_du = 1

    elif du <= 100:

        if du_orani <= 15:
            p_du = 10
        elif du_orani <= 30:
            p_du = 7
        elif du_orani <= 50:
            p_du = 4
        else:
            p_du = 1

    elif du <= 200:

        if du_orani <= 20:
            p_du = 10
        elif du_orani <= 40:
            p_du = 7
        elif du_orani <= 65:
            p_du = 4
        else:
            p_du = 1

    else:

        if du_orani <= 25:
            p_du = 10
        elif du_orani <= 50:
            p_du = 7
        elif du_orani <= 80:
            p_du = 4
        else:
            p_du = 1

    # U Dil

    if u_dil == 0:
        p_u_dil = 10
    elif u_dil <= 1.5:
        p_u_dil = 7
    elif u_dil <= 3:
        p_u_dil = 4
    else:
        p_u_dil = 1


    # C Formu Dil Sayısı

    if c_dil == "Yok":
        p_c_dil = 10

    elif c_dil == "1":
        p_c_dil = 10

    elif c_dil == "2":
        p_c_dil = 7

    elif c_dil == "3":
        p_c_dil = 4

    else:  # 3+
        p_c_dil = 1

    # Zıvana Ölçüsü

    if zivana_sayisi == 0:
        p_zivana_olcu = 10

    elif 51 <= zivana_olcusu <= 200:
        p_zivana_olcu = 10

    elif 10 <= zivana_olcusu <= 50:
        p_zivana_olcu = 7

    elif 3 <= zivana_olcusu <= 9:
        p_zivana_olcu = 4

    else:
        p_zivana_olcu = 1

    # Zıvana Sayısı

    if zivana_sayisi == 0:
        p_zivana_sayi = 10

    elif zivana_sayisi == 1:
        p_zivana_sayi = 10

    elif zivana_sayisi == 2:
        p_zivana_sayi = 7

    elif 3 <= zivana_sayisi <= 4:
        p_zivana_sayi = 4

    else:
        p_zivana_sayi = 1

    # Profil Ebatı

    if profil_ebat <= 200:
        p_profil = 10
    elif profil_ebat <= 220:
        p_profil = 7
    elif profil_ebat <= 250:
        p_profil = 4
    else:
        p_profil = 1

    # Solid Yapısal İz

    yapisal_iz = (smax - smin) / smin

    if yapisal_iz == 0:
        p_solid = 10
    elif yapisal_iz <= 0.30:
        p_solid = 7
    elif yapisal_iz <= 1:
        p_solid = 4
    else:
        p_solid = 1

    # Köprülü Yapısal İz

    if t_baglanti == 0:
        p_koprulu = 10
    elif t_baglanti == 1:
        p_koprulu = 7
    elif t_baglanti == 2:
        p_koprulu = 4
    else:
        p_koprulu = 1

    # RED KONTROLÜ

    if profil_ebat > 300:
        st.error("❌ Profil ölçüsü 300 mm üzeri. RED")

    # PUAN HESAPLARI
    
    ekstruzyon_sonuc = (p_ekstruzyon * 15) / 10
    sekil_sonuc = (p_sekil * 15) / 10
    du_sonuc = (p_du * 10) / 10
    u_dil_sonuc = (p_u_dil * 10) / 10
    c_dil_sonuc = (p_c_dil * 10) / 10
    zivana_olcu_sonuc = (p_zivana_olcu * 10) / 10
    zivana_sayi_sonuc = (p_zivana_sayi * 10) / 10
    profil_sonuc = (p_profil * 5) / 10
    solid_sonuc = (p_solid * 5) / 10
    koprulu_sonuc = (p_koprulu * 5) / 10
    

    # GENEL PUAN

    genel_puan = (
        ekstruzyon_sonuc +
        sekil_sonuc +
        du_sonuc +
        u_dil_sonuc +
        c_dil_sonuc +
        zivana_olcu_sonuc +
        zivana_sayi_sonuc +
        profil_sonuc +
        solid_sonuc +
        koprulu_sonuc
    )

    # RİSK DEĞERLENDİRMESİ

    if profil_ebat > 300:

        st.error("🔴 RED KARARI")

    elif genel_puan >= 80:

        st.success("🟢 Düşük Risk")

    elif genel_puan >= 60:

        st.warning("🟡 Orta Risk")

    else:

        st.error("🔴 Yüksek Risk")
       
    st.divider()

    st.subheader("Kalıphane Sonuçları")

    import pandas as pd

    
    sonuc_df = pd.DataFrame({
    "Kriter": [
        "Ekstrüzyon Oranı",
        "Şekil Oranı",
        "DU / Ana Et",
        "U Formu Dil",
        "C Formu Dil",
        "Zıvana Ölçüsü",
        "Zıvana Sayısı",
        "Profil Ebatı",
        "Solid Yapısal İz",
        "Köprülü Yapısal İz"
    ],

    "Etki %": [
        15,15,10,10,10,10,10,5,5,5
    ],

    "Alınan Puan": [
        ekstruzyon_sonuc,
        sekil_sonuc,
        du_sonuc,
        u_dil_sonuc,
        c_dil_sonuc,
        zivana_olcu_sonuc,
        zivana_sayi_sonuc,
        profil_sonuc,
        solid_sonuc,
        koprulu_sonuc
    ]
})

    st.subheader("Kalıphane Sonuç Tablosu")

    st.dataframe(
    sonuc_df,
    use_container_width=True
    )

    st.divider()

    st.success(f"Genel Kalıphane Puanı : {round(genel_puan,2)} / 100")

