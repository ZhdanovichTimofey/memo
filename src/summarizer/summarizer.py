from config.config import SBER_API_KEY

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

MODEL = "gpt-3.5-turbo-1106"
MAX_WORDS = 1000  # max_tokens = 2048


system_prompt = '''Твоя задача выделить главную информацию из записи совещания. 
            Выдели несколько главных тезисов, которые обсуждались и перечисли их.
            Постарайся сохранить важные детали.
            Твой ответ должен содержать ТОЛЬКО ТЕЗИСЫ, в формате "{порядковый_номер}. {Тезис}\n".
            '''
class Summarizer():
    def __init__(self, combined_text):
        self.texts = [text for (text, speaker) in combined_text]
        self.speakers = [speaker for (text, speaker) in combined_text]
        self.chat = GigaChat(credentials=SBER_API_KEY, verify_ssl_certs=False)        

    def summarize(self):
        summaries = self.get_summary()
        size = len(summaries)
        summary = ''
        for i, part in enumerate(summaries):
            summary += f'Часть {i + 1} из {size}:\n'
            if part.split('\n')[0] == 'Тезисы:':
                part = '\n'.join(part.split('\n')[1:])
            summary += part + '\n\n'
        return summary

    def get_summary(self):
        texts = self.prepare_texts()
        result = []
        for text in texts:
            prompt = text
            try:
                response = self.get_completion(prompt)
            except:
                response = self.get_completion(prompt)
            result.append(response)
        return result

    def prepare_texts(self):
        curr_size = 0
        curr_text = ''
        text = []
        for line in self.texts:
            num_words = len(line.split(' '))
            if num_words + curr_size < MAX_WORDS:
                curr_text += line
                curr_size += num_words
            else:
                text.append(curr_text)
                curr_text = line
                curr_size = num_words
        text.append(curr_text)
        return text

    def get_completion(self, prompt, model=MODEL):
        messages = [SystemMessage(content=system_prompt)]
        messages.append(HumanMessage(content=prompt))
        response = self.chat(messages)
        return response.content