import spacy
import json
import random

PIPE_NAME = "addr_label_shfl_ner"


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def init_new_pipeline():
    nlp = spacy.blank('pl')
    ner = nlp.create_pipe("ner")

    ner.add_label("VOIVODESHIP")
    ner.add_label("COUNTY")
    ner.add_label("COMMUNITY")
    ner.add_label("CITY")
    ner.add_label("STREET")
    ner.add_label("HOUSENUMBER")
    ner.add_label("ZIPCODE")

    nlp.add_pipe(ner, name=PIPE_NAME)

    return nlp


def train_spacy(TRAIN_DATA, iterations, pipe_path=None, new=False):
    if not new and pipe_path:
        try:
            nlp = spacy.load(pipe_path)
        except Exception as e:
            print(f'Pipeline {pipe_path} not exists. Creating new one.')
            nlp = init_new_pipeline()

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != pipe_path]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        random.shuffle(TRAIN_DATA)
        train_data = TRAIN_DATA[0:10000]
        for itn in range(iterations):
            print(f'Starting iteration: {str(itn)}')
            losses = {}
            for text, annotations in train_data:
                nlp.update(
                    [text],
                    [annotations],
                    drop=0.2,
                    sgd=optimizer,
                    losses=losses
                )
            print(losses)

    nlp.to_disk(pipe_path)
    return nlp


def train():
    TRAIN_DATA = load_data("ner_address_shfld_1mln.json")
    # random.shuffle(TRAIN_DATA)
    trained = train_spacy(TRAIN_DATA, 5)

    text_to_analyze = "Mazowieckie 16a Krzywoprzysięstwa 01-666 Smolniki"
    analyze(text_to_analyze, trained)


def analyze(text, model=None, model_path=''):
    model = model or spacy.load(model_path)
    doc = model(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)