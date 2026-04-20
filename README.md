# Ueda-ryu Shakuhachi-do Sheet Music Translation Release Tool

Personal project for the generation and release of Ueda-ryu sheet music.

# How to use

## Setup
Add the original sheet music pdf's to the respective folders under input
by their type (the numbers after underscores mean how many separate pieces are
in the sheet in question, unless just 1).

Add 428_(reference).pdf and 428_(reference).yaml and uedaryu_gakufu_kaisetsu.pdf inside the ueda_smtr/ai -directory, which are the Japanese original pdf for Yuki no Yo, and a yaml made for it to serve as reference for the ai. Currently prompt.txt also includes the contents of 428_(reference).yaml

Also add lyrics.json within that directory, which contains json data on lyrics for pieces
that have them. The format is as such:

{
   "(piece number)":
    {
        "piece_name": "(piece name here)",
        "lyrics": "(lyrics in Japanese here)",
        "explanation" : "(explanation of piece in Japanese here)"
    },
    ...
}

add ueda.secrets.json to the repo root, containing the api key to use gemini:

{
    "GEMINI_API_KEY" : "(api key)"
}

Activate and install poetry dependencies.

## Run AI generation of yamls
Then you should be able to run generate_yamls.py within the ueda_smtr/ai directory

Due to limit of free tokens to use gemini, currently there is a break on line 71 of generate_yamls.py, so it just creates one of the files when the script is ran.
The free tokens should be enough to generate perhaps about 10 pdf's per day?,
so the break could be adjusted to run after 10 iterations or something...
Just adjust it to however much free tokens you have. Best would be to implement some check
to how much tokens are available and adjust the amount of input pdf's accordingly.
If too much is being passed, nothing comes back except just error message that quota is exceeded.

## Edit the yamls manually

The AI generated yamls are far from perfect, so they all need to be checked and edited manually.

## Run the main tool

Run index.py in the ueda_stmr directory.
It takes no arguments, just assumes that the input data is set in the way that it supposes, and generates the pdf's into the ueda_smtr/output/pdf/ directory.
  I'm planning to make another additional feature to be able to upload the finished pdf's to the Ueda-ryu website, but that is not done yet.

