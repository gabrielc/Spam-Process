#! /usr/bin/python
# vim:fileencoding=utf-8

# Bibliotecas
import os,sys,datetime,re,MySQLdb
from pprint import pprint # para debug...

class LogFileProcess:
    """A simple example class"""
    i = 12345
    def f(self):
        return 'hello world'


class SimpleDataBase:
    """ Deals with the connection and transferences with the "spam_data" mysql
    database.
    """

    def __init__(self, DB_HOST,DB_USER,DB_PASSWD,DB_SCHEMA):

        # Make the connection.

        try:
            self.conn = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWD, DB_SCHEMA)
        except:
            erro = "Erro: SimpleDataBase: Não foi possivel conectar ao banco."
            print >>sys.stderr, erro
            print >>sys.stdout, erro
            raise

        # Important Queries:
        self.QUERY_MAIN = """INSERT INTO `spam_data`.`fatorial_dados_gerais`
        (`id`, `dia`, `mes`, `ano`, `targ`, `ip`, `num_men`, `num_con`,
        `n_rcpt`, `n_dom`, `acc_size`)
        VALUES ( NULL , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        self.QUERY_GET_ID_GENERIC = [
            "SELECT `id` FROM `fatorial_dados_gerais_",
            "` WHERE `",
            "` = %s"
            ]

        self.QUERY_INSERT_GENERIC = [
            "INSERT INTO `spam_data`.`fatorial_dados_gerais_",
            "` (`id`, `",
            "`) VALUES (NULL, %s)"
            ]

        self.QUERY_INSERT_LIG_GENERIC = [
           "INSERT INTO `spam_data`.`fatorial_dados_gerais_lig_",
           "` (`id`, `id_",
           "`) VALUES (%s, %s);"
           ]

        self.QUERY_GET_ID_DOMAIN = 'domain'.join(QUERY_GET_ID_GENERIC)
        self.QUERY_INSERT_DOMAIN = 'domain'.join(QUERY_INSERT_GENERIC)
        self.QUERY_INSERT_LIG_DOMAIN = 'domain'.join(QUERY_INSERT_LIG_GENERIC)

        self.QUERY_GET_ID_PROTOCOL = 'protocol'.join(QUERY_GET_ID_GENERIC)
        self.QUERY_INSERT_PROTOCOL = 'protocol'.join(QUERY_INSERT_GENERIC)
        self.QUERY_INSERT_LIG_PROTOCOL = 'protocol'.join(
            QUERY_INSERT_LIG_GENERIC)
        self.QUERY_INSERT_RCPT = ''' INSERT INTO
        `spam_data`.`fatorial_dados_gerais_rcpt`
        (`id`, `mail`, `domain`) VALUES (%s, %s, %s); '''

        




if __name__ == '__main__':
    function()
