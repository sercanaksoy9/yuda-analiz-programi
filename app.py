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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Kalıphane",
    "🏭 Pres",
    "🎨 Boyahane",
    "⭐ Genel Sonuç",
    "⚙️ Pres Seçimi"
])


with tab1:
    st.subheader("Teknik Resim")
    bulunan_alan = 0.0
    bulunan_cevre = 0.0
    bulunan_du = 0.0
    bulunan_agirlik = 0.0
    genel_puan = 0.0

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
        st.session_state["genel_puan"] = genel_puan


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
        st.session_state["pres_genel_puan"] = pres_genel_puan
        
        if pres_genel_puan >= 80:

            st.success("🟢 Düşük Risk")

        elif pres_genel_puan >= 60:

            st.warning("🟡 Orta Risk")

        else:

            st.error("🔴 Yüksek Risk")

        st.success(
        f"🏭 Pres Genel Puanı : {round(pres_genel_puan,2)} / 100"
            )
    with tab3:

        st.header("🎨 Boyahane Fizibilitesi")

        # GRAMAJ

        gramaj = st.number_input(
            "🔴 Gramaj (kg/m)",
            min_value=0.0,
            value=bulunan_agirlik,
            step=0.01
        )

        if gramaj >= 2.5:
            p_gramaj = 10

        elif 1.51 <= gramaj <= 2.49:
            p_gramaj = 7

        elif 0.31 <= gramaj <= 1.50:
            p_gramaj = 4

        else:
            p_gramaj = 1


        # SİPARİŞ BOYU

        siparis_boyu_boya = st.selectbox(
            "🔴 Sipariş Boyu",
            [
                "6000-8000",
                "4001-5999",
                "2001-4000",
                "2000 ve altı"
            ]
        )

        if siparis_boyu_boya == "6000-8000":
            p_boya_boy = 10

        elif siparis_boyu_boya == "4001-5999":
            p_boya_boy = 7

        elif siparis_boyu_boya == "2001-4000":
            p_boya_boy = 4

        else:
            p_boya_boy = 1


        # ASKI İZİ

        aski_izi = st.selectbox(
            "🔴 Askı İzi",
            [
                "Var",
                "Yok"
            ]
        )

        if aski_izi == "Var":
            p_aski = 10
        else:
            p_aski = 1


        # SATİNAJ

        satinaj = st.selectbox(
            "🔴 Kesitin Satinaja Uygunluğu",
            [
                "Uygun",
                "Uygun Değil"
            ]
        )

        if satinaj == "Uygun":
            p_satinaj = 10
        else:
            p_satinaj = 1


        # RENK MİKTARI

        renk_miktari = st.selectbox(
            "🔴 Renk Miktarı",
            [
                "Standart Renk - 1000 kg ve üzeri",
                "Özel Renk - 1000 kg ve üzeri",
                "Standart Renk - 999 kg altı",
                "Özel Renk - 999 kg altı"
            ]
        )

        if renk_miktari == "Standart Renk - 1000 kg ve üzeri":
            p_renk = 10

        elif renk_miktari == "Özel Renk - 1000 kg ve üzeri":
            p_renk = 7

        elif renk_miktari == "Standart Renk - 999 kg altı":
            p_renk = 4

        else:
            p_renk = 1


        # BAĞLAMA ŞEKLİ

        baglama = st.selectbox(
            "🔴 Bağlama Şekli",
            [
                "Kancalı Kaba Profiller",
                "İnce Profiller"
            ]
        )

        if baglama == "Kancalı Kaba Profiller":
            p_baglama = 10
        else:
            p_baglama = 7


        # ÇAPAK ADEDİ

        capak = st.selectbox(
            "🔴 Kabul Edilen Metredeki Çapak Adedi",
            [
                "5-6 Adet",
                "3-4 Adet",
                "1-2 Adet",
                "Hiç Çapak Yok"
            ]
        )

        if capak == "5-6 Adet":
            p_capak = 10

        elif capak == "3-4 Adet":
            p_capak = 7

        elif capak == "1-2 Adet":
            p_capak = 4

        else:
            p_capak = 1


        # KULLANIM YERİ

        kullanim_yeri = st.selectbox(
            "🔴 Profilin Kullanım Yeri",
            [
                "Cephe Sistemleri - Cotta Serisi",
                "Isı Bariyeri",
                "Cam Balkon - Tır Dorsesi",
                "Mobilya - Otomotiv"
            ]
        )

        if kullanim_yeri == "Cephe Sistemleri - Cotta Serisi":
            p_kullanim = 10

        elif kullanim_yeri == "Isı Bariyeri":
            p_kullanim = 7

        elif kullanim_yeri == "Cam Balkon - Tır Dorsesi":
            p_kullanim = 4

        else:
            p_kullanim = 1


        # GÖRÜNÜR YÜZEY

        gorunur_yuzey = st.selectbox(
            "🔴 Görünür Yüzey",
            [
                "Köprülü Kalıp - Kancalı Asılabilenler",
                "Görünür Yüzey Harici Askılama Yapılacak Profiller",
                "Her Yer Görünür Yüzey - Şartlı Onay Alınan",
                "Her Yer Görünür Yüzey - Şartlı Onay Alınmayan"
            ]
        )

        if gorunur_yuzey == "Köprülü Kalıp - Kancalı Asılabilenler":
            p_gorunur = 10

        elif gorunur_yuzey == "Görünür Yüzey Harici Askılama Yapılacak Profiller":
            p_gorunur = 7

        elif gorunur_yuzey == "Her Yer Görünür Yüzey - Şartlı Onay Alınan":
            p_gorunur = 4

        else:
            p_gorunur = 1


        # BOYA RENGİ

        boya_rengi = st.selectbox(
            "🔴 Boya Rengi",
            [
                "Dalga Yapmayan Düz Renkler",
                "Pütürlü Dalga Yapabilecek Renkler"
            ]
        )

        if boya_rengi == "Dalga Yapmayan Düz Renkler":
            p_boya_rengi = 10
        else:
            p_boya_rengi = 4

        gramaj_sonuc = (p_gramaj * 10) / 10
        boy_sonuc = (p_boya_boy * 10) / 10
        aski_sonuc = (p_aski * 10) / 10
        satinaj_sonuc = (p_satinaj * 10) / 10
        renk_sonuc = (p_renk * 10) / 10
        baglama_sonuc = (p_baglama * 10) / 10
        capak_sonuc = (p_capak * 10) / 10
        kullanim_sonuc = (p_kullanim * 10) / 10
        gorunur_sonuc = (p_gorunur * 10) / 10
        boya_rengi_sonuc = (p_boya_rengi * 10) / 10

        boyahane_genel_puan = (
            gramaj_sonuc +
            boy_sonuc +
            aski_sonuc +
            satinaj_sonuc +
            renk_sonuc +
            baglama_sonuc +
            capak_sonuc +
            kullanim_sonuc +
            gorunur_sonuc +
            boya_rengi_sonuc
        )

        st.session_state["boyahane_genel_puan"] = boyahane_genel_puan


        if boyahane_genel_puan >= 80:

            st.success("🟢 Düşük Risk")

        elif boyahane_genel_puan >= 60:

            st.warning("🟡 Orta Risk")

        else:

            st.error("🔴 Yüksek Risk")

        st.divider()

        st.subheader("Boyahane Sonuç Tablosu")

        boya_df = pd.DataFrame({

            "Kriter": [
                "Gramaj",
                "Sipariş Boyu",
                "Askı İzi",
                "Satınaj Uygunluğu",
                "Renk Miktarı",
                "Bağlama Şekli",
                "Çapak Adedi",
                "Kullanım Yeri",
                "Görünür Yüzey",
                "Boya Rengi"
            ],

            "Etki %": [
                10,10,10,10,10,
                10,10,10,10,10
            ],

            "Alınan Puan": [
                gramaj_sonuc,
                boy_sonuc,
                aski_sonuc,
                satinaj_sonuc,
                renk_sonuc,
                baglama_sonuc,
                capak_sonuc,
                kullanim_sonuc,
                gorunur_sonuc,
                boya_rengi_sonuc
            ]
        })

        st.dataframe(
            boya_df,
            use_container_width=True,
            hide_index=True,
            height=500
        )

        st.success(
            f"🎨 Boyahane Genel Puanı : {round(boyahane_genel_puan,2)} / 100"
        )

