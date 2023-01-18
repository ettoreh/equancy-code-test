# test.py

import pandas as pd
import difflib as dl

from collections import Counter 
from unidecode import unidecode
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop



# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------

def selectArticleById(
    df: pd.DataFrame, id: str, col: list = []) -> pd.DataFrame:
    """ 
    select a row of the dataset using the id of the article with choosing 
    the columns.

    Args:
        df (pd.DataFrame): the dataset of articles.
        id (str): the id of the article to select.
        col (list, optional): a list of columns. Defaults to [] which means 
        all selected.

    Returns:
        pd.DataFrame: the row of the article selected with the choosen columns.
    """
    if len(col)==0:
        row = df.loc[df.id == id, :].reset_index(inplace=False, drop=True)
    elif len(col)==1:
        row = df.loc[df.id == id, col].reset_index(inplace=False, drop=True) 
    else:
        row = df.loc[df.id == id, col]
    return row.reset_index(inplace=False, drop=True)            



# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------

def removeExactDuplicates(
    df: pd.DataFrame) -> list:
    """
    compares each articles to each other and remove those with the exact same
    title and text.

    Args:
        df (pd.DataFrame): the dataset of articles.

    Returns:
        list: the list of article ids which doesn't contain exact duplicates.
    """
    text_ids = list(df.id)
    for id1 in text_ids:
        for id2 in text_ids[text_ids.index(id1)+1:]:
            text1 = selectArticleById(df, id1, ['texte', 'titre'])
            text2 = selectArticleById(df, id2, ['texte', 'titre'])
            if (text1 == text2).sum(1).values[0] == 2:
                text_ids.remove(id2)
    return text_ids



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

def articleSimilarity(
    text1: str, text2: str) -> float:
    """
    compute the text similarity using the difflib library.

    Args:
        text1 (str): a first text.
        text2 (str): a second text to compare with the first.

    Returns:
        float: a percentage of similarity between 0 and 1.
    """
    return dl.SequenceMatcher(None, text1[0], text2[0]).ratio()


def articleToRemove(
    df: pd.DataFrame, id1: str, id2: str) -> str:
    """
    with two article ids, returns the one to remove according to the says of 
    the exercice.

    Args:
        df (pd.DataFrame): the dataset of articles.
        id1 (str): id of the first article.
        id2 (str): id of the second article to compare to the first.

    Returns:
        str: the id of the article to remove
    """
    article1date = selectArticleById(df, id1, ['date_de_publication']).values[0]
    article2date = selectArticleById(df, id2, ['date_de_publication']).values[0]
    article1title = selectArticleById(df, id1, ['titre']).values[0]
    article2title = selectArticleById(df, id2, ['titre']).values[0]
    if article1date == article2date:
        if len(article1title) > len(article2title):
            return id1
    else:
        if article1date < article2date:
            return id1
    return id2


def removeDuplicates(
    df: pd.DataFrame) -> list:
    """
    compares each articles to each other and remove those with textes that are
    the same or almost (modify or edit).

    Args:
        df (pd.DataFrame): the dataset of articles.

    Returns:
        list: the list of article ids which doesn't contain duplicates.
    """
    
    text_ids, to_remove = list(df.id), []
    for id1 in text_ids:
        for id2 in text_ids[text_ids.index(id1)+1:]:
            if (id1 not in to_remove) & (id2 not in to_remove):
                text1 = selectArticleById(df, id1, ['texte']).values[0]
                text2 = selectArticleById(df, id2, ['texte']).values[0]     
                ratio = dl.SequenceMatcher(None, text1[0], text2[0]).ratio()
                # ratio = wordFrequencyScore(text1[0], text2[0])
                if ratio >= 0.9:
                    id = articleToRemove(df, id1, id2)
                    to_remove.append(id)
                    if id == id1:
                        break
    for id in to_remove:
        text_ids.remove(id)
    return text_ids


def wordFrequencyScore(t1: str, t2: str) -> float:
    """
    compute the text similarity using the word frequency of each article.

    Args:
        t1 (str): one text.
        t2 (str): a second text to compare to the first.

    Returns:
        float: a percentage of similarity between 0 and 1.
    """
    for p in ['\n', '\xa0', '.', ':', ',', '!', '?', ';', '«', '»', '(', ')', '’']:
        t1, t2 = t1.replace(p, ' '), t2.replace(p, ' ')
    
    t1, t2 = unidecode(t1.lower()).split(), unidecode(t2.lower()).split()
    
    for w1, w2 in zip(t1, t2):
        if w1 in fr_stop:
            t1.remove(w1)
        if w2 in fr_stop:
            t2.remove(w2)
        
    freq1, freq2 = Counter(t1), Counter(t2)   
    words = list(freq1.keys())
    words.extend(list(freq2.keys()))
    words = list(set(words))

    diff, somme = [], []
    for word in words:
        diff.append(abs(freq1[word]-freq2[word]))
        somme.append(freq1[word])
        somme.append(freq2[word])
    
    return (1-(sum(diff)/sum(somme)))



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------

def includedArticleToRemove(
    df: pd.DataFrame, id1: str, id2: str) -> str:
    """
    for two article ids with one included in the other, returns the one to
    remove according to the says of the exercice.

    Args:
        df (pd.DataFrame): the dataset of articles.
        id1 (str): id of the first article.
        id2 (str): id of the second article to compare to the first.

    Returns:
        str: _description_
    """
    text1 = len(selectArticleById(df, id1, ['texte']).values[0])
    text2 = len(selectArticleById(df, id2, ['texte']).values[0])
    id = id2
    if text1 >= text2:
        id = id1
    return id
    
            
def duplicatedArticleToRemove(
    df: pd.DataFrame, id1: str, id2: str) -> str:
    """
    for two article ids with close textes, returns the one to remove according 
    to the says of the exercice.

    Args:
        df (pd.DataFrame): the dataset of articles.
        id1 (str): id of the first article.
        id2 (str): id of the second article to compare to the first.

    Returns:
        str: _description_
    """
    article1date = selectArticleById(df, id1, ['date_de_publication']).values[0]
    article2date = selectArticleById(df, id2, ['date_de_publication']).values[0]
    article1title = selectArticleById(df, id1, ['titre']).values[0]
    article2title = selectArticleById(df, id2, ['titre']).values[0]
    if article1date == article2date:
        if len(article1title) > len(article2title):
            return id1
    else:
        if article1date < article2date:
            return id1
    return id2


def removeDuplicatesAndInsides(
    df: pd.DataFrame) -> list:
    """
    compares each articles to each other and remove those with textes that are
    the same, almost the same (modify or edit) or those that are inside an 
    other.

    Args:
        df (pd.DataFrame): the dataset of articles.

    Returns:
        list: the list of article ids which doesn't contain duplicates.
    """
    
    text_ids, to_remove = list(df.id), []
    for id1 in text_ids:
        for id2 in text_ids[text_ids.index(id1)+1:]:
            if (id1 not in to_remove) & (id2 not in to_remove):
                text1 = selectArticleById(df, id1, ['texte']).values[0]
                text2 = selectArticleById(df, id2, ['texte']).values[0]     
                ratio = dl.SequenceMatcher(None, text1[0], text2[0]).ratio()
                id = id2
                if ratio >= 0.9:
                    id = duplicatedArticleToRemove(df, id1, id2)
                    to_remove.append(id)
                elif ratio >= 0.5:
                    id = includedArticleToRemove(df, id1, id2)
                    to_remove.append(id)
                if id == id1:
                    break
    for id in to_remove:
        text_ids.remove(id)
    return text_ids



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------

