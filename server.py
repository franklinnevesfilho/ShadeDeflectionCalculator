from flask import Flask
import math
import matplotlib.pyplot as plt

app = Flask(__name__)

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
deflection_limit = 5  # max of 1mm of deflection
conversion_value = 1000  # 1 m = 1000 mm

tube_deflections = []
available_tubes = []


def get_tube_deflection(load, span, outer_diameter, inner_diameter):
    elasticity_modulus = 68900
    inertia = (math.pi / 64) * ((outer_diameter ** 4) - (inner_diameter ** 4))  # moment of inertia
    moment = (load * (span ** 2)) / (2 * elasticity_modulus * inertia)  # deflection
    deflection_mm = abs(moment) * 1000  # Convert deflection from meters to millimeters and ensure positive value
    return deflection_mm


def convert_gsm_to_newtons(g, length, width):
    print(g * ((length * width) / 1000) * 9.8)
    return g * ((length * width) / 1000) * 9.8


'''
def main():
    shadeWidth = float(input("Enter shade width (m): "))
    shadeDrop = float(input("Enter shade drop height (m): "))
    shadeWeight = float(input("Enter shade weight (gsm): "))

    load = convert_gsm_to_newtons(shadeWeight, shadeWidth, shadeDrop)
    span = shadeWidth * conversion_value  # conversion value is used to get the proper deflection comparison

    for tube in tubes:
        deflection = get_tube_deflection(load, span, tube['outerDiameter'], tube['innerDiameter'])
        print(f"{tube['name']}: {deflection:.2f} mm")
        tube_deflections.append(deflection)
        if deflection <= deflection_limit:
            available_tubes.append(tube['name'])

    # To get a bar chart of the data uncomment the block below
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
'''


@app.route("/get-deflections/<shade_width>/<shade_drop>/<shade_weight>")
def get_deflections(shade_width, shade_drop, shade_weight):
    tube_deflections.clear()
    available_tubes.clear()

    shade_width = float(shade_width)
    shade_drop = float(shade_drop)
    shade_weight = float(shade_weight)

    load = convert_gsm_to_newtons(shade_weight, shade_width, shade_drop)
    span = shade_width * conversion_value  # conversion value is used to get the proper deflection comparison
    for tube in tubes:
        deflection = get_tube_deflection(load, span, tube['outerDiameter'], tube['innerDiameter'])
        # print(f"{tube['name']}: {deflection:.2f} mm")
        tube_deflections.append(deflection)
        if deflection <= deflection_limit:
            available_tubes.append(tube['name'])

    return tube_deflections


@app.route("/get-available-tubes")
def get_available_tubes():
    return available_tubes


if __name__ == "__main__":
    app.run(debug=True)
