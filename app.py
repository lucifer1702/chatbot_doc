## the main file used for the code 
import streamlit as st 
import asyncio
# import guardrails as gd
# from guardrails.validators import Validator, EventDetail, register_validator
# from typing import Dict, List
from rich import print
from llm import chatbotLLM


# rail_str = """
# <rail version="0.1">

# <script language='python'>

# @register_validator(name="is-profanity-free", data_type="string")
# class IsProfanityFree(Validator):
#     global predict
#     global EventDetail
#     def validate(self, key, value, schema) -> Dict:
#         text = value
#         prediction = predict([value])
#         if prediction[0] == 1:
#             raise EventDetail(
#                 key,
#                 value,
#                 schema,
#                 f"Value {value} contains profanity language",
#                 "",
#             )
#         return schema
# </script>

# <output>
#     <string
#         name="CHATBOT RESPONSE"
#         description="do question answering based on the query given to you by searching answers for it from the data"
#         format="is-profanity-free"
#         on-fail-is-profanity-free="fix" 
#     />
# </output>


# <prompt>

# do question answering for the query given to you based off the data

# {{statement_to_be_translated}}

# @complete_json_suffix
# </prompt>

# </rail>
# """
# guard = gd.Guard.for_rail_string(rail_str)
## need to add guardrails for the output
async def main():
  
   text_area = st.text_area("Query")

   if st.button("Enter"):
        if len(text_area)>0:
            st.info(text_area)

            st.warning("Translation Without Guardrails")

            without_guardrails_result = await chatbotLLM(text_area, 'input.pdf')
            st.success(without_guardrails_result)

if __name__=="__main__":
    asyncio.run(main())