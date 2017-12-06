from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier                  # метод опорных векторов
from sklearn.linear_model import LogisticRegression             # Логистическая регрессия


good_categories = ['Музыка\n', 'Технологии\n', 'Кино\n', 'Авто\n',
                       'Финансы\n', 'Спорт\n', 'Власть\n', 'Общество\n', 'Происшествия\n']


def delete_category(fake_news,fake_category):
    i = 0
    while i < len(fake_category):
        if fake_category[i] not in good_categories:
            fake_category.pop(i)
            fake_news.pop(i)
            continue
        i += 1
    return fake_news,fake_category


def find_target(one_category):
    for i in range(len(categories_sort)):
        if one_category == categories_sort[i]:
            return target[i]


def get_mas_target(category):
    mas_target = []
    for i in range(len(category)):
        mas_target.append(find_target(category[i]))
    return mas_target


def sort_category(category):
    categories_sort = []
    for x in category:
        if x in categories_sort:
            continue
        else:
            categories_sort.append(x)
    target = [i for i in range(len(categories_sort))]
    return categories_sort,target


def get_news_and_category_from_file():
    with open('file_news_correct.txt', 'r', encoding='utf8') as output_file:
        length_file = len(output_file.readlines())
        output_file.seek(0)
        mas_news = []
        for i in tqdm(range(0, length_file)):
            line = output_file.readline()
            mas_news.append(line)
        output_file.seek(0)
    with open('file_category_correct.txt', 'r', encoding='utf8') as output_file:
        length_file = len(output_file.readlines())
        output_file.seek(0)
        mas_category = []
        for i in tqdm(range(0, length_file)):
            line = output_file.readline()
            mas_category.append(line)
        output_file.seek(0)

    return mas_news,mas_category


def classifier():
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(news)
    tfidf_transformer = TfidfTransformer()
    x_train_tfidf = tfidf_transformer.fit_transform(x_train)
    clf = LogisticRegression().fit(x_train_tfidf, mas_target)
    text_clf = Pipeline([('vectorizer', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', LogisticRegression())])# 0.71 - SVM; 0.82 - LogReg;
    # обучение
    text_clf = text_clf.fit(news, mas_target)
    return text_clf, vectorizer, tfidf_transformer, clf


news, category = get_news_and_category_from_file()
news, category = delete_category(news,category)
categories_sort, target = sort_category(category)
mas_target = get_mas_target(category)
text_clf, vectorizer, tfidf_transformer, clf = classifier()