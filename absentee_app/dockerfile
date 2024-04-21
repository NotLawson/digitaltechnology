FROM tensorflow/tensorflow:latest

COPY app /

VOLUME [ "/etc/localtime:/etc/localtime:ro" ]

RUN python3 -m pip install pillow flask numpy blinker==1.4

CMD ["python3", "main.py"]
#CMD ["/bin/bash"]