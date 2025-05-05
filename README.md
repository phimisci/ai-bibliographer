A protoype web app that sends handwritten bibliographical references input by the user to the API of a LLM and returns the output as a `.bib` file. Currently, only Anthropic is supported.

The presence of an `.env` file is expected, containing at minimum:

```
ANTHROPIC_API_KEY=your_api_key
WEBSITE_TITLE=Title of website 
```

This web app is built with streamlit. To run it:

```
$ streamlit run ai_bibliographer.py
```


# Sample Dockerfile

```dockerfile
FROM python:3-slim
WORKDIR /ai-bibliographer

COPY . /ai-bibliographer
RUN pip install --no-cache-dir anthropic python-dotenv streamlit
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "ai_bibliographer.py", "--server.port=8501"]
```
