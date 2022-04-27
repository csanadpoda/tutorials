# Tutorials
## (Mostly Python and ML/AI) tutorials for you to learn from!

### 1 - DialoGPT Chatbot

I put together a quick demo on how to use huggingface models in your own chatbots. In the `backend/load_model.py` file you can replace the model name in the line `model_name = "microsoft/DialoGPT-medium"` to any dialogue-capable model to play around with it. The `frontend` folder has a small React app that allows you to interface with the model.

To set it up, you can either run `load_model.py` on your console and then start `app.py` to host the model's API and also the frontend via an `npm start` after installing the node requirements, or you can easily containerize them as separate containers for frontend and backend via the supplied `Dockerfile`s. When running with Docker or via localhost, NVIDIA GPU support is enabled (for Docker use the `--gpus=all` flag to allow this). You can also deploy the dockerized images via Kubernetes with the supplied `config.yaml` file and expose the service via the supplied `service.yaml` file. This is NOT a production-ready system, many npm-related vulnerabilities have not been fixed. It's for learning purposeds only.

Big thanks for [huggingface](https://huggingface.co/microsoft/DialoGPT-medium) for hosting the models and [DialoGPT](https://github.com/microsoft/DialoGPT) specifically, and [Lucas Bassetti](https://www.google.com) whose [React Simple Chatbot](https://lucasbassetti.com.br/react-simple-chatbot/#/) NPM-module I've hacked for this to work.

### 2 - Transfer Learning

We take a look at what Transfer Learning is, how it works and how you can modify it to teach it something new with Keras!

### 3- Classification

We perform basic classification on some telco data: Some data cleaning and feature selection methods are demonstrated in addition to multiple models. We also check some methods on how to deal with an unbalanced dataset.

### 4- MNDWRK webinar [HUN]

A spiced-up version of SKLearn's "Faces recognition example using eigenfaces and SVMs" tutorial, used for a webinar for MNDWRK. Additional explanation of steps in Hungarian.
