FROM python-base as production
USER $USER_NAME
RUN python3 -m venv $VENV_PATH
WORKDIR /code/src
COPY . .
COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade setuptools==59.6.0 \
    && poetry config experimental.new-installer false \
    && poetry install --no-dev --no-interaction --no-ansi
RUN cp .env.example .env
ENTRYPOINT ["bash", "/code/src/docker-entrypoint.sh"]
CMD ["uvicorn", "news.main:app", "--port=8000", "--host=0.0.0.0"]