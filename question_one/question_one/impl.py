import fasttext
from openfda.api import QuestionOneData
import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from tqdm import tqdm


class CountrySimilarities:
    def __init__(self):
        self.all_countries = None
        self.all_reactions = None
        self.country_reactions_d = None
        self.openfda_session = None

    def create_openfda_session(self, openfda_env_var='openfda'):
        self.openfda_session = QuestionOneData(openfda_env_var)

    def load_countries(self):
        countries_d = self.openfda_session.get_all_occur_countries()
        self.all_countries = set(pd.DataFrame.from_dict(countries_d)['term'].values)

    def load_country_reactions(self):
        self.load_countries()
        all_reactions = set()
        country_reactions_d = {}
        text_preprocessor = TextPreprocessor()

        for country in tqdm(self.all_countries):
            reactions_d = self.openfda_session.get_all_patient_reactions_for_country(country)
            country_reactions = pd.DataFrame.from_dict(reactions_d)['term'].str.lower().values
            trans_country_reactions = text_preprocessor.transform(country_reactions)
            all_reactions = all_reactions | set(trans_country_reactions)
            country_reactions_d[country] = trans_country_reactions
        self.all_reactions = all_reactions
        self.country_reactions_d = country_reactions_d

    def jaccard_similarity(self, c1, c2):
        c1_reactions = set(self.country_reactions_d[c1])
        c2_reactions = set(self.country_reactions_d[c2])
        return len((c1_reactions & c2_reactions)) / len((c1_reactions | c2_reactions))

    def get_jaccard_similarity_with_reference_to_country(self, country):
        result_d = {}
        comparison_countries = self.all_countries - set(country)
        for comp_country in tqdm(comparison_countries):
            result_d[comp_country] = self.jaccard_similarity(country, comp_country)
        return result_d


class TextEmbedder:
    def __init__(self, model_path):
        self.bioword_model = fasttext.load_model(model_path)

    def transform(self, reactions, method='doc_average'):
        if method=='doc_average':
            embed_sum = np.zeros((1, 200))
            for reaction in reactions:
                tokens = reaction.split()
                embeds = [self.bioword_model[token] for token in tokens]
                reaction_embed = np.sum(embeds, axis=0) / len(tokens)
                embed_sum += reaction_embed
            return embed_sum / len(reactions)


class TextPreprocessor:
    def __init__(self):
        nltk.download('stopwords')
        self.en_stop_words = stopwords.words('english')

    def transform(self, reactions):
        combined_hash_d = {}
        no_stop_words_patient_reactions = []

        for i, reaction in enumerate(reactions):
            no_stop_word_tokens = [token for token in reaction.split() if token not in self.en_stop_words]
            tokenized_event = frozenset(no_stop_word_tokens)
            if tokenized_event not in combined_hash_d:
                combined_hash_d[tokenized_event] = 1
                no_stop_words_patient_reactions.append(' '.join(no_stop_word_tokens))

        return no_stop_words_patient_reactions
