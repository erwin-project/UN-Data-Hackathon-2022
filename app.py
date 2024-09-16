from streamlit_multipage import MultiPage
from utils import check_email, check_account, update_json, replace_json, machine_learning as ml
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from utils import visualization as vs
import warnings
warnings.filterwarnings("ignore")

app = MultiPage()


def sign_up(st, **state):
    placeholder = st.empty()

    with placeholder.form("Sign Up"):
        image = Image.open("images/logo_sensei_data.png")
        st1, st2, st3 = st.columns(3)

        with st2:
            st.image(image)

        st.warning("Please sign up your account!")

        # name_ = state["name"] if "name" in state else ""
        name = st.text_input("Name: ")

        # username_ = state["username"] if "username" in state else ""
        username = st.text_input("Username: ")

        # email_ = state["email"] if "email" in state else ""
        email = st.text_input("Email")

        # password_ = state["password"] if "password" in state else ""
        password = st.text_input("Password", type="password")

        save = st.form_submit_button("Save")

    if save and check_email(email) == "valid email":
        placeholder.empty()
        st.success("Hello " + name + ", your profile has been save successfully")
        MultiPage.save({"name": name,
                        "username": username,
                        "email": email,
                        "password": password,
                        "login": "True",
                        "edit": True})

        update_json(name, username, email, password)

    elif save and check_email(email) == "duplicate email":
        st.success("Hello " + name + ", your profile hasn't been save successfully because your email same with other!")

    elif save and check_email(email) == "invalid email":
        st.success("Hello " + name + ", your profile hasn't been save successfully because your email invalid!")
    else:
        pass


def login(st, **state):
    st.snow()
    # Create an empty container
    placeholder = st.empty()

    try:
        # Insert a form in the container
        with placeholder.form("login"):
            image = Image.open("images/logo_sensei_data.png")
            st1, st2, st3 = st.columns(3)

            with st2:
                st.image(image)

            st.markdown("#### Login Sensei Data Website")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            st.write("Are you ready registered account in this app? If you don't yet, please sign up your account!")

            name, username, status = check_account(email, password)

        if submit and status == 'register':
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.success("Login successful")
            MultiPage.save({"name": name,
                            "username": username,
                            "email": email,
                            "password": password,
                            "login": "True"})

        elif submit and status == 'wrong password':
            st.error("Login failed because your password is wrong!")

        elif submit and status == 'not register':
            st.error("You haven't registered to this app! Please sign up your account!")

        else:
            pass

    except:
        st.error("Please login with your registered email!")


def dashboard(st, **state):
    # Title
    image = Image.open("images/logo_sensei_data.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Dashboard</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data Insight"])

    with tab1:
        data_temp = pd.read_excel("data/temperature/temperature_indonesia.xlsx",
                                  engine="openpyxl")

        st1, st2 = st.columns(2)
        with st1:
            kind = st.radio("Please select kind of crops do you want!",
                            ["Plantations",
                             "Agriculture",
                             "Vegetables"])
        with st2:
            if kind == "Plantations":
                data = pd.read_excel("data/produktivitas/plantation_fix.xlsx",
                                     engine="openpyxl")
            elif kind == "Agriculture":
                data = pd.read_excel("data/produktivitas/rice_fix.xlsx",
                                     engine="openpyxl")
            elif kind == "Vegetables":
                data = pd.read_excel("data/produktivitas/vegetables_fix.xlsx",
                                     engine="openpyxl")

            commodity = st.selectbox("Please select commodity do you want!",
                                     data['commodity'].unique())

        st3, st4 = st.columns(2)
        with st3:
            fig1, ax1 = vs.visualization_data(data_temp,
                                              "year",
                                              "mean_temperature",
                                              "Year",
                                              "Temperature $(^o C)$",
                                              "Graph Temperature Indonesia from 1901 - 2021")

            st.pyplot(fig1)

        with st4:
            dataset = data.groupby(["commodity", "year"],
                                   as_index=False).aggregate({'total_productivity': np.sum})
            fig2, ax2 = vs.visualization_data(dataset[dataset["commodity"] == commodity],
                                              "year",
                                              "total_productivity",
                                              "Year",
                                              "Production (TON)",
                                              str("Graph " + kind + " Production in West Java from 2013 - 2021"))

            st.pyplot(fig2)

    with tab2:
        kind = st.selectbox("Please select kind of crops do you want!",
                            ["All",
                             "Plantations",
                             "Agriculture",
                             "Vegetables"])

        dataset = ml.add_rate(kind)

        dec = dataset[dataset["rate_change"] < -1]
        inc = dataset[dataset["rate_change"] > 1]
        net = dataset[(dataset["rate_change"] > -1) & (dataset["rate_change"] < 1)]

        labels = ["increase", "decrease", "stable"]
        sized = [len(inc), len(dec), len(net)]

        fig, ax = vs.chart_pie(labels, sized, kind)

        st.pyplot(fig)

        st1, st2, st3 = st.columns(3)
        with st1:
            st.markdown("List of Commodity Increase")
            st.dataframe(inc["commodity"].reset_index().drop('index', axis=1))
        with st2:
            st.markdown("List of Commodity Decrease")
            st.dataframe(dec["commodity"].reset_index().drop('index', axis=1))
        with st3:
            st.markdown("List of Commodity Neutral")
            st.dataframe(net["commodity"].reset_index().drop('index', axis=1))


