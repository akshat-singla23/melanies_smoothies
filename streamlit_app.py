# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Ypur Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you would like in your smoothie.
    """
)



name_on_order = st.text_input('Name on the order:')
st.write('The name on your order will be:', name_on_order)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)



# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingridents_list = st.multiselect(
    'Choose upto 5 ingridents',
    my_dataframe,
    max_selections = 5
)
if ingridents_list:
    st.write(ingridents_list)
    st.text(ingridents_list)
    ingridents_string = ''
    for fruit_chosen in ingridents_list:
        ingridents_string += fruit_chosen + ' '
    st.write(ingridents_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, order_filled)
            values ('""" + ingridents_string + """','"""+name_on_order+ """','"""+'FALSE'+ """')"""
    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
