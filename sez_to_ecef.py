# sez_to_ecef.py
# Access Python through CMD: cd Desktop\Phyton
# Clear Sreen on CMD: cls
#
# Usage: sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Example: python3 sez_to_ecef.py 37.207 -80.419 0.63 -0.5 0 0.15
#  Output: 846.598324055394
#         -5015.504048669726
#          3836.5848942674197

# Parameters:
#  o_lat_deg: geocentric lattitude in degrees
#  o_long_deg: geocentric longtitude in degrees
#  o_hae_km: height of ellipsoid in km
#  (s,e,z) [km]: SEZ coordinates
#  ...
# Output:
#  ECEF vector in (x,y,z) [km] from SEZ origin
#
# Written by Ryo Jumadiao
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.137
E_E = 0.081819221456

# helper functions
def calc_denom (E_E,lat_rad):
    return math.sqrt(1.0-E_E**2.0 * math.sin(lat_rad)**2.0)

# initialize script arguments
o_lat_deg = float('nan') #Latitude in degrees
o_lon_deg = float('nan') #Longtitude in degrees
o_hae_km = 0.0 #height above ref ellipsoid

s_km = 0.0
e_km = 0.0
z_km = 0.0

# parse script arguments
# How many arguments are passed to python -- 6 arguments pass 7
# Converts string to float

if len(sys.argv)==7:
    o_lat_deg = float(sys.argv[1])
    o_lon_deg = float(sys.argv[2])
    o_hae_km = float(sys.argv[3])
    s_km = float(sys.argv[4])
    e_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
    
else:
   print(\
    'Usage: '\
    'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
   )
   exit()

#======================================
o_lat_rad = o_lat_deg * math.pi/180.0
o_lon_rad = o_lon_deg * math.pi/180.0

r_sez_km = math.sqrt(s_km**2 + e_km**2 + z_km**2)

#Rotation Matrix Multiplication
Ry_r_sez_1 = s_km*math.sin(o_lat_rad)+z_km*math.cos(o_lat_rad)
Ry_r_sez_2 = e_km*(1)
Ry_r_sez_3 = s_km*-math.cos(o_lat_rad)+z_km*math.sin(o_lat_rad)

R_ecef_1 = Ry_r_sez_1*math.cos(o_lon_rad)-Ry_r_sez_2*math.sin(o_lon_rad)
R_ecef_2 = Ry_r_sez_1*math.sin(o_lon_rad)+Ry_r_sez_2*math.cos(o_lon_rad)
R_ecef_3 = Ry_r_sez_3*(1)

denom = calc_denom(E_E,o_lat_rad)

C_E = R_E_KM/denom
S_E = (R_E_KM*(1.0-E_E**2.0)) / denom

r_X = (C_E+o_hae_km)*math.cos(o_lat_rad)*math.cos(o_lon_rad)
r_Y = (C_E+o_hae_km)*math.cos(o_lat_rad)*math.sin(o_lon_rad)
r_Z = (S_E+o_hae_km)*math.sin(o_lat_rad)
r_XYZ_km = math.sqrt(r_X**2 + r_Y**2 + r_Z**2)

#ECEF vector added to SEZ origin
ecef_1 = r_X + R_ecef_1
ecef_2 = r_Y + R_ecef_2
ecef_3 = r_Z + R_ecef_3

print(str(ecef_1))
print(str(ecef_2))
print(str(ecef_3))