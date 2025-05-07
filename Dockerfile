# this sets up to container with python 3.10 installed
FROM python:3.10-slim

# this copies everything in current directory to the app/directory in the container
COPY . /app

# this sets the /app directory as the working directory for any run, cmd,  entrypoint or copy instructions that follw
WORKDIR /app

#this runs pip install for all the packages listed in  requirements.txt file
RUN pip install -r requirements.txt

# this tells docker to listen on port 80 at runtime
EXPOSE 80

#this command creates a .stremalit directory in the home directory of the container
RUN mkdir -/.stremalit

# this copies streamlit configuration file into the .streamlit directory just created
RUN cp config.toml -/streamlit/config.toml

#copies streamlit credentials file into the .streamlit directory
RUN cp credentials.toml -/streamlit/credentials.toml

#sets the default commant for the container to run the app with streamlit
ENTRYPOINT [ "streamlit","run" ]

# tells streamlit to run app.py script when the container starts
CMD [ "main.py" ]