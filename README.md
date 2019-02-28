## Normalizer

The application is written in Python 3.7.2. In order to run the application you might need to install one of the libraries, 'pytz', first.

    `python -m pip install pytz==2019.9 --user`

There is a csv file to test for possible errors called invalidValues.csv. In the second column, where the address is supposed to be, is a brief description of the error it is supposed to throw.
The csv file called edgeCases.csv contains some edge cases where for example floating point math could lead to odd results.

run in with: 
    
	`python normalizer.py < inputfile.csv > outputfile.csv`
