import os
import logging
from datetime import datetime
import ueda_conf
from generate import Generator
from template_handling import UedaSmtrTemplateHandler

##################### UEDA-SMTR MAIN INTERFACE #####################
#                                                                  #
#    Ueda-ryu Shakuhachi-do Sheet Music Translation Release Tool   #
#                                                                  #
#             Invokes the following tool features >>               #
#       (the below is not yet the case, mostly future features)    #
#                                                                  #
#     1. Sheet Music Content Parser                                #
#          - AI pattern recognition                                #
#          - reads the sheet music and generates                   #
#          .shaku files *custom format music xml                   #
#          file which I made for the Shakunotator                  #
#          tool back in the day. - after that it                   #
#          becomes directly editable in Shakunotator.              #
#                                                                  #
#     2. Sheet Music Translation Generator                         #
#     3. Generator Result Verifier                                 #
#     4. Website Uploader                                          #
#     5. Website Upload Sanity Checker                             #
#     6. Discord Announcement Bot                                  #
#                                                                  #
#       In addition to their main function, each submodule         #
#     collects data about the music, its status on the site,       #
#     the translations and other notes by translator etc.          #
#     on the site etc. and outputs it to a central                 #
#     csv datastorage.                                             #
#                                                                  #
#       Furthermore the translations and short explanations of     #
#     the sheet music are collated into a LaTex files for          #
#     possible separate further manual edit and release.           #
#                                                                  #
#     (Book on Uedaryu Honkyoku, Book on Koten Honkyoku,           #
#     Book on Jiuta, Book on Nagauta, Book on Sokyoku and          #
#     a master file containing all of them. Because we may         #
#     want to categorize them multiple ways for side by side       #
#     comparison, alternative LaTex files could also be            #
#     generated where pieces with similar characteristics are      #
#     grouped together. For instance, Jiuta with Ni-agari          #
#     tuning, pieces that start with ha-ro, or tsu-re,             #
#     pieces that incliude)                                        #
#                                                                  #
#                                                                  #
####################################################################

if __name__ == "__main__":
    logger = logging.getLogger("ueda_smtr")
    logging.basicConfig(filename='output/logs/ueda_smtr.log', encoding='utf-8', level=logging.DEBUG)
    started = datetime.now()
    divider = "#" * 25
    start_msg = f"\n\nUEDA-SMTR started at {started} {divider}"
    logger.info(start_msg)
    # TODO : Run Sheet Music Content Parser
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ueda_conf.TEMPLATE_DIR)
    tmpl_handler = UedaSmtrTemplateHandler(template_dir, logger)
    template_dict = tmpl_handler.form_category_to_template_dict(ueda_conf.CATEGORIES)
    generator = Generator(template_dict, logger)
    generator.generate_sheets(ueda_conf)
    # TODO : Run Generator Result Verifier
    # TODO : Run Website Uploader 
    # TODO : Run Website Uploader Sanity Checker
    # TODO : Run Discord Announcement Bot
    finished = datetime.now()
    end_msg = f"UEDA-SMTR finished at {finished} and the run took {finished-started}"
    logger.info(end_msg)
