import openai
from sklearn.metrics.pairwise import cosine_similarity

from markdown_cleaner import clean_markdown


class TextAnalyser:
    MATCHING_THRESHOLD = 0.805
    openai_key = ""
    resume_embedding: list[float]

    def __init__(self, openai_key, resume_text):
        self.openai_key = openai_key
        self.resume_embedding = self.get_embedding(clean_markdown(resume_text))

    def get_embedding(self, text):
        """
        This function generates an embedding using OpenAI's API for the input text.

        Args:
            text (str): The text to generate an embedding for.

        Returns:
            list: A list of embeddings for the input text.
        """
        client = openai.OpenAI(api_key=self.openai_key)  # Initialize OpenAI client
        model = "text-embedding-ada-002"

        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding

    def get_similarity(self, job_description):
        job_embedding = self.get_embedding(clean_markdown(job_description))
        similarity = cosine_similarity([self.resume_embedding], [job_embedding])
        return similarity[0][0]

    def matching(self, job_description):
        similarity = self.get_similarity(job_description)
        print(similarity)
        return similarity >= self.MATCHING_THRESHOLD
