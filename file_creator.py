
import os
import sqlite3
from xlsxwriter import Workbook


def get_consumer_list(con, tablename):

    cursor = con.cursor()
    arg = 'SELECT consumer Connection FROM {}'. format(tablename)
    cursor.execute(arg)
    results = cursor.fetchall()
    # print(results)
    return results


def get_queries_from_db(con, tablename):
    table_name = tablename
    cursor = con.cursor()
    result_container = []

    for i in ['C1', "C2", "C3", "C4", "C5"]:
        args = "SELECT ImportUnits, ExportUnits, DifUnits FROM {} WHERE  Connection = '{}'".format(tablename, i)
        cursor.execute(args)
        result = cursor.fetchall()
        result_container.append(result)
    return result_container


def write_cons_excel(row, column, db_results, worksheet):
    r = row
    c = column
    previous_consumer = None
    for cons in db_results:
        consumer = cons[0]
        if consumer != previous_consumer or consumer == None:
            worksheet.write(r, c, consumer)
            r += 1
            previous_consumer = consumer

        else:
            pass


def write_excel(row, column, db_results, worksheet):
    r = row
    c = column
    for result in db_results:
        imp, exp, dif = (result)
        worksheet.write(r, c, imp)
        worksheet.write(r, c + 5, exp)
        worksheet.write(r, c + 10, dif)
        r += 1


def writer(con, tablename, workbook, worksheet):
    cons = get_consumer_list(con, tablename)
    results = get_queries_from_db(con, tablename)
    write_cons_excel(0, 0, cons, worksheet)
    c = 1
    for i in results:
        write_excel(0, c, i, worksheet)
        c += 1
    workbook.close()


def xldownloader(filename):
    con = sqlite3.connect('ReadingsV1onAPP.db')
    workbook = Workbook('{}.xlsx'.format(filename))
    worksheet = workbook.add_worksheet(filename)
    tablename = filename
    writer(con, tablename, workbook, worksheet)
