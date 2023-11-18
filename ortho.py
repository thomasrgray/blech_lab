# Import necessary libraries
import time
import random
import logging

# Import RPi.GPIO library for Raspberry Pi GPIO control
import RPi.GPIO as GPIO

class Experiment:
    def __init__(self, solenoid_pins, intan_pins):
        # Define GPIO pin mapping for various components
        self.PINS = {
            'cue_light': 15,
            'ir_beam': 16,
            'vacuum_solenoid': 23,
            'odor_solenoids': [33, 35, 37, 31],
            'taste_solenoid': solenoid_pins['taste'],
            'water_solenoid': solenoid_pins['water'],
            'reward_solenoid': solenoid_pins['reward'],
            'odor_intan_pin': intan_pins['odor'],
            'taste_intan_pin': intan_pins['taste'],
            'water_intan_pin': intan_pins['water'],
            'reward_intan_pin': intan_pins['reward']
        }
        # Initialize GPIO pins
        self.setup_gpio_pins()
        self.log_filename = log_filename
        self.setup_logging()    def setup_gpio_pins(self):
            
        # Set up GPIO configuration
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
    
    def activate_solenoid(self, pin):
        # Activate the specified solenoid by setting the GPIO output to 1
        GPIO.output(pin, 1)

    def deactivate_solenoid(self, pin):
        # Deactivate the specified solenoid by setting the GPIO output to 0
        GPIO.output(pin, 0)

    def activate_intan_input(self, pin):
        # Activate the specified Intan digital input pin by setting the GPIO output to 1
        GPIO.output(pin, 1)

    def deactivate_intan_input(self, pin):
        # Deactivate the specified Intan digital input pin by setting the GPIO output to 0
        GPIO.output(pin, 0)

    def activate_cue_light(self):
        # Activate the cue light by setting the GPIO output to 0
        GPIO.output(self.PINS['cue_light'], 0)

    def deactivate_cue_light(self):
        # Deactivate the cue light by setting the GPIO output to 1
        GPIO.output(self.PINS['cue_light'], 1)

    def log_event(self, event_name):
        # Log an event with a timestamp
        timestamp = time.time()
        timestamp_tenths = int((timestamp % 1) * 10)
        formatted_timestamp = time.strftime("%Y-%m-%d %H:%M:%S.", time.localtime()) + str(timestamp_tenths)

        # Log to console
        print(f"[{formatted_timestamp}] {event_name}")

        # Log to CSV file
        with open(self.log_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([formatted_timestamp, event_name])

    def setup_logging(self):
        # Set up logging to a CSV file
        logging.basicConfig(filename=self.log_filename, level=logging.INFO, format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %H:%M:%S.%f')

    def run_experiment(self, num_trials, selected_odors, water_open_time, reward_open_time, taste_open_time):
        try:
            for trial in range(num_trials):
                # Begin each trial by turning on the cue light
                self.log_event("Cue light turned On")
                self.activate_cue_light()

                # Wait for the IR beam to be crossed for at least 0.5 seconds
                self.log_event("Waiting for IR beam to be crossed for 0.5 seconds...")
                start_time = time.time()
                crossed_duration = 0
                while crossed_duration < 0.5:
                    if GPIO.input(self.PINS['ir_beam']) == 1:
                        crossed_duration = time.time() - start_time
                    else:
                        crossed_duration = 0  # Reset the timer if the beam is broken
                    time.sleep(0.1)  # Adjust the sleep time as needed

                # Turn off the cue light and activate the vacuum solenoid
                self.log_event("Cue light turned Off")
                self.log_event("Vacuum Off")
                self.activate_solenoid(self.PINS['vacuum_solenoid'])
                self.deactivate_cue_light()

                # Randomly select an odor for the current trial
                selected_odor_pin = random.choice(selected_odors)

                # Activate the selected odor solenoid and its corresponding Intan digital input pin
                self.log_event("Odor solenoid turned On")
                self.activate_solenoid(self.PINS['odor_solenoids'][selected_odor_pin])
                self.log_event("Activating Odor Intan Pin")
                self.activate_intan_input(self.PINS['odor_intan_pin'])

                # Activate the water solenoid and its corresponding Intan digital input pin
                self.log_event("Water solenoid turned On")
                self.activate_solenoid(self.PINS['water_solenoid'])
                self.activate_intan_input(self.PINS['water_intan_pin'])

                # Sleep for the specified water solenoid open time
                time.sleep(water_open_time)

                # Turn off the water solenoid and deactivate its corresponding Intan digital input pin
                self.log_event("Water solenoid turned Off")
                self.deactivate_solenoid(self.PINS['water_solenoid'])
                self.deactivate_intan_input(self.PINS['water_intan_pin'])

                # Turn off the odor solenoid and deactivate its corresponding Intan digital input pin
                self.log_event("Odor solenoid turned Off")
                self.deactivate_solenoid(self.PINS['odor_solenoids'][selected_odor_pin])
                self.log_event("Deactivating Odor Intan Pin")
                self.deactivate_intan_input(self.PINS['odor_intan_pin'])

                # Allow for a 2-second delay and then activate the vacuum solenoid
                time.sleep(2)
                self.log_event("Vacuum On")
                self.deactivate_solenoid(self.PINS['vacuum_solenoid'])

                # Allow for a 90-second delay before activating the reward solenoid
                time.sleep(90)
                
                self.log_event("Reward solenoid turned On")
                self.activate_solenoid(self.PINS['reward_solenoid'])
                self.activate_intan_input(self.PINS['reward_intan_pin'])
    
                # Sleep for the specified reward solenoid open time
                time.sleep(reward_open_time)
    
                # Turn off the reward solenoid and deactivate its corresponding Intan digital input pin
                self.log_event("Reward solenoid turned Off")
                self.deactivate_solenoid(self.PINS['reward_solenoid'])
                self.deactivate_intan_input(self.PINS['reward_intan_pin'])
                
        except KeyboardInterrupt:
            # Handle keyboard interruption during the experiment
            print("Experiment interrupted by user.")

        finally:
            # Clean up GPIO pins after the experiment
            GPIO.cleanup()

def main():
    try:
        # Get user input for solenoid and Intan digital input pins
        solenoid_pins = {
            'water': int(input("Enter water solenoid pin (e.g., 11): ")),
            'taste': int(input("Enter taste solenoid pin (e.g., 13): ")),
            'reward': int(input("Enter reward solenoid pin (e.g., 21): "))
        }

        intan_pins = {
            'odor': int(input("Enter Intan digital input pin for odor: ")),
            'taste': int(input("Enter Intan digital input pin for taste solenoid: ")),
            'water': int(input("Enter Intan digital input pin for water solenoid: ")),
            'reward': int(input("Enter Intan digital input pin for reward solenoid: "))
        }

        # Get user input for experiment parameters
        num_trials = int(input("Enter the number of trials: "))
        selected_odors = [int(odor) for odor in input("Enter selected odors separated by spaces (e.g., 0 1 2): ").split()]

        if len(selected_odors) < 1:
            # Exit program if no odors are selected
            print("No odors selected. Exiting program.")
            return

        water_open_time = float(input("Enter water solenoid open time (in seconds, e.g., 0.1): "))
        taste_open_time = float(input("Enter taste solenoid open time (in seconds, e.g., 0.1): "))
        reward_open_time = float(input("Enter reward solenoid open time (in seconds, e.g., 0.1): "))

        # Display the selected pins and open times for reference
        print("Water Solenoid Pins:", solenoid_pins['water'])
        print("Taste Solenoid Pins:", solenoid_pins['taste'])
        print("Odor Intan Pin:", intan_pins['odor'])
        print("Taste Intan Pin:", intan_pins['taste'])
        print("Water Intan Pin:", intan_pins['water'])
        print("Reward Intan Pin:", intan_pins['reward'])
        print("Water Solenoid Open Time:", water_open_time, "seconds")
        print("Taste Solenoid Open Time:", taste_open_time, "seconds")
        print("Reward Solenoid Open Time:", reward_open_time, "seconds")

        # Create an instance of the Experiment class and run the experiment
        experiment = Experiment(solenoid_pins, intan_pins)
        experiment.run_experiment(num_trials, selected_odors, water_open_time, reward_open_time, taste_open_time)

    except Exception as e:
        # Handle general exceptions
        print(f"Error: {e}")

    except KeyboardInterrupt:
        # Handle keyboard interruption during user input
        print("Experiment interrupted by user.")

    finally:
        # Display "done" message when the program is finished
        print("done")

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
