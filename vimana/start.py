import logging

from core import App

import os
 
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger(__name__)

BANNER = """               
                               x___________x       
                                    |                          
                               _   _|_   _                       
                              (i)-/   \-(i)     
       _                         /\___/\                         _
      (G)______xxxxx____________( ( x ) )____________xxxxx______(G)
                                 \_____/                                          

 ,ggg,         ,gg                                                             
dP""Y8a       ,8P                                                              
Yb, `88       d8'                                                              
 `"  88       88  gg                                                           
     88       88  ""                                                           
     I8       8I  gg    ,ggg,,ggg,,ggg,     ,gggg,gg   ,ggg,,ggg,     ,gggg,gg 
     `8,     ,8'  88   ,8" "8P" "8P" "8,   dP"  "Y8I  ,8" "8P" "8,   dP"  "Y8I 
      Y8,   ,8P   88   I8   8I   8I   8I  i8'    ,8I  I8   8I   8I  i8'    ,8I 
       Yb,_,dP  _,88,_,dP   8I   8I   Yb,,d8,   ,d8b,,dP   8I   Yb,,d8,   ,d8b,
        "Y8P"   8P""Y88P'   8I   8I   `Y8P"Y8888P"`Y88P'   8I   `Y8P"Y8888P"`Y8
                                                                               
    Codename: Angry Arianna                                      __   
                                                                 \ \_____
    Initalisation is complete. Vimana Server is ready to fly. ###[==_____>     
                                                                 /_/      
                                                                                                                                                                  
"""


def start():
    logger.info(BANNER)
    from abci import ABCIServer

    app = ABCIServer(app=App())
    app.run()


if __name__ == '__main__':
    start()