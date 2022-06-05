from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import WordFinder
# import logging
import logging.config

# logging.basicConfig(filename='mainlog.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


# F:
# cd python\FastApiTestProject
# uvicorn main:app --port 8000
# --log-config "F:/python/FastApiTestProject/CONFIG_FILE_NAME"
# test
# some changes +
# new commit i`m just testing pyCharm

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print_hi('PyCharm')


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/words/")
def read_item(letters: str = "abcdefghijklmnopqrstuvwxyz", mask: str = ""):
    res = []
    err_msg = ""
    inner_mask = ""
    try:
        word_len = len(mask)
        print(word_len)
        print(letters)
        finder = WordFinder.WordFinder(letters, word_len)
        print(f"Mode: {finder.MODE}")
        if mask is not None:
            inner_mask = "^"
            cnt = 0
            for ch in mask:
                if ch == '*' or ch == '?':
                    cnt += 1
                else:
                    if cnt > 0:
                        inner_mask += "\\w{"+str(cnt)+"}"
                        cnt = 0
                    inner_mask += ch
            if cnt > 0:
                inner_mask += "\\w{"+str(cnt)+"}"
            inner_mask += "$"
            print(inner_mask)
            res = finder.find_all_words_mask_rpt(inner_mask)
        else:
            res = finder.find_all_words()
        print(res)
        print(f"Found count: {len(res)}")
    except ValueError as err:
        logger.error(err)
        err_msg = str(err)
        print("Could not convert data.")
    except (RuntimeError, UnboundLocalError) as err:
        logger.error(err)
        err_msg = str(err)
        print(f"Some error occurred. {err}")
    except ZeroDivisionError as err:
        logger.error(err)
        err_msg = str(err)
        print('Handling run-time error:', err)
    except BaseException as err:
        logger.error(err)
        err_msg = str(err)
        print(f"Unexpected {err=}, {type(err)=}")

    data = {"letters": letters, "mask": mask, "inner_mask": inner_mask, "err_msg": err_msg, "result": res}
    logger.info(data)
    return data


@app.get("/words/{letters_amount}")
def read_item(letters_amount: int = 5, letters: str = "abcdefghijklmnopqrstuvwxyz"):
    res = []
    err_msg = ""
    try:
        finder = WordFinder.WordFinder(letters, letters_amount)
        res = finder.find_all_words()
        print(res)
        print(f"Found count: {len(res)}")
    except ValueError as err:
        err_msg = str(err)
        print("Could not convert data.")
    except (RuntimeError, UnboundLocalError) as err:
        err_msg = str(err)
        print(f"Some error occurred. {err}")
    except ZeroDivisionError as err:
        err_msg = str(err)
        print('Handling run-time error:', err)
    except BaseException as err:
        err_msg = str(err)
        print(f"Unexpected {err=}, {type(err)=}")

    return {"item_id": letters, "mask": "", "inner_mask": "", "err_msg": err_msg, "result": res}
