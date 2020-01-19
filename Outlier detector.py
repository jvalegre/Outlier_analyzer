#!/usr/bin/python
from __future__ import print_function, absolute_import

#######################################################################
#                                                                     #
#                        Outlyer.py                                   #
#  Automated evaluation of the results obtained in the TS             #
#  Benchmarking from Gaussian using different levels of theory,       #
#  including quasi-RRHO entropy corrections obtained using GoodVibes. #
#                                                                     #
#######################################################################
####     Written by:  Juan V. Alegre-Requena                       ####
######                                                           ######
#######  Last modified:  July 25, 2018 ################################
#######################################################################

import numpy, math
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import seaborn as sb
from decimal import Decimal
from scipy import stats
import matplotlib.patches as mpatches
from argparse import ArgumentParser
from optparse import OptionParser

parser = ArgumentParser()
parser.add_argument("--file", dest="file", help="Name of the file to analyze", default='file', metavar="FILE")
parser.add_argument("--sheet", dest="sheet", help="Excel sheet with the results", default='Sheet1', metavar="SHEET")
parser.add_argument("--tvalue", dest="tvalue", help="t-value applied as the threshold", type=float, default=2.0, metavar="tvalue")
(options, args) = parser.parse_known_args()

# Take data from the excel file with the results
pi4_sigma = []
log_dr = []
names = []
pi4_sigma_no_outlayers = []
log_dr_no_outlayers = []

df = pd.read_excel(options.file+'.xlsx', sheetname=options.sheet)
for i in df.index:
    pi4_sigma.append(df['sigma comput'][i])
    log_dr.append(df['full'][i])
    names.append(df['substituent'][i])

for i in range(len(pi4_sigma)):
    pi4_sigma_no_outlayers.append(pi4_sigma[i])
    log_dr_no_outlayers.append(log_dr[i])

