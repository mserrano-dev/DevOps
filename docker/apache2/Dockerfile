FROM ubuntu:17.10
LABEL maintainer="markanthony.serrano2@gmail.com"

RUN apt-get update \
    && apt-get install -y apache2 php libapache2-mod-php php-mcrypt php-mysql \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled/rewrite.load \
    && ln -s /etc/apache2/mods-available/expires.load /etc/apache2/mods-enabled/expires.load \
    && rm /etc/apache2/sites-enabled/000-default.conf \
    && service apache2 restart
    
EXPOSE 80/tcp

CMD /usr/sbin/apache2ctl -D FOREGROUND
