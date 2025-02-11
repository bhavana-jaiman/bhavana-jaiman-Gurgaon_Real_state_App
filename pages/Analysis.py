import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle
from wordcloud import wordcloud


st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')
st.markdown("you can check average price of every sector here! ")
new_df = pd.read_csv("datasets/data_viz1.csv")

feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))

group_df =  new_df.groupby('sector')[['price','price_per_sqft','built_up_area','Latitude','Longitude']].mean()
st.header("Sector Price per sqft GeoMap")
fig = px.scatter_mapbox(group_df, lat="Latitude", lon="Longitude",     color="price_per_sqft", size="built_up_area",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                   mapbox_style = "open-street-map", width = 1200,
                        height = 700, hover_name = group_df.index)
fig.show()

st.plotly_chart(fig, use_container_width = True)
# lattitude(distance north or south) or longitude(distance east or west)
# if we able to find latlong of all four cordinates of sector we can make chropleth map
st.markdown("you cam check animities here!")


plt.rcParams["font.family"]=="Arial"
st.header("features WordCloud")
wordcloud = WordCloud(width = 800, height = 800,       # wordcloud object
                     background_color = 'white',
                     stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

plt.figure(figsize = (8,8), facecolor = None)
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)               # Adjusts the layout to remove unnecessary padding around the word cloud.
st.pyplot()

# now we can do give a dropdown for particular sector


st.header("Area Vs Price")
property_type = st.selectbox('Select Property Type',['flats','house'])
if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x='built_up_area', y='price', color='bedRoom', title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x='built_up_area', y='price', color='bedRoom', title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header("BHK pie Chart")
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')
selected_sector = st.selectbox("Select Sector", sector_options)
if selected_sector == 'overall':
    fig2 = px.pie(new_df, names="bedRoom")
    # show the fig
    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names = "bedRoom")
    # show the fig
    st.plotly_chart(fig2, use_container_width=True)

st.header("side by side BHK comparison")
fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x ='bedRoom', y = "price", title = "BHK Price Range")
st.plotly_chart(fig3, use_container_width = True)


st.header("Side by Side Distplot for property type")

fig4 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'], label = 'house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label = 'flat')
plt.legend()
st.pyplot(fig4)
