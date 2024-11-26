FROM mysql:9.1

COPY ./conf.d/my.cnf /etc/mysql/conf.d/my.cnf

COPY ./sql/ /sql/

RUN chmod 644 etc/mysql/conf.d/my.cnf && mkdir -p /var/log/mysql \
    && chown -hR mysql:mysql /var/log/mysql