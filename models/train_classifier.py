import sys
import pandas as pd
import sklearn
import nltk
import pickle as pkl
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.base import BaseEstimator, TransformerMixin
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def load_data(database_filepath):
    """
    This function loads the data from the database created in the process data.py file and gets the input | labels from
    the data, together with the labels columns.
    :param database_filepath: String containing the name of the database created before.
    :return: input values for the model, labels (ground truth) and ground truth columns.
    """
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table('message', engine)
    X = df['message']
    Y = df.drop(['id', 'message', 'original', 'genre'], axis=1)
    return X, Y, Y.columns

def tokenize(text):
    """
    This function takes input text from the input data, tokenizes, lemmatizes and cleans it for NLP purposes.
    :param text: String (sentence) for tokenization.
    :return: Tokenized list of words.
    """
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    """
    Creates a sklearn pipeline for training model together with previous data-treatment processing.
    :return: Model creation pipeline.
    """
    pipeline = Pipeline([
    ('vect', CountVectorizer(tokenizer=tokenize)),
    ('tfidf', TfidfTransformer()),
    ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    parameters = {'clf__estimator__n_estimators': [10, 20, 100]}

    pipeline = GridSearchCV(pipeline, param_grid=parameters)
    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """
    This function takes real testing data and gets metrics for the performance of the model.
    :param model: Pipeline created in the build model function.
    :param X_test: Input data never seen by the model.
    :param Y_test: Ground truth data never seen by the model.
    :param category_names: Classification names for the ground truth values.
    :return: None
    """
    y_pred = model.predict(X_test)
    y_pred = pd.DataFrame(y_pred, columns = category_names)

    for i, var in enumerate(Y_test):
        print('--- ',var,'category ---')
        print(classification_report(Y_test.iloc[:,i], y_pred.iloc[:,i]))
        print('\n'*3)
    print("Model's overall accuracy: ", (y_pred.values == Y_test.values).mean())
   


def save_model(model, model_filepath):
    """
    This function saves the model to a desired path.
    :param model: Final trained pipeline | model.
    :param model_filepath: String of the desired path for the introduced model.
    :return: None
    """
    pkl.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()