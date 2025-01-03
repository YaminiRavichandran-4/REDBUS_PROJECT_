import streamlit as st
import pymysql
import pandas as pd

# Add custom CSS for background color
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f8ff;  /* Replace with your desired color */
    }
    </style>
    """, unsafe_allow_html=True
)

# Connect to MySQL database
def get_connection():
    return pymysql.connect(host='localhost', user='root', passwd='Umaravidaryam@2810', database='redbus')

state_to_routes ={
    "rajasthan":["Aligarh (uttar pradesh) to Jaipur (Rajasthan)","Beawar (Rajasthan) to Jaipur (Rajasthan)","Bikaner to Sikar",
    "Jaipur (Rajasthan) to Aligarh (uttar pradesh)","Jaipur (Rajasthan) to Bharatpur","Jaipur (Rajasthan) to Jodhpur",
    "Jaipur (Rajasthan) to Kota(Rajasthan)","Jaipur (Rajasthan) to Mathura","Jaipur (Rajasthan) to Pilani","Jodhpur to Ajmer",
    "Jodhpur to Beawar (Rajasthan)","Kishangarh to Jaipur (Rajasthan)","Kota(Rajasthan) to Jaipur (Rajasthan)","Kota(Rajasthan) to Udaipur",
    "Pali (Rajasthan) to Udaipur","Sikar to Bikaner","Sikar to Jaipur (Rajasthan)","Udaipur to Jaipur (Rajasthan)","Udaipur to Jodhpur",
    "Udaipur to Pali (Rajasthan)"],
    "punjab":["Amritsar to Delhi","Amritsar to Delhi Airport","Chandigarh to Patiala","Delhi Airport to Jalandhar",
    "Delhi Airport to Ludhiana","Delhi Airport to Patiala","Delhi to Amritsar","Delhi to Jalandhar","Delhi to Ludhiana",
    "Delhi to Patiala","Delhi to Phagwara","Jalandhar to Delhi","Jalandhar to Delhi Airport","Ludhiana to Delhi",
    "Ludhiana to Delhi Airport","Patiala to Amritsar","Patiala to Delhi","Phagwara to Delhi","Phagwara to Delhi Airport"],
    "assam":["Biswanath Charali to Dibrugarh", "Biswanath Charali to Guwahati", "Bokakhat to Dibrugarh", 
    "Dhubri to Guwahati", "Dibrugarh to Biswanath Charali", "Dibrugarh to Jorhat", "Dibrugarh to North Lakhimpur", 
    "Dibrugarh to Tezpur", "Gohpur to Dibrugarh", "Gohpur to Guwahati", "Guwahati to Biswanath Charali", 
    "Guwahati to Dhubri", "Guwahati to Gohpur", "Guwahati to Kaliabor", "Guwahati to Nagaon (Assam)",
     "Guwahati to Silchar", "Moran to Tezpur", "Nagaon (Assam) to Guwahati", "North Lakhimpur to Guwahati", 
     "North Lakhimpur to Jorhat", "North Lakhimpur to Nagaon (Assam)", "North Lakhimpur to Sibsagar (Assam)", 
     "North Lakhimpur to Tezpur", "Tezpur to Dibrugarh", "Tezpur to Guwahati", "Tezpur to Moran", "Tezpur to North Lakhimpur", 
     "Tezpur to Tinsukia", "Tinsukia to Jorhat", "Tinsukia to Tezpur"], 
     "kadamba":["Bangalore to Goa", "Belagavi to Goa", "Belagavi to Marcel", "Belagavi to Ponda", 
     "Belagavi to Saquelim", "Calangute (goa) to Goa Airport", "Calangute (goa) to Panaji", "Goa Airport to Calangute (goa)",
     "Goa Airport to Panaji", "Goa to Bangalore", "Goa to Belagavi", "Goa to Kolhapur(Maharashtra)", "Goa to Miraj",
     "Goa to Mopa Airport", "Goa to Mumbai", "Goa to Pandharpur", "Goa to Pune", "Goa to Sangli", "Goa to Sangola (Solapur)",
     "Goa to Satara", "Goa to Shivamogga", "Goa to Solapur", "Mopa Airport to Calangute (goa)", "Mopa Airport to Goa",
     "Mopa Airport to Margao", "Mopa Airport to Panaji", "Mumbai to Goa", "Panaji to Goa Airport", "Panaji to Mopa Airport", 
     "Pandharpur to Goa", "Pune to Goa", "Sangola (Solapur) to Goa", "Shirdi to Goa", "Shivamogga to Goa", "Solapur to Goa"],
     "jammukashmir":["Delhi to Srinagar", "Jammu (J and K) to Katra (Jammu and Kashmir)", "Katra (Jammu and Kashmir) to Jammu (J and K)"],
     "andhra":["Amalapuram to Visakhapatnam", "Anantapur (Andhra Pradesh) to Bangalore", "Bangalore to Anantapur (Andhra Pradesh)",
     "Bangalore to Chittoor (Andhra Pradesh)", "Bangalore to Kadapa", "Bangalore to Kadiri", "Bangalore to Madanapalli", 
     "Bangalore to Rayachoti", "Bangalore to Tirupati", "Chennai to Tirupati", "Chittoor (Andhra Pradesh) to Bangalore", 
     "Eluru to Hyderabad", "Guntur (Andhra Pradesh) to Hyderabad", "Hyderabad to Eluru", "Hyderabad to Guntur (Andhra Pradesh)",
     "Hyderabad to Kurnool", "Hyderabad to Macherla (Andhra Pradesh)", "Hyderabad to Markapuram", "Hyderabad to Nandyal",
     "Hyderabad to Narasaraopet", "Hyderabad to Ongole", "Hyderabad to Vijayawada", "Hyderabad to Vinukonda", "Kadapa to Bangalore",
     "Kadiri to Bangalore", "Kakinada to Vijayawada", "Kakinada to Visakhapatnam", "Kurnool to Bangalore", "Kurnool to Hyderabad", 
     "Kurnool to Vijayawada", "Macherla (Andhra Pradesh) to Hyderabad", "Madanapalli to Bangalore", "Narasaraopet to Hyderabad", 
     "Nellore to Bangalore", "Ongole to Hyderabad", "Rajahmundry to Hyderabad", "Rajahmundry to Vijayawada", 
     "Rajahmundry to Visakhapatnam", "Rayachoti to Bangalore", "Tadipatri to Bangalore", "Tirupati to Bangalore", 
     "Tirupati to Chennai", "Vijayawada to Hyderabad", "Vijayawada to Visakhapatnam", "Visakhapatnam to Amalapuram",
     "Visakhapatnam to Kakinada", "Visakhapatnam to Rajahmundry", "Visakhapatnam to Vijayawada"],
     "bihar":["Agra to Motihari", "Balmiki Nagar (Bihar) to Patna (Bihar)", "Bettiah to Patna (Bihar)", "Delhi to Motihari", 
     "Gopalganj (Bihar) to Delhi", "Gopalganj (Bihar) to Lucknow", "Hazaribagh to Muzaffarpur (Bihar)", "Hazaribagh to Patna (Bihar)", 
     "Katihar to Patna (Bihar)", "Lucknow to Gopalganj (Bihar)", "Lucknow to Motihari", "Motihari to Agra", "Motihari to Delhi",
     "Motihari to Lucknow", "Muzaffarpur (Bihar) to Hazaribagh", "Muzaffarpur (Bihar) to Ranchi", "Patna (Bihar) to Araria (Bihar)", 
     "Patna (Bihar) to Balmiki Nagar (Bihar)", "Patna (Bihar) to Bettiah", "Patna (Bihar) to Darbhanga", "Patna (Bihar) to Forbesganj", 
     "Patna (Bihar) to Hazaribagh", "Patna (Bihar) to Katihar", "Patna (Bihar) to Motihari", "Patna (Bihar) to Muzaffarpur (Bihar)", 
     "Patna (Bihar) to Purnea", "Patna (Bihar) to Ramgarh (Jharkhand)", "Patna (Bihar) to Ranchi", "Patna (Bihar) to Saharsa", 
     "Patna (Bihar) to Simrahi Bazar (Bihar)", "Purnea to Patna (Bihar)", "Ranchi to Bihar Sharif", "Ranchi to Muzaffarpur (Bihar)", 
     "Ranchi to Patna (Bihar)"],
     "kerala":["Bangalore to Kalpetta (Kerala)", "Bangalore to Kannur (Kerala)", "Bangalore to Kozhikode", "Ernakulam to Kozhikode", 
     "Kalpetta (Kerala) to Bangalore", "Kottayam to Kozhikode", "Kozhikode to Aluva", "Kozhikode to Bangalore", "Kozhikode to Ernakulam", 
     "Kozhikode to Kottayam", "Kozhikode to Mysore", "Kozhikode to Thiruvananthapuram", "Kozhikode to Thrissur", "Mysore to Kozhikode", 
     "Thiruvananthapuram to Kozhikode", "Thrissur to Kozhikode"],
     "telangana":["Godavarikhani to Hyderabad", "Guntur (Andhra Pradesh) to Hyderabad", "Hyderabad to Adilabad", 
     "Hyderabad to Anantapur (Andhra Pradesh)", "Hyderabad to Armoor", "Hyderabad to Bhadrachalam", "Hyderabad to Godavarikhani", 
     "Hyderabad to Guntur (Andhra Pradesh)", "Hyderabad to Karimnagar", "Hyderabad to Khammam", "Hyderabad to Kodad", 
     "Hyderabad to Kothagudem", "Hyderabad to Mancherial", "Hyderabad to Nirmal", "Hyderabad to Ongole", "Hyderabad to Srisailam", 
     "Hyderabad to Tirupati", "Hyderabad to Vijayawada", "Hyderabad to Warangal", "Jagityal to Hyderabad", "Karimnagar to Hyderabad", 
     "Khammam to Hyderabad", "Kodad to Hyderabad", "Kothagudem to Hyderabad", "Peddapalli (Telangana) to Hyderabad"],
     "westbengal":["Digha to Kolkata", "Kolkata to Digha", "Kolkata to Mandarmani", "Mandarmani to Kolkata"]






}    

# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_route_names(connection, starting_letter):
    query = f"SELECT DISTINCT Route_Name FROM bus_routes WHERE Route_Name LIKE '{starting_letter}%' ORDER BY Route_Name"
    route_names = pd.read_sql(query, connection)['Route_Name'].tolist()
    return route_names

# Function to fetch data from MySQL based on selected Route_Name, price sort order, price range, and seat availability
def fetch_data(connection, route_name, price_sort_order, min_price, max_price, min_seats):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"""
        SELECT * FROM bus_routes 
        WHERE Route_Name = %s 
        AND Price BETWEEN %s AND %s
        AND Seat_Availability >= %s
        ORDER BY Star_Rating DESC, Price {price_sort_order_sql}
    """
    df = pd.read_sql(query, connection, params=(route_name, min_price, max_price, min_seats))
    return df

# Function to get the maximum price from the database
def get_max_price(connection):
    query = "SELECT MAX(Price) FROM bus_routes"
    max_price = pd.read_sql(query, connection).iloc[0, 0]
    return int(max_price)  # Ensure max_price is an integer

# Function to classify bus types based on keywords in the Bus_Type column
def classify_bus_type(bus_type):
    bus_type = bus_type.lower()
    if 'ac seater' in bus_type or 'a/c seater' in bus_type:
        return 'AC Seater'
    elif 'ac sleeper' in bus_type or 'a/c sleeper' in bus_type:
        return 'AC Sleeper'
    elif 'non-ac' in bus_type and 'seater' in bus_type:
        return 'Non-AC Seater'
    elif 'non-ac' in bus_type and 'sleeper' in bus_type:
        return 'Non-AC Sleeper'
    else:
        return 'Other'

# Function to filter data based on Star_Rating, Bus_Type, and seat availability
def filter_data(df, star_ratings, bus_types):
    filtered_df = df[df['Star_Rating'].isin(star_ratings) & df['Classified_Bus_Type'].isin(bus_types)]
    return filtered_df

# Home Page
def home_page():
    st.title("Welcome to the Online Bus Tickets Booking App 🚌")
    st.image(r"C:\Users\YAMINI RAVICHANDRAN\Downloads\busj.jpg")
    st.subheader('Synopsis:')
    st.write("""
        This app allows you to search for bus routes, filter them by price, seats, and ratings,
        and get detailed information about the available buses. You can navigate through 
        different pages to find the routes, apply filters, and explore the features.Skills take away from this project are 
        Web Scraping using Selenium, Python, Streamlit , SQL. First I have done web scraping using selenium. Later applied python coding to 
        create a SQL database. And Streamlit for deploying the derived data.
    """)
    st.subheader('Problem Statement:')
    st.markdown("""
                The "Redbus Data Scraping and Filtering with Streamlit Application"
                 aims to revolutionize the transportation industry by providing a comprehensive 
                 solution for collecting, analyzing, and visualizing bus travel data.
                  By utilizing Selenium for web scraping, this project automates the extraction
                   of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. 
                   By streamlining data collection and providing powerful tools for data-driven decision-making,
                    this project can significantly improve operational efficiency and strategic 
                    planning in the transportation industry.
                """)


# About Page
def about_page():
    st.title("About the Developer")
    st.write("""
        This app is Designed by Yamini Ravichandran.Iam from Coimbatore,TamilNadu. I have completed my Undergraduate from
        PSG College of Arts and Science in Bachelors of Commerce . I have worked in Data Analysis Company called
        NielsenIq in Chennai for two and half years. Iam doing my Datascience course in GUVI. For my capstone Project I have done this Web page
        for filtering bus routes.
    """)
    st.image(r"C:\Users\YAMINI RAVICHANDRAN\Downloads\th.jpg")

# Route Selection Page
def route_page():
    st.header('Online Bus Tickets Booking 🚌')

    connection = get_connection()

    try:
        state_list = list(state_to_routes.keys())
        selected_state = st.sidebar.selectbox('Select State', state_list)

        # Get the maximum price from the database and convert to integer
        max_price = get_max_price(connection)

        # Sidebar - Price slider to filter by price range (dynamically set max price)
        min_price, max_price_slider = st.sidebar.slider('Select Price Range', 0, max_price, (0, max_price), step=50)

        # Sidebar - Seat availability filter (minimum seats)
        min_seats = st.sidebar.slider('Minimum Available Seats', 1, 100, 1)
        
        if selected_state:
            routes_in_state = state_to_routes[selected_state]
            st.write(f"### Routes available in {selected_state}")

            selected_route = st.sidebar.radio('Select Route Name', routes_in_state)  # Corrected usage

            if selected_route:
                price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                # Fetch data based on selected Route_Name, price sort order, price range, and seat availability
                data = fetch_data(connection, selected_route, price_sort_order, min_price, max_price_slider, min_seats)

                if not data.empty:
                    data['Classified_Bus_Type'] = data['Bus_Type'].apply(classify_bus_type)  # Classify bus types

                    st.write(f"### Data for Route: {selected_route}")
                    st.write(data)

                    star_ratings = data['Star_Rating'].unique().tolist()
                    selected_ratings = st.multiselect('Filter by Star Rating', star_ratings)

                    classified_bus_types = ['AC Seater', 'AC Sleeper', 'Non-AC Seater', 'Non-AC Sleeper', 'Other']
                    selected_bus_types = st.multiselect('Filter by Bus Type', classified_bus_types)

                    if selected_ratings and selected_bus_types:
                        filtered_data = filter_data(data, selected_ratings, selected_bus_types)

                        # Limit the number of rows (e.g., show only the first 10 rows)
                        filtered_data = filtered_data.head(10)

                        st.write(f"### Filtered Data for Star Rating: {selected_ratings} and Bus Type: {selected_bus_types}")
                        st.dataframe(filtered_data)  # Display all columns

            else:
                st.write(f"No data found for Route: {selected_route} with the specified price sort order, price range, and seat availability.")
        else:
            st.write("No states found")
    
    finally:
        connection.close()

# Main function to display content based on selected page
def main():
    page = st.sidebar.radio("Select a Page", ["Home", "Route Selection", "About"])

    if page == "Home":
        home_page()
    elif page == "Route Selection":
        route_page()
    elif page == "About":
        about_page()

if __name__ == '__main__':
    main()

   