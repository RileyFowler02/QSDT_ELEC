import pvlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the location
latitude = 44.2334  # Example latitude
longitude = -76.4930  # Example longitude
tz = 'Etc/GMT+5'  # Example timezone

# Create a location object
location = pvlib.location.Location(latitude, longitude, tz=tz)

# Define the time range
times = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H', tz=tz)

# Get solar position
solar_position = location.get_solarposition(times)

# Define the surface azimuth (180 degrees for south-facing)
surface_azimuth = 180

# Function to calculate total irradiance for a given tilt angle
def calculate_irradiance(tilt):
    # Get clear sky data
    clearsky = location.get_clearsky(times)
    
    # Calculate the total irradiance on the tilted surface
    total_irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'],
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi']
    )
    
    # Return the sum of the total irradiance over the year
    return total_irradiance['poa_global'].sum()

# Optimize the tilt angle
tilt_angles = np.arange(0, 90, 1)
irradiance_values = [calculate_irradiance(tilt) for tilt in tilt_angles]

# Find the tilt angle that maximizes the irradiance
optimal_tilt = tilt_angles[np.argmax(irradiance_values)]

print(f'The optimal tilt angle is {optimal_tilt} degrees.')

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(tilt_angles, irradiance_values, label='Total Irradiance')
plt.axvline(optimal_tilt, color='r', linestyle='--', label=f'Optimal Tilt: {optimal_tilt}°')
plt.xlabel('Tilt Angle (degrees)')
plt.ylabel('Total Irradiance (Wh/m²)')
plt.title('Total Irradiance vs. Tilt Angle')
plt.legend()
plt.grid(True)
plt.show()