import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import text2emotion as te
import plotly.graph_objects as go
import numpy as np
from textblob import TextBlob

from tensorflow.keras.models import load_model

def renderPage():
    st.title("Sentiment Analysis ")
    components.html("""<hr style="height:3px;border:none;color:#333;background-color:#333; margin-bottom: 10px" /> """)
    st.subheader("Review analysis")
    st.text("Analyzing review data given by the user and find sentiments within it.")
    st.text("")
    userText = st.text_input('Sample Review', placeholder='Input text HERE')
    st.text("")
    type = st.selectbox(
        'Type of analysis',
        ('Positive/Negative/Neutral ', 'Happy/Sad/Angry/Fear/Surprise - text2emotion', 'Positive/Negative/Neutral - Model'))
    st.text("")
    if st.button('Predict'):
        if userText != "" and type is not None:
            st.text("")
            st.components.v1.html("""
                                <h3 style="color: #0284c7; font-family: Source Sans Pro, sans-serif; font-size: 28px; margin-bottom: 10px; margin-top: 50px;">Result</h3>
                                """, height=100)
            getSentiments(userText, type)

def plotPie(labels, values):
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hoverinfo="label+percent",
            textinfo="value"
        ))
    st.plotly_chart(fig)

def getPolarity(userText):
    tb = TextBlob(userText)
    polarity = round(tb.polarity, 2)
    subjectivity = round(tb.subjectivity, 2)
    if polarity > 0:
        return polarity, subjectivity, "Positive"
    elif polarity == 0:
        return polarity, subjectivity, "Neutral"
    else:
        return polarity, subjectivity, "Negative"

def getSentiments(userText, type):
    if type == 'Positive/Negative/Neutral ':
        polarity, subjectivity, status = getPolarity(userText)
        if status == "Positive":
            image = Image.open('./images/positive.PNG')
        elif status == "Negative":
            image = Image.open('./images/negative.PNG')
        else:
            image = Image.open('./images/neutral.PNG')
        col1, col2, col3 = st.columns(3)
        col1.metric("Polarity", polarity, None)         
        col2.metric("Subjectivity", subjectivity, None)
        col3.metric("Result", status, None)
        st.image(image, caption=status)
    
        # Display the results

if __name__ == "__main__":
    renderPage()
