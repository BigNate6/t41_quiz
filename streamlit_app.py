import streamlit as st

# --- DATA STRUCTURES ---
boldface_data = {
    "EMERGENCY ENGINE SHUTDOWN ON THE GROUND": [
        "MIXTURE - FULL LEAN",
        "FUEL SHUTOFF KNOB - PULL OUT",
        "IGNITION SWITCH - OFF",
        "MASTER SWITCH - OFF"
    ],
    "ABORT": [
        "THROTTLE - IDLE",
        "BRAKES - AS REQUIRED"
    ],
    "ENGINE FAILURE IMMEDIATELY AFTER TAKEOFF/FORCED LANDING": [
        "GLIDE - ESTABLISH",
        "MIXTURE - FULL LEAN",
        "FUEL SHUTOFF KNOB - PULL OUT",
        "IGNITION SWITCH - OFF",
        "FLAPS - AS REQUIRED",
        "MASTER SWITCH - OFF"
    ],
    "ENGINE FIRE DURING FLIGHT": [
        "MIXTURE - FULL LEAN",
        "FUEL SHUTOFF KNOB - PULL OUT",
        "IGNITION SWITCH - OFF",
        "GLIDE - ESTABLISH",
        "FLAPS - AS REQUIRED",
        "MASTER SWITCH - OFF"
    ],
    "ELECTRICAL FIRE/HIGH AMMETER READING": [
        "MASTER SWITCH - OFF"
    ]
}

ops_limits_data = {
    "AIRSPEED LIMITATIONS (KIAS)": {
        "Maximum (glide, dive, or smooth air)": "158",
        "Caution Range": "126-158",
        "Normal Operating Range": "55-126",
        "Max Flaps Extended": "87",
        "Maneuvering Speed*": "110"
    },
    "FUEL FLOW INDICATOR": {
        "Normal Operating Range": "4.5-11.5 gal/hr",
        "Minimum": "3.0 psi",
        "Maximum": "18.5 psi"
    },
    "FUEL QUANTITY INDICATORS (US Gal)": {
        "Full Mark (total fuel on board)": "52",
        "Usable Fuel (level flight)": "51",
        "Usable Fuel (all flight conditions)": "46",
        "Minimum Fuel (Usable)": "9",
        "Emergency Fuel (Usable)": "6"
    },
    "CYLINDER HEAD TEMPERATURE (°F)": {
        "Normal Operating Range": "200-400",
        "Maximum Allowable": "460"
    },
    "SUCTION GAUGE (\"Hg)": {
        "At 1800 RPM or Above": "4.6-5.4"
    },
    "OIL TEMPERATURE GAUGE (°F)": {
        "Normal Operating Range": "0-240",
        "Maximum Allowable": "240"
    },
    "AMMETER GAUGE": {
        "Normal": "0 to +2 needle widths",
        "Maximum (for flight)": "+2 needle widths"
    },
    "OIL PRESSURE GAUGE (PSI)": {
        "Minimum Idling": "10",
        "Normal Operating Range": "30-60",
        "Maximum": "100",
        "Positive indication within ___ of engine start": "30 seconds",
        "(___ when the temperature is below 0°F)": "1 minute",
        "If engine cold soaked, up to ___ may be required for indications": "10 minutes"
    },
    "LANDING/TAXI LIGHTS (MIN)": {
        "Taxi Light (On Ground)": "15",
        "Landing Light (On Ground)*": "5"
    },
    "OIL CAPACITY (QTS)": {
        "Minimum for Engine Start": "6",
        "Flight <3 Hours": "7",
        "Flight >3 Hours": "8",
        "Maximum": "10"
    },
    "PROHIBITED MANEUVERS": {
        "1.": "Whip stalls",
        "2.": "Maneuvers requiring >60° bank or >50° pitch",
        "3.": "Zero or negative G flight",
        "4.": "Slips w/ >30° flaps extended",
        "5.": "Planned flight into known or forecast icing"
    },
    "STARTING": {
        "If engine does not start within ___ of cumulative cranking": "30 seconds",
        "...allow starter to cool for ___": "3 minutes"
    },
    "TACHOMETER (RPM)": {
        "Normal Operating Range": "2200-2600",
        "Maximum Allowable": "2800",
        "Minimum for Takeoff": "2650",
        "Minimum Idle": "850+-50",
        "Engine Runup: Maximum Allowable Magneto Drop": "150",
        "Engine Runup: Maximum Magneto Difference": "50"
    },
    "WIND LIMITS (KTS)": {
        "Maximum Wind for Takeoff": "26",
        "Maximum Wind for Landing": "35",
        "Maximum Tailwind (Takeoff or Landing)": "10",
        "Taxi Cease (Steady State or Gusts)": ">35",
        "Maximum Crosswind (Takeoff or Landing): 0-20° Flaps": "15",
        "Maximum Crosswind (Takeoff or Landing): >20° Flaps": "10"
    },
    "MANIFOLD PRESSURE GAUGE (\"Hg)": {
        "Normal Operating Range": "15-25"
    },
    "G-LIMITS (Gs)": {
        "Normal Category (flaps up)": "-1.52 to +3.8",
        "Utility Category (flaps up)": "-1.76 to +4.4",
        "All Categories (flaps down)": "0 to +3.5"
    },
    "AURAL STALL WARNING (KTS)": {
        "Range Above Stalling Speed": "5 to 10"
    }
}

