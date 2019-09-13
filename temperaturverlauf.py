import math as m
def temperature_Haus(hours, temp_diff, temp_max, temp_min, tmin):
    return round((1/2*temp_diff*m.sin(m.pi*1/12*(hours-6-tmin))+((temp_max-temp_min)/2)*m.sin(m.pi*1/4320*(hours-2160))+(((temp_max-temp_min)/2)+temp_min)),2)

def get_temperaturverlauf(months_start, months_end, days, temp_diff, temp_max, temp_min, tmin):
    temperaturverlauf_haus = list()
    for hours in range(24*30*(months_start-1), 24*30*months_end+(24*days), 1): #24 Stunden * 30 Tage 
        temperaturverlauf_haus.append(temperature_Haus(hours, temp_diff, temp_max, temp_min, tmin))
    
    return temperaturverlauf_haus

        
