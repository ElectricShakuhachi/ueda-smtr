import json
from pathlib import Path
from google import genai
from google.genai import types
from response_schema import Yamls 

gemini_model = "gemini-2.5-flash"

def get_relevant_pieces_from_json(pieces):
    res = {}
    with open("lyrics.json") as f:
        lyrics = json.load(f)
    for key, value in lyrics.items():
        if key in pieces:
            res[key] = value
    return res

if not Path("lyrics.json").exists():
    raise Exception("lyrics.json not found. Please generate or copy it from somewhere.")

SECRETS_PATH = Path(__file__).parent.parent.parent / "ueda.secrets.json"
with SECRETS_PATH.open() as f:
    api_key = json.load(f)["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

PROMPT_PATH = Path(__file__).parent / "prompt.txt"
with PROMPT_PATH.open(encoding="utf-8") as prompt_file:
    prompt_text = prompt_file.read()

thisfile = Path(__file__)
input_dir = thisfile.parent.parent / "input"
output_dir = thisfile.parent.parent / "input"
output_dir.mkdir(parents=True, exist_ok=True)

input_files: dict[str, Path] = {}
existing: set[str] = set()

for input_dir_item in input_dir.iterdir():
    if input_dir_item.is_dir():
        for file_path in input_dir_item.iterdir():
            if not file_path.is_file():
                continue
            if file_path.suffix == ".pdf":
                input_files[file_path.stem] = file_path
            elif file_path.suffix == ".yaml":
                existing.add(file_path.stem)

for removable in existing:
    input_files.pop(removable, None)

uploaded_files = []
pieces = []
for uploadable_path in input_files.values():
    uploaded_file = client.files.upload(
        file=uploadable_path,
        config={
            "mime_type": "application/pdf",
            "display_name": uploadable_path.name
        }
    )
    pieces.append(uploadable_path.name.replace(".pdf", ""))
    uploaded_files.append(uploaded_file)
    print(f"UPLOADING: {uploadable_path.name}")
    name_of_res_file = uploadable_path.name.replace(".pdf", ".yaml")
    break # for now just doing one file at a time
if len(uploaded_files) == 0:
    print("No pdf files in input folders without an associated yaml. Quitting...")

reference_pdf_path = thisfile.parent / "428_(reference).pdf"
reference_file = client.files.upload(
    file=reference_pdf_path,
    config={
        "mime_type": "application/pdf",
        "display_name": "428_(reference).pdf"
    }
)

reference_yaml_path = thisfile.parent / "428_(reference).yaml"
reference_y_file = client.files.upload(
    file=reference_yaml_path,
    config={
        "mime_type": "text/plain",
        "display_name": "428_(reference).yaml"
    }
)

expl_pdf_path = thisfile.parent / "uedaryu_gakufu_kaisetsu.pdf"
expl_file = client.files.upload(
    file=expl_pdf_path,
    config={
        "mime_type": "application/pdf",
        "display_name": "uedaryu_gakufu_kaisetsu.pdf"
    }
)

contents = []
for uf in uploaded_files:
    contents.append(
        types.Part(
            file_data=types.FileData(
                file_uri=uf.uri, 
                mime_type=uf.mime_type
            )
        )
    )

contents.append(
    types.Part(
        file_data=types.FileData(
            file_uri=reference_file.uri, 
            mime_type=reference_file.mime_type
        )
    )
)

contents.append(
    types.Part(
        file_data=types.FileData(
            file_uri=reference_y_file.uri, 
            mime_type=reference_y_file.mime_type
        )
    )
)

contents.append(
    types.Part(
        file_data=types.FileData(
            file_uri=expl_file.uri, 
            mime_type=expl_file.mime_type
        )
    )
)


contents.append(types.Part(text=prompt_text))

lyrics_json = get_relevant_pieces_from_json(pieces)
contents.append(types.Part(text=str(lyrics_json)))

response = client.models.generate_content(
    model=gemini_model,
    contents=contents,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Yamls,
    ),
)

response_data = response.parsed
for yaml_item in response_data["yamls"]:
    for in_dir in output_dir.iterdir():
        if Path(name_of_res_file.replace(".yaml", ".pdf")).exists():
            output_dir = in_dir
            break
    output_path = output_dir / name_of_res_file
    output_path.write_text(yaml_item["content"], encoding="utf-8")

print("Generation complete.")
