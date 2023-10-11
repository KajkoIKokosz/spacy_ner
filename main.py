import warnings

from backend.addr_nlp import AddressNer
from backend.preprocessing_data import prepare_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # prepare_data(1000000, 'data/ner_address_shfld_1mln.json')


    train_ner = AddressNer(
        data_path='data/ner_address_shfld_100tys.json',
        pipe_path='address_extraction'
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        train_ner.train_spacy()

    # analysis_ner = AddressNer(pipe_path='address_extraction', pipe_name='ceQyD')
    # search = ['Warszawa 02-987']
    # for s in search:
    #     analysis_ner.analyze_text(s)