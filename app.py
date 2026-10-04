import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Gruppo Vartec - Gare & Offerte Tecniche", layout="centered")

st.title("Gruppo Vartec")
st.subheader("Analisi Gare d'Appalto & Generatore Offerte Tecniche")

# Barra laterale per caricare il bando ufficiale
st.sidebar.header("📁 Documentazione di Gara")
bando_file = st.sidebar.file_uploader("Carica Bando / Capitolato (PDF)", type=["pdf"])

tab_analisi, tab_offerta = st.tabs(["📊 Analisi Parametri Gara", "📝 Generatore Offerta Tecnica"])

with tab_analisi:
    st.header("Valutazione di Convenienza e Ribasso")
    
    if bando_file:
        st.success(f"Bando caricato con successo: **{bando_file.name}**")
    else:
        st.info("💡 Puoi caricare il PDF del bando o del capitolato dalla barra laterale per tenerlo associato alla simulazione.")

    importo_base = st.number_input("Importo Base d'Asta (€):", min_value=0.0, value=200000.0, step=5000.0)
    ribasso_offerto = st.slider("Percentuale di Ribasso (%)", min_value=0.0, max_value=40.0, value=12.5, step=0.1)
    
    peso_eco = st.slider("Peso Offerta Economica (%)", min_value=10, max_value=90, value=70)
    peso_tec = 100 - peso_eco
    st.info(f"Rapporto di valutazione: **Economica {peso_eco}%** - **Tecnica {peso_tec}%**")

    if st.button("Calcola Simulazione Gara"):
        valore_ribasso = importo_base * (ribasso_offerto / 100.0)
        importo_netto = importo_base - valore_ribasso
        
        st.success("Analisi completata!")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Valore del Ribasso", value=f"{valore_ribasso:,.2f} €")
        with col2:
            st.metric(label="Importo Netto Offerta", value=f"{importo_netto:,.2f} €")

with tab_offerta:
    st.header("Composizione Relazione Tecnica")
    st.write("Seleziona le migliorie e le specifiche da inserire nella relazione tecnica da allegare alla documentazione di gara.")

    oggetto_lavori = st.text_input("Oggetto / Titolo dei Lavori:", value="Lavori di realizzazione fondazioni e strutture in c.a.")
    
    migliorie = st.multiselect("Seleziona Miglioramenti Tecnici da Offrire:", [
        "Utilizzo di calcestruzzi a ridotto impatto ambientale e alte prestazioni",
        "Maggiore spessore dell'armatura e dei copriferro rispetto al minimo di capitolato",
        "Procedure avanzate di casseratura con sistemi Faresin per finiture faccia a vista",
        "Riduzione dei tempi di esecuzione del cronoprogramma del 15%",
        "Maggiore attenzione alla sicurezza con monitoraggio costante delle linee vita e dei parapetti provvisori"
    ], default=[
        "Utilizzo di calcestruzzi a ridotto impatto ambientale e alte prestazioni",
        "Riduzione dei tempi di esecuzione del cronoprogramma del 15%"
    ])

    note_personalizzate = st.text_area("Note specifiche di cantiere o particolari costruttivi:", value="Particolare cura nella gestione degli scavi e nella compattazione dei sottofondi per garantire la massima stabilità strutturale.")

    def genera_pdf_offerta(oggetto, lista_migliorie, note):
        pdf_path = "offerta_tecnica_vartec.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('Title', parent=styles['Normal'], fontSize=18, leading=22, alignment=1, textColor=colors.HexColor('#051e3e'), fontName='Helvetica-Bold')
        h2_style = ParagraphStyle('H2', parent=styles['Normal'], fontSize=12, leading=16, textColor=colors.HexColor('#051e3e'), fontName='Helvetica-Bold')
        normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=14)

        story.append(Spacer(1, 10))
        story.append(Paragraph("GRUPPO VARTEC - RELAZIONE TECNICA DI OFFERTA", title_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(f"<b>Oggetto:</b> {oggetto}", normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("1. Premessa e Metodologia Esecutiva", h2_style))
        story.append(Paragraph("L'impresa Gruppo Vartec vanta una consolidata esperienza nel settore delle costruzioni edili, garantendo standard elevati di qualità, rispetto dei tempi contrattuali e rigorosa applicazione delle normative di sicurezza.", normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("2. Proposte migliorative offerte", h2_style))
        for m in lista_migliorie:
            story.append(Paragraph(f"• {m}", normal_style))
            story.append(Spacer(1, 4))
            
        story.append(Spacer(1, 6))
        story.append(Paragraph("3. Specifiche Tecniche e Operative", h2_style))
        story.append(Paragraph(note, normal_style))
        
        doc.build(story)
        return pdf_path

    if st.button("Genera Documento Offerta Tecnica in PDF"):
        path_pdf = genera_pdf_offerta(oggetto_lavori, migliorie, note_personalizzate)
        with open(path_pdf, "rb") as file_pdf:
            st.download_button(
                label="Scarica Relazione Tecnica PDF",
                data=file_pdf,
                file_name="Offerta_Tecnica_Vartec.pdf",
                mime="application/pdf"
            )
