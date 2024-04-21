# Absentee app

## Docker (Recomended)

```docker run --name absentee_app -v /etc/localtime:/etc/localtime:ro -p <outside>:8080 -d ghcr.io/notlawson/absentee_app```

## Python

Install packages <br> `pip install tensorflow-cpu==2.15.0 pillow flask numpy`
<br> Run with <br> `python main.py`
