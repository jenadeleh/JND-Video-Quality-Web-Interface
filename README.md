## Goal
 
## Set up the environment
Clone repo
```
git git@github.com:jenadeleh/JND-Video-Quality-Web-Interface.git
```

Add a SECRET_KEY of Django to ~/.bashrc <br />
Get a token from https://django-secret-key-generator.netlify.app/

```
> echo 'export SECRET_KEY="token"' >> ~/.bashrc 
> source ~/.bashrc
```

Setup Python virtual environment
```
> apt install python3-venv
> python3 -m venv videojnd-venv
> source videojnd-venv/bin/activate
```
Install python dependencies <br />
In directory ../video_jnd
```
> pip install requirements.txt
```

Configure Django project <br />
In directory ../video_jnd/videoJnd
```
> python3 manage.py makemigrations
> python3 manage.py migrate
> python3 manage.py createsuperuser # for admin page
```

Launch website <br />
In directory ../video_jnd/videoJnd
```
> python3 manage.py runserver
# Open http://127.0.0.1:8000/quahit/ in firefox
```

## For development
- Front-end <br/>
../video_jnd/GUI is for study HIT <br/>
../video_jnd/gui_quahit is for qualification HIT <br/>

  We developed the two HITs separately. However, most of the functions are the same. So the better way refactor the code.

    To run the two interfaces, run the following commands in ../video_jnd/GUI and ../video_jnd/gui_quahit, respectively.
    ```
    npm install
    npm start
    ```
    To compile the code, please run
    ```
    webpack ./src/main.js -o ./dist/bundle.js
    ```
    The compiled codes are stored in folder ../dist. <br/>
    After finished developing the front-end, the .html, .js, .css files need to be copied to the folder of Django project.

    Go to folder video_jnd/videoJnd/videoJnd/src/utils
    ```
    # comment / uncomment
    # hit = "studyhit"
    # hit = "quahit"

    python3 cp_front_files.py
    ```

- Back-end <br/>
../video_jnd/videoJnd is for backend <br/>


  
