import warnings

from backend.addr_nlp import AddressNer
from backend.preprocessing_data import prepare_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # prepare_data(1000, 'ner_address_shfld_1tys.json')
    # init_nlp("addr_nlp_ner")
    address_ner = AddressNer(data_path='data/ner_address_shfld_1tys.json')



    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        address_ner.train_spacy()
