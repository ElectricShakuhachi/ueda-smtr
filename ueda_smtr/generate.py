import os
import glob
import time
import subprocess
import yaml
from jinja2 import Environment, FileSystemLoader
from PyPDF2 import PdfMerger
from copy import deepcopy

class Generator:
    def __init__(self, categories, logger):
        self._categories = categories
        self._logger = logger

    def _reformat_dates(self, spec_data):
        date_fields = [
            "orig_publ_date",
            "print_date",
            "int_publ_date"
        ]
        month_mapping = {
            "1" : "Jan.",
            "2" : "Feb.",
            "3" : "Mar.",
            "4" : "Apr.",
            "5" : "May",
            "6" : "June",
            "7" : "July",
            "8" : "Aug.",
            "9" : "Sep.",
            "10" : "Oct.",
            "11" : "Nov.",
            "12" : "Dec."
        }
        for date in date_fields:
            day, month, year = spec_data[date].split(".")
            spec_data[date] = f"{month_mapping[month]} {day}. {year}"
        return spec_data

    def _ready_spec_data(self, spec_file: str, mappings: dict):
        with open(spec_file, "r") as f:
            spec_data = yaml.safe_load(f)
        mark_mapping = mappings["markings_mapping"]
        for marking in spec_data["markings"]:
            marking["translation"] = mark_mapping[marking["id"]]
        price_mapping = mappings["price_mapping"]
        date_mapping = mappings["date_mapping"]
        spec_data["price"] = price_mapping[spec_data["orig_price"]]
        day, month, year = spec_data["orig_publ_date"].split(".")
        match_data = None
        for m_year, data in date_mapping:
            if m_year > int(year):
                break
            match_data = data
        date_results = match_data
        spec_data["printer"] = date_results["print"]
        spec_data["print_loc"] = date_results["print_location"]
        spec_data["rights_owner"] = date_results["rights"]
        spec_data["rights_loc"] = date_results["rights_loc"]
        spec_data["payment_acc"] = date_results["payment_acc"]
        spec_data = self._reformat_dates(spec_data)
        return spec_data

    def _split_lines(self, text: str, line_lenght: int):
        lines = []
        words = text.split()
        line = []
        i = 0
        while i < len(words):
            line_i = line_lenght
            while i < len(words) and line_i - len(words[i]) > 0:
                line.append(words[i])
                line_i -= len(words[i])
                i += 1
            lines.append(" ".join(line))
            line = []
        return lines

    def _copy_spec_without_markings_or_texts(self, spec_info):
        new = deepcopy(spec_info)
        new["markings"] = []
        textfields = [
            "orig_lyrics",
            "trans_lyrics",
            "orig_notes",
            "trans_notes",
            "extra_notes"
        ]
        for text in textfields:
            new.pop(text)
        return new

    def _get_repeats_and_split_contexts_for_ep_pages(self, spec_info, ueda_conf):
        self._logger.info("Counting how many pages needed for markings and texts")
        repeats = 1
        contexts = []
        space = 0
        copy = self._copy_spec_without_markings_or_texts(spec_info)
        contexts.append(copy)
        self._logger.info("(initial)")
        space = ueda_conf.SPACE_ON_FIRST_EP
        for i in spec_info["markings"]:
            space -= 1
            if space > 0:
                copy["markings"].append(i)
            else:
                space = ueda_conf.SPACE_ON_OTHER_EP
                repeats += 1
                copy = self._copy_spec_without_markings_or_texts(spec_info)
                contexts.append(copy)
                self._logger.info("(markings)")
                copy["markings"].append(i)
        space -= len(spec_info["markings"]) % 1
        texts = {
            "orig_lyrics": "Original Lyrics: ",
            "trans_lyrics": "Translated Lyrics: ",
            "orig_notes": "Original Notes by Author: ",
            "trans_notes": "Translated Notes: ", 
            "extra_notes": "Extra Notes by Translator: "
        }
        # we dont want a page to end with a small slither of text continuing to next page
        # however, we also gotta check if there is gonna be any texts, because
        # we dont need to add and empty page if none is going to be written
        texts_empty = True
        for i in texts.keys():
            if i != None and len(i) > 0:
                texts_empty = False
        copy["texts"] = []
        if not texts_empty and space <= 1: 
            repeats += 1
            copy = self._copy_spec_without_markings_or_texts(spec_info)
            contexts.append(copy)
            copy["texts"] = []
            self._logger.info("(texts)")
            space = ueda_conf.SPACE_ON_OTHER_EP
            #the above mapping would be logical to come from ueda_conf
        for text, caption in texts.items():
            content = spec_info[text]
            if content is None or len(content) == 0:
                continue
            space -= 2 # for caption
            lines = self._split_lines(content, ueda_conf.LINE_LENGHT)
            first = True
            while space < len(lines):
                text_dict = {}
                if first:
                    text_dict["caption"] = caption
                    first = False
                else:
                    text_dict["caption"] = ""
                text_dict["content"] = " ".join(lines[:space])
                copy["texts"].append(text_dict)
                lines = lines[space:]
                repeats += 1
                copy = self._copy_spec_without_markings_or_texts(spec_info)
                contexts.append(copy)
                copy["texts"] = []
                space = ueda_conf.SPACE_ON_OTHER_EP
            text_dict = {}
            if first:
                text_dict["caption"] = caption
                first = False
            else:
                text_dict["caption"] = ""
            text_dict["content"] = " ".join(lines)
            copy["texts"].append(text_dict)
            space -= len(lines) 
            space -= ueda_conf.DIVIDER
        self._logger.info(f"Counted need for {repeats} pages for marking and text content")
        self._logger.info(f"Jinja context divided to {len(contexts)} for them")
        return (repeats, contexts)

    def _generate_and_concatenate_pdf_from_tex_files(self, output_dir: str, input_files: list, basefile, out_filename: str):
        merger = PdfMerger()
        merger.append(basefile)
        self._logger.info("Compiling generated Latex files into pdfs")
        for input_file in input_files:
            result = subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{input_file}"], cwd="templates", capture_output=False, text=True)
            self._logger.info(f"pdflatex subprocess ran with result: {result}")
            pdf_page = os.path.join("templates", input_file.replace(".tex", ".pdf"))
            merger.append(pdf_page)
        merger.write(os.path.join(output_dir, out_filename))
        merger.close()

    def _generate_sheet(self, spec_file: str, input_dir: str, output_dir: str, templates: list, ueda_conf):
        spec_data = self._ready_spec_data(spec_file, ueda_conf.MAPPINGS)
        env = Environment(loader=FileSystemLoader("./templates"))
        page = 0
        self._logger.info(f"Generating a pdf for spec at {spec_file}")
        pagefiles = []
        for template, repeats in templates:
            repeats = int(repeats)
            ep = False
            if repeats == 0:
                ep = True
                repeats, contexts = self._get_repeats_and_split_contexts_for_ep_pages(spec_data, ueda_conf)
            self._logger.info(f"Generating {repeats} pages for for template: {template}")
            for i in range(repeats):
                if ep == True:
                    context = contexts[i]
                    context["page_i"] = i
                else:
                    context = spec_data
                template = env.get_template(template)
                output_content = template.render(context)
                outfilename = f"{context["romaji_name"]}_{page}_tmp.tex"
                output_path = f"templates/{outfilename}"
                pagefiles.append(outfilename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True) # necessary?
                with open(output_path, "w") as f:
                    f.write(output_content)
                page += 1
        basefilename = str(context["product_no"]) + ".pdf"
        basefile = os.path.join(input_dir, basefilename)
        filename = ueda_conf.FILENAME_SPACER.join([basefilename, context["romaji_name"]] ).replace(".pdf", "") + ".pdf"
        self._generate_and_concatenate_pdf_from_tex_files(output_dir, pagefiles, basefile, filename)

    def _generate_sheet_category(self, templates: list, input_dir: str, output_dir: str, ueda_conf):
        for source_file in os.listdir(input_dir):
            if source_file[-5:] == ".yaml":
                source_file = os.path.join(os.path.abspath(input_dir), source_file)
                self._generate_sheet(source_file, input_dir, output_dir, templates, ueda_conf)

    def _clean_temp_files(self, dir):
        self._logger.info(f"Removing temporary files")
        removables = [
            f"{dir}/*.aux",
            f"{dir}/*.tex",
            f"{dir}/*.log",
            f"{dir}/*_tmp.pdf"
        ] # it would make sense to change temp files to be generated in some other directory anyways but for now
        for rem_match in removables:
            for file in glob.glob(rem_match):
                os.remove(file)
                self._logger.info(f"Removed {file}")

    def _equalize_page_sizes(self, target_dir):
        self._logger.info("Equalizing pdf page sizes")
        result = subprocess.run(["bash", "../../equalize_output_pdf_sizes.sh"], cwd=target_dir, capture_output=True, text=True)
        self._logger.info(f"Pdf size equalizing script ran with result: {result}")

    def generate_sheets(self, ueda_conf):
        for category, templates in self._categories.items():
            input_dir = os.path.join(ueda_conf.INPUT_DIR, category)
            output_dir = os.path.join(ueda_conf.OUTPUT_DIR, "pdf")
            self._generate_sheet_category(templates, input_dir, output_dir, ueda_conf)
        self._clean_temp_files("templates")
        self._equalize_page_sizes(os.path.join(ueda_conf.OUTPUT_DIR, "pdf"))
