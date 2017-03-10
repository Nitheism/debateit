from nltk import word_tokenize, pos_tag, data
import numpy as np
from collections import Counter
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


# The algorithm for agrumentation rating

def get_rating(text):
    # add my static folder to nltk path so it can work on the host as well
    data.path.append('static/nltk_data/')
    dictionary = joblib.load('static/MLmodels/CountVect.pkl')
    count_vectorizer = CountVectorizer(vocabulary=dictionary, max_df=0.8, ngram_range=(1, 3))

    words = word_tokenize(text)
    # if len(words) < 2:
    #     return -1

    tags = pos_tag(words)
    counts = Counter(tag for word, tag in tags)
    md, can, could, shall, should, must, may, might, will, would = get_modals(words, len(words), counts.get('MD'))
    advb_ratio, adj_ratio, jjs_ratio, rbs_ratio = get_adj_adv(counts, len(words))
    noun_ratio, verb_ratio = noun_verb_rates(counts, len(words))
    pro_ratio, prep_ratio, interj_ratio = prep_pro_interj(counts, len(words))
    # noun ratio + adj ratio + prepositions ratio  - pronoun ratio - verb ratio -
    # adverb - interjection + 1
    context_measure = (noun_ratio + adj_ratio + prep_ratio - pro_ratio -
                       verb_ratio - advb_ratio - interj_ratio + 1) * 0.5
    x = count_vectorizer.transform(words)
    x = x.toarray()
    features = pd.DataFrame(x)
    features['adj'] = pd.Series(adj_ratio, index=features.index)
    features['advb'] = pd.Series(advb_ratio, index=features.index)
    features['noun'] = pd.Series(noun_ratio, index=features.index)
    features['prep'] = pd.Series(prep_ratio, index=features.index)
    features['pro'] = pd.Series(pro_ratio, index=features.index)
    features['interj'] = pd.Series(interj_ratio, index=features.index)
    features['verb'] = pd.Series(verb_ratio, index=features.index)
    features['rbs'] = pd.Series(rbs_ratio, index=features.index)
    features['jjs'] = pd.Series(jjs_ratio, index=features.index)
    features['contextuality'] = pd.Series(context_measure, index=features.index)
    features['modals'] = pd.Series(md, index=features.index)
    features['will'] = pd.Series(will, index=features.index)
    features['should'] = pd.Series(should, index=features.index)
    features['could'] = pd.Series(could, index=features.index)
    features['can'] = pd.Series(can, index=features.index)
    features['may'] = pd.Series(may, index=features.index)
    features['might'] = pd.Series(might, index=features.index)
    features['shall'] = pd.Series(shall, index=features.index)
    features['would'] = pd.Series(would, index=features.index)
    features['must'] = pd.Series(must, index=features.index)
    features['must'] = pd.Series(len(words), index=features.index)

    regression = joblib.load('static/MLmodels/Regression.pkl')

    return np.median(regression.predict(features))


def prep_pro_interj(counts, length):
    all_prep = 0
    all_interj = 0
    all_pro = 0
    if counts.get('UH') is not None:
        all_interj = counts.get('UH')
    if counts.get('IN') is not None:
        all_prep = counts.get('IN')
    if counts.get('PRP') is not None:
        all_pro += counts.get('PRP')
    if counts.get('PRP$') is not None:
        all_pro += counts.get('PRP$')
    if all_pro != 0:
        all_pro = all_pro / length
    if all_prep != 0:
        all_prep = all_prep / length
    if all_interj != 0:
        all_interj / length
    return all_pro, all_prep, all_interj


def noun_verb_rates(counts, lenght):
    all_verbs = 0
    all_nouns = 0
    if counts.get('VB') is not None:
        all_verbs += counts.get('VB')
    if counts.get('VBG') is not None:
        all_verbs += counts.get('VBG')
    if counts.get('VBD') is not None:
        all_verbs += counts.get('VBD')
    if counts.get('VBN') is not None:
        all_verbs += counts.get('VBN')
    if counts.get('VBP') is not None:
        all_verbs += counts.get('VBP')
    if counts.get('VBZ') is not None:
        all_verbs += counts.get('VBZ')
    if counts.get('NN') is not None:
        all_nouns += counts.get('NN')
    if counts.get('NNS') is not None:
        all_nouns += counts.get('NNS')
    if counts.get('NNP') is not None:
        all_nouns += counts.get('NNP')
    if counts.get('NNPS') is not None:
        all_nouns += counts.get('NNPS')

    if all_verbs != 0:
        all_verbs = all_verbs / lenght
    if all_nouns != 0:
        all_nouns = all_nouns / lenght
    return all_nouns, all_verbs


def get_adj_adv(counts, lenght):
    jjs = 0
    jj = 0
    jjr = 0
    rbs = 0
    rbr = 0
    rb = 0
    jjs_ratio = 0
    rbs_ratio = 0
    advb_ratio = 0
    adj_ratio = 0
    if counts.get('JJS') is not None:
        jjs = counts.get('JJS')
    if counts.get('JJ') is not None:
        jj = counts.get('JJ')
    if counts.get('JJR') is not None:
        jjr = counts.get('JJR')
    if counts.get('RB') is not None:
        rb = counts.get('RB')
    if counts.get('RBS') is not None:
        rbs = counts.get('RBS')
    if counts.get('RBR') is not None:
        rbr = counts.get('RBR')

    all_advb = rb + rbr + rbs
    all_adj = jjs + jj + jjr
    if all_advb != 0:
        rbs_ratio = rbs / all_advb
        advb_ratio = all_advb / lenght
    if all_adj != 0:
        jjs_ratio = jjs / all_adj
        adj_ratio = all_adj / lenght
    return advb_ratio, adj_ratio, jjs_ratio, rbs_ratio


def get_modals(words, lenght, all_md):
    can = 0
    could = 0
    might = 0
    may = 0
    must = 0
    should = 0
    will = 0
    would = 0
    shall = 0
    md = 0
    for a in words:
        if a == 'could':
            could += 1
        if a == 'can':
            can += 1
        if a == 'might':
            might += 1
        if a == 'may':
            may += 1
        if a == 'should':
            should += 1
        if a == 'will':
            will += 1
        if a == 'would':
            would += 1
        if a == 'shall':
            shall += 1
        if a == 'must':
            must += 1
    if can != 0:
        can = can / lenght

    if could != 0:
        could = could / lenght

    if might != 0:
        might = might / lenght
    if may != 0:
        may = may / lenght

    if must != 0:
        must = must / lenght

    if should != 0:
        should = should / lenght

    if will != 0:
        will = will / lenght

    if would != 0:
        would = would / lenght

    if shall != 0:
        shall = shall / lenght

    if all_md is not None:
        md = all_md / lenght

    return md, can, could, shall, should, must, may, might, will, would
