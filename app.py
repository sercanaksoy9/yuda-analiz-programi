import re

import streamlit as st
import pdfplumber
import pandas as pd
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
        YÜDA ANALİZ PROGRAMI
        </h1>

        <h4 style='color:#666666;'>
        Alüminyum Ekstrüzyon Kalıp ve Pres Fizibilite Analizi
        </h4>
        """,
        unsafe_allow_html=True
    )
    tab1, tab2 = st.tabs([
    "📋 Kalıphane",
    "🏭 Pres"
])

with tab1:
    st.subheader("Teknik Resim")
    bulunan_alan = 0.0
    bulunan_cevre = 0.0
    bulunan_du = 0.0
    bulunan_agirlik = 0.0

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
                bulunan_agirlik = 0.0

                agirlik = re.search(
                r"([\d.,]+)\s*kg\s*/\s*m",
                metin,
                re.IGNORECASE
            )
                if agirlik:

                    bulunan_agirlik = float(
                    agirlik.group(1)
                    .replace(",", ".")
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
        gramaj = st.number_input(
                "🟢 Gramaj (kg/m)",
                min_value=0.0,
                value=bulunan_agirlik,
                step=0.01
    )

        if gramaj > 0:

            sekil_faktoru = (
        (profil_cevresi / 10)
        /
        gramaj
    )

        else:

            sekil_faktoru = 0

        st.info(
            f"Şekil Faktörü = {round(sekil_faktoru,2)}"
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

        # Şekil Faktörü

        if 1 <= sekil_faktoru <= 25:
            p_sekil = 10

        elif 25 < sekil_faktoru <= 50:
            p_sekil = 7

        elif 50 < sekil_faktoru <= 75:
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
        profil_sonuc = (p_profil * 10) / 10
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
            15,15,10,10,10,10,10,10,5,5
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

        st.divider()
    with tab2:

        st.header("🏭 Pres Fizibilitesi")
        col1, col2 = st.columns(2)
        with col1:

            alasim_turu = st.selectbox(
            "🔴 Alaşım Türü",
            [
                "6060",
                "6063",
                "6463",
                "6101B",
                "6101",
                "6005",
                "6061",
                "6082",
                "6351",
                "6013",
                "6026",
                "6056",
                "5005",
                "5754",
                "7xxx"
            ]
        )
        if alasim_turu in [
            "6060",
            "6063",
            "6463",
            "6101B",
            "6101",
            "6005"
        ]:

            radyus = st.selectbox(
                "🔴 Minimum Radyüs",
                [
                    "R3<",
                    "R2",
                    "R1",
                    "R0,3>"
                ]
            )

        elif alasim_turu in [
            "6061",
            "6082",
            "6351",
            "6013",
            "6026",
            "6056"
        ]:

            radyus = st.selectbox(
                "🔴 Minimum Radyüs",
                [
                    "R3<",
                    "R2",
                    "R1",
                    "R0,5>"
                ]
            )

        else:  # 5xxx ve 7xxx

            radyus = st.selectbox(
                "🔴 Minimum Radyüs",
                [
                    "R4<",
                    "R4",
                    "R3",
                    "R2>"
                ]
            )
       

        if radyus in ["R3<", "R4<"]:
            p_radyus = 10

        elif radyus in ["R2", "R4"]:
            p_radyus = 7

        elif radyus == "R1" or radyus == "R3":
            p_radyus = 4

        else:
            p_radyus = 1

        

        # Alaşım Türü Puanı

        if alasim_turu in [
            "6060",
            "6063"
        ]:
            p_alasim = 10

        elif alasim_turu in [
            "1050",
            "6005"
        ]:
            p_alasim = 7

        elif alasim_turu in [
            "6026",
            "6082",
            "6351",
            "6061"
        ]:
            p_alasim = 4

        else:
            p_alasim = 1

        
        

        if smin > 0:

            homojen_et = smax / smin

        

            if homojen_et <= 3:
                p_homojen = 10

            elif homojen_et <= 6:
                p_homojen = 7

            elif homojen_et <= 9.9:
                p_homojen = 4

            else:
                p_homojen = 1

            
            
    
        if 40 <= ekstruzyon_orani <= 50:
            p_pres_ekstruzyon = 10

        elif 51 <= ekstruzyon_orani <= 70:
            p_pres_ekstruzyon = 7

        elif 71 <= ekstruzyon_orani <= 90:
            p_pres_ekstruzyon = 4

        else:
            p_pres_ekstruzyon = 1

        

    
    
        if sorti == 1:
            p_sorti = 10

        elif sorti == 2:
            p_sorti = 7

        elif 3 <= sorti <= 4:
            p_sorti = 4

        else:
            p_sorti = 1

        
        tolerans_turu = st.selectbox(
            "🔴 Tolerans Türü",
            [
                "755-9",
                "12020-2",
                "Özel Tolerans Sayısı <4",
                "Özel Tolerans Sayısı >=4"
            ]
        )
        if tolerans_turu == "755-9":
            p_tolerans = 10

        elif tolerans_turu == "12020-2":
            p_tolerans = 7

        elif tolerans_turu == "Özel Tolerans Sayısı <4":
            p_tolerans = 4

        else:
            p_tolerans = 1

        
        if alasim_turu in [
            "6060",
            "6063",
            "6463",
            "6101B",
            "6101"
        ]:

            kondusyon = st.selectbox(
                "🔴 Kondüsyon",
                [
                    "T4-T5-T6",
                    "T64",
                    "T66"
                ]
            )

        elif alasim_turu == "6005":

            kondusyon = st.selectbox(
                "🔴 Kondüsyon",
                [
                    "T4",
                    "T66"
                ]
            )

        elif alasim_turu in [
            "6061",
            "6082",
            "6351",
            "6013"
        ]:

            kondusyon = st.selectbox(
                "🔴 Kondüsyon",
                [
                    "T4",
                    "T5-T6"
                ]
            )

        elif alasim_turu in [
            "6026",
            "6056"
        ]:

            kondusyon = st.selectbox(
                "🔴 Kondüsyon",
                [
                    "T4",
                    "T6"
                ]
            )

        else:

            kondusyon = st.selectbox(
                "🔴 Kondüsyon",
                ["Standart"]
            )


        
        # Kondüsyon Puanı
        p_kondusyon = 1

        if alasim_turu in [
            "6060",
            "6063",
            "6463",
            "6101B",
            "6101"
        ]:

            if kondusyon in ["T4-T5-T6", "T64"]:    

                if 1.5 <= ana_et <= 4:
                    p_kondusyon = 10

                elif 4 < ana_et <= 6:
                    p_kondusyon = 7

                elif 6 < ana_et <= 8:
                    p_kondusyon = 4

                else:
                    p_kondusyon = 1

            elif kondusyon == "T66":

                if 1.5 <= ana_et <= 3:
                    p_kondusyon = 10

                elif 3 < ana_et <= 5:
                    p_kondusyon = 7

                elif 5 < ana_et <= 6:
                    p_kondusyon = 4

                else:
                    p_kondusyon = 1


            elif alasim_turu == "6005":

                if kondusyon == "T4":

                    if 1.5 <= ana_et <= 4:
                        p_kondusyon = 10

                    elif 4 < ana_et <= 6:
                        p_kondusyon = 7

                    elif 6 < ana_et <= 8:
                        p_kondusyon = 4

                    else:
                        p_kondusyon = 1

            elif kondusyon == "T66":

                    if 1.5 <= ana_et <= 3:
                        p_kondusyon = 10

                    elif 3 < ana_et <= 4:
                        p_kondusyon = 7

                    elif 4 < ana_et <= 6:
                        p_kondusyon = 4

                    else:
                        p_kondusyon = 1

            
            elif alasim_turu in [
                "6061",
                "6082",
                "6351",
                "6013"
            ]:

                if kondusyon == "T4":

                    if 1.8 <= ana_et <= 3:
                        p_kondusyon = 10

                    elif 3 < ana_et <= 5:
                        p_kondusyon = 7

                    elif 5 < ana_et <= 8:
                        p_kondusyon = 4

                    else:
                        p_kondusyon = 1

                elif kondusyon == "T5-T6":

                    if 1.8 <= ana_et <= 3:
                        p_kondusyon = 10

                    elif 3 < ana_et <= 4:
                        p_kondusyon = 7

                    elif 4 < ana_et <= 5:
                        p_kondusyon = 4

                    else:
                        p_kondusyon = 1


            elif alasim_turu in [
                "6061",
                "6082",
                "6351",
                "6013"
            ]:

                if kondusyon == "T4":

                    if 1.8 <= ana_et <= 3:
                        p_kondusyon = 10

                    elif 3 < ana_et <= 5:
                        p_kondusyon = 7

                    elif 5 < ana_et <= 8:
                        p_kondusyon = 4

                    else:
                        p_kondusyon = 1

                elif kondusyon == "T5-T6":

                    if 1.8 <= ana_et <= 3:
                        p_kondusyon = 10

                    elif 3 < ana_et <= 4:
                        p_kondusyon = 7

                    elif 4 < ana_et <= 5:
                        p_kondusyon = 4

                    else:
                        p_kondusyon = 1

        siparis_miktari = st.selectbox(
            "🔴 Sipariş Miktarı (Kg)",
            [
                ">2001",
                "1001-2000",
                "501-1000",
                "500<"
            ]
        )

        if siparis_miktari == ">2001":
            p_siparis = 10

        elif siparis_miktari == "1001-2000":
            p_siparis = 7

        elif siparis_miktari == "501-1000":
            p_siparis = 4

        else:
            p_siparis = 1

        
        siparis_boyu = st.selectbox(
            "🔴 Sipariş Boyu (mm)",
            [
                "4000-6000",
                "6001-8000",
                "2000-3999",
                "2000< ve >8000"
            ]
        )

        if siparis_boyu == "4000-6000":
            p_boy = 10

        elif siparis_boyu == "6001-8000":
            p_boy = 7

        elif siparis_boyu == "2000-3999":
            p_boy = 4

        else:
            p_boy = 1

       
        yuzey_durumu = st.selectbox(
            "🔴 Yüzey Durumu",
            [
                "Pres",
                "Boyalı",
                "Mat",
                "Parlak ve ÖE"
            ]
        )

        if yuzey_durumu == "Pres":
            p_yuzey = 10

        elif yuzey_durumu == "Boyalı":
            p_yuzey = 7

        elif yuzey_durumu == "Mat":
            p_yuzey = 4

        else:
            p_yuzey = 1

        

        if zivana_sayisi == 1:
            p_zivana = 10

        elif zivana_sayisi == 2:
            p_zivana = 7

        elif 3 <= zivana_sayisi <= 4:
            p_zivana = 4

        else:
            p_zivana = 1

        
        et_orani = bulunan_du / ana_et


        if bulunan_du < 50:

            if et_orani <= 10:
                p_et = 10

            elif et_orani <= 20:
                p_et = 7

            elif et_orani <= 35:
                p_et = 4

            else:
                p_et = 1

        elif bulunan_du <= 100:

            if et_orani <= 15:
                p_et = 10

            elif et_orani <= 30:
                p_et = 7

            elif et_orani <= 50:
                p_et = 4

            else:
                p_et = 1

        elif bulunan_du <= 200:

            if et_orani <= 20:
                p_et = 10

            elif et_orani <= 40:
                p_et = 7

            elif et_orani <= 65:
                p_et = 4

            else:
                p_et = 1

        else:

            if et_orani <= 25:
                p_et = 10

            elif et_orani <= 50:
                p_et = 7

            elif et_orani <= 80:
                p_et = 4

            else:
                p_et = 1

        

        yurume_yuzeyi = st.selectbox(
            "🔴 Profilin Tezgahta Yürüme Yüzeyi",
            [
                "Görünmeyen Yüzey",
                "2.Görünür Yüzey",
                "1.Görünür Yüzey",
                "Dekoratif-Ezik"
            ]
        )

        if yurume_yuzeyi == "Görünmeyen Yüzey":
            p_yurume = 10

        elif yurume_yuzeyi == "2.Görünür Yüzey":
            p_yurume = 7

        elif yurume_yuzeyi == "1.Görünür Yüzey":
            p_yurume = 4

        else:
            p_yurume = 1

        
        biyet_boyu = st.selectbox(
            "🔴 Biyet Boyu (Max. Biyet Boyuna Yakınlık %)",
            [
                "%85-100",
                "%71-84",
                "%50-70",
                "%50>"
            ]
        )

        if biyet_boyu == "%85-100":
            p_biyet = 10

        elif biyet_boyu == "%71-84":
            p_biyet = 7

        elif biyet_boyu == "%50-70":
            p_biyet = 4

        else:
            p_biyet = 1

        
        fire_miktari = st.selectbox(
            "🔴 Fire Miktarı",
            [
                "<%15",
                "%15-%20",
                "%20-%30",
                "%30>"
            ]
        )

        if fire_miktari == "<%15":
            p_fire = 10

        elif fire_miktari == "%15-%20":
            p_fire = 7

        elif fire_miktari == "%20-%30":
            p_fire = 4

        else:
            p_fire = 1

        
       

        if 20 <= bulunan_du <= 99:
            p_du = 10

        elif 100 <= bulunan_du <= 149:
            p_du = 7

        elif 150 <= bulunan_du <= 249:
            p_du = 4

        else:
            p_du = 1

        
        radyus_sonuc      = (p_radyus * 5) / 10
        homojen_sonuc     = (p_homojen * 5) / 10
        ekstruzyon_sonuc  = (p_pres_ekstruzyon * 15) / 10
        sorti_sonuc       = (p_sorti * 5) / 10
        tolerans_sonuc    = (p_tolerans * 5) / 10
        alasim_sonuc      = (p_alasim * 10) / 10
        kondusyon_sonuc   = (p_kondusyon * 5) / 10
        siparis_sonuc     = (p_siparis * 5) / 10
        boy_sonuc         = (p_boy * 5) / 10
        yuzey_sonuc       = (p_yuzey * 5) / 10
        zivana_sonuc      = (p_zivana * 5) / 10
        et_sonuc          = (p_et * 5) / 10
        yurume_sonuc      = (p_yurume * 5) / 10
        biyet_sonuc       = (p_biyet * 5) / 10
        fire_sonuc        = (p_fire * 10) / 10
        du_sonuc          = (p_du * 5) / 10

        st.divider()

        st.subheader("Pres Sonuç Tablosu")

        pres_df = pd.DataFrame({
        "Kriter": [
            "Radyüs",
            "Homojen Et Kalınlığı",
            "Ekstrüzyon Oranı",
            "Sorti Sayısı",
            "Tolerans Türü",
            "Alaşım Türü",
            "Kondüsyon",
            "Sipariş Miktarı",
            "Sipariş Boyu",
            "Yüzey Durumu",
            "Zıvana Sayısı",
            "Et Kalınlığı",
            "Tezgahta Yürüme Yüzeyi",
            "Biyet Boyu",
            "Fire Miktarı",
            "DU"
        ],

        "Etki %": [
            5, 5, 15, 5, 5, 10, 5, 5,
            5, 5, 5, 5, 5, 5, 10, 5
        ],

        "Alınan Puan": [
            radyus_sonuc,
            homojen_sonuc,
            ekstruzyon_sonuc,
            sorti_sonuc,
            tolerans_sonuc,
            alasim_sonuc,
            kondusyon_sonuc,
            siparis_sonuc,
            boy_sonuc,
            yuzey_sonuc,
            zivana_sonuc,
            et_sonuc,
            yurume_sonuc,
            biyet_sonuc,
            fire_sonuc,
            du_sonuc
        ]
    })

        st.dataframe(
        pres_df,
        use_container_width=True,
        hide_index=True,
        height=650
    )


        st.divider()

        pres_genel_puan = (
                radyus_sonuc +
                homojen_sonuc +
                ekstruzyon_sonuc +
                sorti_sonuc +
                tolerans_sonuc +
                alasim_sonuc +
                kondusyon_sonuc +
                siparis_sonuc +
                boy_sonuc +
                yuzey_sonuc +
                zivana_sonuc +
                et_sonuc +
                yurume_sonuc +
                biyet_sonuc +
                fire_sonuc +
                du_sonuc
            )
        if pres_genel_puan >= 80:

            st.success("🟢 Düşük Risk")

        elif pres_genel_puan >= 60:

            st.warning("🟡 Orta Risk")

        else:

            st.error("🔴 Yüksek Risk")

        st.success(
        f"🏭 Pres Genel Puanı : {round(pres_genel_puan,2)} / 100"
            )
