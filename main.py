import warnings

from backend.addr_nlp import AddressNer
from backend.preprocessing_data import prepare_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # prepare_data(100, 'data/ner_address_shfld_10000.json', labels=['HOUSENUMBER'])


    # train_ner = AddressNer(
    #     new=True,
    #     data_path='data/ner_address_shfld_100_housenumber_only.json',
    #     pipe_path='address_extraction_housenr',
    #     pipe_name='house_number_only',
    #     labels=['HOUSENUMBER'],
    #     iterations=10
    # )
    #
    # with warnings.catch_warnings():
    #     warnings.simplefilter("ignore")
    #     train_ner.train_spacy()

    analysis_ner = AddressNer(pipe_path='address_extraction', pipe_name='pqVJi')
    search = [
        'Moskity 12-b Warszawa 02-987',
        'Gluty Lubińkowskiego 8 00-000 Małopolskie',
        'Krakowska 15b Janki',
        'Dolinka Służewiecka, Warszawa, 00-222',
        # 'Bonifraterska 7a Warszawa 02-987',
        # '7a Warszawa Bonifraterska 02-987',
        # 'Warszawa 02-987 7a Bonifraterska',
    ]
    for s in search:
        analysis_ner.analyze_text(s)