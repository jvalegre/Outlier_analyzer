# Outlier_analyzer
Simple Python code to detect outliers at different p values.

Instructions:

(1) The program plots your data using the columns:
sigma, log(dr) and substituent, but you can change the name of the columns as you prefer (the code needs to be modified).

(2) The program plots log(dr) (y axis) vs sigma (x axis).

(3) It shows you a graph containing a grey square where you outlyers are represented as red circles (blue circles for the rest of the data points).
The names of the substituents associated to those outlyers are also shown.

(4) Then, it takes out all the outlyers and plots log(dr) vs sigma again (with no outlyers).


Command and options:

python 'Outlyer detector.py' --file FILENAME --sheet SHEETNAME --tvalue TVALUE

--file : specify the file name without quotation marks and without the .xlsx (if you have a csv, just change the extension to xlsx)

--sheet : specify the sheet name without quotation marks (use Sheet1 if you have trouble, default is Sheet1)

--tvalue : statistical t-value used as the cut-off (i.e. approx 1.96 corresponds to a 95% confidence interval in a normal distribution)

i.e. python 'Outlyer detector.py' --file Hammet --tvalue 1.96
