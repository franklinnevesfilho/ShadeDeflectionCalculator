import math
import matplotlib.pyplot as plt

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
deflection_limit = 2.5  # max of 5mm of deflection
conversion_value = 1000  # 1 m = 1000 mm

tube_deflections = []
available_tubes = []


def get_tube_deflection(load, span, outer_diameter, inner_diameter):
    elasticity_modulus = 68900  # Derived
    inertia = (math.pi / 64) * ((outer_diameter ** 4) - (inner_diameter ** 4))  # moment of inertia
    moment = (5 * load * (span ** 4)) / (384 * elasticity_modulus * inertia)  # Deflection Formula

    return moment


def get_load(gsm, drop):
    #     g/m^2 / 1000 = kg/m^2 * drop / 1000 =>  drop(kg/mm^2) * 9.81 = Newtons
    return (((gsm/conversion_value) * drop) / conversion_value) * 9.81


def get_input(prompt):
    valid_input = False
    response = None

    while not valid_input:
        response = input(prompt)
        if response is float or int:
            response = float(response)
            valid_input = True
        else:
            if response == 'q' or response == 'r':
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

        for measurement in measurements:
            response = get_input(measurement['prompt'])
            if response == 'q':
                print("Exited")
                return
            if response == 'r':
                break
            else:
                measurement['value'] = response
        else:
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
    main()