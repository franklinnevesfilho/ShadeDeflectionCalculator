import math
import matplotlib.pyplot as plt

# Bottom rail weight in G / MM
BOTTOM_RAIL = 0.0000115


# Error messages
fileNotFound = 'Cannot find file: '

#  This Tube data was requested from Vertilux
tubes = [
    {"name": "32mm LGH", "outerDiameter": 32, "innerDiameter": 30},
    {"name": "32mm STD", "outerDiameter": 32.6, "innerDiameter": 30},
    {"name": "38mm STD", "outerDiameter": 38.43, "innerDiameter": 35.89},
    {"name": "38mm HD", "outerDiameter": 40.3, "innerDiameter": 35.9},
    {"name": "45mm", "outerDiameter": 45, "innerDiameter": 41.5},
    {"name": "50mm", "outerDiameter": 51.25, "innerDiameter": 47},
    {"name": "63mm", "outerDiameter": 65.3, "innerDiameter": 61.7},
    {"name": "83mm", "outerDiameter": 83, "innerDiameter": 77},
]

# The Deflection limit was determined by Industry standard
deflection_limit = 5  # will default to 0 if not specified in deflectionLimit.txt
conversion_value = 1000  # 1 m = 1000 mm

tube_deflections = []
available_tubes = []


# Get Data from files
def read_deflection_limit(filename='deflectionLimit.txt'):
    global deflection_limit
    try:
        with open(filename, 'r') as file:
            content = file.readline().strip()  # read file
            limit = str(content)
            if limit is int or float:  # is valid? if not switch to default
                deflection_limit = float(limit)
    except FileNotFoundError:
        print(f"{fileNotFound}'{filename}'")
    except Exception as e:
        print(f"Error: {e}")

    print("Loaded deflection limit --------------------\n")


def read_tube_data(filename='tubeData.txt'):
    global tubes
    try:
        with open(filename, 'r') as file:
            next(file)  # Skip instruction line

            for line in file:
                parts = line.strip().split(',')
                if len(parts) < 3:  # ensures only tubes with all their values will be read
                    break
                else:
                    if parts[1] is int or float \
                            and parts[2] is int or float:
                        # If valid values create tube
                        newTube = {
                            "name": parts[0],
                            "outerDiameter": float(parts[1]),
                            "innerDiameter": float(parts[2])
                        }
                        # Is tube already added
                        tubeExists = False
                        for tube in tubes:
                            #  If tube has the same name and values exit
                            if newTube["name"] == tube["name"] and \
                                newTube["outerDiameter"] == tube["outerDiameter"] and \
                                    newTube["innerDiameter"] == tube["innerDiameter"]:
                                tubeExists = True
                                break
                        if not tubeExists:  # add tube if not present
                            tubes.append(newTube)

    except FileNotFoundError:
        print(f"{fileNotFound}'{filename}'")
    except Exception as e:
        print(f"Error: {e}")

    print("Loaded Tube Data --------------------\n")


def get_tube_deflection(load, span, outer_diameter, inner_diameter):
    elasticity_modulus = 68900  # Derived
    inertia = (math.pi / 64) * ((outer_diameter ** 4) - (inner_diameter ** 4))  # moment of inertia
    moment = (5 * load * (span ** 4)) / (384 * elasticity_modulus * inertia)  # Deflection Formula

    return moment


def get_load(gsm, drop):
    return ((((gsm / conversion_value) * drop) / conversion_value) + (BOTTOM_RAIL / conversion_value)) * 9.81


def is_float(s):
    return s.replace('.', '', 1).lstrip('-').isnumeric()


def get_input(prompt):
    valid_input = False
    response = None

    while not valid_input:
        response = input(prompt).lower()
        if is_float(response):
            response = float(response)
            valid_input = True
        else:
            if response in ('q', 'r'):
                break
            else:
                print("Invalid input, try again.", end="\n")

    return response


def show_plot(shadeWidth, shadeDrop):
    plt.figure(figsize=(9, 9))
    title = "Tube Deflections Based on Shade Size: " + str(shadeWidth) + "m" + " x " + str(shadeDrop) + "m"
    plt.title(title)
    plt.xlabel('Tube Names')
    plt.ylabel('Tube Deflection (mm)')
    plt.bar(range(len(tubes)), tube_deflections, align='center')
    plt.hlines(y=deflection_limit, xmin=0, xmax=len(tubes), linestyles='--', colors='red', label='Deflection Limit')
    plt.xticks(range(len(tubes)), [tube['name'] for tube in tubes], rotation=45)
    plt.legend()
    plt.show()


def main():
    while True:
        tube_deflections.clear()

        instructions = ('-----------------------------------------------------\n'
                        '  answer the following 3 questions about the shade.\n'
                        '           press "q" to quit anytime\n'
                        '               press "r" to reset\n'
                        '-----------------------------------------------------\n')

        measurements = [
            {"prompt": "Enter shade width (m): ", "field": "shadeWidth", "value": 0},
            {"prompt": "Enter shade drop height (m): ", "field": "shadeDrop", "value": 0},
            {"prompt": "Enter shade weight (gsm): ", "field": "shadeWeight", "value": 0}
        ]

        print(instructions)

        response = ''
        for measurement in measurements:
            response = get_input(measurement['prompt'])
            if response == 'q':
                print("Exited")
                return
            if response == 'r':
                break
            else:
                measurement['value'] = response

        if response != 'r':
            shadeWidth = measurements[0].get('value')
            shadeDrop = measurements[1].get('value')
            shadeWeight = measurements[2].get('value')

            load = get_load(shadeWeight, shadeDrop)
            span = shadeWidth * conversion_value  # conversion value is used to get the proper deflection comparison

            for tube in tubes:
                deflection = get_tube_deflection(load, span, tube['outerDiameter'], tube['innerDiameter'])
                print(f"{tube['name']}: {deflection:.2f} mm")
                tube_deflections.append(deflection)
                if deflection <= deflection_limit:
                    available_tubes.append(tube['name'])
            print("\nAvailable tubes: ", available_tubes)

            # Show chart
            show_plot(shadeWidth, shadeDrop)

            return 0


if __name__ == "__main__":
    read_tube_data()
    read_deflection_limit()
    main()
