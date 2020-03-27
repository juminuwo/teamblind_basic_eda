import spacy
import pandas as pd

threads = pd.read_csv('threads.csv').drop_duplicates().reset_index(drop=True)
threads.columns = ['content', 'company', 'url']
nlp = spacy.load('en_core_web_lg')

content_table = []
for content1 in threads['content']:
    content_table_inner = []
    for content2 in threads['content']:
        similarity = nlp(content1).similarity(nlp(content2))
        content_table_inner.append(similarity)
        print(similarity)
    content_table.append(content_table_inner)

counter = 0
for sim_scores in content_table:
    threads = pd.concat(
        [threads, pd.DataFrame({'doc' + str(counter): sim_scores})], axis=1)
    counter += 1

threads.to_csv('threads_scores.csv', index=False)
