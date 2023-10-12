import spacy
import json
import random
import string


class AddressNer:
    def __init__(self, new=False, data_path='', pipe_path='', pipe_name='', iterations=5, labels=[]):
        self.new = new
        self.data_path = data_path
        self.pipe_path = pipe_path
        self.pipe_name = pipe_name or self.generate_random_string(5)
        self.iterations = iterations
        self.labels = labels
        self.nlp = self.init_pipeline()
        if data_path:
            self.train_data = self.load_data()

    def init_pipeline(self):
        if self.pipe_path and not self.new:
            # Note: If both pipe_path and pipe_name are provided, pipe_path model will be prioritized if it exists,
            # while pipe_name will be ignored.
            return spacy.load(self.pipe_path)
        return self.init_new_pipeline()

    def init_new_pipeline(self):
        nlp = spacy.blank('pl')
        ner = nlp.create_pipe("ner")
        for label in self.labels:
            ner.add_label(label)
        nlp.add_pipe(ner, name=self.pipe_name)
        return nlp

    def load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def train_spacy(self):
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != self.pipe_name]
        # other_pipes = []
        with self.nlp.disable_pipes(*other_pipes):
            optimizer = self.nlp.begin_training()
            random.shuffle(self.train_data)
            train_data = self.train_data[0:10000]
            # train_data = TRAIN_DATA
            for itn in range(self.iterations):
                print(f'Starting iteration: {str(itn)}')
                losses = {}
                for text, annotations in train_data:
                    self.nlp.update(
                        [text],
                        [annotations],
                        drop=0.2,
                        sgd=optimizer,
                        losses=losses
                    )
                print(losses)

        self.nlp.to_disk(self.pipe_path)
        return self.nlp

    def analyze_text(self, txt):
        doc = self.nlp(txt)
        print(f'Starting to analysing text: {txt}')
        for ent in doc.ents:
            print(ent.text, ent.label_)
        print('-----------------------------------')

    @staticmethod
    def generate_random_string(length):
        characters = string.ascii_letters
        return ''.join(random.choice(characters) for i in range(length))

