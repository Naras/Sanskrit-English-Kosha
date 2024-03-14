#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'NarasMG'

import peewee, os

from Transliterate import transliterate_lines
from iscii2utf8 import *
# print(os.path.join(os.getcwd(), 'Amarakosha.db'))
conn_unicode = peewee.SqliteDatabase(os.path.join(os.getcwd(), 'Amarakosha.db'), pragmas={'journal_mode': 'wal','cache_size': -1024 * 64})
maxrows = 5

mypar = Parser()
mypar.set_script(1)
def flatMap(f, li):
    mapped = map(f, li)
    flattened = flatten_single_dim(mapped)
    yield from flattened
def flatten_single_dim(mapped):
    for item in mapped:
        for subitem in item:
            yield subitem

# isascii = lambda s: len(s) == len(s.encode())
def isascii(s):
    # import re
    # return re.search('[^\x00-\x7F]', s) is None
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False
def iscii_unicode(iscii_string, script=1):
    mypar.set_script(script)
    flush = 0
    x_as_List = [ord(char) for char in iscii_string+' ']
    n = mypar.iscii2utf8(x_as_List, flush)
    # y = x[n:]
    return ''.join([ch for ch in mypar.write_output()])
def unicode_iscii(unicode_string, script=1):
    mypar.set_script(script)
    try:
        scripts_map_unicode = mypar.make_script_maps_unicode_to_iscii()
        result_as_list = []
        for i, ch in enumerate(unicode_string):
            # print('ch %s hex %s dec %s'%(ch, hex(ord(ch)), ord(ch)))
            result_as_list.append(chr(scripts_map_unicode[ord(ch)]))
            if ord(ch) in nukta_specials.values(): result_as_list.append(chr(ISCII_NUKTA))
        return ''.join(result_as_list)
    except Exception as e:
        raise Exception('unicode_iscii: character %s unicode-string %s character %s' % (e, unicode_string, ch))
def schemaParse():
    cursor = conn_unicode.get_tables()
    mypar = Parser()
    mypar.set_script(1)
    tbls = []
    for row in cursor:
        tbls.append(row)
    return tbls
def sqlQueryUnicode(sql, param=None, maxrows=5, duplicate=False, script=1):
    # lstParam = [x for x in param] if isinstance(param,tuple) else param
    # print('sql=%s param=%s'%(sql, lstParam))
    current = 0
    if param==None: rowcursor = conn_unicode.execute_sql(sql)
    else:
        if not isinstance(param,tuple): param = (param,)
        rowcursor = conn_unicode.execute_sql(sql, param)
    try:
        result = []
        for r in rowcursor.fetchall():
            # print(r)
            resultRow = []
            for field in r:
                # resultRow.append(field)
                if isascii(str(field)):
                    resultRow.append(field)
                    if duplicate: resultRow.append(field)
                else:
                    resultRow.append(field)
                    if duplicate: resultRow.append(unicode_iscii(field))
            result += [resultRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)

    columns = [column[0] for column in rowcursor.description]
    if duplicate: columns = list(flatMap(lambda x: (x, x), columns))
    return columns, result
def tblSelectUnicode(table_name,maxrows=5,duplicate=False, script=1):
    current = 0
    rowcursor = conn_unicode.execute_sql('select * from ' + table_name)
    try:
        tbl = []
        for r in rowcursor.fetchall():
            # print(r)
            tblRow = []
            for field in r:
                if isascii(str(field)):
                    tblRow.append(field)
                    if duplicate: tblRow.append(field)
                else:
                    tblRow.append(field)
                    if duplicate: tblRow.append(unicode_iscii(str(field), script))
            tbl += [tblRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)
    columns = [column[0] for column in rowcursor.description]
    if duplicate: columns = list(flatMap(lambda x: (x, x), columns))

    return columns, tbl


