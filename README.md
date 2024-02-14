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
```

### Requests
***
#### HTTPS://URL:PORT/get-deflections/:shade_width/:shade_drop/:shade_weight
* Returns an array with the deflections of every tube stored in mm.
***
#### HTTPS://URL:PORT/get-available-tubes
* Returns an array of tubes that are equal to or below the deflection limit
***
