# mtbpred
MicroTubule Associated and Binding Proteins Predictor
1. Install python from https://www.python.org/downloads/
2. While installing, make sure “ADD PYTHON TO ENVIRONMENT VARIABLE” checkbox is checked OR add Python to the list of your
computer’s environment variables from Control Panel.
3. Installing dependencies for this tool:
1. Head to Command Prompt.
2. Install the following dependencies by typing “pip install dependency_name” command in Command Prompt:
1. Tkinter
2. Pandas
3. Numpy
4. Sklearn
5. Matplotlib
6. E.g: pip install pandas
4. Download MTBPpred from here: https://www.bioinfoindia.org/mtbpred/downloads.html.
5. Open the file “tool.py” in Python IDLE and go to Run->Run Module.
6. Give any FASTA file containing protein sequences as input.
7. Alternatively, you can also paste the sequences in FASTA format only.
8. Make sure the sequences don’t contain any ambiguous amino acid characters- B, J, O, U, X & Z.
9. Choose one desired classifier out of Random Forest and Support Vector Machine.
10. Choose one feature among the following five features:
1. Amphiphilic Pseudo-Amino Acid Composition (APAAC)
2. Composition (CTDC)
3. CTDT(Transition)
4. Normalized Moreau Broto (NMBroto)
5. Dipeptide Composition (DPC)
11. Click on “Predict” button to get your results.
12. Wait for some time to see the results.
13. Press close button and check back the folder “MTBPred” for your results file named “Output.csv” and "Pie-Chart.png".

   In the Results Section Follwing Items will be displayed:
   
1. Summary statistics of the best model used for training is displayed.
2. Out of the total sequences in input file, the number of sequences falling in each class is displayed.
3. A pie chart depicting the percentage of sequences in each class is displayed and also saved in the tool’s folder.
4. Finally, an output file “Output.csv” consisting of the sequence ID and its corresponding class is generated in the MTBPred folder.

   MTBPred Summary: 
A tool developed in Python 3.7 which takes a FASTA sequence(s) file as an input and classifies each sequence as belonging to MTBP or non-MTBP.
It validates the input file for not containing ambiguous amino acid characters-B, J, O, U, X & Z.
It gives user an option to choose between the two classification methods: Random Forest and Support Vector Machine.
It also enables users to choose among five features: Amphiphilic Pseudo-Amino Acid Composition (APAAC), Composition (CTDC), CTDT(Transition), Normalized Moreau Broto (NMBroto), Dipeptide Composition (DPC).
The results are predicted with ~90% accuracy for both the features.
The tool generates a pie-chart depicting the percentage of sequences falling in the two categories and saves it to the MTBPred folder.
At the end, an output CSV enlisting all the sequence IDs and their corresponding class is also written into the MTBPred folder.