if __name__ == '__main__':
    # try:
        cols, linesAmara = tblSelectUnicode('Amara_Words', maxrows=1, duplicate=False)
        # print('Amarawords: %s\n%s' % (cols, linesAmara))
        synonyms = {}
        for amaralineno, line in enumerate(linesAmara):
            amaraWord = line[1]
            cols, lines = sqlQueryUnicode('select * from Janani1 where Words like ?', '%' + amaraWord + '%') #"स्वर्ग"
            if len(lines) == 0: continue
            dictSynonyms = {}
            for lineJanani1 in lines:
                dictSynonyms['synonyms'] = lineJanani1[(cols.index("Words"))]
                for meaning in ['KanWord', 'EngWord', 'HinWord']: dictSynonyms[meaning] = lineJanani1[cols.index(meaning)]
            synonyms[amaraWord] = dictSynonyms
            vyutpattis = {}
            for table in ['V_Sanskrit', 'V_Hindi', 'V_Odiya']:
                qry = 'select Vytpatti from ' + table + ' V, Amara_Words A where V.IdNo = A.ID and A.Word = ?'
                _, linesVytpatti = sqlQueryUnicode(qry, param=amaraWord, maxrows=0)
                vyutpattis[table[2:]] = linesVytpatti
                nishpattis={}
            for table in ['N_Sanskrit', 'N_Hindi', 'N_Odiya']:
                qry = 'select Nishpatti from N_Sanskrit N, Amara_Words A where N.IdNo = A.ID and A.Word = ?'
                _, linesNishpatti = sqlQueryUnicode(qry, param=amaraWord, maxrows=0)
                nishpattis[table[2:]]=linesNishpatti
                for line in lines:
                    '''
                    print('Word/Synonyms: row % s word %s synonyms %s' % (amaralineno, amaraWord, line[(cols.index("Words"))]))
                    # for vyutpatti in linesVytpatti: print('Vyutpatti: %s'%vyutpatti)
                    # for nishtpatti in linesNishpatti: print('Nishpatti: %s'%nishtpatti)
                    # print('Vyutpattis %s\nNishpattis %s'%(vyutpattis, nishpattis))
                    print('vyutpattis')
                    for k,v in vyutpattis.items():
                        for line in v: print('\t%s %s'%(k, line))
                    print('nishpattis')
                    for k,v in nishpattis.items():
                        for line in v: print('\t%s %s'%(k, line))
                    '''
                    synonyms[amaraWord]['vyutpattis'] = vyutpattis; synonyms[amaraWord]['nishpattis'] = nishpattis
        # print(synonyms)

        import csv
        header = ['word','synonyms','Kannada','English','Hindi']
        # print(header)
        with open('synonyms.csv', 'w', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(header)  # write the header
            for k0, v0 in synonyms.items():
                writer.writerow([k0, v0['synonyms'], transliterate_lines(v0['KanWord'], 'kannada'), v0['EngWord'], v0['HinWord']])
        header = ['word', 'etymology']
        # print(header)
        with open('etymology.csv', 'w', encoding='utf-8-sig') as fv:
                writer = csv.writer(fv)
                writer.writerow(header)  # write the header
                for k0, v0 in synonyms.items():
                    # least = min(len(v0['vyutpattis']['Sanskrit']), len(v0['vyutpattis']['Hindi']), len(v0['vyutpattis']['Odiya']))
                    for etymology in v0['vyutpattis']['Sanskrit']:
                        writer.writerow([k0, etymology]) #v0['vyutpattis']['Sanskrit'][i][0], v0['vyutpattis']['Hindi'][i][0], v0['vyutpattis']['Odiya'][i][0]])
        header = ['word', 'derivation'] #'Sanskrit', 'Hindi', 'Odiya']
        # print(header)
        with open('derivation.csv', 'w', encoding='utf-8-sig') as fn:
                writer = csv.writer(fn)
                writer.writerow(header)  # write the header
                for k0, v0 in synonyms.items():
                    # least = min(len(v0['nishpattis']['Sanskrit']), len(v0['nishpattis']['Hindi']), len(v0['nishpattis']['Odiya']))
                    for derivation in v0['nishpattis']['Sanskrit']:
                        writer.writerow([k0, derivation])  #v0['nishpattis']['Sanskrit'][i][0], v0['nishpattis']['Hindi'][i][0], v0['nishpattis']['Odiya'][i][0]])
    # except Exception as e:
    #     print('row %s word %s e %s '%(amaralineno, amaraWord, e))
        # print('row %s word %s e %s least %s i %s'%(amaralineno, amaraWord, e, least, i))




