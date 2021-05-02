import numpy as np
def tolerance(base_x,y,tolerance):
        z=(base_x-y)/base_x
        z=np.abs(z)*100
        most_near_index=np.argmin(z)
        most_near_number_percentage=z[most_near_index]
        if most_near_number_percentage <tolerance:
            return most_near_index
        else: 
            return "" 
   
base_x=294.75
y=np.array([339.01,324.11,319.38,312.96,304.37,299.17,295.17,293.48,291.24,283.31]) 

z=tolerance(base_x,y, .05)
print(z)
