FROM tensorflow/tensorflow:2.8.4

RUN python -m pip install --upgrade pip
RUN pip install prompt_toolkit==2.0.10 pygments websockets

COPY datasets/mnist.npz /root/.keras/datasets/mnist.npz
RUN python --version
COPY . /project
WORKDIR /project


ENV PYTHONPATH=${PYTHONPATH}:/project

ENTRYPOINT [ "python", "main.py"]


