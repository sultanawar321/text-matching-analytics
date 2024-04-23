import re
from loguru import logger
import pandas as pd

# import fuzzywuzzy
from fuzzywuzzy import fuzz

# import nltk packages
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# define global variables
STOP_WORDS = set(stopwords.words("english"))
MATCHING_WORDS = ["account", "name", "phone number", "address", "postcode"]


class TextMatchingFuzzyWuzzy:
    """
    This class provides functionality for text matching using the FuzzyWuzzy algorithm.
    It includes methods for loading data, preprocessing text, and performing fuzzy matching.
    """

    def __init__(self) -> None:
        self.matching_threshold = 60
        self.matching_words = MATCHING_WORDS
        self.stop_words = STOP_WORDS

    def load_data(self):
        """
        Load input calls data file.
        """
        input_data = pd.read_csv("data.csv")
        input_data = input_data[input_data["TEXT"].notnull()]
        return input_data

    def preprocess_text(self, text: str) -> list:
        """
        Clean and preprocess the calls text
        """
        # remove text in square brackets
        text = re.sub(r"\[.*?\]", "", text)
        # remove special characters
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
        # tokenize
        tokens = word_tokenize(text.lower())
        # remove stop_words
        tokens = [word for word in tokens if word not in self.stop_words]
        return tokens

    def fuzzy_wuzyy(self, document: list, features: list, match: int) -> set:
        """
        It finds the similartiy matching rate between each word in the transcript
        with the predefined matching terms and then it returns the words with a
        matching rate higher than the threshold
        """
        result = []
        # finding unique features
        for feature in set(features):
            len_feature = len(feature.split(" "))
            for i in range(len(document) - len_feature + 1):
                wordtocompare = ""
                j = 0
                for j in range(i, i + len_feature):
                    wordtocompare = wordtocompare + " " + document[j]
                wordtocompare.strip()
                if wordtocompare != "":
                    if (
                        fuzz.ratio(wordtocompare, feature) >= match
                        and feature not in result
                    ):
                        result.append(feature)
        return set(result)

    def missing_words(self, compliance: set, terms: list) -> set:
        """
        It looks up missing compliance words from each call text
        """
        missing = []
        for term in terms:
            if term not in compliance:
                missing.append(term)
        return set(missing)


if __name__ == "__main__":
    # Instantiate the matcher class
    matcher = TextMatchingFuzzyWuzzy()

    # Load data
    logger.info("Loading the input calls data")
    calls_data = matcher.load_data()

    # Preprocess text
    logger.info("Performing data preprocessing")
    calls_data["TEXT"] = calls_data["TEXT"].apply(matcher.preprocess_text)

    # Apply Fuzzywuzzy
    logger.info("Finding the matched compliance words in the calls text")
    calls_data["MATCHING_TEXT"] = calls_data["TEXT"].apply(
        lambda x: matcher.fuzzy_wuzyy(
            x, matcher.matching_words, matcher.matching_threshold
        )
    )

    # Find Missing words
    logger.info("Finding the missing compliance words")
    calls_data["MISSING_TEXT"] = calls_data["MATCHING_TEXT"].apply(
        lambda x: matcher.missing_words(x, matcher.matching_words)
    )

    # check the results
    logger.info(f"total calls: {len(calls_data)}")
    logger.info(
        f"Unique matching words: {calls_data['MATCHING_TEXT'].apply(tuple).unique()}"
    )
    logger.info(
        f"Value counts of matching words: {calls_data['MATCHING_TEXT'].value_counts()}"
    )