def projection(st, **state):
    # Title
    image = Image.open("images/logo_sensei_data.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Projection</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    # Start Code Adit

    # End Code Adit


def deployment_model(st, **state):
    # Title
    image = Image.open("images/logo_sensei_data.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Projection</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    # Start Code Adit

    # End Code Adit


def report(st, **state):
    # Title
    image = Image.open("images/logo_sensei_data.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Messages Report</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    placeholder = st.empty()

    with placeholder.form("Message"):
        email = st.text_input("Email")
        text = st.text_area("Messages")
        submit = st.form_submit_button("Send")

    if submit and check_email(email) == "valid email" or check_email(email) == "duplicate email":
        placeholder.empty()
        st.success("Before your message will be send, please confirm your messages again!")
        vals = st.write("<form action= 'https://formspree.io/f/xeqdqdon' "
                        "method='POST'>"
                        "<label> Email: <br> <input type='email' name='email' value='" + str(email) +
                        "'style='width:705px; height:50px;'></label>"
                        "<br> <br>"
                        "<label> Message: <br> <textarea name='Messages' value='" + str(text) +
                        "'style='width:705px; height:200px;'></textarea></label>"
                        "<br> <br>"
                        "<button type='submit'>Confirm</button>"
                        "</form>", unsafe_allow_html=True)

        if vals is not None:
            st.success("Your messages has been send successfully!")

    elif submit and check_email(email) == "invalid email":
        st.success("Your message hasn't been send successfully because email receiver not in list")

    else:
        pass


def account(st, **state):
    # Title
    image = Image.open("images/logo_sensei_data.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Account Setting</h3>", unsafe_allow_html=True)

    restriction = state["login"]
    password = state["password"]

    if ("login" not in state or restriction == "False") or ("password" not in state):
        st.warning("Please login with your registered email!")
        return

    placeholder = st.empty()

    st.write("Do you want to edit your account?")
    edited = st.button("Edit")
    state["edit"] = np.invert(edited)

    old_email = state['email']

    with placeholder.form("Account"):
        name_ = state["name"] if "name" in state else ""
        name = st.text_input("Name", placeholder=name_, disabled=state["edit"])

        username_ = state["username"] if "username" in state else ""
        username = st.text_input("Username", placeholder=username_, disabled=state["edit"])

        email_ = state["email"] if "email" in state else ""
        email = st.text_input("Email", placeholder=email_, disabled=state["edit"])

        if edited:
            current_password = st.text_input("Old Password", type="password", disabled=state["edit"])
        else:
            current_password = password

        # current_password_ = state["password"] if "password" in state else ""
        new_password = st.text_input("New Password", type="password", disabled=state["edit"])

        save = st.form_submit_button("Save")

    if save and current_password == password:
        st.success("Hi " + name + ", your profile has been update successfully")
        MultiPage.save({"name": name,
                        "username": username,
                        "email": email,
                        "password": new_password,
                        "edit": True})

        replace_json(name, username, old_email, email, new_password)

    elif save and current_password != password:
        st.success("Hi " + name + ", your profile hasn't been update successfully because your current password"
                                  " doesn't match!")

    elif save and check_email(email) == "invalid email":
        st.success("Hi " + name + ", your profile hasn't been update successfully because your email invalid!")

    else:
        pass


def logout(st, **state):
    st.success("Your account has been log out from this app")
    MultiPage.save({"login": "False"})


app.st = st

app.navbar_name = "Menu"
app.navbar_style = "VerticalButton"

app.hide_menu = False
app.hide_navigation = True

app.add_app("Sign Up", sign_up)
app.add_app("Login", login)
app.add_app("Dashboard", dashboard)
app.add_app("Projection", projection)
app.add_app("Deployment Model", deployment_model)
app.add_app("Report", report)
app.add_app("Account Setting", account)
app.add_app("Logout", logout)

app.run()
