# Chat PDF

Ask questions of any PDF.

A 100% on-device Retrieval Augmented Generation (RAG) example using ollama / tinyllama with langchain. User interface courtesy of streamlit.

## Pre-requisites

- You'll need docker desktop: https://www.docker.com/products/docker-desktop/
- A decent computer with at least 8GB RAM should suffice. You'll need several GB of disk space for the llama models.


## I just want to run it!

1. `docker-compose up` Watch the console output. When it stops the model is downloaded and ready.
2. Open up this url: http://localhost:8051 and follow the instructions.
3. Please be patient... it takes 5 minutes to vectorize the PDF in the `testing` folder.
4. Please be patient... it takes a few minutes to answer your questions. I have an 11th gen Intel i9.
5. When you are done, make sure to `docker-compose down`

## I want to see the code!

Good! The application was written in a VS Code devcontainer.

1. Open `vscode`
2. Open the `chat-pdf` folder.
3. You will be asked to load the dev container. Do this, but be patient as it takes time to build.
4. You can now run or debug the `app.py` program!

NOTE: If the devcontainer does not work you likely have stopped containers, run: `docker-compose down` 

Thanks,
m
