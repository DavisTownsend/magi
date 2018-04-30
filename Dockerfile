FROM continuumio/anaconda3
ADD https://raw.githubusercontent.com/DavisTownsend/Cryfolio/master/requirements.txt /tmp/
RUN mkdir opt/notebooks
#installs gcc C++ compiled libraries
RUN apt-get update && apt-get install -y gcc unixodbc-dev

#RUN conda install --yes --file /home/requirements.txt
#install and upgrade pip installer
RUN conda install pip
RUN pip install pip --upgrade

#install requirements file
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/

ADD https://raw.githubusercontent.com/DavisTownsend/Dask-fcast/master/example_notebooks/Parallel%20Time%20Series%20Forecasting%20in%20Python%20with%20Dask.ipynb opt/notebooks

#EXPOSE 8888
#CMD ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token='demo'"]
#CMD jupyter notebook --no-browser --ip 0.0.0.0 --port 8888 /notebooks
