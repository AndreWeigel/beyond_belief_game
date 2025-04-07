import random
import wiki_api
import lie_gen

def main_game_loop():
    page_title, sentences = wiki_api.get_valid_wikipedia_page_info()

    selected_sentences = random.sample(sentences[:6], 3)

    # Step 2: Apply transformation to one random sentence
    index_to_transform = random.randrange(3)
    selected_sentences[index_to_transform] = lie_gen.generate_lie(selected_sentences[index_to_transform])


    print(page_title)
    for sentence in selected_sentences:

        if sentence == selected_sentences[index_to_transform]:
            print(f"LIE:{sentence}")
        else:
            print(sentence)



main_game_loop()


"""
1 - when we have dates the number trick does not work
2 - when there is math in the sentence it does not work
3 - there are all these equal signs that are kinda weird

"""