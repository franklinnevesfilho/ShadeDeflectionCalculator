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
There are 3 
