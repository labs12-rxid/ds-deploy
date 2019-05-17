import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import pandas as pd
from itertools import permutations
import json
from dotenv import load_dotenv
import os

load_dotenv()


# ______query_from rekog __________
def query_from_rekog(rekog_results):
    if len(rekog_results) > 1:
        results = [x for x in list(map(";".join, permutations(rekog_results)))]
    else:
        results = rekog_results

    total_results = []
    for result in results:
        qry_r = query_sql_data({
            "pill_name": "",
            "imprint": result,
            "color": "", "shape": ""
            })
        if qry_r == '':
            continue
        else:
            total_results.append(qry_r)
    return total_results


#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    im_print = parameter_list.get('imprint')
    pill_name = parameter_list.get('pill_name')
    sha_pe = parameter_list.get('shape')
    col_or = parameter_list.get('color')

    # if sha_pe==0 or sha_pe=='None':
    #     shape_text = None
    # else:
    #     for i in range(len(shape_codes)):
    #         if shape_codes[i].get("code") == sha_pe:
    #             dict_index = i
    #     shape_text = shape_codes[dict_index].get("name").upper()

    # if col_or == 0 or col_or == 'None':
    #     color_text = None
    # else:
    #     for i in range(len(color_codes)):
    #         if color_codes[i].get("code") == col_or:
    #             dict_index = i
    #     color_text = color_codes[dict_index].get("name").upper()

    db_engine = db_connect()
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name

    query = """SELECT
                    author,
                    splimprint,
                    image_id,
                    spl_strength,
                    spl_ingredients,
                    splsize,
                    splcolor_text,
                    splshape_text,
                    product_code,
                    DEA_SCHEDULE_CODE,
                    setid,
                    spl_inactive_ing
                    FROM """ + table_string + """
                WHERE """

    ctr = 0
    if im_print is not None:
        if ctr > 0:
            query = query + " AND "
        query = query + " UPPER(splimprint) ILIKE '%%" + im_print.upper() + "%%'"
        ctr += 1
    if sha_pe == "" or sha_pe == "None":
        pass
    else:
        if ctr > 0:
            query = query + " AND "
        query = query + " splshape_text ILIKE " + "'" + sha_pe + "'"
        ctr += 1
    if col_or == "" or col_or == "None":
        pass
    else:
        if ctr > 0:
            query = query + " AND "
        query = query + " splcolor_text ILIKE " + "'" + col_or + "'"
        ctr += 1

    if pill_name == '' or pill_name == 'None':
        pass
    else:
        if ctr > 0:
            query = query + " AND "
        query = query + " medicine_name ILIKE '%%" + pill_name.upper() + "%%'"
        ctr += 1

    query = query + " LIMIT 25;"
    """
        WHERE splimprint  LIKE ''       im_print
        AND splshape_text LIKE 'OVAL'   shape_text
        AND splcolor_text LIKE 'YELLOW'  color_text

        ----use double %% for wildcards!!!!!----
        AND medicine_name LIKE '%%PANTO%%'  pill_name
    """
    results = db_engine.execute(query).fetchall()
    df = pd.DataFrame(results, columns=[
        'author',
        'imprint',
        'image_id',
        'spl_strength',
        'medicine_name',
        'size',
        'color_text',
        'shape_text',
        'product_code',
        'DEA_schedule',
        'setid',
        'spl_inactive_ing'
        ])
    df.loc[df['image_id'] != None, 'image_id'] += '.jpg'
    results_json = df.to_json(orient='records')
    return results_json[1:-1]


#  ____________  CONNECT TO DATABASE ___________________
def db_connect():
    # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
    dbname = os.getenv("DS_DB_NAME")
    user = os.getenv("DS_DB_USER")
    host = os.getenv("DS_DB_HOST")
    passw = os.getenv("DS_DB_PASSWORD")
    pgres_str = 'postgresql+psycopg2://' + user + ':' + passw + '@' + host + '/' + dbname
    pgres_engine = create_engine(pgres_str)
    return pgres_engine