# Representation of ee with Seaborn
# For the model including the outlayers
Plotdata_pi4 = {'pi4_sigma': pi4_sigma, 'log_dr': log_dr}
df_pi4 = pd.DataFrame.from_dict(Plotdata_pi4)
plt.scatter(df_pi4["pi4_sigma"], df_pi4["log_dr"],
             c='b', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points
# Point for legend
# plt.scatter(0.44, 5.5,
#              c='b', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points

#build the plot
plot = sb.regplot("pi4_sigma", "log_dr", data=df_pi4, scatter=False, color=".1", truncate=True)

plt.xlabel('$\sigma$$_p$',fontsize=19)
plt.xticks(fontsize=17)
plt.ylabel('log(dr)',fontsize=19)
plt.yticks(fontsize=17)

slope_pi4, intercept_pi4, r_value_pi4, p_value_pi4, std_err_pi4 = stats.linregress(pi4_sigma,log_dr)
slope_pi4 = numpy.asarray(slope_pi4)
predict_log_dr = intercept_pi4 + (slope_pi4 * pi4_sigma)
rsquared_pi4 = r_value_pi4**2

# MAE and Rsquared
plt.text(0.7275, 0.793, "$R^2$ = "+str(Decimal(str(rsquared_pi4)).quantize(Decimal('.01'))), fontsize=16, ha='center', transform=plt.gcf().transFigure)
plt.text(0.7275, 0.753, "y = "+str(Decimal(str(intercept_pi4)).quantize(Decimal('.01')))+" - "+str(Decimal(str(numpy.absolute(slope_pi4))).quantize(Decimal('.01')))+"x", fontsize=16, ha='center', transform=plt.gcf().transFigure)

# plt.text(0.72, 0.81, "4$\pi$ cycliz.", fontsize=16, ha='left', transform=plt.gcf().transFigure)

plt.grid(linestyle='--', linewidth=1)
# plt.yticks(numpy.round(numpy.linspace(-0.4, 1.6, 5), 1))
# plt.xticks(numpy.round(numpy.linspace(-1, 0.9, 5), 1))
# plt.axis('equal')

#set limits
plt.ylim(-0.5, 1.6)
# plt.xlim(-1, 0.9)

plt.savefig('Hammet plot calculated WITH outlayers.png', dpi=400, bbox_inches='tight')
# If you want to include ticks in all the borders. For booleans, you have to specify NAME = True (or False)
#      plt.tick_params(top=True)
#      plt.tick_params(right=True)

# Outlayer detector graph
# Normalize the data
error_abs, error_dr_normal = [], []
error_no_outlyer = []
error_outlyer = []
outlyer_names = []
list_to_remove_sigma, list_to_remove_dr = [], []
outlyer_list =''

for i in range(len(predict_log_dr)):
    error_abs.append(numpy.absolute(predict_log_dr[i] - log_dr[i]))
Mean = numpy.mean(error_abs)
SD = numpy.std(error_abs)

for i in range(len(pi4_sigma)):
    error_dr_normal.append((error_abs[i]-Mean)/SD)
    if numpy.absolute(error_dr_normal[i]) > options.tvalue and error_abs[i] > numpy.absolute(Mean):
        error_outlyer.append(error_dr_normal[i])
        outlyer_names.append(names[i])
        list_to_remove_sigma.append(pi4_sigma_no_outlayers[i])
        list_to_remove_dr.append(log_dr_no_outlayers[i])
    else:
        error_no_outlyer.append(error_dr_normal[i])

for i in range(len(list_to_remove_sigma)):
    pi4_sigma_no_outlayers.remove(list_to_remove_sigma[i])
    log_dr_no_outlayers.remove(list_to_remove_dr[i])
for i in range(len(outlyer_names)):
    outlyer_list += outlyer_names[i]
    outlyer_list += ', '
outlyer_list = outlyer_list[:(len(outlyer_list)-2)]

# Plot outliers in red
fig, ax = plt.subplots()
Plot_outliers = {'error_outlyer': error_outlyer}
Plot_no_outliers = {'error_no_outlyer': error_no_outlyer}
df_outliers = pd.DataFrame.from_dict(Plot_outliers)
df_no_outliers = pd.DataFrame.from_dict(Plot_no_outliers)
plt.scatter(df_no_outliers["error_no_outlyer"], df_no_outliers["error_no_outlyer"],
             c='b', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points
plt.scatter(df_outliers["error_outlyer"], df_outliers["error_outlyer"],
             c='r', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points

plt.scatter(-3.3, 3.5,
             c='r', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points

plt.xlabel('$\sigma$$_l$$_o$$_g$$_($$_d$$_r$$_)$',fontsize=19)
plt.xticks(fontsize=17)
plt.ylabel('$\sigma$$_l$$_o$$_g$$_($$_d$$_r$$_)$',fontsize=19)
plt.yticks(fontsize=17)

plt.text(-3, 3.32, "Outliers: " + outlyer_list, fontsize=16, ha='left')

plt.grid(linestyle='--', linewidth=1)

#set limits
plt.ylim(-4, 4)
plt.xlim(-4, 4)

# Plot rectangles in corners
Rectangle2 = mpatches.Rectangle(xy=(4, 4), width=-(4-options.tvalue), height=-(4-options.tvalue), facecolor='grey', alpha=0.3)
# ax.add_patch(Rectangle)
ax.add_patch(Rectangle2)

plt.savefig('Hammet plot outlyer detector.png', dpi=400, bbox_inches='tight')
# If you want to include ticks in all the borders. For booleans, you have to specify NAME = True (or False)
#      plt.tick_params(top=True)
#      plt.tick_params(right=True)

# Graph the data without outlayers
ax2 = plt.subplots()
Plotdata_pi4_no_outlayers = {'pi4_sigma_no_outlayers': pi4_sigma_no_outlayers, 'log_dr_no_outlayers': log_dr_no_outlayers}
df_pi4_no_outlayers = pd.DataFrame.from_dict(Plotdata_pi4_no_outlayers)
plt.scatter(df_pi4_no_outlayers["pi4_sigma_no_outlayers"], df_pi4_no_outlayers["log_dr_no_outlayers"],
             c='b', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points

# Point for legend
# plt.scatter(0.44, 5.5,
#              c='b', s=60, edgecolor='k', linewidths=1.2)  # Include border to the points

#build the plot
plot = sb.regplot("pi4_sigma_no_outlayers", "log_dr_no_outlayers", data=df_pi4_no_outlayers, scatter=False, color=".1", truncate=True)

plt.xlabel('$\sigma$$_p$',fontsize=19)
plt.xticks(fontsize=17)
plt.ylabel('log(dr)',fontsize=19)
plt.yticks(fontsize=17)

slope_pi4_no_outlayers, intercept_pi4_no_outlayers, r_value_pi4_no_outlayers, p_value_pi4_no_outlayers, std_err_pi4_no_outlayers = stats.linregress(pi4_sigma_no_outlayers,log_dr_no_outlayers)
slope_pi4_no_outlayers = numpy.asarray(slope_pi4_no_outlayers)
predict_log_dr_no_outlayers = intercept_pi4_no_outlayers + (slope_pi4_no_outlayers * pi4_sigma_no_outlayers)

rsquared_pi4_no_outlayers = r_value_pi4_no_outlayers**2

# MAE and Rsquared
plt.text(0.7275, 0.793, "$R^2$ = "+str(Decimal(str(rsquared_pi4_no_outlayers)).quantize(Decimal('.01'))), fontsize=16, ha='center', transform=plt.gcf().transFigure)
plt.text(0.7275, 0.753, "y = "+str(Decimal(str(intercept_pi4_no_outlayers)).quantize(Decimal('.01')))+" - "+str(Decimal(str(numpy.absolute(slope_pi4_no_outlayers))).quantize(Decimal('.01')))+"x", fontsize=16, ha='center', transform=plt.gcf().transFigure)

# plt.text(0.72, 0.81, "4$\pi$ cycliz.", fontsize=16, ha='left', transform=plt.gcf().transFigure)

plt.grid(linestyle='--', linewidth=1)
# plt.axis('equal')

#set limits
# plt.xlim(-0.4, 0.8)
plt.ylim(-0.5, 1.6)

plt.savefig('Hammet plot calculated WITHOUT outlayers.png', dpi=400, bbox_inches='tight')
# If you want to include ticks in all the borders. For booleans, you have to specify NAME = True (or False)
#      plt.tick_params(top=True)
#      plt.tick_params(right=True)

plt.show()
