import streamlit as st


def calculate(building_price, building_size, basement_size,
            basement_livable, shareable_space, related_expenses,
            renovation_cost, renovation_size,unexpected_expenses, average_sale_price):

    try:
        building_minus_basement = building_size - basement_size
        net_building_size = building_minus_basement - (building_minus_basement*shareable_space/100)
        building_price_no_unexpected = (building_price + (building_price*related_expenses/100) +
                                (renovation_cost * renovation_size))
        final_building_price = building_price_no_unexpected + (building_price_no_unexpected*unexpected_expenses/100)
        net_building_price_per_meter = final_building_price/net_building_size
        total_sale_price = average_sale_price*net_building_size
        revenue = total_sale_price - final_building_price
        revenue_percent = (average_sale_price - net_building_price_per_meter)/net_building_price_per_meter*100

        if basement_livable:
            net_basement_size = basement_size - (basement_size*15/100)
            basement_price = average_sale_price - (average_sale_price*30/100)
            total_sale_price_with_basement = total_sale_price + (basement_price*net_basement_size)
            st.session_state.result_text = f"""
                                        Total Building Sale Price: {total_sale_price:,.2f}€
                                        
                                        Building Cost Per Meter: {net_building_price_per_meter:,.2f}€
                                        
                                        Total Basement Sale Price: {basement_price*net_basement_size:,.2f}€
                                        
                                        Basement Cost Per Meter: {basement_price/net_basement_size:,.2f}€
                                        
                                        Total Sale Price: {total_sale_price_with_basement:,.2f}€
                                        
                                        Revenue: {(total_sale_price_with_basement - final_building_price)/
                                                  final_building_price*100:.2f}%
                                        """
        else:
            st.session_state.result_text = f"""
                                        Total Building Sale Price: {total_sale_price:,.2f}€
                                        
                                        Building Cost Per Meter: {net_building_price_per_meter:,.2f}€
                                        
                                        Revenue: {revenue_percent:.2f}%                
                                        """
    except ZeroDivisionError:
        pass


if "result_text" not in st.session_state:
    st.session_state.result_text = ""

row1 = st.columns(4)
row2 = st.columns(4)
row3 = st.columns(2)

with st.container():
    building_price = row1[0].number_input("Building Price (€)", min_value=0)
    building_size = row1[1].number_input("Building Size ($m^2$)", min_value=0)
    basement_size = row1[2].number_input("Basement Size ($m^2$)", min_value=0)
    with row1[3]:
        st.write("#")
        basement_livable = st.checkbox("Basement Livable", key="basement_livable")

with st.container():
    shareable_space = row2[0].number_input("Shareable Space (%)", min_value=0, max_value=100)
    related_expenses = row2[1].number_input("Related Expenses (%)", min_value=0, max_value=100)
    renovation_cost = row2[2].number_input("Renovation Cost (€ Per $m^2$)", min_value=0)
    renovation_size = row2[3].number_input("Size To Renovate ($m^2$)", min_value=0, max_value=building_size)

with st.container():
    unexpected_expenses = row3[0].number_input("Unexpected Expenses (%)", min_value=0, max_value=100)
    average_sale_price = row3[1].number_input("Average Sale Price In Area (€)", min_value=0)

with st.container():
    st.button("Calculate", on_click=calculate, args=(building_price, building_size, basement_size,
                                                     basement_livable, shareable_space, related_expenses,
                                                     renovation_cost, renovation_size,
                                                     unexpected_expenses, average_sale_price))

with st.container():
    st.write(st.session_state.result_text)