# ______  return colors, shapes list in reponse to GET request from /rxdata
def get_colors_shapes():
    out_put = {
        "valid_colors": [
            "YELLOW;RED;ORANGE",
            "BROWN;PURPLE",
            "WHITE;BLUE",
            "GRAY;ORANGE",
            "PINK;ORANGE;YELLOW;WHITE",
            "ORANGE;PINK",
            "RED;YELLOW",
            "BROWN;GREEN",
            "RED;ORANGE",
            "BROWN;BROWN",
            "BROWN;ORANGE",
            "ORANGE;YELLOW;GREEN;PINK",
            "WHITE;YELLOW",
            "YELLOW;PINK;GREEN",
            "PINK;YELLOW",
            "BROWN;RED",
            "WHITE;TURQUOISE",
            "RED;WHITE;YELLOW",
            "PINK;BLUE;PINK",
            "TURQUOISE;PINK",
            "GRAY;PURPLE",
            "YELLOW;PURPLE",
            "YELLOW;PINK;ORANGE;WHITE",
            "ORANGE;WHITE",
            "BLUE",
            "RED;PURPLE;YELLOW;ORANGE",
            "PURPLE;GRAY",
            "GREEN;GREEN",
            "PINK;ORANGE;PURPLE",
            "YELLOW;ORANGE;PINK",
            "WHITE;RED;GREEN",
            "GREEN;ORANGE;PINK;YELLOW",
            "RED;PINK",
            "PINK;YELLOW;ORANGE",
            "PINK;RED;BLUE",
            "GREEN;BLUE;WHITE",
            "ORANGE;YELLOW;RED",
            "BROWN;TURQUOISE",
            "RED;YELLOW;ORANGE;GREEN",
            "GRAY;GREEN",
            "YELLOW",
            "YELLOW;GREEN;RED;ORANGE",
            "PURPLE;ORANGE",
            "PINK;ORANGE",
            "PURPLE;GREEN",
            "PURPLE;PINK",
            "PINK;YELLOW;ORANGE;PINK",
            "ORANGE;YELLOW",
            "BROWN;BLUE",
            "BLUE;YELLOW",
            "ORANGE;BLUE",
            "YELLOW;BLUE",
            "YELLOW;ORANGE;RED;PURPLE",
            "RED;GREEN;YELLOW;ORANGE",
            "BLUE;PINK",
            "WHITE;PURPLE",
            "ORANGE;PINK;YELLOW",
            "GRAY;WHITE",
            "GRAY;RED",
            "YELLOW;GRAY",
            "YELLOW;ORANGE;RED;GREEN",
            "GREEN;YELLOW",
            "BLUE;GREEN;PINK",
            "RED;GREEN",
            "BLUE;GRAY",
            "RED",
            "RED;BLUE;GRAY",
            "BLUE;ORANGE;YELLOW;PURPLE",
            "PINK;RED",
            "RED;PINK;PURPLE",
            "GREEN;BLACK",
            "BLUE;GRAY;BLUE",
            "WHITE;GRAY",
            "PINK;BROWN",
            "RED;GREEN;ORANGE;YELLOW",
            "RED;BROWN",
            "RED;GRAY;BLUE",
            "GREEN;GRAY",
            "BLACK;GREEN",
            "TURQUOISE;TURQUOISE",
            "YELLOW;WHITE",
            "BLACK",
            "GREEN;WHITE;YELLOW",
            "BLACK;YELLOW",
            "PINK;BLACK",
            "GRAY;BLACK",
            "ORANGE;PINK;PURPLE",
            "PINK;WHITE;BLUE",
            "BROWN;PINK",
            "GREEN;BROWN",
            "GRAY",
            "PURPLE;WHITE",
            "ORANGE;ORANGE",
            "YELLOW;PINK;ORANGE",
            "WHITE",
            "BLUE;TURQUOISE",
            "GRAY;RED;PURPLE;ORANGE",
            "GREEN;BLUE",
            "BLUE;BLACK",
            "GRAY;BROWN",
            "ORANGE;RED",
            "RED;BLUE",
            "RED;ORANGE;YELLOW;GREEN",
            "BROWN;WHITE",
            "RED;PURPLE",
            "YELLOW;ORANGE;WHITE;RED",
            "GRAY;BLUE",
            "YELLOW;BLACK",
            "RED;BLUE;PURPLE",
            "RED;ORANGE;WHITE;YELLOW",
            "WHITE;ORANGE",
            "ORANGE;BROWN",
            "PINK;WHITE;RED",
            "TURQUOISE",
            "WHITE;GREEN",
            "PINK;ORANGE;YELLOW;GREEN",
            "BLUE;ORANGE",
            "GREEN",
            "YELLOW;ORANGE",
            "WHITE;ORANGE;YELLOW;RED",
            "BLUE;GREEN",
            "BLUE;PINK;PURPLE",
            "GREEN;PINK",
            "PINK;ORANGE;YELLOW",
            "BLUE;WHITE",
            "PURPLE;BLUE;GRAY",
            "GREEN;PURPLE",
            "BLACK;PURPLE",
            "TURQUOISE;WHITE",
            "ORANGE;RED;PURPLE",
            "BLUE;PURPLE;WHITE",
            "PURPLE;BLUE",
            "BLACK;PINK",
            "GRAY;PINK",
            "GRAY;RED;ORANGE",
            "PINK",
            "YELLOW;GREEN",
            "GREEN;WHITE",
            "GREEN;TURQUOISE;WHITE",
            "BLUE;BLUE",
            "YELLOW;RED;ORANGE;WHITE",
            "ORANGE;YELLOW;PINK",
            "BLUE;RED",
            "RED;YELLOW;ORANGE",
            "PURPLE",
            "RED;YELLOW;GREEN;ORANGE",
            "GREEN;ORANGE",
            "BLACK;WHITE",
            "ORANGE;RED;YELLOW;PURPLE",
            "BROWN",
            "BROWN;YELLOW",
            "YELLOW;YELLOW",
            "ORANGE",
            "PURPLE;YELLOW",
            "ORANGE;PURPLE",
            "GREEN;RED",
            "PINK;GREEN",
            "PURPLE;PURPLE",
            "YELLOW;RED",
            "BROWN;GRAY",
            "RED;GRAY",
            "RED;WHITE",
            "GRAY;GRAY",
            "PINK;BLUE;PURPLE",
            "YELLOW;ORANGE;PINK;GREEN",
            "GRAY;YELLOW",
            "BLUE;BROWN",
            "WHITE;GREEN;BLUE",
            "YELLOW;PINK",
            "WHITE;RED;ORANGE;YELLOW",
            "WHITE;BLACK",
            "PINK;PINK;PURPLE",
            "BLUE;PURPLE",
            "ORANGE;GREEN",
            "ORANGE;GRAY",
            "RED;RED",
            "PINK;WHITE",
            "YELLOW;GREEN;ORANGE;RED",
            "WHITE;PINK",
            "WHITE;RED",
            "PURPLE;TURQUOISE",
            "RED;PURPLE;GRAY",
            "PINK;TURQUOISE",
            "YELLOW;BROWN",
            "WHITE;WHITE",
            "PINK;PINK",
            "PINK;BLUE",
            "GRAY;RED;PURPLE",
            "PINK;ORANGE;YELLOW;RED",
            "TURQUOISE;BLUE",
            "PINK;GRAY",
            "WHITE;BROWN",
            "PURPLE;RED"
        ],
        "valid_shapes": [
           "ROUND", "OVAL", "CAPSULE", "DIAMOND", "TRIANGLE",
           "PENTAGON (5 SIDED)", "HEXAGON (6 SIDED)", "RECTANGLE", "BULLET",
           "FREEFORM", "SQUARE", "OCTAGON (8 SIDED)", "TRAPEZOID",
           "DOUBLE CIRCLE", "TEAR", "SEMI-CIRCLE", "CLOVER"
        ]
    }
    return out_put


# __________ M A I N ________________________
if __name__ == '__main__':
    print(query_from_rekog(['126']))
