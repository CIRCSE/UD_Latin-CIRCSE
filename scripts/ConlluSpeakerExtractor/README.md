# Speaker Extractor

This python script extracts all the speeches releated to each speaker and extracts a number of formal properties including type-token ratio, number of (tokens/sentences), sentence depth and a graph showing the tree for each sentence. 

The extraction is based on a speaker annotation included in the conllu file.

## How to use

clone the repository with:
```
git clone https://github.com/CIRCSE/UD_Latin-CIRCSE.git
cd UD_Latin-CIRCSE/scripts/ConlluSpeakerExtractor
```

to create a virtual environment with virtualenv, do as follows:
```
virtualenv -p python3 env
source env/bin/activate
```
install the dependencies with:
```
pip install -r requirements.txt
```
run the script with: 
```
python SpeakerExtractor.py -i <file_conllu>
```
i.e.:
```
python SpeakerExtractor.py -i file1.conllu
```
if you want to save the results on a separate file it's possible to redirect the output with ">" command i.e:
```
python SpeakerExtractor.py file1.conllu > output.txt
```
if you want to save the conllu of each speaker add ```-sc``` parameter to the command line.
```
python SpeakerExtractor.py -sc -i file1.conllu > output.txt
```

