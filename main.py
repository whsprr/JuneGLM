import re
from collections import Counter
import random

def process_text_operations(file_path, chunk_size, user_phrase):
  def preprocess_text(text):
      return text

  def process_text_in_chunks(file_path, chunk_size, n):
      ngram_dict = {}
      with open(file_path, 'r') as file:
          while True:
              chunk = file.read(chunk_size)
              if not chunk:
                  break

              chunk = preprocess_text(chunk)
              words = chunk.split()
              for i in range(len(words) - n):
                  context = tuple(words[i:i + n])
                  next_word = words[i + n]

                  if context in ngram_dict:
                      ngram_dict[context].append(next_word)
                  else:
                      ngram_dict[context] = [next_word]

      return ngram_dict

  def find_word_occurrences_in_chunks(file_path, phrase, chunk_size):
      occurrences = []
      with open(file_path, 'r') as file:
          while True:
              chunk = file.read(chunk_size)
              if not chunk:
                  break

              chunk = preprocess_text(chunk)
              words = chunk.split()
              input_words = phrase.split()

              for i in range(len(words) - 1):
                  if words[i].lower() == input_words[0].lower():
                      if words[i + 1].lower().startswith(input_words[1].lower()):
                          occurrences.append(words[i + 1])

      return occurrences

  def generate_sentence_with_correction(ngram_dict, input_context, corrected_word):
      sentence = list(input_context[:-1])  # Exclude the incomplete part of the phrase
      sentence.append(corrected_word)  # Append the corrected word
      sentence.extend(predict_next_word(ngram_dict, sentence))  # Generate sentence
      return ' '.join(sentence)

  def predict_next_word(ngram_dict, context, max_words=100):
     predicted_words = []
     current_context = tuple(context)  # Convert context to a tuple

     for _ in range(max_words):
         if current_context in ngram_dict:
             possible_next_words = ngram_dict[current_context]
             if len(possible_next_words) == 1 and possible_next_words[0] == '.':
                 predicted_words.append('.')
                 break  # Stop if the only predicted word is a full stop
             next_word = random.choice(possible_next_words)
             predicted_words.append(next_word)
             if next_word == '.':
                 break  # Stop if the predicted word is a full stop
             current_context = tuple(list(current_context[1:]) + [next_word])
         else:
             break

     return predicted_words
  default_n = 2  # Default n-gram size if the input is shorter
  ngram_dictionary = process_text_in_chunks(file_path, chunk_size, default_n)

  word_occurrences = find_word_occurrences_in_chunks(file_path, user_phrase, chunk_size)

  if len(word_occurrences) > 0:
      most_common_word = Counter(word_occurrences).most_common(1)[0][0]
      print(f"The most common word following the first word in the phrase is: {most_common_word}")

      input_context = user_phrase.split()
      input_context[-1] = most_common_word

      corrected_sentence = generate_sentence_with_correction(ngram_dictionary, input_context, most_common_word)
      print(f"Generated sentence starting from '{' '.join(input_context)}': \n {corrected_sentence}")
  else:
      print(f"No words following the first word in the phrase were found in the text.")

print("""                                                                         
       _|                                  _|_|_|  _|        _|      _|  
       _|  _|    _|  _|_|_|      _|_|    _|        _|        _|_|  _|_|  
       _|  _|    _|  _|    _|  _|_|_|_|  _|  _|_|  _|        _|  _|  _|  
 _|    _|  _|    _|  _|    _|  _|        _|    _|  _|        _|      _|  
   _|_|      _|_|_|  _|    _|    _|_|_|    _|_|_|  _|_|_|_|  _|      _|  
                            
""")


file_path = "TextModel.txt"  # Replace with the path to your text file
chunk_size = 10000  # Define your chunk size here
user_phrase = input("Enter a phrase to find occurrences and predict the next words: ")

process_text_operations(file_path, chunk_size, user_phrase)
