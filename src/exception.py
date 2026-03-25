import sys 
from src.logger import logging

def eror_message_details(eror,eror_detail:sys):
   _,_,exc_tb=eror_detail.exc_info()
   file_name=exc_tb.tb_frame.f_code.co_filename
   eror_message="Eror Occured in Python Script name [{0}] line number [{1}] eror message [{2}]".format(file_name,exc_tb.tb_lineno,str(eror))
   return eror_message



class CustomException(Exception):
   def __init__(self,eror_message,eror_detail:sys):
      super().__init__(eror_message)
      self.eror_message=eror_message_details(eror_message,eror_detail=eror_detail)
   def __str__(self):
      return self.eror_message
   
# if __name__=="__main__":
#    try:
#       a=1/0
#    except Exception as e:
#       logging.info("Division By Zero")
#       raise CustomException(e,sys)