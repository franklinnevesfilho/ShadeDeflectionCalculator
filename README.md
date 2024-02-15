# Shade Deflection Calculator 
***

### Formulas
#### Deflection
```
    (δ) = (F * L^3) / (3 * E * I)
    
    δ -> Deflection
    F -> Force in newtons
    L -> Length of tube
    E -> Elasticity Modulus
    I -> Moment of Inertia
```
#### GSM to Newtons
```
    N = ((GSM * L * W ) / conversion_value) * 9.8
    
    Force (N) = kg/m^2 × Area (m^2)
    
    GSM * L * W -> Calculates the amount of grams based on the size
    converstion_value = 1000 to turn into kg^2
    
    then multiply by 9.8 to get the value in Newtons
    
    How it is implemented:
        g/m^2 / 1000 =>  kg/m^2 * drop / 1000 =>  drop(kg/mm^2) * 9.81 = Newtons
```

### How to use
***
#### Setting up Deflection Limit
The deflection limit file titled 'deflectionLimit.txt' 
contains a single number that represents the deflection limit in mm for the chart.
If no value is specified the limit will default to 0
***
#### Setting up Tube data
The program already has a list of tubes, however if you wish to add your own tube. In a new line you must write this information.
```
    tube name, outer diameter, inner diameter
    
    Ex: 83mm, 83.5, 60
```