import csv
import datetime
import streamlit as st
import pandas as pd
import os

# Define the file path
file_path = "C:\\Users\\HomePC\\PycharmProjects\\pythonProject11_bmi\\wellness_data.csv"


def create_file_if_not_exists():
    """Check if the wellness_data.csv file exists. If not, create it with headers."""
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Creating a new file with headers.")
        # Create an empty DataFrame with the required columns
        data1 = pd.DataFrame(columns=['Timestamp', 'BMI', 'Number', 'Is Even'])
        data1.to_csv(file_path, index=False)


def load_data():
    """Load data from wellness_data.csv. If the file doesn't exist, create it and return an empty DataFrame."""
    create_file_if_not_exists()
    # Load the existing CSV file
    return pd.read_csv(file_path)


def save_data(bmi_value, number, is_even):
    """Append a new row of data (BMI, number, and even/odd check) to wellness_data.csv."""
    create_file_if_not_exists()
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), bmi_value, number, is_even])


def calculate_bmi(weight=None, height=None):
    """Calculate BMI based on user input or provided weight and height."""
    if weight is None or height is None:
        try:
            weight = float(input("Please enter your weight (kgs): "))
            height = float(input("Please enter your height (metres): "))
            if height <= 0 or weight <= 0:
                print("Values must be greater than zero.")
                return None
        except ValueError:
            print("Invalid input. Please enter numerical values.")
            return None

    bmi_value = weight / (height ** 2)
    print("Your BMI is: {:.2f}".format(bmi_value))
    if bmi_value < 18:
        print("You are underweight.")
    elif 18 <= bmi_value <= 25:
        print("Your weight is OK.")
    else:
        print("You are overweight.")

    save_data(bmi_value, None,  None)
    return bmi_value


def check_even(num=None):
    """Check if a number is even or odd."""
    if num is None:
        try:
            num = int(input("Please enter a number: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            return None

    is_even = num % 2 == 0
    if is_even:
        print("The number is even.")
    else:
        print("The number is not even.")

    save_data(None, num, is_even)  # Store the number and its even/odd status
    return num, is_even


def main_menu():
    """Main menu for the fitness and wellness application."""
    while True:
        print("\nFitness and Wellness Application")
        print("1. Calculate BMI")
        print("2. Check if a number is even or odd")
        print("3. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            bmi_value = calculate_bmi()
            if bmi_value is not None and bmi_value > 25:  # Suggest workout if overweight
                num, is_even = check_even()  # Unpack the tuple returned by check_even()
                if is_even:
                    print("Since the number is even, try doing 20 push-ups!")
                else:
                    print("Since the number is odd, try going for a 15-minute walk!")
        elif choice == '2':
            check_even()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Start the main menu in a console environment
    main_menu()

    # Streamlit for displaying the dashboard
    st.title("Wellness Data Dashboard")

    # Load and display data
    data = load_data()
    st.write(data)

    # Example of visualizing BMI distribution
    st.subheader("BMI Distribution")
    st.bar_chart(data['BMI'].value_counts())


# Load and display data
data = load_data()

# Check if data is empty
if data.empty:
    st.write("No data available. Please add some data.")
else:
    st.write(data)
    # Example of visualizing BMI distribution
    st.subheader("BMI Distribution")
    st.bar_chart(data['BMI'].value_counts())

    st.subheader("BMI Histogram")
    st.bar_chart(data['BMI'].plot(kind='hist', bins=20))