with tab4:

    st.header("⭐ Genel Sonuç")
    genel_puan = st.session_state.get("genel_puan", 0)
    pres_genel_puan = st.session_state.get("pres_genel_puan", 0)
    boyahane_genel_puan = st.session_state.get("boyahane_genel_puan", 0)

    st.metric(
        "📋 Kalıphane Puanı",
        round(genel_puan, 1)
    )

    st.metric(
        "🏭 Pres Puanı",
        round(pres_genel_puan, 1)
    )

    st.metric(
        "🎨 Boyahane Puanı",
        round(boyahane_genel_puan, 1)
    )

    puanlar = []

    if genel_puan > 0:
        puanlar.append(genel_puan)

    if pres_genel_puan > 0:
        puanlar.append(pres_genel_puan)

    if boyahane_genel_puan > 0:
        puanlar.append(boyahane_genel_puan)

    if len(puanlar) > 0:
        genel_fizibilite = sum(puanlar) / len(puanlar)
    else:
        genel_fizibilite = 0

    st.divider()

    if genel_fizibilite >= 80:

        st.success(
            f"🟢 Genel Fizibilite : {round(genel_fizibilite,1)} / 100"
        )

    elif genel_fizibilite >= 60:

        st.warning(
            f"🟡 Genel Fizibilite : {round(genel_fizibilite,1)} / 100"
        )

    else:

        st.error(
            f"🔴 Genel Fizibilite : {round(genel_fizibilite,1)} / 100"
        )

    with tab5:

        st.header("⚙️ Pres Seçimi")

        gramaj = st.number_input(
            "Profil Gramajı (gr/m)",
            min_value=1.0
        )

        profil_boyu = st.number_input(
            "Profil Boyu (cm)",
            min_value=1.0
        )

        du = st.number_input(
            "DU (mm)",
            min_value=1.0
        )

        ara_is = st.number_input(
            "Ara İş Boyu (cm)",
            min_value=0.0,
            value=5.0
        )
        germe_firesi = st.number_input(
            "Germe-Kesme Firesi (m)",
            min_value=0.0,
            value=2.0,
            step=0.1
        )

        kalip_tipi = st.selectbox(
            "Kalıp Tipi",
            ["Düz Kalıp", "Köprülü Kalıp"]
        )
        if st.button("🏆 En Uygun Presi Bul"):

                sonuclar = []

                kaliplar = [
                        {"cap":180, "paket":130, "pres":["6"]},
                        {"cap":200, "paket":160, "pres":["6","8"]},
                        {"cap":230, "paket":160, "pres":["6","8"]},
                        {"cap":260, "paket":160, "pres":["6","8"]},
                        {"cap":300, "paket":200, "pres":["8"]},
                        {"cap":330, "paket":250, "pres":["8"]},
                        {"cap":350, "paket":160, "pres":["6"]},
                        {"cap":360, "paket":200, "pres":["8"]},
                        {"cap":475, "paket":200, "pres":["8"]}
]
                presler = [
                {
                    "pres": '6"',
                    "kovan": 19597,
                    "kg_cm_biyet": 0.489,
                    "max_biyet": 85,
                    "max_du_duz": 180,
                    "max_du_koprulu": 160,
                    "sorti_max": 4,
                    "gramaj_min": 300,
                    "gramaj_max": 1500,
                },
                {
                    "pres": '8"',
                    "kovan": 34618,
                    "kg_cm_biyet": 0.868,
                    "max_biyet": 120,
                    "max_du_duz": 280,
                    "max_du_koprulu": 250,
                    "sorti_max": 6,
                    "gramaj_min": 1501,
                    "gramaj_max": 15000,
                }
            ]

                for pres in presler:

                    for sorti in range(1, pres["sorti_max"] + 1):

                        # Kullanılan standart sortiler

                        if sorti not in [1, 2, 4, 6]:
                            continue

                        # DU'ya göre maksimum sorti

                        if du > 150:
                            max_sorti_du = 1

                        elif du > 100:
                            max_sorti_du = 2

                        else:
                            max_sorti_du = 6

                        if sorti > max_sorti_du:
                            continue

                        # Gramaja göre sorti limiti

                        if gramaj >= 2000:
                            max_sorti_izin = 2
                        elif gramaj >= 1500:
                            max_sorti_izin = 3
                        elif gramaj >= 800:
                            max_sorti_izin = 4
                        else:
                            max_sorti_izin = 6

                        if sorti > max_sorti_izin:
                            continue

                        etkin_gramaj = gramaj * sorti
                        if not (
                            pres["gramaj_min"]
                            <= etkin_gramaj
                            <= pres["gramaj_max"]
                        ):
                            continue

                        if etkin_gramaj < pres["gramaj_min"]:
                            continue

                        if etkin_gramaj > pres["gramaj_max"]:
                            continue
                        

                        if kalip_tipi == "Düz Kalıp" and du > pres["max_du_duz"]:
                            continue

                        if kalip_tipi == "Köprülü Kalıp" and du > pres["max_du_koprulu"]:
                            continue

                        max_biyet_kg = (
                            pres["max_biyet"]
                            * pres["kg_cm_biyet"]
                        )

                        ara_is_kg = (
                            ara_is
                            * pres["kg_cm_biyet"]
                        )

                        profil_icin_kg = (
                            max_biyet_kg
                            - ara_is_kg
                        )

                        toplam_metre = (
                            profil_icin_kg
                            / (gramaj / 1000)
                        )

                        metre_sorti = (
                            toplam_metre
                            / sorti
                        )

                        net_metre = (
                            metre_sorti
                            - germe_firesi
                        )
                        sehpa_boy_sayisi = int(
                            (52 - germe_firesi)
                            /
                            (profil_boyu / 100)
                        )

                        biyet_boy_sayisi = int(
                            net_metre
                            /
                            (profil_boyu / 100)
                        )

                        boy_sayisi = sehpa_boy_sayisi

                        while boy_sayisi > 0:

                                uretilen_kg = (
                                    boy_sayisi
                                    * (profil_boyu / 100)
                                    * (gramaj / 1000)
                                    * sorti
                                )

                                toplam_metre = (
                                    (boy_sayisi * (profil_boyu / 100))
                                    + germe_firesi
                                ) * sorti

                                hesaplanan_biyet_kg = (
                                    toplam_metre
                                    * (gramaj / 1000)
                                )

                                net_biyet_boyu = (
                                    hesaplanan_biyet_kg
                                    / pres["kg_cm_biyet"]
                                )

                                biyet_boyu = (
                                    net_biyet_boyu
                                    + ara_is
                                )

                                if biyet_boyu <= float(pres["max_biyet"]):
                                    break

                                boy_sayisi -= 1

                        if boy_sayisi < 1:
                                continue

                        hedef_cap = du * 2

                        kalip_capi = None
                        paket_boyu = None

                        for kalip in kaliplar:

                            if kalip["cap"] >= hedef_cap:

                                kalip_capi = kalip["cap"]
                                paket_boyu = kalip["paket"]

                                break

                            if kalip["cap"] >= hedef_cap:

                                    kalip_capi = kalip["cap"]
                                    paket_boyu = kalip["paket"]
                                    break

                        if kalip_tipi == "Düz Kalıp":

                                    fiyatlar = {
                                        (180,130): {1:385, 2:424, 4:489, 6:501},
                                        (200,160): {1:495, 2:545, 4:629, 6:644},
                                        (230,160): {1:645, 2:710, 4:819, 6:839},
                                        (260,160): {1:785, 2:864, 4:997, 6:1021},
                                        (300,200): {1:1360, 2:1496, 4:1727, 6:1768},
                                        (330,250): {1:1890, 2:2079, 4:2400, 6:2457},
                                        (350,160): {1:1590, 2:1749, 4:2019, 6:2067},
                                        (360,200): {1:2185, 2:2404, 4:2775, 6:2841},
                                        (475,200): {1:3720, 2:4092, 4:4724, 6:4836},
                                        }

                        else:

                                    fiyatlar = {
                                        (180,130): {1:480, 2:528, 4:610, 6:624},
                                        (200,160): {1:620, 2:682, 4:787, 6:806},
                                        (230,160): {1:805, 2:886, 4:1022, 6:1047},
                                        (260,160): {1:980, 2:1078, 4:1245, 6:1274},
                                        (300,200): {1:1700, 2:1870, 4:2159, 6:2210},
                                        (330,250): {1:2365, 2:2602, 4:3004, 6:3075},
                                        (350,160): {1:1985, 2:2184, 4:2521, 6:2581},
                                        (360,200): {1:2730, 2:3003, 4:3467, 6:3549},
                                        (475,200): {1:4650, 2:5115, 4:5906, 6:6045},
                                        }

                        kalip_bedeli = fiyatlar[(kalip_capi, paket_boyu)][sorti]
                                
        
                        toplam_biyet_kg = (
                                biyet_boyu
                                * pres["kg_cm_biyet"]
                            )
                        fire = (
                                (toplam_biyet_kg - uretilen_kg)
                                / toplam_biyet_kg
                            ) * 100

                        doluluk = (
                                uretilen_kg
                                / toplam_biyet_kg
                            ) * 100

                        biyet_kullanim = (
                                biyet_boyu
                                / pres["max_biyet"]
                            ) * 100

                        if boy_sayisi < 1:
                            continue

                        kalip_bedeli = fiyatlar[(kalip_capi, paket_boyu)][sorti]

                        sonuclar.append({

                        "Ekstrüzyon": round(
                        pres["kovan"] / (249.6 * sorti),
                        1
                        ),
                        "Pres": pres["pres"],
                        "Sorti": sorti,
                        "Kalıp": f"{kalip_capi} x {paket_boyu}",
                        "Kalıp Bedeli €": kalip_bedeli,
                        "Etkin Gramaj": gramaj * sorti,
                        "Boy Sayısı": boy_sayisi,
                        "Biyet Boyu (cm)": round(biyet_boyu, 2),
                        "Biyet Kullanım %": round(biyet_kullanim, 2),
                        "Üretilen Kg": round(uretilen_kg, 2),
                        "Toplam Biyet Kg": round(toplam_biyet_kg, 2),
                        "Fire %": round(fire, 2),
                        "Doluluk %": round(doluluk, 2),
                        "Biyet Kullanım %": round(biyet_kullanim, 2)
                        
                    })

                if len(sonuclar) > 0:

                    sonuc_df = pd.DataFrame(sonuclar)

                    with st.expander("Detay Hesap Tablosu"):

                        st.dataframe(
                            sonuc_df,
                            use_container_width=True
                    )
                        
                    sonuc_6 = sonuc_df[
                        sonuc_df["Pres"] == '6"'
                    ]

                    sonuc_8 = sonuc_df[
                        sonuc_df["Pres"] == '8"'
                    ]

                    if len(sonuc_6) > 0:

                            en_iyi_6 = sonuc_6.sort_values(
                            by=["Biyet Kullanım %", "Fire %"],
                            ascending=[False, True]
                        ).iloc[0]

                    if len(sonuc_8) > 0:

                            en_iyi_8 = sonuc_8.sort_values(
                            by=["Biyet Kullanım %", "Fire %"],
                            ascending=[False, True]
                        ).iloc[0]

                    col1, col2 = st.columns(2)

                    with col1:

                    

                        if len(sonuc_6) > 0:

                            st.info(f"""
                    ### 🔵 6" PRES

                    ✅ Sorti : {en_iyi_6['Sorti']}

                    ✅ Boy Sayısı : {en_iyi_6['Boy Sayısı']}

                    🔩 Kalıp : {en_iyi_6['Kalıp']}

                    💰 Kalıp Bedeli : € {en_iyi_6['Kalıp Bedeli €']}

                    📏 Biyet Boyu : {en_iyi_6['Biyet Boyu (cm)']:.2f} cm

                    ⚖️ Üretilen Kg : {en_iyi_6['Üretilen Kg']:.2f}

                    🔥 Fire : %{en_iyi_6['Fire %']:.2f}

                    📊 Biyet Kullanımı : %{en_iyi_6['Biyet Kullanım %']:.2f}
                        """)


                        else:
                            st.warning("Bu gramaj için uygun değil")


                    with col2:

                        if len(sonuc_8) > 0:

                            st.success(f"""
                        ### 🟢 8" PRES

                        ✅ Sorti : {en_iyi_8['Sorti']}

                        ✅ Boy Sayısı : {en_iyi_8['Boy Sayısı']}

                        🔩 Kalıp : {en_iyi_8['Kalıp']}

                        💰 Kalıp Bedeli : € {en_iyi_8['Kalıp Bedeli €']}

                        📏 Biyet Boyu : {en_iyi_8['Biyet Boyu (cm)']:.2f} cm

                        ⚖️ Üretilen Kg : {en_iyi_8['Üretilen Kg']:.2f}

                        🔥 Fire : %{en_iyi_8['Fire %']:.2f}

                        📊 Biyet Kullanımı : %{en_iyi_8['Biyet Kullanım %']:.2f}
                            """)

                            st.divider()

                            st.warning(f"""

                        ⭐ GENEL TAVSİYE

                        🏭 Pres : {en_iyi_8['Pres']}

                        🔢 Sorti : {en_iyi_8['Sorti']}

                        📏 Biyet Boyu : {en_iyi_8['Biyet Boyu (cm)']:.2f} cm

                        ⚖️ Üretilen Kg : {en_iyi_8['Üretilen Kg']:.2f}

                        🔥 Fire : %{en_iyi_8['Fire %']:.2f}
                                """)

                        else:
                            st.warning("Bu gramaj için uygun değil")

                else:
                    st.error("Uygun pres kombinasyonu bulunamadı.")  

                   