# --- HELPER FUNCTIONS ---
def format_input(text):
    """Removes leading/trailing spaces and ignores case for fairness."""
    return str(text).strip().upper()

# --- APP CONFIG & NAVIGATION ---
st.set_page_config(page_title="T-41D Study Tool", page_icon="✈️", layout="centered")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a mode:", ["Home", "Boldface", "Ops Limits"])

if page == "Home":
    st.title("✈️ T-41D Study Tool")
    st.markdown("Welcome to the T-41D Study Tool. Use the sidebar on the left to navigate to the Boldface or Ops Limits quizzes.")
    st.info("**Rules:** Type your answers exactly as they appear on the key. Any single mistake is an automatic FAIL.")

elif page == "Boldface":
    st.title("T-41D BOLDFACE QUIZ")
    st.write("Type out the entire procedure in the box. Press **Enter** to start a new step.")

    with st.form("boldface_form"):
        user_answers = {}
        for procedure, steps in boldface_data.items():
            st.subheader(procedure)
            # Create a multi-line text area instead of individual inputs
            ans = st.text_area(f"Enter all {len(steps)} steps for {procedure}:", height=125, key=f"bf_{procedure}")
            user_answers[procedure] = ans

        submitted = st.form_submit_button("Submit & Grade Boldface")

        if submitted:
            st.markdown("---")
            errors = []
            for procedure, steps in boldface_data.items():
                # Split the text area input by newlines and remove empty lines
                raw_ans = user_answers[procedure]
                user_lines = [line for line in raw_ans.split('\n') if line.strip()]

                if len(user_lines) != len(steps):
                    errors.append(f"**[{procedure}] Step Count Error:** \n❌ You provided {len(user_lines)} steps, but there are {len(steps)} steps.")
                
                # Grade whatever steps they did provide up to the maximum required
                min_len = min(len(user_lines), len(steps))
                for i in range(min_len):
                    if format_input(user_lines[i]) != format_input(steps[i]):
                        errors.append(f"**[{procedure}] Step {i+1}:** \n❌ You entered: `{user_lines[i]}`  \n✅ Correct: `{steps[i]}`")

            if errors:
                st.error("🚨 **RESULT: FAIL [UNSAT]**")
                st.write("You must be 100% accurate. Review your errors below:")
                for error in errors:
                    st.warning(error)
            else:
                st.success("🎉 **RESULT: PASS [EXCELLENT]**")
                st.write("100% accurate. Outstanding work.")

elif page == "Ops Limits":
    st.title("T-41D OPS LIMITS QUIZ")
    st.write("Fill out all limits below, then click Submit to be graded.")

    with st.form("ops_limits_form"):
        user_answers = {}
        for section, limits in ops_limits_data.items():
            st.subheader(section)
            user_answers[section] = {}
            for prompt_text in limits.keys():
                ans = st.text_input(prompt_text, key=f"ops_{section}_{prompt_text}")
                user_answers[section][prompt_text] = ans

        submitted = st.form_submit_button("Submit & Grade Ops Limits")

        if submitted:
            st.markdown("---")
            errors = []
            for section, limits in ops_limits_data.items():
                for prompt_text, correct_answer in limits.items():
                    user_ans = user_answers[section][prompt_text]
                    if format_input(user_ans) != format_input(correct_answer):
                        errors.append(f"**[{section}] {prompt_text}:** \n❌ You entered: `{user_ans}`  \n✅ Correct: `{correct_answer}`")

            if errors:
                st.error("🚨 **RESULT: FAIL [UNSAT]**")
                st.write("You must be 100% accurate. Review your errors below:")
                for error in errors:
                    st.warning(error)
            else:
                st.success("🎉 **RESULT: PASS [EXCELLENT]**")
                st.write("100% accurate. Outstanding work.")