import warnings
import argparse
from backend.addr_nlp import train
from backend.preprocessing_data import prepare_data

training = True
analyze_text = ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NER analysis arguments")
    parser.add_argument('-t', '--train', type=str, help='Train NER')
    parser.add_argument('-a', '--analyze-text', type=str, help='Text NER analyze')
    # prepare_data(1000000, 'ner_address_shfld_1mln.json')
    # init_nlp("addr_nlp_ner")

    args = parser.parse_args()

    training = args.train or training
    if not training:
        analyze_text = args.analyze_text or analyze_text

    if training:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            train()
